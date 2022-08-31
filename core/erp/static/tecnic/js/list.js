// funcion de peticion ajax para listar los clientes en el datatable
$(function () {
    $('#data').DataTable({
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
            {"data": "id"},
            {"data": "name"},
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
                    var buttons = '<a href="/erp/tecnic/update/' + row.id + '/" class="btn btn-warning btn-xs"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/tecnic/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a>'
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});