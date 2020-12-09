$(document).ready(function() {
    // Toggle between caret-down and caret-up icons for navbar-expand icon
    navbarExpandBtn = $("#down-up-navbar-btn")
    navbarExpandIcon = $("#down-up-navbar-icon")

    navbarExpandBtn.click(function() {

        if (navbarExpandIcon.hasClass('fa-caret-up'))
            navbarExpandIcon.addClass('fa-caret-down').removeClass('fa-caret-up')

        else if (navbarExpandIcon.hasClass('fa-caret-down'))
            navbarExpandIcon.addClass('fa-caret-up').removeClass('fa-caret-down')
    })
});