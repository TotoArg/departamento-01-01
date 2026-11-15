const { spawn } = require('child_process');
const http = require('http');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const TARGET_URL = 'http://localhost:8101';
const DEBUG_PORT = 9240;

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
    const userDataDir = 'C:\\Users\\tomas\\.gemini\\antigravity\\brain\\1e627548-1da8-4dd8-a641-13dac54942ad\\scratch\\chrome_check_' + Date.now();
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

        const testScript = `(function() {
            const checks = {};

            // 1. Check Table
            let tableMesh = null;
            window.scene.traverse(obj => {
                if (obj.userData && obj.userData.nombre && obj.userData.nombre.includes('Mesa de Comedor')) {
                    tableMesh = obj;
                }
            });
            checks.tableFound = !!tableMesh;
            checks.tableDimensions = tableMesh ? tableMesh.userData.dimensiones : null;
            checks.tableAnimState = window.diningTableAnimState ? {
                stage: window.diningTableAnimState.stage,
                labels: window.diningTableAnimState.stageLabels
            } : null;

            // 2. Check Logical Walls
            const westWall = window.logicalWallsRegistry ? window.logicalWallsRegistry.get('muro-ext-oeste-medianera') : null;
            checks.westWallFound = !!westWall;
            checks.westWallDims = westWall ? westWall.dimensiones : null;
            checks.totalLogicalWalls = window.logicalWallsRegistry ? window.logicalWallsRegistry.size : 0;

            // 3. Check Bookcase Banker's Lamp in WiZ list
            checks.wizStudyFixtures = (window.wizFixturesList || []).filter(f => f.room === 'study').length;

            // 4. Check Camera and preserveDrawingBuffer
            checks.preserveDrawingBuffer = window.renderer ? window.renderer.getContextAttributes().preserveDrawingBuffer : null;
            checks.isMobileOrLowEnd = typeof isMobileOrLowEnd !== 'undefined' ? isMobileOrLowEnd : null;

            // 5. Test 2D Switch & 3D Switch
            if (typeof switchTo2D === 'function') switchTo2D();
            checks.activeCameraAfter2D = (window.activeCamera === window.orthoCam) ? 'ortho' : 'persp';

            if (typeof switchTo3D === 'function') switchTo3D('isom', 'sims', true);
            checks.activeCameraAfter3D = (window.activeCamera === window.perspCam) ? 'persp' : 'ortho';

            return checks;
        })()`;

        const res = await sendCmd('Runtime.evaluate', { expression: testScript, returnByValue: true });

        console.log('RUNTIME ERRORS:', JSON.stringify(runtimeErrors, null, 2));
        console.log('RES:', JSON.stringify(res, null, 2));

        ws.close();
        chrome.kill();
    } catch (e) {
        console.error(e);
        try { chrome.kill(); } catch (_) {}
    }
})();