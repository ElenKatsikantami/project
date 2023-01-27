
$(document).ready(function () {

    $('#profile-form').validate({
        rules: {
            name: {
                required: true,
                minlength: 2
            }
        },
        messages: {
            name: {
                required: "Name must be there",
                minlength: "your name must consist of at least 2 characters"
            }
        },
        submitHandler: function (form) {
            $.ajax({
                type: "POST",
                url: '/profileform',
                data: $(form).serialize(),
                success: function (data, status) {
                    $("#contact-form").trigger('reset');
                    bootbox.alert({
                        message: data.message,
                    });
                },
                error: function () {
                    bootbox.alert({
                        message: data.message,
                        size: 'small'
                    });
                    // $('#contact-form').fadeTo( "slow", 0.15, function() {
                    // 	$('#error').fadeIn();
                    // });
                }
            });
        }
    });
})