function is_umich_email(email)
{
    return email.split('@')[1] === 'umich.edu';
}

// Adapted from: http://benjamin-schweizer.de/jquerypostjson.html
$.postJSON = function(url, data, callback) {
    return jQuery.ajax({
        'type': 'POST',
        'url': url,
        'contentType': 'application/json',
        'data': JSON.stringify(data),
        'dataType': 'json',
        'success': callback
    });
};

// Adapted from: http://www.jsviews.com/#samples/jsr/composition/remote-tmpl
function lazy_get_template(name)
{
    // If the named remote template is not yet loaded and compiled
    // as a named template, fetch it. In either case, return a promise
    // (already resolved, if the template has already been loaded)
    var deferred = $.Deferred();
    var tmpl = $.templates[name];
    if (tmpl)
    {
        deferred.resolve(tmpl);
    }
    else
    {
        var url = '/static/autograder/jsrender-templates/' + name + '.tmpl';
        $.get(url).done(function(data) {
            // console.log(data);
            $.templates(name, data);
            deferred.resolve($.templates[name]);
        });
    }
    return deferred.promise();
}

function ajax_link_click_handler(e)
{
    e.preventDefault();
    var page_url = $(this).attr("href");
    window.history.pushState(null, "", page_url);
    load_view();
}
