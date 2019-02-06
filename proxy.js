let http = require('http');
let request = require('request')
let argv = require('yargs').argv


let localhost = '127.0.0.1'
let scheme = 'http://'
let host = argv.host || localhost
let port = argv.port || (host === localhost ? 8000 : 80)
let destinationUrl = scheme + host + ':' + port


let echoServer = http.createServer(function(req, res) {
  console.log('echoServer')
  for(let header in req.headers){
    res.setHeader(header, req.headers[header])
  }
  req.pipe(res)
})
echoServer.listen(8000)

let proxyServer = http.createServer(function(req, res){
  console.log("proxyServer")
  console.log(req.url)
  // x-destination-url

  let url = destinationUrl
  if(req.headers['x-destination-url']){
  	url = 'http://' + req.headers['x-destination-url']
  }

  let options = {
    url: url + req.url
  }

  let outboundRequest = request(options)
  req.pipe(outboundRequest).pipe(res)
})
proxyServer.listen(9000)