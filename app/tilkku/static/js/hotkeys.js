$(document).ready(function() {
    $("body").on("keypress", function(e) {
        if(settings.hotkeys == 0) return;
        if($("input").is(":focus") || $("textarea").is(":focus")) {
            return;
        }

        console.log(e.keyCode);

        if(e.keyCode == 101) { // e
            e.preventDefault();
            toolbox_tool('events');
            new_topic_modal_open();
        }

        if(e.keyCode == 108) { // l
            e.preventDefault();
            toolbox_tool('sites');
            $("#sites-site-search").focus();
        }

        if(e.keyCode == 112) { // p
            e.preventDefault();
            toolbox_tool('contacts');
            $("#contacts-search").focus();
        }

        if(e.keyCode == 25) { // ctrl+y
            e.preventDefault();
            toolbox_tool('contacts');
            new_contact_modal_open();
        }

        if(e.keyCode == 99) { // c
            e.preventDefault();
            toolbox_tool('chat');
            $("#chat-input").focus();
        }

        if(e.keyCode == 109) { // m
            e.preventDefault();
            toolbox_menu();
        }

        if(e.keyCode == 115) { // s
            e.preventDefault();
            settings_open();
        }
    });
});