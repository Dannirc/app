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
            {
                "data": "name",
                "defaultContent": ''
            },
            {
                "data": "date_of_work",
                "defaultContent": ''
            },
            {
                "data": "date",
                "defaultContent": ''
            },
            {
                "data": "tecnic.name",
                "defaultContent": ''
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
                    var buttons = '<a href="/erp/zone/route/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs"><i class="fas fa-file-pdf"></i></a> ';
                    return buttons;
                }
            },
            {
                targets: [2],
                class: 'text-center',
                render: $.fn.dataTable.render.moment('DD/MM/YYYY')
            },
            {
                targets: [1],
                class: 'text-left text-capitalize',
            },
        ],
        order: [[3, 'asc'], [2, 'asc']],
        createdRow: function( row, data, dataIndex){
                            date = new Date(data.date)
                            // se corrige el horario por defecto +0 a -3 (arg)
                            // de lo contrario mostraria 1 dia atrasado
                            date.setMinutes(date.getMinutes() + date.getTimezoneOffset())
                            date_now = new Date()
                            if( data.date_of_work === 'Servicio Completo'  ){
                                $(row).css('background-color', '#59BB66');
                            }
                            else {
                                if (date.getMonth() === date_now.getMonth() && date.getFullYear() === date_now.getFullYear()){
                                    $(row).css('background-color', '#F6DDCC');
                                }
                            }

                        },
        initComplete: function (settings, json) {

        }
    });
});