/**
  Homepage feeds
*/

$(function(){
  var feed_container = $('#latest-changes');

  $.ajax({type:'GET', url:'/dataset?q=&sort=metadata_modified+desc'})
    .done(function(data){
      feed_container.css({
        'padding': '10px',
        'overflow': 'auto',
        'height': '190px',
      });
      feed_container.html($(data).find('.dataset-list'));
    });
});