var usage = require('usage');

function trackPID(pid, interval, callback) {
  var self = this;
  this.int = setInterval(function checkUsage() {
    // you can use any valid PID instead
    usage.lookup(pid, { keepHistory: true }, function (err, result) {
      if (!err)
        callback(result);
      else
        console.error(err);
    });
  }, interval);
};

trackPID.prototype.stop = function () {
  clearInterval(this.int);
}

module.exports = trackPID;
