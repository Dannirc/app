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

function getClient(tecnic_id, zone_id) {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'search_client',
            'zone_id': zone_id,
            'tecnic_id': tecnic_id
        },
        success: function (data) {
            document.getElementById('id_cli').innerHTML = '<option value="0">Todos</option>'
            data.forEach(function (elemento) {
                document.getElementById('id_cli').innerHTML += '<option value="' + elemento.id + '">' + elemento.name + '</option>'
            });
        },
        error: function () {
            console.log("No se ha podido obtener la información");
        }
    });
}

$(function () {
    // obtengo los clientes al cargar la pagina
    getTecnics();

    getClient('0','0')

    // obtengo las zonas al seleccionar el tecnico
    $('#select_tecnic').on('change', function () {
        tecnic_id = document.getElementById('select_tecnic').value
        console.log(tecnic_id)
        getZone(tecnic_id)
        getClient(tecnic_id, '0')
    });

    // obtengo los clientes de la zona seleccionada
    $('#select_zone').on('change', function () {
        zone_id = document.getElementById('select_zone').value
        console.log(zone_id)
        getClient('0', zone_id)
    });
})