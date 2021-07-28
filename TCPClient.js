const net = require('net');
const os = require('os');

const SERVER_ADDRESS = os.hostname()
const SERVER_PORT = 8000

var client = new net.Socket();
client.connect(SERVER_PORT, SERVER_ADDRESS, function() {
    console.log('Connected');
    client.write('Hello, server! Love, Client.');
});

client.on('data', function(data) {
    console.log('Received: ' + data);
    client.destroy(); // kill client after server's response
});