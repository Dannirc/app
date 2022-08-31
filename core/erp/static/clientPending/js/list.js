let tecnic_id;

function dataTable(){
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
                    'id': tecnic_id,
                }, // parametros
                // dataSrc se utiliza cuando en una peticion envio los datos dentro de una variable, por lo tanto se definir esa variable
                // en este caso no lo envio en formato de variable
                dataSrc: ""
            },
            columns: [
                {"data": "date"},
                {"data": "cli.name"},
                {"data": "cli.tecnic.name"},
                {"data": "dateToMake"},
                {"data": "observation"},
                {"data": "opc"},
            ],
            // personaliza las columnas
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="/erp/clientPending/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a>'
                        return buttons;
                    }
                }
            ],
            initComplete: function (settings, json) {

            }
        });
}

function getTecnics() {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'search_tecnic',
        },
        success: function (data) {
            document.getElementById('select_tecnic').innerHTML += '<option value="0" selected>Todos</option>'
            data.forEach(function (elemento) {
                document.getElementById('select_tecnic').innerHTML += '<option value="' + elemento.id + '">' + elemento.name + '</option>'
            });
        },
        error: function () {
            console.log("No se ha podido obtener la información de tecnicos");
        }
    });
}

// funcion de peticion ajax para listar los clientes en el datatable
$(function () {
    getTecnics();
    tecnic_id = '0'
    dataTable();

    $('#select_tecnic').on('change', function () {
        tecnic_id = document.getElementById('select_tecnic').value
    });

    $('#searchClientPending').on('click', function () {
        dataTable();
    });

    $('#button_print').on('click', function () {
        $.ajax({
            url: window.location.pathname + 'pdf/' + tecnic_id + '/',
            type: 'GET',
            data: {
                'tecnic_id': tecnic_id,
            },
            success: function (data) {
                window.open( window.location.pathname + 'pdf/' + tecnic_id + '/','_blank') ;
            },
            error: function () {
                console.log("No se ha podido obtener la información");
            }
        });
    })
});