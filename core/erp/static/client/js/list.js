function tbody(data) {
    var html = '';
    if (data.length === 0) {
        //     $('#myModelDet').modal('hide');
        //     Swal.fire({
        //         position: 'center',
        //         icon: 'info',
        //         title: 'No existen registros para este cliente',
        //         showConfirmButton: true,
        //         timer: 2000
        //     })
        // html += '<tr>';
        // html += '<td colspan="5" class="text-center"> No existen registros para este cliente</td>';
        // html += '</tr>';
    } else {
        for (let i = 0; i < data.length - 1; i++) {
            html += '<tr>';
            html += '<td>' + data[i].date_joined + '</td>';
            html += '<td>' + data[i].id + '</td>';
            html += '<td> $ ' + data[i].total + '</td>';
            html += '<td>' + data[i].status + '</td>';
            html += '</tr>';
        }

        html += '<tfoot>';
        html += '<tr>';
        html += '<th></th>';
        html += '<th>Saldo total:</th>';
        html += '<th>$ ' + data[data.length - 1] + '</th>';
        html += '<th></th>';
        html += '</tr>';
        html += '</tfoot>';
    }
    return html;
}

function datatableLoad() {
    let cliEnable = document.getElementById('id_clients-enable').value;
    console.log(cliEnable)
    let loading = Swal.fire({
        width: 400,
        background: '#ECECEC',
        html: 'Cargando datos...',// add html attribute if you want or remove
        allowOutsideClick: false,
        onBeforeOpen: () => {
            Swal.showLoading()
        },
    });
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
                'cliEnable': cliEnable,
            }, // parametros
            // dataSrc se utiliza cuando en una peticion envio los datos dentro de una variable, por lo tanto se definir esa variable
            // en este caso no lo envio en formato de variable
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "name"},
            {
                "data": "address",
                "defaultContent": "N/A"
            },
            {
                "data": "cuit",
                "defaultContent": "N/A"
            },
            {
                "data": "equipos",
                "defaultContent": "N/A"
            },
            {"data": "enable"},
            {"data": "opc"},
        ],
        // personaliza las columnas
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a type="button" rel="details" class="btn btn-success btn-xs" title="Consultar Saldo"><i class="fas fa-search-dollar"></i></a> ';
                    buttons += '<a rel="clientPending" class="btn btn-secondary btn-xs" title="Orden de Mantenimiento"><i class="fas fa-wrench"></i></a> ';
                    buttons += '<a href="/erp/client/update/' + row.id + '/" class="btn btn-warning btn-xs" title="Editar"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a rel="service_down" class="btn btn-danger btn-xs" title="Retirar / Suspender"><i class="fas fa-thumbs-down"></i></a> ';
                    buttons += '<a href="/erp/client/delete/' + row.id + '/" type="button" class="btn btn-dark btn-xs" title="Eliminar"><i class="fas fa-trash-alt"></i></a>'
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
            // {
            //     targets: [-4],
            //     class: 'text-right',
            //     render: function (data, type, row) {
            //         var buttons = '<a rel="details" class="btn btn-primary btn-xs"><i class="fas fa-search"></i></a> ';
            //         return '$' + parseFloat(data).toFixed(2) + ' ' + buttons;
            //     }
            // },
        ],
        order: [[1, "asc"]],
        initComplete: function (settings, json) {
        }
    });
    $(document).ajaxComplete(function () {
        loading.close();
    });
}

function serviceDownModal(data) {
    let selectOdo = document.getElementById('selectCantOdo')
    let selectAer = document.getElementById('selectCantAer')
    let selectGot = document.getElementById('selectCantGot')
    let client = document.getElementById('serviceDownClient')

    client.innerHTML = data['client'].name
    document.getElementById('serviceDownClientId').value = data['client'].id
    selectOdo.innerHTML = ''
    selectAer.innerHTML = ''
    selectGot.innerHTML = ''

    if (data['odorizadores'] > 0) {
        for (let i = 1; i < data['odorizadores'] + 1; i++) {
            selectOdo.innerHTML += '<option value=' + i + '>' + i + '</option>'
        }
    } else {
        selectOdo.innerHTML += '<option value=' + 0 + '>' + 0 + '</option>'
    }
    if (data['aerosoles'] > 0) {
        for (let i = 1; i < data['aerosoles'] + 1; i++) {
            selectAer.innerHTML += '<option value=' + i + '>' + i + '</option>'
        }
    } else {
        selectAer.innerHTML += '<option value=' + 0 + '>' + 0 + '</option>'
    }
    if (data['goteos'] > 0) {
        for (let i = 1; i < data['goteos'] + 1; i++) {
            selectGot.innerHTML += '<option value=' + i + '>' + i + '</option>'
        }
    } else {
        selectGot.innerHTML += '<option value=' + 0 + '>' + 0 + '</option>'
    }
}

