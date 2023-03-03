
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
                url: '/project/profileform',
                data: $(form).serialize(),
                success: function (data, status) {
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

    $('#generate-default-profile').validate({
        submitHandler: function (form) {
            $.ajax({
                type: "POST",
                url: '/project/generate/default/profile',
                data: $(form).serialize(),
                success: function (data, status) {
                    defaultmodal.style.display = "None";
                    alert('Default Profile successfully generated');
                },
                error: function () {
                    $defaultmodal.style.display = "None";
                    alert('Default Profile generation Failed');
                }
            });
        }
    });
})