$(document).ready(function() {
    $("body").on("keypress", function(e) {
        if($("input").is(":focus") || $("textarea").is(":focus")) {
            return;
        }

        console.log(e.keyCode);

        if(e.keyCode == 97) {
            e.preventDefault();
            toolbox_tool('events');
            new_topic_modal_open();
        }

        if(e.keyCode == 112) {
            e.preventDefault();
            toolbox_tool('sites');
            $("#sites-site-search").focus();
        }

        if(e.keyCode == 121) {
            e.preventDefault();
            toolbox_tool('contacts');
            $("#contacts-search").focus();
        }

        if(e.keyCode == 25) {
            e.preventDefault();
            toolbox_tool('contacts');
            new_contact_modal_open();
        }

        if(e.keyCode == 99) {
            e.preventDefault();
            toolbox_tool('chat');
            $("#chat-input").focus();
        }

        if(e.keyCode == 109) {
            e.preventDefault();
            toolbox_menu();
        }

        if(e.keyCode == 113) {
            e.preventDefault();
            settings_open();
        }
    });
});