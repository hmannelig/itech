'use strict';

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
