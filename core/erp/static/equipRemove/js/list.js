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
            {"data": "opc"},
        ],
        // personaliza las columnas
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/equipRemove/pdf/' + row.id + '/" target="_blank" class="btn btn-warning btn-xs"><i class="fas fa-file-pdf"></i></a> '
                    buttons += '<a rel="remove" class="btn btn-danger btn-xs"><i class="fas fa-trash"></i></a> '
                    return buttons;
                }
            },
        ],
        order: [[0, "desc"]],
        initComplete: function (settings, json) {
        }
    });
}

function changeSelectOption(select, cant) {
    for (let i = 1; i <= cant; i++) {
        if (i === cant) {
            select.innerHTML += '<option value=' + i + ' selected>' + i + '</option>'
        } else {
            select.innerHTML += '<option value=' + i + '>' + i + '</option>'
        }
    }
}

// funcion de peticion ajax para listar los clientes en el datatable
$(function () {

    datatableLoad();

    $('#data tbody').on('click', 'a[rel="remove"]', function () {
        let dataTable = $('#data').DataTable()
        let tr = dataTable.cell($(this).closest('td, li ')).index()
        var remove = dataTable.row(tr.row).data()
        let client = document.getElementById('serviceDownClient')
        client.innerHTML = remove.cli.name
        document.getElementById('serviceDownClientId').value = remove.cli.id

        selectOdo = document.getElementById('selectCantOdo')
        selectOdo.innerHTML = '<option value=0>0</option>'
        selectAer = document.getElementById('selectCantAer')
        selectAer.innerHTML = '<option value=0>0</option>'
        selectGot = document.getElementById('selectCantGot')
        selectGot.innerHTML = '<option value=0>0</option>'
        changeSelectOption(selectOdo, remove.cantOdo)
        changeSelectOption(selectAer, remove.cantAer)
        changeSelectOption(selectGot, remove.cantGot)

        $('#removeModal').modal('show')
    })

    $('#serviceDownConfirm').click(function () {
        let cli_id = document.getElementById('serviceDownClientId').value
        let cant_odo = document.getElementById('selectCantOdo').value
        let cant_aer = document.getElementById('selectCantAer').value
        let cant_got = document.getElementById('selectCantGot').value
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'service_down',
                'id': cli_id,
                'cant_odo': cant_odo,
                'cant_aer': cant_aer,
                'cant_got': cant_got,
            },
            dataType: 'json',
        }).done(function (data) {
            alert('Formulario enviado')
            $('#serviceDown').modal('hide');
            location.reload();
        }).fail(function (jqXHR, textStatus, errorThrown) {
            //alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
        });
    })

});

