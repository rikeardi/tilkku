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

        if(e.keyCode == 89) {
            e.preventDefault();
            toolbox_tool('contacts');
            $("#contacts-search").focus();
        }

        if(e.keyCode == 67) {
            e.preventDefault();
            toolbox_tool('chat');
            $("#chat-input").focus();
        }
    });
});