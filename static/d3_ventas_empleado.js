d3.json("/API", { method: "POST", headers: { "Content-type": "application/json" } }).then(function(data) {

    let venta_total = data.venta_acumulada[0]
    let empleado_max = []
    let empleado_max_propina = []
    let empleado_max_clientes = []
    let cantidad_venta = parseFloat(d3.select("#venta_meta").text())
    var sum_array = arr => arr.reduce((a, b) => a + b, 0)
    d3.select("#cantidad_visitas").text(sum_array(data.clientes_empleado.clientes))
    var venta_format = function(d) { return "$" + d3.format(",.2f")(d); };
    d3.select("#venta_meta").text(venta_format(d3.select("#venta_meta").text()));
    d3.select("#venta_acumulada").text(venta_format(venta_total[0]));

    let venta_max = Math.max(...data.venta_empleado.venta)
    d3.select("#cantidad_text").text(venta_format(venta_max))

    let propina_max = Math.max(...data.propinas.propina)
    d3.select("#max_propina").text(venta_format(propina_max))

    let clientes_max = Math.max(...data.clientes_empleado.clientes)
    d3.select("#max_clientes").text(clientes_max)

    for (let i = 0; i < data.venta_empleado.nombre.length; i++) {
        if (data.venta_empleado.venta[i] == venta_max) {
            empleado_max.push(data.venta_empleado.nombre[i])
        }
    }

    for (let i = 0; i < data.propinas.propina.length; i++) {
        if (data.propinas.propina[i] == propina_max) {
            empleado_max_propina.push(data.propinas.nombre[i])
        }
    }

    for (let l = 0; l < data.clientes_empleado.nombre.length; l++) {
        if (data.clientes_empleado.clientes[l] == clientes_max) {
            empleado_max_clientes.push(data.clientes_empleado.nombre[l])
        }
    }

    d3.select("#empleado_max").text(empleado_max)
    d3.select("#empleado_max_propina").text(empleado_max_propina)
    d3.select("#empleado_max_clientes").text(empleado_max_clientes)


    var propinas = {
        type: 'bar',
        x: data.propinas.propina,
        y: data.propinas.nombre,
        orientation: 'h',
        name: "Propinas recibidas"
    };

    var clientes = {
        type: 'bar',
        x: data.clientes_empleado.clientes,
        y: data.clientes_empleado.nombre,
        orientation: 'h',
        name: "Clientes atendidos"
    };

    var ventas = {
        type: 'bar',
        x: data.venta_empleado.venta,
        y: data.venta_empleado.nombre,
        orientation: 'h',
        name: "Venta por empleado"
    };

    var layout_prop_clientes = {
        barmode: 'group',
        title: "Propinas / Clientes / Ventas por empleado",
        font: {
            size: 11,
            color: 'black'
        },
        autosize: false,
        width: 1000,
        height: 400,
        margin: {
            l: 150,
            r: 0,
            b: 25,
            t: 25,
            pad: 4
        },
        plot_bgcolor: "rgba(220,220,220 ,1 )",
        paper_bgcolor: "rgba(220,220,220 ,1 )",
        xaxis: {
            range: [0, data.propinas.propinas]
        }
    };

    var data_prop_clientes = [propinas, clientes, ventas]
    Plotly.newPlot('propinas', data_prop_clientes, layout_prop_clientes);


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


    var consumo_prom = [{
        type: 'bar',
        x: data.consumo_promedio.nombre,
        y: data.consumo_promedio.consumo,
        name: "Consumo promedio por empleado"
    }];


    var layout_consumo = {
        title: "Consumo promedio por empleado",
        height: 650,
        width: 600,
        plot_bgcolor: "rgba(220,220,220 ,1 )",
        paper_bgcolor: "rgba(220,220,220 ,1 )"
    }

    Plotly.newPlot('consumo_promedio', consumo_prom, layout_consumo);




});