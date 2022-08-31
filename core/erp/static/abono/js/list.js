// funcion de peticion ajax para listar los clientes en el datatable
let tblAbono;

$(function () {
    tblAbono = $('#data').DataTable({
        responsive: true,
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
            {"data": "name"},
            {"data": "price"},
            {"data": "type"},
            {"data": "description"},
            {"data": "date_updated"},
            {"data": "opc"},
        ],
        // personaliza las columnas
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="detailsAbonoCLientList"  class="btn btn-success btn-xs"><i class="fas fa-search"></i></a> ';
                    buttons += '<a href="/erp/abono/update/' + row.id + '/" class="btn btn-warning btn-xs"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/abono/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a>'
                    return buttons;
                }
            },

            {
                targets: [-5],
                class: 'text-left',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
        ],
        order: [[2, "desc"], [1, "desc"]],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="detailsAbonoCLientList"]', function () {
            // obtengo la posicion del elemento y guardo los datos del objeto seleccionado
            var tr = tblAbono.cell($(this).closest('td, li ')).index();
            var data = tblAbono.row(tr.row).data();


            $('#tblAbonoClientList').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                // defRender se utiliza cuando trabajamos con mas de 50mil registros para agilizar la carga
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'view_abono_client_list',
                        'id': data.id
                    }, // parametros
                    // dataSrc se utiliza cuando en una peticion envio los datos dentro de una variable, por lo tanto se definir esa variable
                    // en este caso no lo envio en formato de variable
                    dataSrc: ""
                },
                columns: [
                    {"data": "cli.id"},
                    {"data": "cli.name"},
                    {
                        "data": "equipos",
                        "defaultContent": "N/A"
                    },
                ],
                // personaliza las columnas
                columnDefs: [
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                order: [[1, "asc"]],
                initComplete: function (settings, json) {
                }
            });
            $('#myModelAbonoClientList').modal('show');
        })
});