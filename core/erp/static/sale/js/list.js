var tblSale;

function format(d) {
    console.log(d);
    var html = '<table class="table">';
    html += '<thead class="thead-light">';
    html += '<tr><th scope="col">Producto</th>';
    html += '<th scope="col">Categoria</th>';
    html += '<th scope="col">PVP</th>';
    html += '<th scope="col">Cantidad</th>';
    html += '<th scope="col">Subtotal</th></tr>';
    html += '</thead>';
    html += '<tbody>';
    $.each(d.det, function (key, value) {
        html += '<tr>'
        html += '<td>' + value.prod.name + '</td>'
        html += '<td>' + value.prod.cat.name + '</td>'
        html += '<td>' + value.price + '</td>'
        html += '<td>' + value.cant + '</td>'
        html += '<td>' + value.subtotal + '</td>'
        html += '</tr>';
    });
    html += '</tbody>';
    return html;

}

// funcion de peticion ajax para listar los clientes en el datatable
$(function () {
    // asigna los datos de la tabla a una variable
    tblSale = $('#data').DataTable({
        // se desactiva responsive porque al trabajar con child row no funciona correctamente el responsive
        // y utilizamos el metodo scrollX para mover el datatable y visualizar los datos
        // responsive: true,
        scrollX: true,
        autoWidth: false,
        destroy: true,
        // defRender se utiliza cuando trabajamos con mas de 50mil registros para agilizar la carga
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            }, // parametros
            // dataSrc se utiliza cuando en una peticion envio los datos dentro de una variable, por lo tanto se definir esa variable
            // en este caso no lo envio en formato de variable
            dataSrc: ""
        },
        columns: [
            {
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            },
            {"data": "id"},
            {"data": "cli.name"},
            {"data": "date_joined"},
            {"data": "subtotal"},
            {"data": "iva"},
            {"data": "total"},
            {"data": "payed"},
            {"data": "opc"},
        ],
        // personaliza las columnas
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="details"  class="btn btn-success btn-xs"><i class="fas fa-search"></i></a> ';
                    buttons += '<a href="/erp/sale/invoice/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs"><i class="fas fa-file-pdf"></i></a> '
                    buttons += '<a href="/erp/sale/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a> '
                    return buttons;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var iconCheck = '<i class="fas fa-check text-success"></i>';
                    var iconNotCheck = '<i class="fas fa-ban text-danger"></i></i> ';
                    if (data) {
                        return iconCheck;
                    } else {
                        return iconNotCheck;
                    }
                }
            },
            {
                targets: [-3, -4, -5],
                class: 'text-left',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-9],
                class: 'text-left',
                orderable: false,
                render: function (data, type, row) {
                    return data;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            // obtengo la posicion del elemento y guardo los datos del objeto seleccionado
            var tr = tblSale.cell($(this).closest('td, li ')).index();
            var data = tblSale.row(tr.row).data();

            $('#tblDet').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                // defRender se utiliza cuando trabajamos con mas de 50mil registros para agilizar la carga
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details_prod',
                        'id': data.id
                    }, // parametros
                    // dataSrc se utiliza cuando en una peticion envio los datos dentro de una variable, por lo tanto se definir esa variable
                    // en este caso no lo envio en formato de variable
                    dataSrc: ""
                },
                columns: [
                    {"data": "prod.name"},
                    {"data": "prod.cat.name"},
                    {"data": "price"},
                    {"data": "cant"},
                    {"data": "subtotal"},
                ],
                // personaliza las columnas
                columnDefs: [
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            var iconCheck = '<i class="fas fa-check text-success"></i>';
                            var iconNotCheck = '<i class="fas fa-ban text-danger"></i></i> ';
                            console.log(data);
                            if (data) {
                                return iconCheck;
                            } else {
                                return iconNotCheck;
                            }
                        }
                    },
                    {
                        targets: [-1, -3],
                        class: 'text-left',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#myModelDet').modal('show');
        })
        .on('click', 'td.details-control', function () {
            // al estar desactivado el metodo responsive puede obtener los datos de esta manera
            var tr = $(this).closest('tr');
            var row = tblSale.row(tr);
            if (row.child.isShown()) {
                // This row is already open - close it
                row.child.hide();
                tr.removeClass('shown');
            } else {
                // Open this row
                row.child(format(row.data())).show();
                tr.addClass('shown');
            }
        });
});