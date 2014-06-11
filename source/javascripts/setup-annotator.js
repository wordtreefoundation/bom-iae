function evaluateXPath(xp, root, nsResolver) {
  return document.evaluate(
        '.' + xp,
        root || document,
        nsResolver || null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
      ).singleNodeValue
}

$(function() {
  if(Annotator.supported()) {
    var elem = document.getElementById('content');

    var Adder = Annotator.Plugin.fetch('Adder');
    var TextSelector = Annotator.Plugin.fetch('TextSelector');
    var LegacyRanges = Annotator.Plugin.fetch('LegacyRanges');
    var Editor = Annotator.Plugin.fetch('Editor');
    var Highlighter = Annotator.Plugin.fetch('Highlighter');
    var Viewer = Annotator.Plugin.fetch('Viewer');
    var Store = Annotator.Plugin.fetch('Store');
    // var Auth = Annotator.Plugin.fetch('Auth');
    // var Permissions = Annotator.Plugin.fetch('Permissions');
    var Unsupported = Annotator.Plugin.fetch('Unsupported');
    var Markdown = Annotator.Plugin.fetch('Markdown');
    var Tags = Annotator.Plugin.fetch('Tags');

    var annotator = (new Annotator.Factory())
      .addPlugin(Adder)
      .addPlugin(TextSelector, elem)
      .addPlugin(LegacyRanges, elem)
      .addPlugin(Highlighter, elem)
      .addPlugin(Viewer, {
        showEditButton: true,
        showDeleteButton: true,
      })
      .addPlugin(Editor)
      .setStore(Store, {prefix: 'http://annotate.wordtree.org/api'})
      // .addPlugin(Auth, {tokenUrl: 'http://localhost:4000/api/token'})
      // .addPlugin(Permissions)
      .addPlugin(Unsupported)
      .addPlugin(Markdown)
      .addPlugin(Tags)
      .getInstance();

    var current_uri = [location.protocol, '//', location.host, location.pathname].join('');
    annotator.subscribe('beforeAnnotationCreated', function (annotation) {
      var xpath = annotation.ranges[0].start;
      var el = evaluateXPath(xpath, elem);
      if (el) {
        var meta = {
          "edition": $(el).data('edition'),
          "book": $(el).data('book'),
          "chapter": $(el).data('chapter'),
          "verse": $(el).data('verse')
        };
        annotation.source_meta = meta;
        console.log("Added metadata: ", meta, annotation);
      } else {
        console.log("Unable to find xpath: ", xpath, annotation);
      }
      annotation.uri = current_uri;
    })
    annotator.attach(elem);
    annotator.annotations.load({uri: current_uri});

    annotator.on("all", function () {
      // console.log("Annotator event:", arguments);
    });
  } else {
    // Fallback for unsupported browsers.
    alert("Annotations are unsupported on your browser.");
  }

});