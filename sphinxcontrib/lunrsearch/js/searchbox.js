var Search = {
    store : null,
    index : null,

    init : function() {
        "use strict";

        this.highlight = $("#ls_lunrsearch-highlight").value === "true";

        $.ajax({
            url: $("#ls_search-index-url").val(),
            data: null, dataType: "script", cache: true,
            complete: function(jqxhr, textstatus) {
              if (textstatus != "success") {
                document.getElementById("lunrsearchindexloader").src = $("#ls_search-index-url").val();
              }
            }
        });
    }, // end init

    setIndex : function(data) {
        "use strict";
        lunr.tokenizer.seperator = '.';
        this.store = data.store;
        this.index = lunr(function () {
            this.field('prefix')
            this.field('name', { boost: 10 })
            this.ref('id')
        });

        for (var id in this.store) {
            this.index.add({
                id: id,
                name: this.store[id].name,
                prefix: this.store[id].prefix,
            });
        }

        this.initSearchCallbacks(this);
    },

    buildHref : function(self, s) {
        var highlightstring = self.highlight ? '?highlight=' + $.urlencode(s.name) : "";

        return DOCUMENTATION_OPTIONS.URL_ROOT + s.filename +
               DOCUMENTATION_OPTIONS.FILE_SUFFIX +
               highlightstring +
               '#' + s.prefix + '.' + s.name;
    }, // buildHref

    onKeyUp : function(self, event) {
        "use strict";
        var keycode = event.keyCode || event.which;

        if (keycode === 13) {
            return;
        }

        if (keycode === 40 || keycode === 38) {
            return this.handleKeyboardNavigation(self, keycode);
        }

        var query = $("#ls_search-field").val();
        var ul = $('#ls_search-results');

        if (query === '') {
            ul.empty().hide();
            return;
        }
        var results = self.index.search(query);
        ul.show();

        if (results.length == 0) {
            ul.empty().append($('<li><a href="#">No results found</a></li>'));
            return;
        }

        ul.empty();
        for (var i = 0; i < Math.min(results.length, 5); i++) {
            var result = results[i];
            var s = self.store[result.ref];
            var prefix = (s.objtype == "py:method") ? (s.last_prefix + ".") : "";

            var el = $('<li>')
                .append($('<a>')
                    .attr('href', self.buildHref(self, s))
                    .text(prefix + s.name)
                    .mouseenter(function() {
                        ul.find('li a').removeClass('hover');
                        $(this).addClass('hover');
                    })
                    .mouseleave(function() {
                        $(this).removeClass('hover');
                    })
                );
            ul.append(el);
        }
    },  // end onKeyUp

    initSearchCallbacks : function(self) {
        "use strict";
        $("#ls_search-field")
            .keyup(function(event) {self.onKeyUp(self, event)})
            .keypress(function(event) {
                if (event.keyCode === 13) {
                    event.preventDefault();
                    var active = $('#ls_search-results li a.hover')[0];
                    active.click();
                }
            })
            .focusout(function(){
                // http://stackoverflow.com/a/13980492/1079728
                window.setTimeout(function() {
                    $('.results').hide();
                }, 100);
            })
            .focusin(function(){
            if ($('#ls_search-results li').length > 0)
                $('#ls_search-results').show();
        });

    }, // end initSearchCallbacks

    handleKeyboardNavigation : function(self, keycode) {
        "use strict";

        var ul = $('#ls_search-results');
        var active = $(ul.find('li a.hover')[0])

        if (keycode === 40) {
            // next
            if (! active.length) {
                $(ul.find('li a')[0]).addClass('hover');
            } else {
                active.removeClass('hover');
                active.parent().next().find('a').addClass('hover');
            }
        } else if (keycode === 38) {
            // prev
            active.removeClass('hover');
            active.parent().prev().find('a').addClass('hover');
        }
    }, // end handle_navigation
};

window.onload = function() {
    Search.init();
}
