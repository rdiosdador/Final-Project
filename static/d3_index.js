d3.json("/API-INDEX", { method: "POST", body: JSON.stringify({ meta: modificar_venta }), headers: { "Content-type": "application/json" } }).then(function(data) {

    let venta_total = data.venta_acumulada[0]
    let empleado_max = []
    let platillo_max = []

    var sum_array = arr => arr.reduce((a, b) => a + b, 0)
    d3.select("#cantidad_visitas").text(sum_array(data.clientes_empleado.clientes))

    var venta_format = function(d) { return "$" + d3.format(",.2f")(d); };
    d3.select("#venta_meta").text(venta_format(d3.select("#venta_meta").text()));
    d3.select("#venta_acumulada").text(venta_format(venta_total[0]));

    let venta_max = Math.max(...data.venta_empleado.venta)
    d3.select("#cantidad_text").text(venta_format(venta_max))

    let max_platillo = Math.max(...data.platillo_max.cantidad)
    d3.select("#max_platillo_cantidad").text(max_platillo)

    for (let i = 0; i < data.venta_empleado.nombre.length; i++) {
        if (data.venta_empleado.venta[i] == venta_max) {
            empleado_max.push(data.venta_empleado.nombre[i])
        }
    }

    d3.select("#empleado_max").text(empleado_max)

    for (let i = 0; i < data.platillo_max.platillo.length; i++) {
        if (data.platillo_max.cantidad[i] == max_platillo) {
            platillo_max.push(data.platillo_max.platillo[i])
        }
    }

    d3.select("#max_platillo").text(platillo_max)

    let trace1 = {
        x: data.venta_grupo.grupo.slice(0, 5),
        y: data.venta_grupo.venta.slice(0, 5),
        type: "line",
        name: "Venta por grupos",
        orientation: "h",
        marker: {
            color: 'rgba(67, 168, 129, 1)'
        }
    };

    let datos = [trace1];
    var layout = {
        // barmode: 'group',
        title: "Venta por grupos de platillos",
        font: {
            size: 10,
            color: 'black'
        },
        autosize: false,
        width: 650,
        height: 500,
        margin: {
            l: 150,
            r: 0,
            b: 25,
            t: 25,
            pad: 4
        },
        plot_bgcolor: "rgba(220,220,220 ,1 )",
        paper_bgcolor: "rgba(220,220,220 ,1 )"
    };

    Plotly.newPlot('ventas_grupo', datos, layout);

    var data_emp = [{
        values: data.venta_empleado.venta,
        labels: data.venta_empleado.nombre,
        type: 'pie'
    }];

    var layout_emp = {
        title: "Venta por empleado",
        height: 650,
        width: 600,
        plot_bgcolor: "rgba(220,220,220 ,1 )",
        paper_bgcolor: "rgba(220,220,220 ,1 )"
    };
    Plotly.newPlot('venta_empleado', data_emp, layout_emp);




});

var venta_format = function(d) { return "$" + d3.format(",.2f")(d); };
d3.select("#modificar_venta").on("click", function() {
    var modificar_venta = prompt("Ingrese el monto meta de venta")
    d3.select("#venta_meta").text(venta_format(modificar_venta))

});