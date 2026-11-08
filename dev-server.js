const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { exec } = require('child_process');

let PORT = parseInt(process.env.PORT || '8101', 10);
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
    console.log(`[REQ] ${req.method} ${req.url} de ${req.socket.remoteAddress}`);
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
