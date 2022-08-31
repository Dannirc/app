let year_now = new Date().getFullYear()

function getYears() {
    const years = []
    for (let i = 2020; i <= year_now; i++) {
        years.push(i);
    }
    return years
}

let years = getYears()

let graphcolumn = Highcharts.chart('container', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Reporte de facturación de servicios'
    },
    subtitle: {
        text: 'Año ' + year_now
    },
    xAxis: {
        categories: [
            'Enero',
            'Febrero',
            'Marzo',
            'Abril',
            'Mayo',
            'Junio',
            'Julio',
            'Agosto',
            'Septiembre',
            'Octubre',
            'Noviembre',
            'Diciembre'
        ],
        crosshair: true
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Valores $'
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} $</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
});

function buttons() {
    const years_buttons = document.getElementById("buttons");
    years_buttons.innerHTML = ''

    years.forEach(function (year) {
        if (year === year_now) {
            years_buttons.innerHTML +=
                '<button id=' + year + ' class="active">'
                + year +
                '</button>'
        } else {
            years_buttons.innerHTML +=
                '<button id=' + year + '>'
                + year +
                '</button>'
        }
    })
}

function get_graph_sales_year_month(year) {
    $.ajax({
        url: window.location.pathname, //window.location.pathname
        type: 'POST',
        data: {
            'action': 'get_graph_sales_year_month',
            'year': year,
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            graphcolumn.addSeries(data);
            return false;
        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
}

function change_selected_year() {
    years.forEach(year => {
        const btn = document.getElementById(year);

        btn.addEventListener('click', () => {

            document.querySelectorAll('.buttons button.active')
                .forEach(active => {
                    active.className = '';
                });
            btn.className = 'active';

            // get_graph_sales_year_month();
            graphcolumn.series[0].remove(false);
            graphcolumn.update({
            //     title: {
            //         text: `Summer Olympics ${year} - Top 5 countries by Gold medals`
            //     },
                subtitle: {
                    text: 'Año ' + year
                },
                series: [
                    get_graph_sales_year_month(year)
                ]
            // }, true, false, {
            //     duration: 800
            });
        });

    });
}

$(function () {
    buttons(year_now);

    get_graph_sales_year_month(year_now);

    change_selected_year()
})