$(document).ready(function() {

    const token = window.localStorage.getItem('access_token');

    $.ajaxSetup({
        headers: {
            'X-CSRF-Token': $("meta[name='csrf-token']").attr("content")
        }
    });

    $("#id_dir_remitente").on("change", function (event) {
        event.preventDefault()
        getDependencias();
    });

    function getDependencias() {
        var Data = $('#FormData0').serializeArray();
        var request = $.ajax({
            type: "POST",
            url: "/getDependencias/",
            data: Data
        });
        request.done(function(response) {
                $("#id_remitente").value(response.titular);
                $("#id_dir_remitente").trigger("change");
        });
    }
});
