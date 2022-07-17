$(document).ready(function() {
    $("body").on("keypress", function(e) {
        if($("input").is(":focus") || $("textarea").is(":focus")) {
            return;
        }

        console.log(e.keyCode);

        if(e.keyCode == 97) {
            e.preventDefault();
            toolbox_tool('events');
        }

        if(e.ctrlKey && e.keyCode == 97) {
            e.preventDefault();
            toolbox_tool('events');
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

        if(e.ctrlKey && e.keyCode == 65) {
            e.preventDefault();
            toolbox_tool('contacts');
            new_contact_modal_open();
        }

        if(e.keyCode == 67) {
            e.preventDefault();
            toolbox_tool('chat');
            $("#chat-input").focus();
        }
    });
});