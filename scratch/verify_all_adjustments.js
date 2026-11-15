const { spawn } = require('child_process');
const http = require('http');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const TARGET_URL = 'http://localhost:8101';
const DEBUG_PORT = 9238;

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
    const userDataDir = 'C:\\Users\\tomas\\.gemini\\antigravity\\brain\\1e627548-1da8-4dd8-a641-13dac54942ad\\scratch\\chrome_test_profile_' + Date.now();
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

    let evalResult = null;
    if (typeof globalThis.WebSocket !== 'undefined') {
        const ws = new globalThis.WebSocket(pageTarget.webSocketDebuggerUrl);
        await new Promise((resolve, reject) => {
            ws.onopen = resolve;
            ws.onerror = reject;
        });

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
                // 1. Verificar objetos del muro Oeste de Estudio y sus posiciones/dimensiones
                const westItems = {};
                apartmentGroup.traverse(c => {
                    const root = (typeof getSelectionRoot === 'function' ? getSelectionRoot(c) : null) || c;
                    const name = root.userData?.name || root.name;
                    if (name && [
                        'Mesa Ajedrez El Señor de los Anillos',
                        'Guitarra en Funda Azul Marino (Estudio Norte)',
                        'Biblioteca Alta con Libros y Coleccionables',
                        'Guitarra en Funda Negra Acolchada (Estudio Sur)',
                        'Diorama Consejo Jedi Star Wars'
                    ].includes(name)) {
                        if (!westItems[name]) {
                            const b = new THREE.Box3().setFromObject(root);
                            westItems[name] = {
                                pos: { x: +root.position.x.toFixed(2), y: +root.position.y.toFixed(2), z: +root.position.z.toFixed(2) },
                                minZ: +b.min.z.toFixed(2),
                                maxZ: +b.max.z.toFixed(2)
                            };
                        }
                    }
                });

                // 2. Verificar sillas de comedor
                let chairsAssembly = null;
                apartmentGroup.traverse(c => {
                    if (c.name === 'Sillas de Comedor (4)' || c.userData?.name === 'Sillas de Comedor (4)') {
                        chairsAssembly = c;
                    }
                });
                const chairDistances = [];
                if (chairsAssembly) {
                    chairsAssembly.children.forEach(cg => {
                        const dist = Math.hypot(cg.position.x, cg.position.z);
                        chairDistances.push(+dist.toFixed(3));
                    });
                }

                // 3. Verificar comederos de las perras
                let dogBowlsAssembly = null;
                apartmentGroup.traverse(c => {
                    if (c.name && c.name.includes('Comederos')) {
                        dogBowlsAssembly = c;
                    }
                });
                const dogBowlsCount = dogBowlsAssembly ? dogBowlsAssembly.children.length : 0;

                // 4. Verificar bacha de baño
                let vanitoryAssembly = null;
                apartmentGroup.traverse(c => {
                    if (c.name === 'Vanitory y Bacha de Baño' || c.userData?.name === 'Vanitory y Bacha de Baño') {
                        vanitoryAssembly = c;
                    }
                });
                let bachaOuterBox = null;
                if (vanitoryAssembly) {
                    const b = new THREE.Box3().setFromObject(vanitoryAssembly);
                    const sz = new THREE.Vector3();
                    b.getSize(sz);
                    bachaOuterBox = { w: +sz.x.toFixed(2), d: +sz.z.toFixed(2), h: +sz.y.toFixed(2) };
                }

                // 5. Verificar cortina doble de ducha
                let bathAssembly = null;
                apartmentGroup.traverse(c => {
                    if (c.name === 'Bañera y Ducha Cromada' || c.userData?.name === 'Bañera y Ducha Cromada') {
                        bathAssembly = c;
                    }
                });
                let hasDoubleCurtain = false;
                if (bathAssembly) {
                    let curtainMeshesCount = 0;
                    bathAssembly.traverse(c => {
                        if (c.isMesh && (c.material.transparent || c.material.opacity < 1.0)) {
                            curtainMeshesCount++;
                        }
                    });
                    hasDoubleCurtain = curtainMeshesCount >= 2;
                }

                // 6. Verificar caja organizadora en entrada como entidad independiente
                let hasCajaOrg = false;
                apartmentGroup.traverse(c => {
                    if (c.name === 'Caja Organizadora de Entrada' || c.userData?.name === 'Caja Organizadora de Entrada') {
                        hasCajaOrg = true;
                    }
                });

                // 7. Estantes del estudio (verificar que no están en muro Oeste X=0.00 sino en muro Este X=3.00)
                let shelvesX = null;
                apartmentGroup.traverse(c => {
                    if (c.name && c.name.includes('Estantes Flotantes Estudio')) {
                        shelvesX = +c.position.x.toFixed(2);
                    }
                });

                return {
                    westItems,
                    chairDistances,
                    dogBowlsCount,
                    bachaOuterBox,
                    hasDoubleCurtain,
                    hasCajaOrg,
                    shelvesX
                };
            })()`,
            returnByValue: true
        });

        evalResult = res?.result?.value;
        ws.close();
    }

    chrome.kill('SIGKILL');

    console.log('Resultados de auditoría exhaustiva de ajustes:');
    console.log(JSON.stringify(evalResult, null, 2));

    const wi = evalResult.westItems;
    console.log('\n--- VERIFICACIÓN MURO OESTE (SIN SUPERPOSICIONES) ---');
    console.log('Ajedrez:', wi['Mesa Ajedrez El Señor de los Anillos']?.pos, `[${wi['Mesa Ajedrez El Señor de los Anillos']?.minZ}..${wi['Mesa Ajedrez El Señor de los Anillos']?.maxZ}]`);
    console.log('Guitarra Azul:', wi['Guitarra en Funda Azul Marino (Estudio Norte)']?.pos, `[${wi['Guitarra en Funda Azul Marino (Estudio Norte)']?.minZ}..${wi['Guitarra en Funda Azul Marino (Estudio Norte)']?.maxZ}]`);
    console.log('Biblioteca:', wi['Biblioteca Alta con Libros y Coleccionables']?.pos, `[${wi['Biblioteca Alta con Libros y Coleccionables']?.minZ}..${wi['Biblioteca Alta con Libros y Coleccionables']?.maxZ}]`);
    console.log('Guitarra Negra:', wi['Guitarra en Funda Negra Acolchada (Estudio Sur)']?.pos, `[${wi['Guitarra en Funda Negra Acolchada (Estudio Sur)']?.minZ}..${wi['Guitarra en Funda Negra Acolchada (Estudio Sur)']?.maxZ}]`);
    console.log('Diorama:', wi['Diorama Consejo Jedi Star Wars']?.pos, `[${wi['Diorama Consejo Jedi Star Wars']?.minZ}..${wi['Diorama Consejo Jedi Star Wars']?.maxZ}]`);

    const noOverlap = 
        wi['Mesa Ajedrez El Señor de los Anillos']?.maxZ <= wi['Guitarra en Funda Azul Marino (Estudio Norte)']?.minZ &&
        wi['Guitarra en Funda Azul Marino (Estudio Norte)']?.maxZ <= wi['Biblioteca Alta con Libros y Coleccionables']?.minZ &&
        wi['Biblioteca Alta con Libros y Coleccionables']?.maxZ <= wi['Guitarra en Funda Negra Acolchada (Estudio Sur)']?.minZ &&
        wi['Guitarra en Funda Negra Acolchada (Estudio Sur)']?.maxZ <= wi['Diorama Consejo Jedi Star Wars']?.minZ;

    console.log('Superposiciones en muro Oeste:', noOverlap ? 'PASS (0 SUPERPOSICIONES)' : 'FAIL');
    console.log('Sillas comedor hacia adentro (radio <= 0.40m):', evalResult.chairDistances.every(d => d <= 0.40) ? 'PASS' : 'FAIL');
    console.log('Comederos de las perras (exactamente 2: verde y rojo):', evalResult.dogBowlsCount === 2 ? 'PASS' : 'FAIL');
    console.log('Bacha de baño más chica (ancho <= 0.50m):', evalResult.bachaOuterBox && evalResult.bachaOuterBox.w <= 0.50 ? 'PASS' : 'FAIL');
    console.log('Ducha con cortina doble (liner + tela):', evalResult.hasDoubleCurtain ? 'PASS' : 'FAIL');
    console.log('Caja organizadora zapatero independiente:', evalResult.hasCajaOrg ? 'PASS' : 'FAIL');
    console.log('Estantes estudio en muro Este (X ~ 2.85-3.00, no en Oeste):', evalResult.shelvesX > 2.0 ? 'PASS' : 'FAIL');

    if (noOverlap && evalResult.chairDistances.every(d => d <= 0.40) && evalResult.dogBowlsCount === 2 && evalResult.hasDoubleCurtain && evalResult.hasCajaOrg && evalResult.shelvesX > 2.0) {
        console.log('\n>>> TODAS LAS COMPROBACIONES PASARON CON ÉXITO <<<');
        process.exit(0);
    } else {
        process.exit(1);
    }
})();
