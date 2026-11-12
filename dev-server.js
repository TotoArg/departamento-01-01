const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { exec, execSync } = require('child_process');

let PORT = parseInt(process.env.PORT || '8101', 10);
const clients = [];

// ============================================================================
// CONFIGURACIÓN DE SINCRONIZACIÓN BIDIRECCIONAL CON GITHUB
// ============================================================================
const GITHUB_REPO = 'TotoArg/departamento-01-01';
const GITHUB_FILE_PATH = 'config.json';
const GITHUB_LEGACY_FILE_PATH = 'layout.json';
let cachedGhToken = process.env.GITHUB_TOKEN || '';

function getGitHubToken() {
    if (cachedGhToken) return cachedGhToken;
    try {
        cachedGhToken = execSync('gh auth token', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
        return cachedGhToken;
    } catch (e) {
        return '';
    }
}

// Descargar config.json (o layout.json) desde GitHub API si es más reciente
async function fetchFileFromGitHub(filePath = GITHUB_FILE_PATH) {
    const token = getGitHubToken();
    return new Promise((resolve) => {
        const options = {
            hostname: 'api.github.com',
            path: `/repos/${GITHUB_REPO}/contents/${filePath}?ref=main`,
            method: 'GET',
            headers: {
                'User-Agent': 'DepartamentoSync/2.0',
                'Accept': 'application/vnd.github.v3+json',
                ...(token ? { 'Authorization': `token ${token}` } : {})
            }
        };

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                if (res.statusCode === 200) {
                    try {
                        const parsed = JSON.parse(data);
                        if (parsed.content) {
                            const decoded = Buffer.from(parsed.content, 'base64').toString('utf8');
                            const layoutObj = JSON.parse(decoded);
                            resolve({ ok: true, sha: parsed.sha, layout: layoutObj });
                            return;
                        }
                    } catch (e) {}
                }
                resolve({ ok: false, status: res.statusCode });
            });
        });
        req.on('error', () => resolve({ ok: false }));
        req.end();
    });
}

async function fetchLayoutFromGitHub() {
    const primary = await fetchFileFromGitHub(GITHUB_FILE_PATH);
    if (primary && primary.ok) return primary;
    return await fetchFileFromGitHub(GITHUB_LEGACY_FILE_PATH);
}

async function putFileToGitHub(filePath, layoutObj, token) {
    const ghInfo = await fetchFileFromGitHub(filePath);
    const currentSha = ghInfo && ghInfo.ok ? ghInfo.sha : undefined;
    const contentBase64 = Buffer.from(JSON.stringify(layoutObj, null, 2), 'utf8').toString('base64');
    const payload = JSON.stringify({
        message: `chore(state): sincronizar ${filePath} [${new Date(layoutObj.updatedAt || Date.now()).toLocaleTimeString()}]`,
        content: contentBase64,
        branch: 'main',
        ...(currentSha ? { sha: currentSha } : {})
    });

    return await new Promise((resolve) => {
        const req = https.request({
            hostname: 'api.github.com',
            path: `/repos/${GITHUB_REPO}/contents/${filePath}`,
            method: 'PUT',
            headers: {
                'User-Agent': 'DepartamentoSync/2.0',
                'Authorization': `token ${token}`,
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(payload)
            }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve({ status: res.statusCode, body: data }));
        });
        req.on('error', (err) => resolve({ status: 500, error: err.message }));
        req.write(payload);
        req.end();
    });
}

// Subir config.json y layout.json a GitHub API (commit automático en rama main)
let isPushingToGitHub = false;
async function pushLayoutToGitHub(layoutObj, retry = 1) {
    if (isPushingToGitHub) return;
    const token = getGitHubToken();
    if (!token) {
        console.warn('[GitHub Sync] No se encontró token de GitHub (gh auth token), omitiendo push a GitHub');
        return;
    }

    isPushingToGitHub = true;
    try {
        const resConfig = await putFileToGitHub(GITHUB_FILE_PATH, layoutObj, token);
        const resLayout = await putFileToGitHub(GITHUB_LEGACY_FILE_PATH, layoutObj, token);

        if ((resConfig.status === 200 || resConfig.status === 201) && (resLayout.status === 200 || resLayout.status === 201)) {
            console.log(`[GitHub Sync] ✓ config.json y layout.json sincronizados con GitHub (rama main)`);
        } else if ((resConfig.status === 409 || resLayout.status === 409) && retry > 0) {
            console.log(`[GitHub Sync] Conflicto de SHA en GitHub, reintentando...`);
            isPushingToGitHub = false;
            return await pushLayoutToGitHub(layoutObj, retry - 1);
        } else {
            console.warn(`[GitHub Sync] Aviso subiendo a GitHub (HTTP ${resConfig.status}/${resLayout.status})`);
        }
    } catch (e) {
        console.warn('[GitHub Sync] Error al comunicar con GitHub:', e.message);
    } finally {
        isPushingToGitHub = false;
    }
}

