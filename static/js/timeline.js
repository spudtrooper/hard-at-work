var events = null;
var tweets = null;

function maybeCreateTimeline(date) {
  if (events && tweets) {
    createTimeline(date);
  }
}

function blockFormat(content) {
  // This is horrible, but don't break inside links. So, replace 'a href' now, then replace
  // back before returning.
  content = content.replace(/a href/g, 'A_HREF', content);
  var maxChars = 100;
  var words = content.split(' ');
  var lines = []
  var curLine = '';
  for (var i=0; i<words.length; i++) {
    var w = words[i];
    if ((w + ' ' + curLine).length > maxChars) {
      lines.push(curLine.trim());
      curLine = w;
    } else {
      curLine += ' ' + w;
    }
  }
  if (curLine) {
    lines.push(curLine.trim());
  }
  var res = lines.join('<br/>');
  res = res.replace(/A_HREF/g, 'a href', res);
  return res;
}

function createTimeline(date) {

  // Groups
  var groups = new vis.DataSet();
  groups.add({id: 1, content: 'Events'});
  groups.add({id: 0, content: 'Tweets'});

  var items = new vis.DataSet();

  for (var i = 0; i < tweets.length; i++) {
    var t = tweets[i];
    var start = t.date;
    var content = htmlize(t.text);
    var group = 1;
    var id = i;
    items.add({
      id: id,
      group: 0,
      align: 'left',
      content: content,
      start: start,
      type: 'box',
      className: 'tweet',
    });
  }
  var minDate = null;
  var maxDate = null;
  for (var i = 0; i < events.length; i++) {
    var e = events[i];
    var start = e.start_date;
    var end = e.end_date;
    var content = e.title || 'Missing @ ' + start;
    var group = 0;
    var id = i + tweets.length;
    if (!minDate || e.start_date < minDate) {
      minDate = e.start_date;
    }
    if (!maxDate || e.end_date > maxDate) {
      maxDate = e.end_date;
    }
    items.add({
      id: id,
      group: 1,
      align: 'left',
      content: blockFormat(content),
      title: content,
      start: start,
      end: end,
      type: 'range',
      className: 'event',
    });
  }

  var container = document.getElementById('timeline');
  var options = {
    groupOrder: function (a, b) {
      return a.id - b.id;
    },
  };
  if (date) {
    // Pad the range by an hour on each side.
    var startDate = new Date(Date.parse(minDate) - 60 * 60 * 1000);
    var endDate = new Date(Date.parse(maxDate) + 60 * 60 * 1000);
    options['start'] = String(startDate);
    options['end'] = String(endDate);
  }

  var timeline = new vis.Timeline(container);
  timeline.setOptions(options);
  timeline.setGroups(groups);
  timeline.setItems(items);
}

function init(date) {
  getWithCallback('/tweets', function(data) {
    tweets = data;
    maybeCreateTimeline(date);
  }, {date: date});
  getWithCallback('/events', function(data) {
    events = data;
    maybeCreateTimeline(date);
  }, {date: date});
}
