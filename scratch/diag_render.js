const { spawn } = require('child_process');
const http = require('http');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const TARGET_URL = 'http://localhost:8101';
const DEBUG_PORT = 9231;

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
    const userDataDir = 'C:\\Users\\tomas\\.gemini\\antigravity\\brain\\1e627548-1da8-4dd8-a641-13dac54942ad\\scratch\\chrome_diag_' + Date.now();
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
            } else if (msg.method === 'Runtime.consoleAPICalled') {
                logs.push((msg.params.args || []).map(a => a.value ?? a.description ?? '').join(' '));
            } else if (msg.method === 'Runtime.exceptionThrown') {
                logs.push('EXC: ' + JSON.stringify(msg.params.exceptionDetails));
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

        const testExpr = `(function() {
            const diag = {};
            diag.isMobileOrLowEnd = typeof isMobileOrLowEnd !== 'undefined' ? isMobileOrLowEnd : null;
            diag.hasComposer = typeof composer !== 'undefined' && !!composer;
            diag.hasSSAO = typeof ssaoPass !== 'undefined' && !!ssaoPass;
            diag.hasSMAA = typeof smaaPass !== 'undefined' && !!smaaPass;
            diag.ssaoEnabled = diag.hasSSAO ? ssaoPass.enabled : null;
            diag.activeCameraIsPersp = activeCamera === perspCam;
            diag.activeCameraIsOrtho = activeCamera === orthoCam;
            diag.activeCameraPos = activeCamera ? { x: activeCamera.position.x, y: activeCamera.position.y, z: activeCamera.position.z } : null;
            diag.controlsPerspTarget = controlsPersp ? { x: controlsPersp.target.x, y: controlsPersp.target.y, z: controlsPersp.target.z } : null;
            diag.perspCamFov = perspCam ? perspCam.fov : null;
            diag.perspCamNear = perspCam ? perspCam.near : null;
            diag.perspCamFar = perspCam ? perspCam.far : null;
            diag.dirtyFrames = dirtyFrames;

            // Sample raw renderer.render vs composer.render
            const cvs = document.querySelector('canvas');
            const gl = renderer.getContext();
            const w = cvs.width, h = cvs.height;
            const buf = new Uint8Array(4);

            // Test 1: native render
            renderer.render(scene, activeCamera);
            gl.readPixels(Math.floor(w/2), Math.floor(h/2), 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, buf);
            diag.nativeRenderPixel = [buf[0], buf[1], buf[2], buf[3]];

            // Test 2: composer render
            if (composer) {
                try {
                    composer.render();
                    gl.readPixels(Math.floor(w/2), Math.floor(h/2), 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, buf);
                    diag.composerRenderPixel = [buf[0], buf[1], buf[2], buf[3]];
                } catch(e) {
                    diag.composerError = e.message;
                }
            }

            // Test 3: what if switchTo2D() is called?
            switchTo2D();
            renderer.render(scene, activeCamera);
            gl.readPixels(Math.floor(w/2), Math.floor(h/2), 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, buf);
            diag.switchTo2DPixel = [buf[0], buf[1], buf[2], buf[3]];

            // Switch back to 3D
            switchTo3D('isom', 'sims', false);
            renderer.render(scene, activeCamera);
            gl.readPixels(Math.floor(w/2), Math.floor(h/2), 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, buf);
            diag.switchBack3DPixel = [buf[0], buf[1], buf[2], buf[3]];

            return diag;
        })()`;

        const res = await sendCmd('Runtime.evaluate', { expression: testExpr, returnByValue: true });
        console.log('RES:', JSON.stringify(res, null, 2));
        console.log('LOGS:', logs);

        ws.close();
        chrome.kill();
    } catch(e) {
        console.error(e);
        try { chrome.kill(); } catch(_) {}
    }
})();