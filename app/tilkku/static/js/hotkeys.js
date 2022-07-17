$(document).ready(function() {
    $("body").on("keydown", function(e) {
        if($("input").is(":focus") || $("textarea").is(":focus")) {
            return;
        }

        console.log(e.keyCode);

        if(e.keyCode == 65) {
            e.preventDefault();
            new_topic_modal_open();
        }

        if(e.keyCode == 80) {
            e.preventDefault();
            toolbox_tool('sites');
            $("#sites-site-search").focus();
        }

        if(e.keyCode == 80) {
            e.preventDefault();
            toolbox_tool('contacts');
            $("#sites-contacts-search").focus();
        }
    });
});