// Watch directory for hot live-reload
let reloadTimeout = null;
try {
    fs.watch(__dirname, { recursive: true }, (eventType, filename) => {
        if (!filename || filename.includes('node_modules') || filename.startsWith('.') || filename.endsWith('.tmp') || filename.includes('layout.json') || filename.includes('config.json')) return;
        if (reloadTimeout) clearTimeout(reloadTimeout);
        reloadTimeout = setTimeout(() => {
            console.log(`[Auto-Reload] Cambio detectado en ${filename}, actualizando navegador...`);
            clients.forEach(res => {
                try { res.write('data: reload\n\n'); } catch (e) {}
            });
        }, 120);
    });
} catch (e) {
    console.warn('Watch no disponible:', e.message);
}

const mimeTypes = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.ico': 'image/x-icon',
    '.svg': 'image/svg+xml'
};

const liveReloadScript = `
<!-- Auto Live-Reload Dev Script -->
<script>
(() => {
    try {
        const sse = new EventSource('/__livereload');
        sse.onmessage = (e) => {
            if (e.data === 'reload') {
                console.log('[LiveReload] Recargando...');
                window.location.reload();
            }
        };
        sse.onerror = () => {
            setTimeout(() => {
                try { new EventSource('/__livereload'); } catch (err) {}
            }, 3000);
        };
    } catch (err) {}
})();
</script>
`;

