// ============================================================================
// QA WEBGL AUDIT SCRIPT (Zero-Dependency Chrome CDP Real Browser Audit)
// ============================================================================
const { spawn } = require('child_process');
const http = require('http');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const TARGET_URL = process.env.AUDIT_URL || 'http://localhost:8101';
const DEBUG_PORT = 9229;

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
    const userDataDir = 'C:\\Users\\tomas\\.gemini\\antigravity\\brain\\1e627548-1da8-4dd8-a641-13dac54942ad\\scratch\\chrome_audit_profile_' + Date.now();
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
        if (!pageTarget) throw new Error('No se pudo conectar al target de Chrome CDP');

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
        await new Promise(r => setTimeout(r, 2500));

        const evalRes = await sendCmd('Runtime.evaluate', {
            returnByValue: true,
            expression: `(function() {
                try {
                    const nanMeshes = [];
                    scene.traverse(obj => {
                        if (obj.isMesh && obj.geometry && obj.geometry.attributes && obj.geometry.attributes.position) {
                            const arr = obj.geometry.attributes.position.array;
                            for (let i = 0; i < arr.length; i++) {
                                if (Number.isNaN(arr[i])) {
                                    nanMeshes.push({
                                        name: obj.name || obj.userData?.name || obj.userData?.nombre || 'unnamed',
                                        parentName: obj.parent ? (obj.parent.name || obj.parent.userData?.name || obj.parent.userData?.nombre || '') : ''
                                    });
                                    break;
                                }
                            }
                        }
                    });

                    const canvas = document.querySelector('#webgl-container canvas');
                    if (!canvas) return JSON.stringify({ hasCanvas: false });

                    if (typeof wakeRenderer === 'function') wakeRenderer();
                    if (typeof composer !== 'undefined' && composer) composer.render();
                    else if (typeof renderer !== 'undefined' && renderer) renderer.render(scene, activeCamera);

                    const gl = renderer.getContext();
                    const w = canvas.width, h = canvas.height;
                    const samplePoints = [
                        [Math.floor(w * 0.5), Math.floor(h * 0.5)],
                        [Math.floor(w * 0.35), Math.floor(h * 0.45)],
                        [Math.floor(w * 0.65), Math.floor(h * 0.45)],
                        [Math.floor(w * 0.5), Math.floor(h * 0.3)],
                        [Math.floor(w * 0.5), Math.floor(h * 0.7)]
                    ];
                    const buf = new Uint8Array(4);
                    const samples3D = samplePoints.map(([x, y]) => {
                        gl.readPixels(x, y, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, buf);
                        return [buf[0], buf[1], buf[2], buf[3]];
                    });
                    const nonBlack3D = samples3D.some(p => (p[0] + p[1] + p[2]) > 30);

                    if (typeof switchTo2D === 'function') switchTo2D();
                    if (typeof composer !== 'undefined' && composer) composer.render();
                    else if (typeof renderer !== 'undefined' && renderer) renderer.render(scene, activeCamera);

                    const samples2D = samplePoints.map(([x, y]) => {
                        gl.readPixels(x, y, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, buf);
                        return [buf[0], buf[1], buf[2], buf[3]];
                    });
                    const nonBlack2D = samples2D.some(p => (p[0] + p[1] + p[2]) > 30);

                    // Verificar 2D también viniendo desde Noche WiZ y Cortinas Blackout cerradas
                    if (typeof switchTo3D === 'function') switchTo3D('isom', 'sims', true);
                    if (typeof setSolarTime === 'function') setSolarTime('night', false);
                    if (typeof animCurtains !== 'undefined') animCurtains.forEach(c => c.setMode && c.setMode('blackout'));
                    if (typeof switchTo2D === 'function') switchTo2D();
                    if (typeof composer !== 'undefined' && composer) composer.render();
                    const samples2DAfterNight = samplePoints.map(([x, y]) => {
                        gl.readPixels(x, y, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, buf);
                        return [buf[0], buf[1], buf[2], buf[3]];
                    });
                    const nonBlack2DAfterNight = samples2DAfterNight.some(p => (p[0] + p[1] + p[2]) > 200);

                    // Restaurar vista 3D diurna y probar simulador estacional y WiZ individual
                    if (typeof animCurtains !== 'undefined') animCurtains.forEach(c => c.setMode && c.setMode('sheer'));
                    if (typeof setSolarTime === 'function') setSolarTime('noon', false);
                    if (typeof setSolarSeason === 'function') {
                        setSolarSeason('winter', false);
                        setSolarSeason('summer', false);
                        setSolarSeason('equinox', false);
                    }
                    if (typeof cycleWizRoomMode === 'function') {
                        cycleWizRoomMode('living', false);
                        setAllWizRoomsMode('auto', false);
                    }
                    if (typeof switchTo3D === 'function') switchTo3D('isom', 'sims', true);
                    if (typeof composer !== 'undefined' && composer) composer.render();

                    const westWallEntry = (typeof logicalWallsRegistry !== 'undefined') ? logicalWallsRegistry.get('muro_ext_oeste') : null;

                    return JSON.stringify({
                        hasCanvas: true,
                        width: w,
                        height: h,
                        nonBlack3D,
                        samples3D,
                        nonBlack2D,
                        samples2D,
                        nonBlack2DAfterNight,
                        samples2DAfterNight,
                        nanMeshes,
                        roomFloorsCount: typeof roomFloorMeshes !== 'undefined' ? roomFloorMeshes.length : 0,
                        logicalWallsCount: typeof logicalWallsRegistry !== 'undefined' ? logicalWallsRegistry.size : 0,
                        westWallDims: westWallEntry ? westWallEntry.dimensiones : null,
                        curtainsCount: typeof animCurtains !== 'undefined' ? animCurtains.length : 0,
                        wizClickCount: typeof wizClickCandidates !== 'undefined' ? wizClickCandidates.length : 0,
                        hasSolarCompass: !!(typeof solarCompassGroup !== 'undefined' && solarCompassGroup)
                    });
                } catch (err) {
                    return JSON.stringify({ evalError: err.stack || err.message });
                }
            })()`
        });

        console.log('=== RESULTADO AUDITORÍA WEBGL ===');
        console.log('Runtime Errors:', JSON.stringify(runtimeErrors, null, 2));
        const rawVal = evalRes?.result?.result?.value ?? evalRes?.result?.value;
        const parsed = typeof rawVal === 'string' ? JSON.parse(rawVal) : evalRes;
        console.log('Canvas & Scene Audit:', JSON.stringify(parsed, null, 2));

        ws.close();
        chrome.kill();
        if (runtimeErrors.length > 0 || !parsed.nonBlack3D || !parsed.nonBlack2D || !parsed.nonBlack2DAfterNight) process.exit(1);
    } catch (err) {
        console.error('Audit Error:', err);
        chrome.kill();
        process.exit(1);
    }
})();
