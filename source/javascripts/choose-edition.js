$(function() {
  $('.choose-bom-edition a').click(function(e) {
    e.preventDefault();

    // Make the button show the selection
    var group = $(e.target).closest('.btn-group');
    var btn = group.find('button');
    btn.html($(e.target).html() + ' <span class="caret"></span>');

    // Show the selected edition of the BoM
    var req_edition = $(e.target).data('edition');
    var verse = group.closest('.verse');
    verse.find('.bom').hide();
    verse.find('.' + req_edition).show();
  });
});