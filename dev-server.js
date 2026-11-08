const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const PORT = process.env.PORT || 3000;
const clients = [];

// Watch directory for hot live-reload
let reloadTimeout = null;
try {
    fs.watch(__dirname, { recursive: true }, (eventType, filename) => {
        if (!filename || filename.includes('node_modules') || filename.startsWith('.') || filename.endsWith('.tmp')) return;
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
            'Cache-Control': 'no-cache, no-store, must-revalidate'
        });
        res.end(content);
    } else {
        res.writeHead(200, {
            'Content-Type': mime,
            'Cache-Control': 'no-cache'
        });
        fs.createReadStream(filePath).pipe(res);
    }
});

server.listen(PORT, () => {
    const url = `http://localhost:${PORT}`;
    console.log(`\n======================================================`);
    console.log(`  🚀 SERVIDOR DE DESARROLLO LOCAL OFFLINE ACTIVO`);
    console.log(`  🔗 URL: ${url}`);
    console.log(`  ⚡ Hot-Reload: Activado (recarga automática al guardar)`);
    console.log(`  📦 Modo: 100% Offline (Three.js y controles en libs/)`);
    console.log(`======================================================\n`);
    
    // Auto abrir en Windows si no se pasa --no-open
    if (!process.argv.includes('--no-open')) {
        try { exec(`start ${url}`); } catch (e) {}
    }
});
