var tblSale;
var html = {};
let date_start = "Desde -";
let date_end = " Hasta";


function format(d) {
    console.log(d);
    var html = '<table class="table">';
    html += '<thead class="thead-light">';
    html += '<tr><th scope="col"></th>';
    html += '<th scope="col">Producto</th>';
    html += '<th scope="col">Precio</th>';
    html += '<th scope="col">Cantidad</th>';
    html += '<th scope="col">Subtotal</th></tr>';
    html += '</thead>';
    html += '<tbody>';
    let a = [0, 1, 2];
    $.each(a, function (key, value) {
        html += '<tr>'
        html += '<td>' + "" + '</td>'
        html += '<td>' + "Odorizador" + '</td>'
        html += '<td>' + 500 + '</td>'
        html += '<td>' + 1 + '</td>'
        html += '<td>' + 500 + '</td>'
        html += '</tr>';
    });
    html += '</tbody>';
    return html;
}

function listaTblDet(data) {
    element_table = '<tr>';
    element_table += '<td> Odorizador </td>'
    element_table += '<td> $ ' + data[0].price_odo + '</td>';
    element_table += '<td>' + data[0].cant_odo + '</td>';
    element_table += '<td> $ ' + data[0].price_odo * data[0].cant_odo + '</td>';
    element_table += '</tr>';
    element_table += '<tr>';
    element_table += '<td> Aerosoles </td>';
    element_table += '<td> $ ' + data[0].price_aer + '</td>';
    element_table += '<td>' + data[0].cant_aer + '</td>';
    element_table += '<td> $ ' + data[0].price_aer * data[0].cant_aer + '</td>';
    element_table += '</tr>';
    element_table += '<tr>';
    element_table += '<td>Goteos </td>';
    element_table += '<td> $ ' + data[0].price_got + '</td>';
    element_table += '<td>' + data[0].cant_got + '</td>';
    element_table += '<td> $ ' + data[0].price_got * data[0].cant_got + '</td>';
    element_table += '</tr>';
    element_table += '<tr>';
    element_table += '<th class="text-center" colspan="3"> Total de la factura: </th>';
    element_table += '<th> $ ' + data[0].subtotal + '</th>';
    element_table += '</tr>';
    return element_table;
}

function loadingDataTable() {
    let loading = Swal.fire({
        width: 400,
        background: '#ECECEC',
        html: 'Cargando datos...',// add html attribute if you want or remove
        allowOutsideClick: false,
        onBeforeOpen: () => {
            Swal.showLoading()
        },
    });

    $(document).ajaxComplete(function () {
        loading.close();
    });
}

// funcion de peticion ajax para listar los clientes en el datatable
$(function () {

    $('input[name="input_date"]').daterangepicker({
        // "autoApply": true,
        "startDate": moment().startOf('month'),
        "endDate": moment(),
        "locale": {
            "format": "DD/MM/YYYY",
            "separator": " - ",
            "applyLabel": "Aplicar",
            "cancelLabel": "Cancelar",
            "fromLabel": "De",
            "toLabel": "A",
            "customRangeLabel": "Otro",
            "weekLabel": "W",
            "daysOfWeek": [
                "Do",
                "Lu",
                "Ma",
                "Mi",
                "Ju",
                "Vi",
                "Sa"
            ],
            "monthNames": [
                "Enero",
                "Febrero",
                "Marzo",
                "Abril",
                "Mayo",
                "Junio",
                "Juilo",
                "Agosto",
                "Septiembre",
                "Octubre",
                "Noviembre",
                "Diciembre"
            ],
            "firstDay": 1
        },
        ranges: {
            'Todo': ["01/01/2020", moment()],
            'Mes Actual': [moment().startOf('month'), moment().endOf('month')],
            'Mes Anterior': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
        },
        opens: 'right'
    }, function (start, end, label) {
        console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (Rango Predefinido: ' + label + ')');
        date_start = start.format('YYYY-MM-DD')
        date_end = end.format('YYYY-MM-DD')
        loadingDataTable()
        $('#data').DataTable().ajax.reload()
    });
    // inicio cuando no se selecciona ninguna fecha
    date_start = moment().startOf('month').format('YYYY-MM-DD');
    date_end = moment().format('YYYY-MM-DD');

    // asigna los datos de la tabla a una variable
    loadingDataTable()
    tblSale = $('#data').DataTable({
        // se desactiva responsive porque al trabajar con child row no funciona correctamente el responsive
        // y utilizamos el metodo scrollX para mover el datatable y visualizar los datos
        // responsive: true,
        scrollX: true,
        autoWidth: false,
        destroy: true,
        order: [1, 'desc'],
        // defRender se utiliza cuando trabajamos con mas de 50mil registros para agilizar la carga
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            // se utiliza una function para ejecutar ajax.reload()
            data: function (d){
                d.action= 'searchdata';
                d.date_start= date_start;
                d.date_end= date_end;
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
                    buttons += '<a href="/erp/invoice/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs"><i class="fas fa-file-pdf"></i></a> '
                    buttons += '<a href="/erp/invoice/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a> '
                    return buttons;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var iconCheck = '<i class="fas fa-check text-success"></i>';
                    var iconNotCheck = '<i class="far fa-clock text-gray"></i>';
                    console.log(data);
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
            var title = '<h5 className="modal-title" id="titletblDet"><i className="fas fa-shopping-cart"></i> Detalle de factura Nro: ' + data.id + '</h5>'
            // limpia los datos que muestra la tblDet
            $("#tblDet > tbody").html("");
            $("#titletblDet").html(title);


            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_details_service',
                    'id': data.id
                }, // parametros
                // dataSrc se utiliza cuando en una peticion envio los datos dentro de una variable, por lo tanto se definir esa variable
                // en este caso no lo envio en formato de variable
                dataSrc: ""
            }).done(function (data) {
                listaTblDet(data);
                $('#tblDet').append(listaTblDet(data));

                if (!data.hasOwnProperty('error')) {
                    // callback(data);
                    return false;
                }
                message_error(data.error);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {
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
