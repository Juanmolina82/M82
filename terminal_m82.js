const express = require('express');
const app = express();
const port = 3000;

const securityProtocol = (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (!authHeader) {
        res.setHeader('WWW-Authenticate', 'Basic realm="M82 Secure Area"');
        return res.status(401).send('Acceso Denegado: Credenciales Requeridas');
    }
    const credentials = Buffer.from(authHeader.split(' ')[1], 'base64').toString().split(':');
    const [user, pass] = [credentials[0], credentials[1]];

    if (user === 'chairman' && pass === 'Molina2026!') {
        next();
    } else {
        res.setHeader('WWW-Authenticate', 'Basic realm="M82 Secure Area"');
        return res.status(401).send('Fallo de Autenticación: Identidad No Verificada');
    }
};

app.use(securityProtocol);

const getMarketFeed = () => [
    { asset: 'BRENT', val: '96.79', diff: '+1.24', p: '1.28%', state: 'up' },
    { asset: 'WTI', val: '91.45', diff: '+0.85', p: '0.94%', state: 'up' },
    { asset: 'IRON', val: '114.50', diff: '+2.10', p: '1.87%', state: 'up' },
    { asset: 'COPPER', val: '9,120', diff: '-45.00', p: '0.49%', state: 'down' }
];

app.get('/', (req, res) => {
    const marketData = getMarketFeed();
    const headerCards = marketData.map(i => `
        <div style="flex:1; border-right:1px solid #222; padding:10px; min-width:130px; background:#111;">
            <div style="font-size:10px; color:#666;">${i.asset}</div>
            <div style="font-size:16px; font-weight:bold; color:#fff;">${i.val}</div>
            <div style="font-size:11px; color:${i.state === 'up' ? '#00ff41' : '#ff3131'};">
                ${i.state === 'up' ? '▲' : '▼'} ${i.diff} (${i.p})
            </div>
        </div>
    `).join('');

    res.send(`
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>M82 TERMINAL | MOLINA HOLDINGS</title>
        </head>
        <body style="background:#000; color:#0f0; font-family:monospace; margin:0; padding-top:80px;">
            <div style="position:fixed; top:0; left:0; width:100%; height:75px; background:#111; display:flex; border-bottom:2px solid #00ff41; z-index:1000; overflow-x:auto;">
                ${headerCards}
            </div>
            <div style="padding:25px; text-align:center;">
                <h1 style="letter-spacing:10px; color:#00ff41;">MOLINA HOLDINGS LLC</h1>
                <div style="border:1px solid #333; background:#050505; padding:25px; border-radius:10px; box-shadow: 0 0 20px rgba(0,255,65,0.1);">
                    <h2 style="color:#fff; margin-bottom:5px;">M82 QUANT AUDIT V50</h2>
                    <p style="color:#444; font-size:12px;">NODE: TENNESSEE // STATUS: ONLINE</p>
                    <hr style="border:0; border-top:1px solid #222; margin:20px 0;">
                    <div style="text-align:left; border-left:3px solid #c00; padding-left:15px; background:rgba(200,0,0,0.05); padding:10px;">
                        <b style="color:#fff;">JSOC IRAN ALERT:</b>
                        <p style="color:#ff3131; margin:5px 0;">Hormuz Stress Index: 0.9705 [CRITICAL]</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
    `);
});

app.listen(port, () => {
    console.log('\x1b[32m%s\x1b[0m', '--- M82 CORE V50: DEPLOYED AND ENCRYPTED (PORT 3000) ---');
});
