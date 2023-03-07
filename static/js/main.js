// funciton to template nabvar

// Calling Register Form
$("#register_form").click(function () {
    $("#user_login").hide();
    $("#user_register").toggleClass('d-none');
    $(".modal-title").text('Register');
    return false;
});

// Going back to Social Forms
$(".back_btn").click(function () {
    $("#user_login").show();
    $("#user_register").toggleClass('d-none');
    $(".modal-title").text('Login');
    return false;
});