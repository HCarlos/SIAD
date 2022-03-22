jQuery(function($) {
    $(document).ready(function() {

        $.ajaxSetup({
            headers: {
                'X-CSRF-Token': $("meta[name='csrf-token']").attr("content")
            }
        });

        var Objs = ["#search_autocomplete","#search_autocomplete_user",".search_autocomplete_user","#search_autocomplete_calle","#search_autocomplete_colonia","#search_autocomplete_cp","#search_autocomplete_comunidad"];
        var Urls = ["/searchAdress","/searchUser","/searchUser","/buscarCalle","/buscarColonia","/buscarCodigopostal","/buscarComunidad"];
        var Gets = ["/getUbi/","/getUser/","/getUser/","/getCalle/","/getColonia/","/getCodigopostal/","/getComunidad/"];
        var Ids =  ["id","id","id","id","id","id","id"];

        // alert(Ids.length);

        for (i=0;i<Objs.length;i++)
            if ( $(Objs[i]) ) callAjax($(Objs[i]), Urls[i], Gets[i], i, Ids[i]);

        function callAjax(Obj, Url, Get, Item, ID, Elem) {
            $(Obj).autocomplete({
                source: function(request, response) {
                    // var ta = $("#tipo_asentamiento") ? $("#tipo_asentamiento").val() : "";

                    $.ajax({
                        url: Url,
                        dataType: "json",
                        data: {
                            search  : request.term,
                        },
                        success: function(data) {
                            response(data);
                        },
                    });

                },
                minLength: 3,
            });

            $( Obj ).on( "autocompleteselect", function( event, ui ) {
                var ox = ID.split('/');
                var Id;
                if ( ox.length ==1 ) Id = ui.item[ID];
                if ( ox.length == 2 ) Id = ui.item[ox[0]]+"/"+ui.item[ox[1]];
                $.get( Get+Id, function( data ) {
                    asignObjects(Obj,Item, data);
                }, "json" );
            });

            $( Obj ).on( "keyup", function( event ) {
                clearObjects(Item);
            });

        }


        function asignObjects(Obj, Item, data) {
            // alert(Item);
            //
            var d = data.data;
            switch (Item) {
                case 0:
                    $("#ubicacion_id").val(d.id);
                    $("#ubicacion_id_span").html(d.id);
                    $("#ubicacion").val(d.calle+' '+d.colonia+' '+d.comunidad+' '+d.ciudad+' '+d.municipio+' '+d.estado+' '+d.cp);
                    $("#ubicacion_nueva_id").val(d.id);
                    break;
                case 1:
                    if ( $("#usuario") )            $("#usuario").val('('+d.id+') '+d.nombre_completo);
                    if ( $("#usuario_domicilio") )  $("#usuario_domicilio").val(d.domicilio);
                    if ( $("#usuario_telefonos") )  $("#usuario_telefonos").val(d.telefonos);
                    if ( $("#usuario_id") )         $("#usuario_id").val(d.id);
                    if ( $("#ubicacion_id") )       $("#ubicacion_id").val(d.ubicacion_id);
                    if ( $("#ubicacion_id_span") )  $("#ubicacion_id_span").html(d.ubicacion_id);
                    if ( $("#ubicacion") )          $("#ubicacion").val(d.domicilio);
                    if ( $("#ubicacion_nueva_id") ) $("#ubicacion_nueva_id").val(d.ubicacion_id);
                    break;
                case 2:
                    if ( $("#lstAsigns") ) $("#lstAsigns").empty();
                    $("#listTarget").val(d.id);
                    getRolesFromUser(Obj, Item, data);
                    break;
                case 3:
                    $("#calle_id").val(d.id);
                    $("#search_autocomplete_calle").val(d.calle);
                    break;
                case 4:
                    $("#colonia_id").val(d.id);
                    $("#search_autocomplete_colonia").val(d.colonia);
                    break;
                case 5:
                    $("#codigopostal_id").val(d.id);
                    $("#search_autocomplete_cp").val(d.cp);
                    break;
                case 6:
                    $("#comunidad_id").val(d.id);
                    $("#search_autocomplete_comunidad").val(d.comunidad);
                    break;
            }
        }

        function clearObjects(Item) {
            switch (Item) {
                case 0:
                    $("#ubicacion_id").val(0);
                    $("#ubicacion_id_span").val("");
                    $("#ubicacion").val("");
                    $("#ubicacion_nueva_id").val(0);
                    break;
                case 1:
                    $("#usuario").val("");
                    $("#usuario_domicilio").val("");
                    $("#usuario_telefonos").val("");
                    $("#usuario_id").val(0);
                    break;
                case 2:
                    if ( $("#lstAsigns") ) $("#lstAsigns").empty();
                    $("#listTarget").val(0);
                    break;
                case 3:
                    $("#calle_id").val(0);
                    break;
                case 4:
                    $("#colonia_id").val(0);
                    break;
                case 5:
                    $("#codigopostal_id").val(0);
                    break;
                case 6:
                    $("#comunidad_id").val(0);
                    break;

            }
        }

        // function clearObjAll(){
        //     if ( $("#ubicacion_id") )               $("#ubicacion_id").val(0);
        //     if ( $("#ubicacion_id_span") )          $("#ubicacion_id_span").val("");
        //     if ( $("#ubicacion_nueva_id") )         $("#ubicacion_nueva_id").val(0);
        //     if ( $("#ubicacion") )                  $("#ubicacion").val("");
        //     if ( $("#usuario_domicilio") )          $("#usuario_domicilio").val("");
        //     if ( $("#usuario_telefonos") )          $("#usuario_telefonos").val("");
        //     if ( $("#usuario_id") )                 $("#usuario_id").val(0);
        //     if ( $("#usuario_id") )                 $("#lstAsigns").empty();
        //     if ( $("#listTarget") )                 $("#listTarget").val(0);
        //     if ( $("#calle_id") )                   $("#calle_id").val(0);
        //     if ( $("#colonia_id") )                 $("#colonia_id").val(0);
        //     //if ( $("#search_autocomplete_calle") )  $("#search_autocomplete_calle").val("");
        // }

        function getRolesFromUser(Obj, Item, data){
            var d = data.data;
            $.get(  $("#getItems").val()+d.id, function( dato ) {
                var count = $.map(dato.data, function(n, i) { return i; }).length;
                $("#totalRolesUsuarios").html( count );
                $.each(dato.data, function( index, value ) {
                    $("#lstAsigns").append("<option value='"+index+"'>"+value+"</option>");
                });
            }, "json" );
        }

            $("#user_address_list").on('change',function(event){
                 $("#ubicacion_nueva_id").val( $(this).val() );
            });


    });
});
