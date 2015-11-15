/*jslint browser: true*/
/*global $, jQuery, alert, lunr, Search, DOCUMENTATION_OPTIONS*/
(function () {
    "use strict";

    var store = null,
        index = null,
        highlight = null;

    function init() {
        var id = null;

        // Search.store is a global that's set before the window load
        // in searchbox.html
        store = Search.store;
        highlight = $("#ls_lunrsearch-highlight").value === "true";

        lunr.tokenizer.seperator = '.';
        index = lunr(function () {
            this.field('prefix');
            this.field('name', { boost: 10 });
            this.ref('id');
        });

        for (id in store) {
            if (store.hasOwnProperty(id)) {
                index.add({
                    id: id,
                    name: store[id].name,
                    prefix: store[id].prefix,
                });
            }
        }

        $("#ls_search-field")
            .keyup(function (event) {
                onKeyUp(event);
            })
            .keypress(function (event) {
                if (event.keyCode === 13) {
                    event.preventDefault();
                    var active = $('#ls_search-results li a.hover')[0];
                    active.click();
                }
            })
            .focusout(function () {
                // http://stackoverflow.com/a/13980492/1079728
                window.setTimeout(function () {
                    $('.results').hide();
                }, 100);
            })
            .focusin(function () {
                if ($('#ls_search-results li').length > 0) {
                    $('#ls_search-results').show();
                }
            });
    } // end init

    function onKeyUp(event) {
        var keycode = event.keyCode || event.which,
            query = $("#ls_search-field").val(),
            ul = $('#ls_search-results'),
            i = 0,
            results = null;

        if (keycode === 13) {
            return;
        }
        if (keycode === 40 || keycode === 38) {
            return handleKeyboardNavigation(keycode);
        }
        if (query === '') {
            ul.empty().hide();
            return;
        }

        results = index.search(query);
        ul.show();

        if (results.length === 0) {
            ul.empty().append($('<li><a href="#">No results found</a></li>'));
            return;
        }

        ul.empty();
        for (i = 0; i < Math.min(results.length, 5); i += 1) {
            ul.append(createResultListElement(store[results[i].ref]));
        }
    }  // end onKeyUp


    function handleKeyboardNavigation(keycode) {
        var ul = $('#ls_search-results'),
            active = $(ul.find('li a.hover')[0]);

        if (keycode === 40) {
            // next
            if (!active.length) {
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
    }  // end handleKeyboardNavigation

    function buildHref(s) {
        var highlightstring = highlight ? '?highlight=' + $.urlencode(s.name) : "";

        return DOCUMENTATION_OPTIONS.URL_ROOT + s.filename +
               DOCUMENTATION_OPTIONS.FILE_SUFFIX +
               highlightstring +
               '#' + s.prefix + '.' + s.name;
    } // end buildHref


    function createResultListElement(s) {
        var prefix = (s.objtype === "py:method") ? (s.last_prefix + ".") : "",
            ul = $('#ls_search-results');

        return $('<li>')
            .append($('<a>')
                .attr('href', buildHref(s))
                .text(prefix + s.name)
                .mouseenter(function () {
                    ul.find('li a').removeClass('hover');
                    $(this).addClass('hover');
                })
                .mouseleave(function () {
                    $(this).removeClass('hover');
                })
                );
    } // end createResultListElement

    window.onload = function () {
        init();
    };
}());
