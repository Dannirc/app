var tblZone;

// funcion de peticion ajax para listar los clientes en el datatable
$(function () {
    tblZone = $('#data').DataTable({
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
        pageLength: 50,
        columns: [
            {"data": "name"},
            {"data": "tecnic.name"},
            {"data": "desc"},
            {"data": "opc"},
        ],
        // personaliza las columnas
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="detailszone"  class="btn btn-success btn-xs"><i class="fas fa-search"></i></a> ';
                    buttons += '<a href="/erp/zone/route/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs"><i class="fas fa-file-pdf"></i></a> '
                    buttons += '<a href="/erp/zone/orderzone/' + row.id + '/" class="btn btn-secondary btn-xs"><i class="fas fa-list-ol"></i></a> '
                    buttons += '<a href="/erp/zone/update/' + row.id + '/" class="btn btn-warning btn-xs"><i class="fas fa-edit"></i></a> '
                    buttons += '<a href="/erp/zone/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a> '
                    return buttons;
                }
            },
        ],
        order: [[ 1, "asc" ], [ 2, "asc" ]],

        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="detailszone"]', function () {
            // obtengo la posicion del elemento y guardo los datos del objeto seleccionado
            var tr = tblZone.cell($(this).closest('td, li ')).index();
            var data = tblZone.row(tr.row).data();


            $('#tblZone').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                // defRender se utiliza cuando trabajamos con mas de 50mil registros para agilizar la carga
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'view_zone_list',
                        'id': data.id
                    }, // parametros
                    // dataSrc se utiliza cuando en una peticion envio los datos dentro de una variable, por lo tanto se definir esa variable
                    // en este caso no lo envio en formato de variable
                    dataSrc: ""
                },
                columns: [
                    {"data": "position"},
                    {"data": "name"},
                    {"data": "address"},
                    {"data": "abono"},
                    {"data": "cant_odo"},
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
                    {
                        targets: [-2],
                        class: 'text-left',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });
            console.log(data);

            $('#myModelZone').modal('show');
        })
});