$(window).ready( function(e){
var emSize = parseFloat($('#accordionSidebar').css("width"))/parseFloat($("body").css("font-size"));
  if(emSize<=6.5){
    $('#collapseUtilities').attr("class","collapse");
    $('#collapseTwo').attr("class","collapse");
  }
});
