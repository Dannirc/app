var tblProducts;
var vents = {
    items: {
        tecnic: '',
        date_pay: '',
        zone: '',
        iva: 0.00,
        total: 0.00,
        efectivo: 0.00,
        cheque: 0.00,
        products: [],
    },
    calculate_invoice: function () {
        var cheque = 0;
        var efectivo = 0;
        var total = 0.00;
        $.each(this.items.products, function (pos, dict) {
            total += parseInt(dict.total);
        });
        this.items.total = total;

        $('input[name="total"]').val(this.items.total.toFixed(2));

        efectivo = this.items.total
        cheque = $('input[name="cheque"]').val();
        efectivo -= cheque;
        this.items.efectivo = efectivo
        this.items.cheque = cheque
        $('input[name="efectivo"]').val(efectivo.toFixed(2));
        document.getElementById("count_invoice").innerHTML = "<p class='text-bold' > Total de recibos: " + vents.items.products.length + "</p>";

    },
    add: function (item) {
        function esRepetido(prod) {
            return prod.id === item.id && prod.type === item.type;
        }

        if (this.items.products.find(esRepetido) === undefined) {
            this.items.products.push(item);
        } else {
            message_error('La factura ya esta agregada')
        }
        this.list();
    },
    list: function () {
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "cli.name"},
                {"data": "type"},
                {"data": "id"},
                {"data": "date_joined"},
                {"data": "total"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        //return '$ ' + parseFloat(data).toFixed(2);
                        return '<input type="text" name="subtotal" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.total + '">';
                    }
                },
            ],
            initComplete: function (settings, json) {
            }
        });
    },
};

// muestra detalle en el buscador
// function formatRepo(repo) {
//     if (repo.loading) {
//         return repo.text;
//     }
//
//     var option = $(
//         '<div class="wrapper container">' +
//         '<div class="row">' +
//         '<div class="col-lg-1">' +
//         '<img src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
//         '</div>' +
//         '<div class="col-lg-11 text-left shadow-sm">' +
//         //'<br>' +
//         '<p style="margin-bottom: 0;">' +
//         '<b>Nombre:</b> ' + repo.name + '<br>' +
//         '<b>Categoría:</b> ' + repo.cat.name + '<br>' +
//         '<b>Precio:</b> <span class="badge badge-warning">$' + repo.pvp + '</span>' +
//         '</p>' +
//         '</div>' +
//         '</div>' +
//         '</div>');
//
//     return option;
// }

// funcion para obtener zonas de un cliente
function searchZone() {
    let id = document.getElementById('id_tecnic').value
    let options = '';
    const zone = document.getElementById('id_zone')
    if (id === '') {
        options = '<option value="">(Seleccione Tecnico)</option>'
        zone.html(options);
        return false;
    }
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'search_zone_id',
            'id': id
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            $.each(data, function (key, value) {
                // el if selecciona la zona al editar una cobranza
                if (value.id === zone.value) {
                    options += '<option value="' + value.id + '">' + value.name + ' selected </option>';
                } else {
                    options += '<option value="' + value.id + '">' + value.name + '</option>';
                }
            });
            options += '<option value="">Cobranza / Pendientes </option>';
            document.getElementById('id_zone').innerHTML = options

            return false;
        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {
        //select_products.html(options);
    });
}


