$(document).ready(function() {
    $("#profile-icon").click(function(event) {
        console.log("error")
        event.preventDefault();
        $("#profile-dropdown").toggle();
    });

    $(document).click(function(event) {
        if (!$(event.target).closest("#profile-icon, #profile-dropdown").length) {
            $("#profile-dropdown").hide();
        }
    });
});
