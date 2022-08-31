var select_sale = $('select[name="sale"]');

$(function () {

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('select[name="cli"]').on('change', function () {
        var id = $(this).val();
        var options = '<option value="">------------</option>';
        if (id === '') {
            select_sale.html(options);
            return false;
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_sale_id',
                'id': id
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                // NO funciona declarando la variable de esta manera
                // select_sale.html('').select2({
                //     theme: "bootstrap4",
                //     language: 'es',
                //     data: data
                // });
                $('select[name="sale"]').html('').select2({
                    theme: "bootstrap4",
                    language: 'es',
                    data: data
                })
                /*$.each(data, function (key, value) {
                    options += '<option value="' + value.id + '">' + value.name + '</option>';
                });*/
                return false;
            }
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
            //select_products.html(options);
        });
    });

    if ($('input[name="action"]').val() === 'edit') {
        var id = $('select[name="cli"]').val();
        var options = '<option value="">--------</option>';
        if (id === '') {
            select_sale.html(options);
            return false;
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_sale_id',
                'id': id
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                // NO funciona declarando la variable de esta manera
                // select_sale.html('').select2({
                //     theme: "bootstrap4",
                //     language: 'es',
                //     data: data
                // });
                $('select[name="sale"]').html('').select2({
                    theme: "bootstrap4",
                    language: 'es',
                    data: data
                })
                /*$.each(data, function (key, value) {
                    options += '<option value="' + value.id + '">' + value.name + '</option>';
                });*/
                return false;
            }
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
            //select_products.html(options);
        });
    }

$('select[name="sale"]')
    .html('<option value="1">------------</option>').select2({
    theme: "bootstrap4",
    language: 'es',
    placeholder: "Debe ingresar un cliente",
})
    .on('change', function () {
        // muestra el valor total de la factura seleccionada en el input mount
        var value = $('select[name="sale"]').select2('data')[0];
        $('input[name="mount"]').val(value.data.total);
        console.log(value);
    });

// falta que muestra el id de las ventas y el autocomplete

// $('input[name="search"]').autocomplete({
//     source: function (request, response) {
//         $.ajax({
//             url: window.location.pathname,
//             type: 'POST',
//             data: {
//                 'action': 'autocomplete',
//         // request.term devuelve lo que el usuario esta escribiendo
//         'term': request.term,
//     },
//         dataType: 'json',
//     }).
//         done(function (data) {
//             response(data);
//         }).fail(function (jqXHR, textStatus, errorThrown) {
//             //alert(textStatus + ': ' + errorThrown);
//         }).always(function (data) {
//
//         });
//     },
//     delay: 500,
//     minLength: 1,
//     select: function (event, ui) {
//         console.log(ui.item);
//     }
// });
//
// $('select[name="search"]').select2({
//     theme: "bootstrap4",
//     language: 'es',
//     allowClear: true,
//     ajax: {
//         delay: 250,
//         type: 'POST',
//         url: window.location.pathname,
//         data: function (params) {
//             var queryParameters = {
//                 term: params.term,
//                 action: 'autocomplete'
//             }
//             return queryParameters;
//         },
//         processResults: function (data) {
//             return {
//                 results: data
//             };
//         },
//     },
//     placeholder: 'Ingrese una descripción',
//     minimumInputLength: 1,
// });
});