function getTecnics() {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'search_tecnic',
        },
        success: function (data) {
            document.getElementById('select_tecnic').innerHTML = '<option value="0">Todos</option>'
            data.forEach(function (elemento) {
                document.getElementById('select_tecnic').innerHTML += '<option value="' + elemento.id + '">' + elemento.name + '</option>'
            });
        },
        error: function () {
            console.log("No se ha podido obtener la información");
        }
    });
}

function getZone(tecnic_id) {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'search_zone',
            'id': tecnic_id,
        },
        success: function (data) {
            document.getElementById('select_zone').innerHTML = '<option value="0">Todas</option>'
            data.forEach(function (elemento) {
                document.getElementById('select_zone').innerHTML += '<option value="' + elemento.id + '">' + elemento.name + '</option>'
            });
        },
        error: function () {
            console.log("No se ha podido obtener la información");
        }
    });
}

let zone_id = 0;
let type_pay_id = 0;
let tecnic_id = 0;
let date_start = "Desde -";
let date_end = " Hasta";

$(function () {
    // obtengo los clientes al cargar la pagina
    getTecnics();

    // obtengo las zonas al seleccionar el tecnico
    $('#select_tecnic').on('change', function () {
        tecnic_id = document.getElementById('select_tecnic').value
        getZone(tecnic_id)
    });

    $('#select_zone').on('change', function () {
        zone_id = document.getElementById('select_zone').value;
        console.log(zone_id);
    })

    $('#select_pay').on('change', function () {
        type_pay_id = document.getElementById('select_pay').value;
        console.log(type_pay_id);
    })

    $('input[name="input_date"]').daterangepicker({
        // "autoApply": true,
        "startDate": "01/01/2022",
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
    });
    // inicio cuando no se selecciona ninguna fecha
    // date_start = moment().startOf('month').format('YYYY-MM-DD');
    date_start = "2022-01-01"
    date_end = moment().format('YYYY-MM-DD');

    $('.btnSaldo').on('click', function () {
        $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            // defRender se utiliza cuando trabajamos con mas de 50mil registros para agilizar la carga
            deferRender: true,
            order: [1, 'asc'],
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'consulta_saldo',
                    'tecnic_id': tecnic_id,
                    'zone_id': zone_id,
                    'type_pay_id': type_pay_id,
                    'date_start': date_start,
                    'date_end': date_end,
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
                    "data": "phone",
                    "defaultContent": "N/A"
                },
                {"data": "cant"},
                {"data": "should"},
            ],
            // personaliza las columnas
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-left',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            initComplete: function (settings, json) {
            }
        })
    });

    $('#button_print').on('click', function () {
        $.ajax({
            url: window.location.pathname + 'pdf/' + tecnic_id + '/' + zone_id + '/' + type_pay_id + '/' + date_start + '/' + date_end + '/',
            type: 'GET',
            data: {
                'action': 'consulta_saldo',
                'tecnic_id': tecnic_id,
                'zone_id': zone_id,
                'type_pay_id': type_pay_id,
                'date_start': date_start,
                'date_end': date_end,
            },
            success: function (data) {
                window.open( window.location.pathname + 'pdf/' + tecnic_id + '/' + zone_id + '/' + type_pay_id + '/' + date_start + '/' + date_end + '/','_blank') ;
            },
            error: function () {
                console.log("No se ha podido obtener la información");
            }
        });
    })

});
