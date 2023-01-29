
$(document).ready(function () {

    $('#profile-form').validate({
        rules: {
            name: {
                required: true,
                minlength: 4
            }
        },
        messages: {
            name: {
                required: "Profile name must be there",
                minlength: "Profile name must consist of at least 4 characters"
            }
        },
        submitHandler: function (form) {
            $.ajax({
                type: "POST",
                url: '/profileform',
                data: $(form).serialize(),
                success: function (data, status) {
                    var message = data.message
                    modal.style.display = "None";
                    alert('Profile added successfully');
                },
                error: function () {
                    $modal.style.display = "None";
                    alert('Profile added Failed');
                }
            });
        }
    });
})