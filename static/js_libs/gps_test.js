var SerialPort = require('serialport');
var port = new SerialPort('/dev/cu.usbmodem1451', {
    baudRate: 9600
}, function(error) {
    if (error) {
        return console.log('Error: ', error.message);
    }
});

// open errors will be emitted as an error event
port.on('error', function(err) {
    console.log('Error: ', err.message);
})

port.on('data', function(data) {
    console.log('Data: ' + data);
});