var tblProducts;
var vents = {
    items: {
        cli: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: [],
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        var iva = $('input[name="iva"]').val();
        $.each(this.items.products, function (pos, dict) {
            dict.subtotal = dict.cant * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * (iva / 100);
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "cat.name"},
                {"data": "pvp"},
                {"data": "cant"},
                {"data": "subtotal"},
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
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        console.log(data)
                        console.log(row)
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            // esta propiedad permite que a medida que se vaya creando un nuevo registro puedo ir modificando ciertos valores de la tabla
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000,
                    step: 1,
                });
            },
            initComplete: function (settings, json) {

            }
        });
    },
};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.name + '<br>' +
        '<b>Categoría:</b> ' + repo.cat.name + '<br>' +
        '<b>Precio:</b> <span class="badge badge-warning">$' + repo.pvp + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'

    });

    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });

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
            vents.list();
        }, function () {

        });
    });

    // event cant
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            // obtengo la posicion del elemento
            var tr = tblProducts.cell($(this).closest('td, li ')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar este producto del detalle?', function () {
                // elimino el elemento del array con el metodo splice
                vents.items.products.splice(tr.row, 1);
                vents.list();
            }, function () {

            });
        })
        .on('change', 'input[name="cant"]', function () {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li ')).index();
            vents.items.products[tr.row].cant = cant;
            vents.calculate_invoice();
            // despues de calcular la factura
            //esta propiedad de datatable actualiza el componente subtotal del producto luego de modificar la cantidad
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
        });

    // boton borrar busqueda de producto en la factura
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();

        if (vents.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        // asigna las variables date_joined y cli que no tenian valor en el diccionario vents
        vents.items.date_joined = $('input[name="date_joined"]').val();
        vents.items.cli = $('select[name="cli"]').val();

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        // Json.stringify convierte el diccionario a string para poder leerlo e iterarlo
        parameters.append('vents', JSON.stringify(vents.items));

        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de actualizar el siguiente elemento?', parameters, function (response) {
            alert_action('Notificación:', '¿Desea imprimir la boleta de venta?', function () {
                window.open('/erp/sale/invoice/pdf/'+response.id+'/', '_blank')
                location.href = '/erp/sale/list/';
            }, function () {
                location.href = '/erp/sale/list/';
            });
        });
    });

    vents.list();

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
                    action: 'search_products'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        data.cant = 1;
        data.subtotal = 0.00;
        // al ser un array se utiliza la propiedad push para poner el producto
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });
});

