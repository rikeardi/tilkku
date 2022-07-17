$(document).ready(function() {
    $("body").on("keydown", function(e) {
        if($("input").hasFocus() || $("textarea").hasFocus()) {
            return;
        }
        console.log(e.keyCode);
    });
});