const INCLUDE_SOURCE_LINK = false;

function render(conflicts) {
  $('#loading').hide();

  var table = $('<table>').addClass('table');
  var tr = $('<tr>');
  table.append(tr);
  tr.append($('<th>').html('Date').addClass('date'));
  tr.append($('<th>').html('Tweet'));
  tr.append($('<th>').html('Event'));
  $(conflicts).each(function(i, c) {
    var tr = $('<tr>');
    table.append(tr);

    // Date
    var dateLink = $('<a>')
      .attr('href', '/timeline?date=' + c['tweet_date'].split(' ')[0])
      .text(c['tweet_date']);
    var dateTd = $('<td>').addClass('date');
    dateTd.append(dateLink);
    tr.append(dateTd);
    
    // Tweet
    var sourceLink = $('<a>')
      .attr('href', 'https://twitter.com/realdonaldtrump/status/' + c['tweet_id'])
      .text('Source');
    var tweetTd = $('<td>');
    tweetTd.append($('<span>').html(htmlize(c['tweet_text'])));
    if (INCLUDE_SOURCE_LINK) {
      tweetTd.append(' [');
      tweetTd.append(sourceLink);
      tweetTd.append(']');
    }
    tr.append(tweetTd);

    // Event
    tr.append($('<td>').html(c['event_title']));
  });
  $('#conflicts').append(table);
  $('#conflicts').show();
}

function init() {
  getWithCallback('/getconflicts', render);
}
