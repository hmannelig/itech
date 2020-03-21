'use strict';

function sendLoginDetails(e) {
    var formId = $(e.target).attr("id");
    var userName = $('#' + formId + ' [name=username]').val();
    var password = $('#' + formId + ' [name=password]').val();
    if(userName == '' || userName == null || password == '' || password  == null) {
        alert('Write your user name and password');
        return false;
    }

    e.target.submit();
}

function registerForm(e) {
    var formId = $(e.target).attr("id");
    var isCooker = $('#' + formId + ' [name=isCooker]').is(":checked");
    var isDiner = $('#' + formId + ' [name=isDinner]').is(":checked");
    if($('#foodies-error').length > 0) 
        $('#foodies-error').remove();

    if(isCooker == false && isDiner  == false) {
        $('<div id="foodies-error" class="alert alert-danger" role="alert">You must select one role!</div>').insertBefore($('#' + formId + ' [name=submit]'));
        return false;
    }
    console.log($(e.target));

    $(e.target).submit();
}

$('#user_form').submit(function(e) {
    // e.preventDefault();
    // registerForm(e);
});
$('#login_form').submit(function(e) {
    // e.preventDefault();
    // sendLoginDetails(e);
});
