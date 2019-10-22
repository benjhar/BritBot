const nodeWrap = require('node-wrap')
const exec = require('child_process')
const dotenv = require('dotenv');
var secret = process.env.SECRET
var repo = process.env.REPO
let http = require('http');
let crypto = require('crypto');

http.createServer(function (req, res) {
    req.on('data', function(chunk) {
        nodeWrap.stop();
        let sig = "sha1=" + crypto.createHmac('sha1', secret).update(chunk.toString()).digest('hex');

        if (req.headers['x-hub-signature'] == sig) {
            exec('cd ' + repo + ' && git pull');
        }
        nodeWrap.start();
    });

    res.end();
    console.log('Updated from Github')
}).listen(8078);

nodeWrap("python bot.py", {
    restartOnCrash: true,                   // whether the child process should be restarted after it crashed
    crashTimeout: 300,                     // the timeout after a crash after which the child process should be restarted
    restartTimeout: 0,                      // the timeout after a restart command after which the child process should be restarted
    console: true,                          // whether node-wrap should log some important info to the main console (stuff like "Starting process" and "Restarting process")
    logFile: "./wrapper.log",               // logs all status codes to that file, leave null or undefined for no file logging
    logConsoleOutput: true,                 // logs all console outputs of the child process to that file, leave null or undefined for no file logging
    logTimestamp: true,                     // whether a timestamp should be added to the above logs
    restartCodes: [0]                        // what additional exit codes should invoke a restart
});
