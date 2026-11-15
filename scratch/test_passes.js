const { spawn } = require('child_process');
const http = require('http');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const TARGET_URL = 'http://localhost:8101';
const DEBUG_PORT = 9232;

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
    const userDataDir = 'C:\\Users\\tomas\\.gemini\\antigravity\\brain\\1e627548-1da8-4dd8-a641-13dac54942ad\\scratch\\chrome_eval_' + Date.now();
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
        const logs = [];

        ws.addEventListener('message', (ev) => {
            const msg = JSON.parse(ev.data);
            if (msg.id && pending.has(msg.id)) {
                pending.get(msg.id)(msg);
                pending.delete(msg.id);
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
        await new Promise(r => setTimeout(r, 2500));

        // Inject inside index.html's own scope by evaluating a script tag or using window objects
        const scriptCode = `
            const cvs = document.querySelector('canvas');
            const gl = window.renderer.getContext();
            const w = cvs.width, h = cvs.height;
            const buf = new Uint8Array(4);

            const out = {
                composerExists: !!window.composer,
                passes: window.composer ? window.composer.passes.map(p => ({
                    type: p.constructor.name,
                    enabled: p.enabled,
                    renderToScreen: p.renderToScreen
                })) : []
            };

            // Read pixels right now
            gl.readPixels(Math.floor(w/2), Math.floor(h/2), 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, buf);
            out.pixelCurrent = [buf[0], buf[1], buf[2], buf[3]];

            // Force native render
            window.renderer.render(window.scene, window.perspCam);
            gl.readPixels(Math.floor(w/2), Math.floor(h/2), 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, buf);
            out.pixelNative = [buf[0], buf[1], buf[2], buf[3]];

            // Force composer render
            if (window.composer) {
                window.composer.render();
                gl.readPixels(Math.floor(w/2), Math.floor(h/2), 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, buf);
                out.pixelComposer = [buf[0], buf[1], buf[2], buf[3]];
            }

            out;
        `;

        const res = await sendCmd('Runtime.evaluate', { expression: scriptCode, returnByValue: true });
        console.log('RES:', JSON.stringify(res, null, 2));

        ws.close();
        chrome.kill();
    } catch(e) {
        console.error(e);
        try { chrome.kill(); } catch(_) {}
    }
})();