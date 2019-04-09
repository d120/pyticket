/*
  initializes the markdown editor for new and edit new_ticket
  replaces id_text/description form field with this custom editor
  used on new_ticket.html and edit_ticket.html
*/
var inscrybmde = new InscrybMDE({
  element: document.getElementById("id_text"),
  hideIcons: ["guide", "image"],
  placeholder: "Hier eingeben...",
  // marked is markdown parser for preview
  previewRender: function(plainText) {
    return marked(plainText); // Returns HTML from a custom parser
  },
  previewRender: function(plainText, preview) { // Async method
    setTimeout(function() {
      preview.innerHTML = marked(plainText);
    }, 250);

    return "Loading...";
  },
  spellChecker: false,
  syncSideBySidePreviewScroll: false,
  styleSelectedText: false,
});

//no Tabs allowed in Editor to allow tabbing to next form field
var map = {Tab : false};
inscrybmde.codemirror.addKeyMap(map);
