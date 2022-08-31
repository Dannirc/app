// function mostrar() {
//     alert($('[name="duallistbox_demo1[]"]').val());
// }

// function details() {
//     // $('select[name="duallistbox_demo1[]"]').bootstrapDualListbox('destroy', true);
//     getClient($('#select_zone').val());
//     $('#myModelDet').modal('show');
// }

// muestra los clientes seleccionados en la lista (es llamado con el metodo onclick del boton guardar desde el html)
function guardar() {
    // obtengo los cliente seleccionados
    var lista = $('[name="duallistbox_demo1[]"]').val();
    const newlista = [];
    // creo una lista de id de los clientes seleccionados
    lista.forEach(nombre =>
        newlista.push(nombre.substring(0, nombre.indexOf(",")))
    );
    // guardo los datos (id) en un input hidden datos tabla
    $('[name="datosTabla"]').val(newlista);

    // muestro los datos en la tabla
    $("table tbody tr").children().remove()
    lista.forEach(nombre =>
        document.getElementById("table").insertRow(-1).innerHTML = '<td>' + nombre.substring(nombre.indexOf(",") + 1) + '</td>'
            + '<td><input class="form-control" placeholder="Ingrese Motivo" name="' + nombre.substring(0, nombre.indexOf(",")) + '-Motivo"></td>'
            + '<td><input type="date" class="form-control" placeholder="Ingrese Fecha" name="' + nombre.substring(0, nombre.indexOf(",")) + '-Fecha"></td>'
    );
}

function guardarClienteRealizado() {
    // obtengo los cliente seleccionados
    var lista = $('[name="duallistbox_cliPend"]').val();
    const newlista = [];
    // creo una lista de id de los clientes seleccionados
    lista.forEach(nombre =>
        newlista.push(nombre.substring(0, nombre.indexOf(",")))
    );
    // guardo los datos (id) en un input hidden datos tabla
    $('[name="clientRealizedList"]').val(newlista);
}

function showTableCliPendList() {
    $('#myModelCliPendList').modal('show');
}

function getTecnics() {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'search_tecnic',
        },
        success: function (data) {
            document.getElementById('select_tecnic').innerHTML += '<option disabled selected>Seleccione un Tecnico </option>'
            data.forEach(function (elemento) {
                document.getElementById('select_tecnic').innerHTML += '<option value="' + elemento.id + '">' + elemento.name + '</option>'
            });
        },
        error: function () {
            console.log("No se ha podido obtener la información de tecnicos");
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
            document.getElementById('select_zone').innerHTML = '<option value="0">Cobranza / Pendientes</option>'
            data.forEach(function (elemento) {
                document.getElementById('select_zone').innerHTML += '<option value="' + elemento.id + '">' + elemento.name + '</option>'
            });
        },
        error: function () {
            console.log("No se ha podido obtener la información de zonas");
        }
    });
}

function getClient(zone_id) {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'search_client',
            'id': zone_id,
        },
        success: function (data) {
            data.forEach(function (elemento) {
                document.getElementById('duallistbox_demo1[]').innerHTML += '<option value="' + elemento + '">' + elemento[1] + '</option>'
            });
            $('[name="duallistbox_demo1[]"]').bootstrapDualListbox('refresh');
            $('[name="duallistbox_demo1[]"]').bootstrapDualListbox();

        },
        error: function () {
            console.log("No se ha podido obtener la información de clientes");
        }
    });
}

function getClientPending(tecnic_id) {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'search_client_pending',
            'id': tecnic_id,
        },
        success: function (data) {
            document.getElementById('duallistbox_cliPend').innerHTML = ''
            data.forEach(function (elemento) {
                document.getElementById('duallistbox_cliPend').innerHTML += '<option value="' + elemento + '">' + elemento[1] + '</option>'
            });
            $('[name="duallistbox_cliPend"]').bootstrapDualListbox('refresh');
            $('[name="duallistbox_cliPend"]').bootstrapDualListbox();

        },
        error: function () {
            console.log("No se ha podido obtener la información de clientes");
        }
    });
}

$(function () {

    getTecnics();

    // obtengo las zonas al seleccionar el tecnico
    $('#select_tecnic').on('change', function () {
        tecnic_id = document.getElementById('select_tecnic').value
        getZone(tecnic_id)
    });

    // obtengo id de la zona seleccionada
    // $('#select_zone').on('change', function () {
    //     zone_id = document.getElementById('select_zone').value;
    // })


    $('#registerJob').on('click', function () {
        document.getElementById('duallistbox_demo1[]').innerHTML = '';
        document.getElementById('duallistbox_cliPend').innerHTML = '';
        getClientPending(document.getElementById('select_tecnic').value)
        zone_id = $('#select_zone').val()
        if (zone_id === null) {
            // alerta SweetAlert2
            var toastMixin = Swal.mixin({
                toast: true,
                animation: false,
                position: 'center',
                showConfirmButton: false,
                timer: 3000,
                title: 'Seleccione zona',
                icon: 'warning'
            });
            toastMixin.fire()
        } else {
            if (zone_id === '0') {
                $('#myModelCliPend').modal('show');
            } else {
                getClient(zone_id);
                $('#myModelDet').modal('show');
            }
        }
    })

    $('#myModelDetButton').on('click', function () {
        guardar();
        blank = document.getElementById('duallistbox_cliPend').innerHTML
        if (blank === '') {
            $('#myModelCliPendList').modal('show');
        } else {
            $('#myModelCliPend').modal('show');
        }
    })

    $('#myModelCliPendButton').on('click', function () {
        // falta crear logica para guardar clientes realizados
        guardarClienteRealizado();
        $('#myModelCliPendList').modal('show');
    })


})
