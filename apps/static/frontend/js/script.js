function Register(url, form_id, result_div)
{
    $.ajax({
        url: url, // the endpoint
        type: "POST", // http method
        processData: false,
        contentType: false,
        data: new FormData(document.getElementById(form_id))
    })
            .done(function (html) {
                $("#" + result_div).empty();
                $("#" + result_div).append(html);
            })
            .fail(function () {
                $("#" + result_div).empty();
                $("#" + result_div).append("ERROR!");
            });
}
function Login(url, form_id, result_div)
{
    $.ajax({type: "POST", url: url, data: $("#" + form_id).serialize()})
            .done(function (html) {
                if (html === '') {
                    window.location.replace("http://localhost/nikos/project.php");
                } else {
                    $("#" + result_div).empty();
                    $("#" + result_div).append(html);
                }
            })
            .fail(function () {
                $("#" + result_div).empty();
                $("#" + result_div).append("ERROR!");
            });
}
function Contact(url, form_id, result_div)
{
    $.ajax({type: "POST", url: url, data: $("#" + form_id).serialize()})
            .done(function (html) {
                $("#" + result_div).empty();
                $("#" + result_div).append(html);
            })
            .fail(function () {
                $("#" + result_div).empty();
                $("#" + result_div).append("ERROR!");
            });
}
function UploadProject(url, form_id, result_div)
{ 
    $.ajax({
        url: url, // the endpoint
        type: "POST", // http method
        processData: false,
        contentType: false,
        data: new FormData(document.getElementById(form_id))
    })
            .done(function (html) {
                $("." + result_div).empty();
                $("." + result_div).append(html);
            })
            .fail(function () {
                $("." + result_div).empty();
                $("." + result_div).append("ERROR!");
            });
}
