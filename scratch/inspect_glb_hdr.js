const { spawn } = require('child_process');
const http = require('http');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const TARGET_URL = 'http://localhost:8101';
const DEBUG_PORT = 9245;

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
    const userDataDir = 'C:\\Users\\tomas\\.gemini\\antigravity\\brain\\1e627548-1da8-4dd8-a641-13dac54942ad\\scratch\\chrome_glb_' + Date.now();
    const chrome = spawn(CHROME_PATH, [
        '--headless=new',
        '--disable-gpu-sandbox',
        '--enable-webgl',
        '--ignore-gpu-blocklist',
        '--use-angle=swiftshader',
        '--window-size=1280,800',
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
        await new Promise(r => setTimeout(r, 4500));

        const glbTestCode = `(async function() {
            const files = ['models/sofa.glb', 'models/plant.glb', 'models/bed.glb', 'models/chair.glb', 'models/desk.glb', 'models/bathtub.glb', 'models/toilet.glb'];
            const results = {};
            const loader = new THREE.GLTFLoader();

            for (const f of files) {
                try {
                    const gltf = await new Promise((resolve, reject) => {
                        loader.load(f, resolve, undefined, reject);
                    });
                    const box = new THREE.Box3().setFromObject(gltf.scene);
                    const size = new THREE.Vector3();
                    box.getSize(size);
                    let meshCount = 0;
                    gltf.scene.traverse(c => { if (c.isMesh) meshCount++; });
                    results[f] = {
                        ok: true,
                        size: { x: +size.x.toFixed(3), y: +size.y.toFixed(3), z: +size.z.toFixed(3) },
                        meshCount
                    };
                } catch(err) {
                    results[f] = { ok: false, error: err.message };
                }
            }

            // Also test loading HDR
            try {
                const rgbe = new THREE.RGBELoader();
                const hdr = await new Promise((resolve, reject) => {
                    rgbe.load('textures/hdr/ferndale_studio_04_1k.hdr', resolve, undefined, reject);
                });
                results['hdr'] = { ok: true, width: hdr.image.width, height: hdr.image.height };
            } catch(e) {
                results['hdr'] = { ok: false, error: e.message };
            }

            return results;
        })()`;

        let res = await sendCmd('Runtime.evaluate', { expression: glbTestCode, awaitPromise: true, returnByValue: true });
        if (res && res.error && res.error.message && res.error.message.includes('navigated')) {
            await new Promise(r => setTimeout(r, 2000));
            res = await sendCmd('Runtime.evaluate', { expression: glbTestCode, awaitPromise: true, returnByValue: true });
        }
        console.log('RES:', JSON.stringify(res.result?.value || res, null, 2));

        ws.close();
        chrome.kill();
    } catch(e) {
        console.error(e);
        try { chrome.kill(); } catch(_) {}
    }
})();