const { spawn } = require('child_process');
const http = require('http');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const TARGET_URL = 'http://localhost:8101';
const DEBUG_PORT = 9230;

function getJson(url) {
    return new Promise((resolve, reject) => {
        http.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
            });
        }).on('error', reject);
    });
}

(async () => {
    const userDataDir = 'C:\\Users\\tomas\\.gemini\\antigravity\\brain\\1e627548-1da8-4dd8-a641-13dac54942ad\\scratch\\chrome_mobile_' + Date.now();
    const chrome = spawn(CHROME_PATH, [
        '--headless=new',
        '--disable-gpu-sandbox',
        '--enable-webgl',
        '--ignore-gpu-blocklist',
        '--use-angle=swiftshader',
        '--window-size=412,915',
        `--remote-debugging-port=${DEBUG_PORT}`,
        `--user-data-dir=${userDataDir}`,
        TARGET_URL
    ], { stdio: 'ignore' });

    try {
        let targets = null;
        for (let i = 0; i < 30; i++) {
            await new Promise(r => setTimeout(r, 300));
            try {
                targets = await getJson(`http://127.0.0.1:${DEBUG_PORT}/json`);
                if (targets && targets.length > 0 && targets.find(t => t.type === 'page')) break;
            } catch (_) {}
        }
        const pageTarget = targets && targets.find(t => t.type === 'page');
        if (!pageTarget) throw new Error('No se pudo conectar a Chrome CDP');

        const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
        await new Promise((resolve, reject) => {
            ws.addEventListener('open', resolve);
            ws.addEventListener('error', reject);
        });

        let msgId = 1;
        const pending = new Map();
        const runtimeErrors = [];

        ws.addEventListener('message', (ev) => {
            const msg = JSON.parse(ev.data);
            if (msg.id && pending.has(msg.id)) {
                pending.get(msg.id)(msg);
                pending.delete(msg.id);
            } else if (msg.method === 'Runtime.exceptionThrown') {
                const d = msg.params.exceptionDetails;
                runtimeErrors.push({
                    text: d.text,
                    description: d.exception ? d.exception.description : '',
                    line: d.lineNumber,
                    col: d.columnNumber
                });
            } else if (msg.method === 'Runtime.consoleAPICalled') {
                const type = msg.params.type;
                const txt = (msg.params.args || []).map(a => a.value ?? a.description ?? '').join(' ');
                if (type === 'error') runtimeErrors.push({ text: 'console.error: ' + txt });
            }
        });

        function sendCmd(method, params = {}) {
            return new Promise((resolve) => {
                const id = msgId++;
                pending.set(id, resolve);
                ws.send(JSON.stringify({ id, method, params }));
            });
        }

        await sendCmd('Runtime.enable');
        await sendCmd('Page.enable');
        await new Promise(r => setTimeout(r, 3000));

        // Evaluate views
        const testCode = `(async function() {
            const results = {};
            function sampleCanvas() {
                const cvs = document.querySelector('canvas');
                if (!cvs) return { found: false };
                const gl = cvs.getContext('webgl2') || cvs.getContext('webgl');
                if (!gl) return { found: true, gl: false };
                const w = gl.drawingBufferWidth;
                const h = gl.drawingBufferHeight;
                const pixels = new Uint8Array(4 * 5);
                const coords = [
                    [Math.floor(w*0.5), Math.floor(h*0.5)],
                    [Math.floor(w*0.25), Math.floor(h*0.25)],
                    [Math.floor(w*0.75), Math.floor(h*0.75)],
                    [Math.floor(w*0.25), Math.floor(h*0.75)],
                    [Math.floor(w*0.75), Math.floor(h*0.25)]
                ];
                const samples = [];
                for (let i = 0; i < coords.length; i++) {
                    const p = new Uint8Array(4);
                    gl.readPixels(coords[i][0], coords[i][1], 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, p);
                    samples.push([p[0], p[1], p[2], p[3]]);
                }
                const nonBlack = samples.some(s => (s[0] > 10 || s[1] > 10 || s[2] > 10));
                return { found: true, width: w, height: h, nonBlack, samples };
            }

            results['initial_3d'] = sampleCanvas();

            // Try 2D view
            const btn2D = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('2D') || b.textContent.includes('Plano'));
            if (btn2D) {
                btn2D.click();
                await new Promise(r => setTimeout(r, 1000));
                results['view_2d_button'] = sampleCanvas();
            }

            // Also check select element if exists
            const selectVista = Array.from(document.querySelectorAll('select')).find(s => s.textContent.includes('2D') || s.textContent.includes('Sims'));
            if (selectVista) {
                results['selectVista_options'] = Array.from(selectVista.options).map(o => o.text);
                // Switch to 2D in select
                for (let opt of selectVista.options) {
                    if (opt.text.includes('2D')) {
                        selectVista.value = opt.value;
                        selectVista.dispatchEvent(new Event('change'));
                        break;
                    }
                }
                await new Promise(r => setTimeout(r, 1000));
                results['view_select_2d'] = sampleCanvas();

                // Switch to Sims in select
                for (let opt of selectVista.options) {
                    if (opt.text.includes('Sims')) {
                        selectVista.value = opt.value;
                        selectVista.dispatchEvent(new Event('change'));
                        break;
                    }
                }
                await new Promise(r => setTimeout(r, 1000));
                results['view_select_sims'] = sampleCanvas();
            }

            // Check camera position and clipping
            results['camera'] = {
                fov: typeof camera !== 'undefined' ? camera.fov : null,
                near: typeof camera !== 'undefined' ? camera.near : null,
                far: typeof camera !== 'undefined' ? camera.far : null,
                position: typeof camera !== 'undefined' ? { x: camera.position.x, y: camera.position.y, z: camera.position.z } : null
            };

            return results;
        })()`;

        const evalRes = await sendCmd('Runtime.evaluate', {
            expression: testCode,
            awaitPromise: true,
            returnByValue: true
        });

        console.log('Runtime Errors:', JSON.stringify(runtimeErrors, null, 2));
        console.log('Mobile Test EvalRes:', JSON.stringify(evalRes, null, 2));

        ws.close();
        chrome.kill();
    } catch (e) {
        console.error('Audit failed:', e);
        try { chrome.kill(); } catch (_) {}
    }
})();
