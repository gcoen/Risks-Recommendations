console.log('This example is different!');
console.log('The result is displayed in the Command Line Interface');
console.log("baga buga")

var http = require('http');

http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('Heilo Woald!');
}).listen(8080);