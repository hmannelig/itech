'use strict';

var site_url = window.location.origin;

var colors = [
    '#F44336',
    '#E91E63',
    '#9C27B0',
    '#673AB7',
    '#3F51B5',
    '#2196F3',
    '#03A9F4',
    '#00BCD4',
    '#009688',
    '#4CAF50',
    '#8BC34A',
    '#CDDC39',
    '#FFEB3B',
    '#FFC107',
    '#FF9800',
    '#FF5722',
    '#795548',
    '#9E9E9E',
    '#FFEB3B',
];

function setRandomColor() {
    for(var index = 0; index < 6; index++) {
        var chosen_colors = colors[Math.floor(Math.random() * colors.length)];
        var selector = $("#categories .random-color")[index];
        if(selector != undefined && $(selector).length > 0) {
            $(selector).find(".bg").css("background-color", chosen_colors);
        }
    }
}


setRandomColor();

$(".check-if-login").on("click", function(e) {
    e.preventDefault();
    var element = $(e.target);
    $.ajax({
        url: site_url + "/is_user_login/",
        statusCode: {
            500: function(data) {
                console.log(data);
                $("#info-modal-title").text("Foodies Error");
                $("#info-modal-message").text("An error occurred, open the JavaScript console to read it.");
                $('#infoModal').modal('show');
            },
            200: function(data) {
                if(!data.is_loggedin) {
                    $("#info-modal-title").text("Foodies Info");
                    $("#info-modal-message").text("Please login/sign up to request a meal.");
                    $('#infoModal').modal('show');
                } else {
                    window.location.href = element[0].href;
                }
            }
        }
    });
});

$(window).on('scroll', function(e) {
    if($(e.target).width() > 767) {
        var heroImgBottomPos = $('.hero-image').offset().top + $('.hero-image').height();
        var footerTopPos = $('footer').offset().top;
        var windowScroll = $(e.target).scrollTop();
        var windowHeight = $(window).height();

        if(windowScroll >= heroImgBottomPos) {

            var sidebarWidth = $(".sidebar").width();
            $(".sidebar > .row").addClass("position-fixed");
            $(".sidebar > .row").width(sidebarWidth + "px");
            $(".sidebar > .row").css({
                "top":"20px"
            });
        }
        if((windowScroll + windowHeight) >= footerTopPos) {
            $(".sidebar > .row").css({
                "top":"initial",
                "bottom": windowScroll + windowHeight - footerTopPos + 20 + "px"
            });
        }
        if (windowScroll < heroImgBottomPos) {
            $(".sidebar > .row").removeClass("position-fixed");
            $(".sidebar > .row").width("auto");
        }

    } else {
        $(".sidebar > .row").removeClass("position-fixed");
        $(".sidebar > .row").width("auto");
        $(".sidebar > .row").css({
            "top": "initial",
            "bottom": "initial"
        });
    }
});