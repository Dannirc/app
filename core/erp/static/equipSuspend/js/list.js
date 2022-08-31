function datatableLoad() {
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
                'action': 'searchdata',
            }, // parametros
            // dataSrc se utiliza cuando en una peticion envio los datos dentro de una variable, por lo tanto se definir esa variable
            // en este caso no lo envio en formato de variable
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "date"},
            {"data": "cli.name"},
            {"data": "cantOdo"},
            {"data": "cantAer"},
            {"data": "cantGot"},
            {
                "data": "date_end",
                "defaultContent": "N/A"
            },
            {"data": "opc"},
        ],
        // personaliza las columnas
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/equipRemove/print/' + row.id + '/" type="button" class="btn btn-success btn-xs"><i class="fas fa-thumbs-up"></i></a> ';
                    buttons += '<a href="/erp/equipRemove/delete/' + row.id + '/" class="btn btn-warning btn-xs"><i class="fas fa-clock"></i></a> '
                    buttons += '<a href="/erp/equipRemove/delete/' + row.id + '/" class="btn btn-danger btn-xs"><i class="fas fa-thumbs-down"></i></a> '
                    return buttons;
                }
            },
        ],
        order: [[0, "desc"]],
        initComplete: function (settings, json) {
        }
    });
}



// funcion de peticion ajax para listar los clientes en el datatable
$(function () {

    datatableLoad();

});