// funcion de peticion ajax para listar los clientes en el datatable
$(function () {

    datatableLoad();

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            // obtengo la posicion del elemento en la tabla y guardo los datos del objeto seleccionado
            tblClientList = $('#data').DataTable();
            var tr = tblClientList.cell($(this).closest('td, li ')).index();
            var cli = tblClientList.row(tr.row).data();
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_details_modal',
                    'id': cli.id,
                },
                dataType: 'json',
            }).done(function (data) {
                html = tbody(data);
                console.log(data.length)
                if (data.length !== 0) {
                    document.getElementById('cliModalResumen').innerHTML = data[0].cli.name;
                    $('#myModelDet').modal('show');
                    document.getElementById('myModelDet_tbody').innerHTML = html;
                } else {
                    // $('#myModelDet').modal('hide');
                    Swal.fire({
                        position: 'center',
                        icon: 'info',
                        title: 'No existen registros para este cliente',
                        showConfirmButton: false,
                        timer: 1000,
                    })
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {
            });
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
        })
        .on('click', 'a[rel="service_down"]', function () {
            // obtengo la posicion del elemento en la tabla y guardo los datos del objeto seleccionado
            tblClientList = $('#data').DataTable();
            var tr = tblClientList.cell($(this).closest('td, li ')).index();
            var cli = tblClientList.row(tr.row).data();
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_cant_eq_modal',
                    'id': cli.id,
                },
                dataType: 'json',
            }).done(function (data) {
                serviceDownModal(data)
                $('#serviceDown').modal('show');
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {
            });
        })
        .on('click', 'a[rel="clientPending"]', function () {
            // obtengo la posicion del elemento en la tabla y guardo los datos del objeto seleccionado
            tblClientList = $('#data').DataTable();
            let tr = tblClientList.cell($(this).closest('td, li ')).index();
            let cli = tblClientList.row(tr.row).data();
            let date = $('#inputDate').val
            let obs = $('#textArea').val
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'client_pending',
                    'id': cli.id,
                },
                dataType: 'json',
            }).done(function (data) {
                // serviceDownModal(data)
                console.log(data)
                document.getElementById('clientPendingId').value = data['client'].id
                document.getElementById('clientPendingName').innerHTML = data['client'].name
                $('#clientPending').modal('show');
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {
            });
        })

    // envio del modal serviceDown
    $('#serviceDownConfirm').click(function () {
        let cli_id = document.getElementById('serviceDownClientId').value
        let type_down = document.getElementById('selectDown').value
        console.log(type_down)
        let cant_odo = document.getElementById('selectCantOdo').value
        let cant_aer = document.getElementById('selectCantAer').value
        let cant_got = document.getElementById('selectCantGot').value
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'service_down',
                'id': cli_id,
                'type_down': type_down,
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
    $('#clientPendingConfirm').click(function () {
        let cli_id = document.getElementById('clientPendingId').value
        let date = document.getElementById('inputDate').value
        let obs = document.getElementById('textArea').value
        console.log(cli_id, date, obs)
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'client_pending_confirm',
                'id': cli_id,
                'date': date,
                'obs': obs,
            },
            dataType: 'json',
        }).done(function (data) {
            alert('Formulario enviado')
            $('#clientPending').modal('hide');
            location.reload();
        }).fail(function (jqXHR, textStatus, errorThrown) {
            //alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
        });
    })

    // script para el switch de cliente habilitado
    var label = document.querySelector('#label2');

    $('#id_clients-enable').click(function () {
        if (this.checked) {
            this.value = true;
            label.textContent = 'Solo Clientes Habilitados';
        } else {
            this.value = false;
            label.textContent = 'Todos los Clientes';
        }
        datatableLoad();
        console.log(this.value);
    })

});

