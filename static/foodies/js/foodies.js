'use strict';

function sendLoginDetails(e) {
    var userName = $('#login_form [name=username]').val();
    var password = $('#login_form [name=password]').val();
    if(userName == '' || userName == null || password == '' || password  == null) {
        alert('Write your user name and password');
        return false;
    }

    e.target.submit();
}

$('#login_form').submit(function(e) {
    // e.preventDefault();
    // sendLoginDetails(e);
});
