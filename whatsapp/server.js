const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const app = express();
app.use(express.json());

const client = new Client({ authStrategy: new LocalAuth() });
client.on('qr', qr => qrcode.generate(qr, { small: true }));
client.on('ready', () => console.log('WhatsApp client ready'));
client.initialize();

app.post('/send', async (req, res) => {
  const { phone, message } = req.body;
  try {
    const chatId = `${phone}@c.us`;
    const result = await client.sendMessage(chatId, message);
    res.json({ ok: true, id: result.id._serialized });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

app.get('/health', (_, res) => res.json({ ok: true }));
app.listen(3000, () => console.log('WhatsApp adapter on 3000'));
