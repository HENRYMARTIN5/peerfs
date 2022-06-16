var http = require("http");

var server = http.createServer(function (request ,response)  {

console.log('got a request');
response.write("<div></br> hey</div>");
response.end();
}
);

server.listen(3000);