const server = http.createServer((req, res) => {
    console.log(`[REQ] ${req.method} ${req.url} de ${req.socket.remoteAddress}`);

    // Headers CORS para sincronización segura desde navegador local, celular o túnel
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    if (req.url === '/__livereload') {
        res.writeHead(200, {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache, no-transform',
            'Connection': 'keep-alive'
        });
        clients.push(res);
        req.on('close', () => {
            const idx = clients.indexOf(res);
            if (idx !== -1) clients.splice(idx, 1);
        });
        return;
    }

    const cleanUrl = req.url.split('?')[0];

    // Endpoint API para Sincronización Bidireccional ZERO DATA LOSS (config.json + layout.json + GitHub)
    if (cleanUrl === '/api/config' || cleanUrl === '/api/layout') {
        const configFilePath = path.join(__dirname, 'config.json');
        const layoutFilePath = path.join(__dirname, 'layout.json');
        if (req.method === 'GET') {
            (async () => {
                let localLayout = null;
                let localTs = 0;
                try {
                    if (fs.existsSync(configFilePath)) {
                        localLayout = JSON.parse(fs.readFileSync(configFilePath, 'utf8'));
                        localTs = localLayout.updatedAt || 0;
                    } else if (fs.existsSync(layoutFilePath)) {
                        localLayout = JSON.parse(fs.readFileSync(layoutFilePath, 'utf8'));
                        localTs = localLayout.updatedAt || 0;
                    }
                } catch (e) {}

                // Consultar GitHub por si hubo modificaciones hechas remotamente
                try {
                    const ghRes = await fetchLayoutFromGitHub();
                    if (ghRes && ghRes.ok && ghRes.layout && ghRes.layout.updatedAt > localTs) {
                        console.log(`[GitHub Sync] Cambios detectados en GitHub (${new Date(ghRes.layout.updatedAt).toLocaleTimeString()}). Actualizando config.json y layout.json...`);
                        const jsonOut = JSON.stringify(ghRes.layout, null, 2);
                        fs.writeFileSync(configFilePath, jsonOut, 'utf8');
                        fs.writeFileSync(layoutFilePath, jsonOut, 'utf8');
                        localLayout = ghRes.layout;
                    }
                } catch (err) {
                    // Si GitHub falla o no hay internet, continuamos con la copia local sin bloquear
                }

                if (localLayout) {
                    res.writeHead(200, {
                        'Content-Type': 'application/json; charset=utf-8',
                        'Cache-Control': 'no-cache, no-store, must-revalidate'
                    });
                    res.end(JSON.stringify(localLayout, null, 2));
                } else {
                    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
                    res.end(JSON.stringify({ app: 'departamento-01-01', schemaVersion: '2026.11.12.v3', updatedAt: 0, decorOverrides: { deleted: [], transforms: {} }, furnitureList: [] }));
                }
            })();
            return;
        }

        if (req.method === 'POST') {
            let body = '';
            req.on('data', chunk => { body += chunk; });
            req.on('end', () => {
                try {
                    const parsed = JSON.parse(body);
                    if (!parsed.updatedAt) parsed.updatedAt = Date.now();
                    parsed.app = 'departamento-01-01';
                    parsed.schemaVersion = parsed.schemaVersion || '2026.11.12.v3';
                    const jsonOut = JSON.stringify(parsed, null, 2);
                    fs.writeFileSync(configFilePath, jsonOut, 'utf8');
                    fs.writeFileSync(layoutFilePath, jsonOut, 'utf8');
                    res.writeHead(200, {
                        'Content-Type': 'application/json; charset=utf-8',
                        'Cache-Control': 'no-cache, no-store, must-revalidate'
                    });
                    res.end(JSON.stringify({ ok: true, updatedAt: parsed.updatedAt, files: ['config.json', 'layout.json'] }));
                    console.log(`[State Sync] config.json y layout.json sincronizados en disco (${new Date(parsed.updatedAt).toLocaleTimeString()})`);

                    // Replicar asíncronamente a GitHub para que GitHub Pages y el repositorio remoto queden sincronizados
                    pushLayoutToGitHub(parsed);
                } catch (err) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: 'JSON inválido', details: err.message }));
                }
            });
            return;
        }
    }

    let filePath = path.join(__dirname, cleanUrl === '/' ? 'index.html' : cleanUrl);

    if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
        filePath = path.join(filePath, 'index.html');
    }

    if (!fs.existsSync(filePath)) {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('404 Archivo no encontrado');
        return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const mime = mimeTypes[ext] || 'application/octet-stream';

    if (ext === '.html') {
        let content = fs.readFileSync(filePath, 'utf8');
        if (content.includes('</body>')) {
            content = content.replace('</body>', `${liveReloadScript}</body>`);
        } else {
            content += liveReloadScript;
        }
        res.writeHead(200, {
            'Content-Type': mime,
            'Cache-Control': 'no-cache, no-store, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0'
        });
        res.end(content);
    } else {
        res.writeHead(200, {
            'Content-Type': mime,
            'Cache-Control': 'no-cache, no-store, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0'
        });
        fs.createReadStream(filePath).pipe(res);
    }
});

function getLanIp() {
    const ifaces = os.networkInterfaces();
    for (const name of Object.keys(ifaces)) {
        for (const net of ifaces[name]) {
            if (net.family === 'IPv4' && !net.internal) {
                return net.address;
            }
        }
    }
    return '127.0.0.1';
}

function startServer(portToTry) {
    server.listen(portToTry, '0.0.0.0', () => {
        const localUrl = `http://localhost:${portToTry}`;
        const lanIp = getLanIp();
        const lanUrl = `http://${lanIp}:${portToTry}`;
        console.log(`\n======================================================`);
        console.log(`  🚀 SERVIDOR DE DESARROLLO LOCAL OFFLINE ACTIVO`);
        console.log(`  🏢 Proyecto: Departamento 01-01`);
        console.log(`  💻 Local (PC):          ${localUrl}`);
        console.log(`  📱 Celular / Red Local: ${lanUrl}`);
        console.log(`  ⚡ Hot-Reload: Activado (recarga automática al guardar)`);
        console.log(`  📦 Modo: 100% Offline (Three.js y controles en libs/)`);
        console.log(`======================================================\n`);
        
        if (!process.argv.includes('--no-open')) {
            try { exec(`start ${localUrl}`); } catch (e) {}
        }
    });

    server.on('error', (err) => {
        if (err.code === 'EADDRINUSE') {
            console.warn(`Puerto ${portToTry} ocupado, intentando con ${portToTry + 1}...`);
            startServer(portToTry + 1);
        } else {
            console.error('Error al iniciar el servidor:', err);
        }
    });
}

startServer(PORT);
