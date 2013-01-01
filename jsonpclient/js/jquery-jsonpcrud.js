/*jslint devel: true, maxerr: 100, browser: true, indent: 4 */
/*
This requires before this file:
    * JQuery : http://code.jquery.com/jquery-1.6.1.js
    * JSON2 : http://www.JSON.org/json2.js

Oisin Mulvihill
2012-12-18.

*/
(function ($) {

    // Joined with the #base_uri input value from index.html:
    var PING_URI = "ping";

    var JSONP_TIMEOUT = 2000;

    function debug_logger(msg) {
        try {
            if (window.console) {
                console.log(msg);
            }
        } catch (e) {
            /* Ignore as firebug is turned off or not available. */
        }
    }

    function server_uri(other) {
        if (!other) {
            other = "";
        }
        var uri = $("#base_uri").val();
        uri = uri + "/" + other;
        debug_logger("server_uri: <" + uri + ">");
        return uri;
    }

    function data_to_send() {
        var data = $("#json_data").val() || "{}";
        debug_logger("data_to_send: <" + data + ">");
        return data;
    }

    function print_message(message, error) {
        debug_logger("print_message: " + message);
        $("#message-box").fadeOut().empty().append(message).fadeIn();
    }

    function jsonp_req(url, method, ok_handler, data) {
        console.log(data);

        if (!data) {
            data = {};
        }

        // set up the special 'header' the server side will use. This
        // instructs the server to use the given method rather then the
        // GET which all JSONP calls are normally.
        //
        data["__headers__"] = {
            "X-HTTP-Method-Override": method
        };

        console.log(data);

        var jqxhr = $.ajax({
                url: url,
                crossDomain: true,
                dataType: "jsonp",
                timeout: JSONP_TIMEOUT,
                data: data
            })
            .done(ok_handler)
            .fail(function (data, textStatus, jqXHR) {
                if (jqXHR === "timeout") {
                    print_message("Connection to '" + url + "' timed out!");

                } else {
                    print_message("Error: " + textStatus);
                }
            });
    }

    function ok(response, textStatus, XMLHttpRequest) {
        debug_logger(textStatus + " response: " + JSON.stringify(response));
        print_message(textStatus + " response: " + JSON.stringify(response));
    }

    function ping() {
        print_message("Testing connection to server.");
        jsonp_req(server_uri(PING_URI), "GET", ok);
    }

    function init() {
        $("#ping-server").click(ping);
        $("#jsonp-get").click(function () {
            jsonp_req(server_uri(), "GET", ok, data_to_send());
        });
        $("#jsonp-post").click(function () {
            jsonp_req(server_uri(), "POST", ok, data_to_send());
        });
        $("#jsonp-put").click(function () {
            jsonp_req(server_uri(), "PUT", ok, data_to_send());
        });
        $("#jsonp-delete").click(function () {
            jsonp_req(server_uri(), "DELETE", ok, data_to_send());
        });
        $("#base_uri").change(function () { ping(); });
    }

    $.extend({
        jsonpcrud: {
            print_message: print_message,
            debug_logger: debug_logger,
            ping: ping,
            init: init
        }
    });

})(jQuery);
