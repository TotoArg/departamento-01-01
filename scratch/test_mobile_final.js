const { spawn } = require('child_process');
const http = require('http');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const TARGET_URL = 'http://localhost:8101';
const DEBUG_PORT = 9235;

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
    const userDataDir = 'C:\\Users\\tomas\\.gemini\\antigravity\\brain\\1e627548-1da8-4dd8-a641-13dac54942ad\\scratch\\chrome_mob_final_' + Date.now();
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
        const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
        await new Promise(r => ws.addEventListener('open', r));

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
        await new Promise(r => setTimeout(r, 4500));

        const testCode = `(async function() {
            const cvs = document.querySelector('canvas');
            const gl = window.renderer.getContext();
            const w = cvs.width, h = cvs.height;
            const buf = new Uint8Array(4);

            function sample() {
                const samples = [];
                const pts = [
                    [Math.floor(w*0.5), Math.floor(h*0.5)],
                    [Math.floor(w*0.3), Math.floor(h*0.4)],
                    [Math.floor(w*0.7), Math.floor(h*0.4)],
                    [Math.floor(w*0.5), Math.floor(h*0.3)],
                    [Math.floor(w*0.5), Math.floor(h*0.7)]
                ];
                for (let [x, y] of pts) {
                    gl.readPixels(x, y, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, buf);
                    samples.push([buf[0], buf[1], buf[2], buf[3]]);
                }
                const nonBlack = samples.some(s => (s[0] + s[1] + s[2]) > 30);
                return { nonBlack, samples };
            }

            // 1. Initial 3D state
            const r3d = sample();

            // 2. Select 2D mode from dropdown
            const sel = document.getElementById('select-view-mode');
            if (sel) {
                sel.value = '2d';
                sel.dispatchEvent(new Event('change'));
            }
            await new Promise(r => setTimeout(r, 800));
            const r2d = sample();

            // 3. Switch back to sims 3d from dropdown
            if (sel) {
                sel.value = 'sims';
                sel.dispatchEvent(new Event('change'));
            }
            await new Promise(r => setTimeout(r, 800));
            const rSims = sample();

            // 4. Verify Mesa de Comedor dimensions
            let diningTableDims = null;
            window.scene.traverse(obj => {
                if (obj.userData && obj.userData.nombre && obj.userData.nombre.includes('Mesa de Comedor')) {
                    diningTableDims = obj.userData.dimensiones;
                }
            });

            return {
                initial3D: r3d,
                dropdown2D: r2d,
                dropdownSims: rSims,
                diningTableDims: diningTableDims
            };
        })()`;

        const evalRes = await sendCmd('Runtime.evaluate', {
            expression: testCode,
            awaitPromise: true,
            returnByValue: true
        });

        console.log('Runtime Errors:', JSON.stringify(runtimeErrors, null, 2));
        console.log('evalRes:', JSON.stringify(evalRes, null, 2));

        ws.close();
        chrome.kill();
    } catch (e) {
        console.error('Audit failed:', e);
        try { chrome.kill(); } catch (_) {}
    }
})();