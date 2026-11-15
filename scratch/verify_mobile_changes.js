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
    const userDataDir = 'C:\\Users\\tomas\\.gemini\\antigravity\\brain\\1e627548-1da8-4dd8-a641-13dac54942ad\\scratch\\chrome_verify_profile_' + Date.now();
    const chrome = spawn(CHROME_PATH, [
        '--headless=new',
        '--disable-gpu-sandbox',
        '--enable-webgl',
        '--ignore-gpu-blocklist',
        '--use-angle=swiftshader',
        '--remote-debugging-port=' + DEBUG_PORT,
        '--user-data-dir=' + userDataDir,
        '--window-size=1280,720',
        TARGET_URL
    ]);

    await new Promise(r => setTimeout(r, 2000));

    let versionInfo;
    for (let i = 0; i < 10; i++) {
        try {
            versionInfo = await getJson(`http://127.0.0.1:${DEBUG_PORT}/json/version`);
            if (versionInfo && versionInfo.webSocketDebuggerUrl) break;
        } catch (e) {
            await new Promise(r => setTimeout(r, 500));
        }
    }

    const pages = await getJson(`http://127.0.0.1:${DEBUG_PORT}/json`);
    const pageTarget = pages.find(p => p.type === 'page');

    const WebSocket = require('net');
    // Simple CDP evaluator via HTTP fetch / evaluate
    // Instead of raw net socket, let's use the ws URL if ws is available, or use node's built-in WebSocket if Node 24+
    let evalResult = null;
    if (typeof globalThis.WebSocket !== 'undefined') {
        const ws = new globalThis.WebSocket(pageTarget.webSocketDebuggerUrl);
        await new Promise((resolve, reject) => {
            ws.onopen = resolve;
            ws.onerror = reject;
        });

        // Wait for page to initialize 3D scene and sync
        await new Promise(r => setTimeout(r, 3000));

        let id = 1;
        function sendCDP(method, params = {}) {
            return new Promise((resolve) => {
                const reqId = id++;
                const handler = (evt) => {
                    const data = JSON.parse(evt.data);
                    if (data.id === reqId) {
                        ws.removeEventListener('message', handler);
                        resolve(data.result);
                    }
                };
                ws.addEventListener('message', handler);
                ws.send(JSON.stringify({ id: reqId, method, params }));
            });
        }

        const res = await sendCDP('Runtime.evaluate', {
            expression: `(() => {
                const deletedNames = [
                    'Bolsa Alimento para Perros (+RP)',
                    'Aspiradora Trineo Amarilla y Negra',
                    'Felpudo de Entrada (65×42 cm)'
                ];

                const deletedFound = [];
                apartmentGroup.traverse(c => {
                    const name = c.userData?.name || c.name;
                    if (name && deletedNames.includes(name)) {
                        deletedFound.push(name);
                    }
                });

                const transforms = {};
                apartmentGroup.traverse(c => {
                    const root = (typeof getSelectionRoot === 'function' ? getSelectionRoot(c) : null) || c;
                    const name = root.userData?.name || root.name;
                    if (name && [
                        'Diorama Consejo Jedi Star Wars',
                        'Guitarra en Funda Negra Acolchada (Estudio Sur)',
                        'Biblioteca Alta con Libros y Coleccionables',
                        'Mesa Ajedrez El Señor de los Anillos',
                        'Panel Calefactor Cuarto',
                        'Perchero y Zapatero Entrada'
                    ].includes(name)) {
                        if (!transforms[name]) {
                            transforms[name] = {
                                pos: { x: +root.position.x.toFixed(2), y: +root.position.y.toFixed(2), z: +root.position.z.toFixed(2) },
                                rotY: +root.rotation.y.toFixed(3)
                            };
                        }
                    }
                });

                return {
                    deletedItemsFoundInScene: Array.from(new Set(deletedFound)),
                    transformsFound: transforms
                };
            })()`,
            returnByValue: true
        });

        evalResult = res?.result?.value;
        ws.close();
    }

    chrome.kill('SIGKILL');

    console.log('Resultado de evaluación en Chrome real (perfil limpio):');
    console.log(JSON.stringify(evalResult, null, 2));

    if (!evalResult) {
        console.error('No se pudo obtener el resultado.');
        process.exit(1);
    }

    const okDeleted = evalResult.deletedItemsFoundInScene.length === 0;
    const okDiorama = Math.abs(evalResult.transformsFound['Diorama Consejo Jedi Star Wars']?.pos.z - 2.49) < 0.05;
    const okGuitarra = Math.abs(evalResult.transformsFound['Guitarra en Funda Negra Acolchada (Estudio Sur)']?.pos.z - 2.06) < 0.05;
    const okBiblio = Math.abs(evalResult.transformsFound['Biblioteca Alta con Libros y Coleccionables']?.pos.z - 1.31) < 0.05;
    const okCalefactor = Math.abs(evalResult.transformsFound['Panel Calefactor Cuarto']?.pos.z - 7.83) < 0.05;
    const okPerchero = Math.abs(evalResult.transformsFound['Perchero y Zapatero Entrada']?.pos.z - 5.02) < 0.05;
    const okAjedrezRot = Math.abs(evalResult.transformsFound['Mesa Ajedrez El Señor de los Anillos']?.rotY - 1.571) < 0.05;

    console.log('\n=== VERIFICACIÓN FINAL ===');
    console.log('Objetos eliminados removidos de escena:', okDeleted ? 'PASS' : 'FAIL (' + evalResult.deletedItemsFoundInScene.join(', ') + ')');
    console.log('Diorama Z=2.49:', okDiorama ? 'PASS' : 'FAIL');
    console.log('Guitarra Sur Z=2.06:', okGuitarra ? 'PASS' : 'FAIL');
    console.log('Biblioteca Z=1.31:', okBiblio ? 'PASS' : 'FAIL');
    console.log('Calefactor Cuarto Z=7.83:', okCalefactor ? 'PASS' : 'FAIL');
    console.log('Perchero Entrada Z=5.02:', okPerchero ? 'PASS' : 'FAIL');
    console.log('Ajedrez RotY=1.571 rad (90°):', okAjedrezRot ? 'PASS' : 'FAIL');

    if (okDeleted && okDiorama && okGuitarra && okBiblio && okCalefactor && okPerchero && okAjedrezRot) {
        console.log('\n>>> TODOS LOS CAMBIOS MÓVILES SE APLICARON Y CARGARON EXITOSAMENTE EN NAVEGADOR LIMPIO <<<');
        process.exit(0);
    } else {
        console.error('\n>>> ERROR: Alguna verificación falló <<<');
        process.exit(1);
    }
})();
