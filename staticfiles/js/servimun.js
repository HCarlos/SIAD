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
            // alert(response.titular)
                $("#id_remitente").val(response.titular);
                // $("#id_dir_remitente").trigger("change");
        });
    }
           //
           // $("#datepicker1").datepicker();
           //
           //
           //  alert('hola');
           //



if ( $(".removeItem").length > 0  ) {

    $(".removeItem").on('click', function (event) {
        event.preventDefault();
        var Url = event.currentTarget.id
        var arr = Url.split('/');
        var respuesta = confirm('Desea eliminar este registro: '+arr[2]);
        if (!respuesta) return false;

            $(function() {
                $.ajax({
                    url: Url,
                    data: null,
                    method: 'POST',
                    contentType: 'application/json',
                    dataType: 'json'
                }).done(function( response ) {
                    if (response["status"] == "OK"){
                        alert(response["message"]);
                        location.reload();
                    }
                }).fail(function(response) {
                    alert("Falló: " + response["message"] );
                });

            });

    });

}






});
