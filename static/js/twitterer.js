function htmlize(s) {
  var str = s;
  str = addSpaces(str, [
      /(pic\.twitter\.com)/,
      /(https?:\/\/)/
  ]);
  str = linkify(str, /https?:\/\/(\S+)\s/g);
  str = linkify(str, /(\w+[\.\w+]+\.[a-z][a-z][a-z]?[\/(\w|\?=&)+]+)/g);
  return str
    .replace(/(@)(\w+\W)/g, '<a href="http://twitter.com/$2">$1$2</a>')
    .replace(/[ ]+/g, ' ');
}

function addSpaces(str, res) {
  for (var i in res) {
    str = str.replace(res[i], ' $1');
  }
  return str;
}
function linkify(str, re) {
  var res = [];
  var parts = str.split(re);
  for (var i in parts) {
    var match = re.exec(parts[i]);
    console.log(i, ' ==> ', parts[i]);
    if (match) {
      console.log('have match ', parts[i], ' length=', match.length);
      var url = match[match.length - 1];
      var link = url;
      var text = url.replace(/https?:\/\//, '').substring(0, 50);
      res.push(' <a href="https://' + link + '">' + text + '</a> ');
    } else {
      res.push(parts[i]);
    }
  }
  return res.join('');
}
