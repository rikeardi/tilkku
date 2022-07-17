$(document).ready(function() {
    $("body").on("keydown", function(e) {
        if($("input").is(":focus") || $("textarea").is(":focus")) {
            return;
        }

        if(e.keyCode == 65) {
            new_topic_modal_open();
        }
    });
});