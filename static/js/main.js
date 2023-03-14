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



// liked song click

function clickLike(elem, token, url_like, url_dislike) {
    if ($(elem).hasClass('active')) {
        dislikedSong(elem, token, url_dislike, true);
    } else {
        likedSong(elem, token, url_like);
    }
};

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

function dislikedSong(elem, token, url, flag) {
    const id = elem.dataset.id;

    $.ajax({
        url: url,
        type: 'POST',
        data: {
            'id': id,
            'csrfmiddlewaretoken': token
        },
        beforeSend: function () {
            $(elem).html('<i id="temp" class="fas fa-spinner fa-spin"></i>');
        },
        success: function (data) {
            $("#temp").remove();
            if (flag == true) {
                $(`#${id}`).toggleClass('active')
            } else {
                $(`#${id}`).removeClass('active');
            }
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function playSong(id, url, token, opt) {
    console.log(id)
    $("#spotify-player").attr('src', `https://open.spotify.com/embed/track/${id}?autoplay=1`);

    if (opt == 1){
        console.log('liked')
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'id': id,
                'csrfmiddlewaretoken': token
            },
            success: function (data) {
                console.log(data);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }
    

}