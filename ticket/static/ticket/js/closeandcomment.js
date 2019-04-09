/*  for old browser support provide a trim function
*/
if (!String.prototype.trim) {
  String.prototype.trim = function () {
    return this.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, '');
  };
}


/*  adds an EventListener for the commenttextbox on show_ticket.html
    if key is pressed and content of textbox is not empty, switch appearance
    of closeBtn and combineBtn else default
*/
// get the comment textbox from show_ticket.html
var textBox = document.getElementById('id_comment');
// get the close Button
closeBtn = document.getElementById('close');
// get the by default hidden "close and comment" button
combineBtn = document.getElementById('id_candc');
if(closeBtn && combineBtn){
  ['keyup','blur'].forEach( function(evt){
    textBox.addEventListener(evt, function(){
      if(!this.checkValidity() || !this.value.trim()){
        closeBtn.hidden = false;
        combineBtn.hidden = true;
      } else {
        closeBtn.hidden = true;
        combineBtn.hidden = false;
      }
    })
   });
}
