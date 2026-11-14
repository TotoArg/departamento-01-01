// ============================================================================
// SERVICE WORKER (sw.js) — GEMELO DIGITAL 3D (PWA OFFLINE-FIRST)
// Estrategia: "Cache First, falling back to Network" para assets 3D, WebGL,
// librerías Three.js, modelos .glb y mapas de iluminación HDRI (.hdr).
// ============================================================================

const CACHE_VERSION = 'gemelo-3d-pwa-v1.6';
const STATIC_CACHE_NAME = `${CACHE_VERSION}-static`;
const RUNTIME_CACHE_NAME = `${CACHE_VERSION}-runtime`;

// Lista completa de archivos estáticos críticos a precargar en la instalación
const PRECACHE_ASSETS = [
    './',
    './index.html',
    './manifest.json',
    './icons/icon-192x192.png',
    './icons/icon-512x512.png',

    // Motor Three.js, Controles y Geometrías Locales
    './libs/three.min.js',
    './libs/OrbitControls.js',
    './libs/geometries/RoundedBoxGeometry.js',

    // Loaders para Modelos 3D (.glb/.gltf) y Entornos HDRI (.hdr)
    './libs/loaders/GLTFLoader.js',
    './libs/loaders/DRACOLoader.js',
    './libs/loaders/RGBELoader.js',

    // Post-Procesamiento WebGL (EffectComposer, SSAO, SMAA, FXAA)
    './libs/math/SimplexNoise.js',
    './libs/postprocessing/EffectComposer.js',
    './libs/postprocessing/RenderPass.js',
    './libs/postprocessing/ShaderPass.js',
    './libs/postprocessing/SMAAPass.js',
    './libs/postprocessing/SSAOPass.js',
    './libs/shaders/CopyShader.js',
    './libs/shaders/FXAAShader.js',
    './libs/shaders/SMAAShader.js',
    './libs/shaders/SSAOShader.js',

    // Subcarpeta de Modelos 3D (.glb)
    './models/bathtub.glb',
    './models/bed.glb',
    './models/chair.glb',
    './models/desk.glb',
    './models/plant.glb',
    './models/sofa.glb',
    './models/toilet.glb',

    // Subcarpeta de Mapas de Iluminación HDRI (.hdr)
    './textures/hdr/ferndale_studio_04_1k.hdr'
];

// 1. INSTALACIÓN: Precarga tolerante a fallos de todos los recursos críticos
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(STATIC_CACHE_NAME).then(async (cache) => {
            await Promise.allSettled(
                PRECACHE_ASSETS.map(async (assetUrl) => {
                    try {
                        const req = new Request(assetUrl, { cache: 'reload' });
                        const res = await fetch(req);
                        if (res && res.ok) {
                            await cache.put(assetUrl, res);
                        }
                    } catch (err) {
                        console.warn('[SW Precache] Omitido temporalmente:', assetUrl);
                    }
                })
            );
            return self.skipWaiting();
        })
    );
});

// 2. ACTIVACIÓN: Limpieza de cachés antiguos y toma de control inmediata
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(
                keys
                    .filter((key) => key !== STATIC_CACHE_NAME && key !== RUNTIME_CACHE_NAME)
                    .map((oldKey) => caches.delete(oldKey))
            )
        ).then(() => self.clients.claim())
    );
});

// 3. INTERCEPTOR FETCH: Estrategia "Cache First, falling back to Network"
self.addEventListener('fetch', (event) => {
    const { request } = event;

    // Solo interceptar peticiones GET
    if (request.method !== 'GET') return;

    const url = new URL(request.url);

    // Ignorar canal SSE de LiveReload local y endpoints de API de sincronización en vivo
    if (url.pathname.includes('/__livereload') || url.pathname.includes('/api/')) {
        return;
    }

    // Para archivos de estado JSON (config.json / layout.json): Network First con fallback a Caché
    if (url.pathname.endsWith('/config.json') || url.pathname.endsWith('/layout.json')) {
        event.respondWith(
            fetch(request)
                .then((netRes) => {
                    if (netRes && netRes.ok) {
                        const clone = netRes.clone();
                        caches.open(RUNTIME_CACHE_NAME).then((c) => c.put(request, clone));
                    }
                    return netRes;
                })
                .catch(() => caches.match(request))
        );
        return;
    }

    // Estrategia principal PWA: "Cache First, falling back to Network"
    // Ideal para index.html, librerías Three.js, modelos .glb, texturas .hdr, CSS e íconos
    event.respondWith(
        caches.match(request, { ignoreSearch: request.mode === 'navigate' }).then((cachedResponse) => {
            if (cachedResponse) {
                // En documentos HTML, actualizar la caché en segundo plano (Stale-While-Revalidate silencioso)
                // para mantener paridad Zero Data Loss sin penalizar la velocidad de arranque instantánea
                if (request.mode === 'navigate' || (request.headers.get('accept') || '').includes('text/html')) {
                    fetch(request)
                        .then((freshRes) => {
                            if (freshRes && freshRes.ok) {
                                caches.open(STATIC_CACHE_NAME).then((c) => c.put('./index.html', freshRes));
                            }
                        })
                        .catch(() => {});
                }
                return cachedResponse;
            }

            // Si no está en caché, ir a la red y guardar en caché automáticamente (.glb, .hdr, .js, .png, etc.)
            return fetch(request)
                .then((networkResponse) => {
                    if (
                        networkResponse &&
                        networkResponse.status === 200 &&
                        (networkResponse.type === 'basic' || networkResponse.type === 'cors')
                    ) {
                        const responseClone = networkResponse.clone();
                        const isHeavy3DAsset =
                            url.pathname.endsWith('.glb') ||
                            url.pathname.endsWith('.gltf') ||
                            url.pathname.endsWith('.hdr') ||
                            url.pathname.includes('/libs/') ||
                            url.pathname.includes('/models/') ||
                            url.pathname.includes('/textures/') ||
                            url.pathname.includes('/icons/');
                        const targetCache = isHeavy3DAsset ? STATIC_CACHE_NAME : RUNTIME_CACHE_NAME;
                        caches.open(targetCache).then((cache) => {
                            cache.put(request, responseClone);
                        });
                    }
                    return networkResponse;
                })
                .catch(() => {
                    // Fallback offline para navegación principal
                    if (request.mode === 'navigate') {
                        return caches.match('./index.html') || caches.match('./');
                    }
                    return new Response('Offline', { status: 503, statusText: 'Offline' });
                });
        })
    );
});

self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});
