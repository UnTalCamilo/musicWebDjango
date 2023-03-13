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

// toogle left navbar
$("#menu-toggle").click(function () {
    $("#sidebar").toggleClass('show');
});

// like button
function likedSong(elem, token, url) {
    const id = elem.dataset.id;
    const name = elem.dataset.name;
    const artist = elem.dataset.artist;
    const uri = elem.dataset.uri;
    const image = elem.dataset.image;
    const song = elem.dataset.song;

    $.ajax({
        url: url,
        type: 'POST',
        data: {
            'id': id,
            'name': name,
            'artist': artist,
            'uri': uri,
            'image': image,
            'song': song,
            'csrfmiddlewaretoken': token
        },
        beforeSend: function () {
            $(elem).html('<i id="temp" class="fas fa-spinner fa-spin"></i>');

        },
        success: function (data) {
            $("#temp").remove();
            $(`#${id}`).toggleClass('active');
        },
        error: function (data) {
            console.log(data);
        }
    });

}

