$(document).ready(function () {
    tblZone = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            }, // parametros
            // dataSrc se utiliza cuando en una peticion envio los datos dentro de una variable, por lo tanto se definir esa variable
            // en este caso no lo envio en formato de variable
            dataSrc: "",
        },
        pageLength: 50,
        columns: [
            {"data": null},
            {"data": "position"},
            {"data": "name"},
            {"data": "address"},
            {"data": "cant_odo"},
            {"data": "abono"},
        ],
        columnDefs: [
            {
                "targets": [1],
                "visible": false
            }
        ],
        order: [[1, "asc"]],
        rowReorder: {
            dataSrc: 'position'
        },
    });

    tblZone.on('order.dt search.dt', function () {
        tblZone.column(0, {search: 'applied', order: 'applied'}).nodes().each(function (cell, i) {
            cell.innerHTML = i + 1;
        });
    }).draw();

    let footer = document.getElementById('card-footer')

    footer.innerHTML = '<a class="btn btn-primary btnTest" id="buttonConfirm"><i class="fas fa-check"></i>\n' +
        '                Confirmar Cambios' +
        '            </a>\n' +
        '            <a href="{{ list_url }}" class="btn btn-success"><i class="fas fa-sync"></i>\n' +
        '                Refrescar\n' +
        '            </a>'

    $('#buttonConfirm').on('click', function () {
        var table = $('#data').DataTable();
        var data = table.rows().data().toArray();
        data = JSON.stringify(data)
        console.log(data)
        $.ajax({
            url: window.location.pathname,
            method: 'POST',
            data: {
                'action': 'confirmOrder',
                'data': data,
            },
        }).done(function (data) {
            alert('Cambios enviados')
            location.reload();
        });
    })

});