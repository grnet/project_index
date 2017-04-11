$(document).ready(function (){

  /**
   * Presents an instance. This is implemented by adding the actual `div`
   * element in an empty row (`#presenter`) which takes up a full screen
   * (horizontally).
   */
  function presentInstance() {

    // remove all already presented items
    restoreAllPresented();
    var instanceHolder = $('#instance-holder-' + this.id.split('-')[1]);
    // remove element from "instance-holder", add it to "presenter"
    instanceHolder.detach().appendTo($('#presenter'));
    // display "deployments-info" div
    instanceHolder.find('.deployments-info').removeClass('hidden');
    // Collapse list with commits
    instanceHolder.find('#collapse-' + this.id.split('-')[1]).addClass('in');
    // Scroll window to top
    window.scrollTo(0,0);
    // unbind handler (we do not want it when Instance is presented
    $(this).unbind('click');
  }

  /**
   * Removes all "presented" `div`s from the `#presenter` `div`
   */
  function restoreAllPresented(){

    $('#presenter').children().find('[class*="deployment-details-"]').addClass('hidden');
    $('#presenter').children().find('[class*="deployments-info"]').addClass('hidden');
    $('#presenter').children().detach().appendTo($('#holder'));
    $('#holder').children().find('[id^="collapse-"]').removeClass('in');
    // rebind previously removed handler
    $('#holder').children().find($('[id^="expander"]'))
    .bind('click', presentInstance);
  }

  function presentCommit(){
    var identifier = $(this).data('c-id');
    var author = $(this).data('c-auth');
    var date = $(this).data('c-date');
    var message = $(this).data('c-message');

    var commitPanel = '';
    commitPanel += '<samp>';
    commitPanel += '<div style="color:#5cb85c">';
    commitPanel += 'commit ' + identifier + '<br/>';
    commitPanel += '</div>';
    commitPanel += 'Author: ' + author + '<br/>';
    commitPanel += 'Date:   ' + date + '<br/>';
    commitPanel += '<br/>' + '<br/>';
    commitPanel += '<pre>' + message + '</pre>';
    commitPanel += '</samp>';

    $(this).parent().parent().children('div.well').html(commitPanel);
    $(this).parent().parent().children('div.well').removeClass('hidden');
  }
  $('[id^="expander"]').bind('click', presentInstance);

  // $('[id^="instance-panel-"]').each(function () {
  $('[id^="undeployed-commits-"], [id^="deployment-commits-"]').click(function () {
    var url = $(this).data('url');

    if ($(this).data('project-slug')){
      url += '?project=' + $(this).data('project-slug');
    }

    $('.deployment-selected').removeClass('deployment-selected');
    $(this).addClass('deployment-selected');
    var that = this;
    var instance_id = this.id.split('-')[2];
    $(that).find('span[class^="gear"]').removeClass('hidden');

    $.get(url).done(function(data){

      $('#commit-list-' + instance_id).children().detach();
      var commitData = data.data;

      var htmlMessage;
      var tooltipText;
      // need case if status is not success
      if (data.status.type === 'success'){
        htmlMessage = commitData.length;
        var index;
        for (index = commitData.length-1 ; index >= 0; index--){

          var commitRowId = 'commit-toggler-' + instance_id + '-' + index;

          var commitRow = '<li class="list-group-item" ';
          commitRow += 'id="' + commitRowId +'"';
          commitRow += 'data-c-id="' + commitData[index].identifier + '"';
          commitRow += 'data-c-auth="' + commitData[index].author + '"';
          commitRow += 'data-c-date="' + commitData[index].date + '"';
          commitRow += 'data-c-message="' + commitData[index].message + '"';
          commitRow += '>';
          commitRow += '<code>#' + commitData[index].identifier.slice(0,6);
          commitRow += '</code> ';
          commitRow += '<samp>' + commitData[index].summary + '</samp>';
          commitRow += '</li>';

          $('#commit-list-' + instance_id).append(commitRow);
          $('#' + commitRowId).bind('click', presentCommit);
        }
      }
      $(that).find('span[class^="gear"]').addClass('hidden');
      $(that).find('span[class^="badge"]').html(htmlMessage);
      $(that).find('span[class^="badge"]').removeClass('hidden');
      $(that).find('span[class^="badge"]').addClass('success');
      $('div[class*="deployment-details-' + instance_id +'"]').removeClass('hidden');

    }).fail(function(param1, param2, param3, param4){

      $(that).find('span[class^="gear"]').addClass('hidden');
      $(that).find('span[class^="badge"]').tooltip(
        {title: param2 + ':' + param3, placement: 'left'});
      $(that).find('span[class^="badge"]').html('!');
      $(that).find('span[class^="badge"]').removeClass('hidden');
      $(that).find('span[class^="badge"]').addClass('error');
    });
  });
});
