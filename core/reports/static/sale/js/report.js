var date_range = null;
var date_now = moment().format('YYYY-MM-DD');

function generate_report() {

    var parameters = {
        'action': 'search_report',
        'start_date': moment().startOf('month').format('YYYY-MM-DD'),
        'end_date': date_now,
    }

    if (date_range !== null) {
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD')
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD')
    }
    console.log(parameters)

    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        // defRender se utiliza cuando trabajamos con mas de 50mil registros para agilizar la carga
        deferRender: true,
        order: false,
        paging: false,
        ordering: false,
        info: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = ['20%','20%','15%','15%','15%','15%'];
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: date_now}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        // columns: [
        //     {"data": "id"},
        //     {"data": "name"},
        //     {
        //         "data": "address",
        //         "defaultContent": "N/A"
        //     },
        //     {
        //         "data": "phone",
        //         "defaultContent": "N/A"
        //     },
        //     {"data": "cant"},
        //     {"data": "should"},
        // ],
        // personaliza las columnas
        columnDefs: [
            {
                targets: [-1, -2, -3],
                class: 'text-left',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    })
}


$(function () {
    $('input[name="date_range"]').daterangepicker({
        // "autoApply": true,
        "startDate": moment().startOf('month'),
        "endDate": moment(),
        "locale": {
            "format": "DD/MM/YYYY",
            "separator": " - ",
            "applyLabel": "<i class='fas fa-chart-pie'> Aplicar",
            "cancelLabel": "<i class='fas fa-times'> Cancelar",
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
        opens: 'right'
    }, function (start, end, label) {
        date_start = start.format('YYYY-MM-DD')
        date_end = end.format('YYYY-MM-DD')
    }).on('apply.daterangepicker', function (ev, picker) {
        date_range = picker
        generate_report()
    }).on('cancel.daterangepicker', function (ev, picker) {
        console.log(date_now)
        $(this).data('daterangepicker').setStartDate(moment().startOf('month'));
        $(this).data('daterangepicker').setEndDate(moment());
        date_range = picker
        generate_report()
    })
    generate_report()
});