$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // $('#id_date_pay').datetimepicker({
    //     format: 'DD-MM-YYYY',
    //     date: moment().format("YYYY-MM-DD"),
    //     locale: 'es',
    //     //minDate: moment().format("YYYY-MM-DD")
    // });

    // document.getElementById('id_zone').innerHTML = '<option value="">---------</option>';

    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 21,
        step: 0.5,
        decimals: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        vents.calculate_invoice();
    });

    // search products
    // $('input[name="search"]').autocomplete({
    //     source: function (request, response) {
    //         $.ajax({
    //             url: window.location.pathname,
    //             type: 'POST',
    //             data: {
    //                 'action': 'search_products',
    //                 // request.term devuelve lo que el usuario esta escribiendo
    //                 'term': request.term,
    //             },
    //             dataType: 'json',
    //         }).done(function (data) {
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
    //         event.preventDefault;
    //         console.clear();
    //         ui.item.cant = 1;
    //         ui.item.subtotal = 0.00;
    //         // al ser un array se utiliza la propiedad push para poner el producto
    //         console.log(vents.items);
    //         vents.add(ui.item);
    //         $(this).val('');
    //     }
    // });

    //boton eliminar todos los item, llamado desde la clase css como btnRemoveAll
    $('.btnRemoveAll').on('click', function () {
        if (vents.items.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los productos?', function () {
            vents.items.products = [];
            vents.calculate_invoice();
            vents.list();
        }, function () {
        });
    });

    // carga los productos al editar una cobranza
    if (vents.items.products.length === 0 && window.location.pathname.includes('update')) {
        searchZone()
        $(function editPay() {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'init_edit',
                },
                dataType: 'json',
            }).done(function (data) {

                for (i of data) {
                    console.log(i)
                    vents.add(i);
                }
                vents.calculate_invoice();
                vents.list();
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        })
    } else {
        document.getElementById('id_zone').innerHTML = '<option value="">---------</option>';
    }

    // event cant
    $('#tblProducts tbody')
        // elimina un producto
        .on('click', 'a[rel="remove"]', function () {
            // obtengo la posicion del elemento
            var tr = tblProducts.cell($(this).closest('td, li ')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar este producto del detalle?', function () {
                // elimino el elemento del array con el metodo splice
                vents.items.products.splice(tr.row, 1);
                vents.calculate_invoice();
                vents.list();
            }, function () {

            });
        })
        .on('change', 'input[name="subtotal"]', function () {
            var total = ($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li ')).index();
            console.log(tr)
            vents.items.products[tr.row].total = total;
            console.log(vents.items)
            vents.calculate_invoice();
            console.log(vents.items)
        });

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();

        if (vents.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        // asigna las variables date_pay y cli que no tenian valor en el diccionario vents
        vents.items.date_pay = $('input[name="date_pay"]').val();
        vents.items.tecnic = $('select[name="tecnic"]').val();
        vents.items.zone = $('select[id="id_zone"]').val();

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        // Json.stringify convierte el diccionario a string para poder leerlo e iterarlo
        parameters.append('vents', JSON.stringify(vents.items));

        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de actualizar el siguiente elemento?', parameters, function (response) {
            alert_action('Notificación:', '¿Desea imprimir la cobranza realizada?', function () {
                window.open('/erp/pay/print/pdf/' + response.id + '/', '_blank')
                location.href = '/erp/pay/list/';
            }, function () {
                location.href = '/erp/pay/list/';
            });
        });
    });

    // inicializa select2 (buscar clientes)
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_client'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese ID o Nombre de cliente',
        minimumInputLength: 1,
        // templateResult: formatRepo,
    }).on('change', function () {
        $('#search_invoice').select2('open');
    });


    // inicializa select2 (buscar facturas cliente)
    $('select[name="search_invoice"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_invoice_client',
                    id: $('select[name="search"]').val()
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Seleccione factura',
        minimumInputLength: 0,
    })
        .on('select2:select', function (e) {
            var data = e.params.data;
            // al ser un array se utiliza la propiedad push para poner el producto
            vents.add(data);
            $(this).val('').trigger('change.select2');
            $('select[name="search"]').val('').trigger('change.select2');
            vents.calculate_invoice();
            $('#search').select2('open');
        })

    // focus en el select de buscar cliente
    $('#search').select2('open');

    // actualiza total en efectivo
    $('input[name="cheque"]').change(function () {
        vents.calculate_invoice();
    });

    $('select[name="tecnic"]').change(function () {
        searchZone();
    });

    // actualiza datatable
    vents.list();

});


