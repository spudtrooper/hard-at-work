const _ALERT_TIMEOUT_MILLIS = 2000;
const _DEFAULT_RELOAD_TIMEOUT_MILLIS = 50;

function reload_(opt_url, opt_timeout) {
  setTimeout(function() {
    document.location = opt_url ? opt_url : String(document.location).replace(/#.*/, '');
  }, opt_timeout || _DEFAULT_RELOAD_TIMEOUT_MILLIS);
}

function request(url, method, opt_data, opt_afterUrl, opt_timeout) {
  var data = opt_data || {};
  $.ajax({
    url: url,
    data: data,
    method: method,
    context: document.body
  }).done(function(str) {
    console.log('Have response: ' + str);
    reload_(opt_afterUrl, opt_timeout);
  });
}

function get(url, opt_data, opt_afterUrl, opt_timeout) {
  request(url, 'GET', opt_data, opt_afterUrl, opt_timeout);
}

function post(url, opt_data, opt_afterUrl, opt_timeout) {
  request(url, 'POST', opt_data, opt_afterUrl, opt_timeout);
}

function requestWithCallback(url, method, callback, opt_data, opt_timeout) {
  var data = opt_data || {};
  $.ajax({
    url: url,
    data: data,
    method: method,
    context: document.body
  }).done(function(str) {
    console.log('Have response: ' + str);
    setTimeout(function() {
      if (callback) {
        callback.call(null, str);
      }
    }, opt_timeout || 50);
  });
}

function getWithCallback(url, callback, opt_data, opt_timeout) {
  requestWithCallback(url, 'GET', 
                      createCallbacksFromCallbacks(callback, undefined /* opt_onFailure */), 
                      opt_data, opt_timeout);
}

function postWithCallback(url, callback, opt_data, opt_timeout) {
  requestWithCallback(url, 'POST', 
                      createCallbacksFromCallbacks(callback, undefined /* opt_onFailure */), 
                      opt_data, opt_timeout);
}

/**
 * Creates a callback that consumes a JSON string with a 'status'
 * field and calls {@code onSuccess} when status == 'OK', otherwise
 * calls {@code opt_onFailure} if this function is defined.
 * @param {function(!Object)=} opt_onSuccess
 * @param {function(!Object)=} opt_onFailure
 * @return {function(string)}
 */
function createCallbacksFromCallbacks(opt_onSuccess, opt_onFailure) {
  var callback = function(str) {
    var obj = JSON.parse(str);
    console.log('Response: ' + str);
    if (obj.status == 'OK') {
      if (opt_onSuccess) {
        opt_onSuccess.call(null, obj.data);
      }
    } else {
      if (opt_onFailure) {
        opt_onFailure.call(null, obj.data);
      }
    }
  };
  return callback;
}

function postWithCallbacks(url, opt_onSuccess, opt_onFailure, opt_data, opt_timeout) {
  requestWithCallback(url, 'POST', 
                      createCallbacksFromCallbacks(opt_onSuccess, opt_onFailure), 
                      opt_data, opt_timeout);
}

function pad(i) {
  return i < 10 ? "0" + i : String(i);
}

function stringToDate(dateString) {
  // 2010-03-15 10:30:00
  var arr = dateString.split(/[- :]/);
  return new Date(arr[0], arr[1]-1, arr[2], arr[3], arr[4], arr[5]);
}

function formatDate(d) {
  return [String(d.getYear() + 1900), pad(d.getMonth() + 1), pad(d.getDate())].join('-');
}
