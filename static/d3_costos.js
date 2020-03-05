d3.json("/API", { method: "POST", headers: { "Content-type": "application/json" } }).then(function(data) {

    let costo_menor_28 = []
    let costo_mayor_28 = []
    let platillos_menor_28 = []
    let platillos_mayor_28 = []
    let venta_total = data.venta_acumulada[0]
    let promedio_costo = data.promedio_costo
    var sum_array = arr => arr.reduce((a, b) => a + b, 0)
    d3.select("#cantidad_visitas").text(sum_array(data.clientes_empleado.clientes))
    console.log(data.utilidad.grupo)

    for (let o = 0; o < data.costo_precio.costo_porcentaje.length; o++) {
        if (data.costo_precio.costo_porcentaje[o] > 28) {
            costo_mayor_28.push(data.costo_precio.costo_porcentaje[o])
            platillos_mayor_28.push(data.costo_precio.descripcion[o])

        } else {
            costo_menor_28.push(data.costo_precio.costo_porcentaje[o])
            platillos_menor_28.push(data.costo_precio.descripcion[o])
        }
    }

    let trace1 = {
        x: costo_menor_28.slice(platillos_menor_28.length - 10, platillos_menor_28.length),
        y: platillos_menor_28.slice(platillos_menor_28.length - 10, platillos_menor_28.length),
        type: "bar",
        name: "Platillos con Costo <28%",
        orientation: "h",
        marker: {
            color: 'rgba(67, 168, 129, 1)'
        }
    };
    let trace2 = {
        x: costo_mayor_28.slice(0, 10),
        y: platillos_mayor_28.slice(0, 10),
        type: "bar",
        name: "Platillos con Costos>28%",
        orientation: "h",
        marker: {
            color: 'rgba(93, 29, 0, 1)'
        }
    };

    let datos = [trace1];
    let datos1 = [trace2]
    var layout = {
        // barmode: 'group',
        title: "Platillos con Costos <28%",
        font: {
            size: 9,
            color: 'black'
        },
        autosize: false,
        width: 700,
        height: 300,
        margin: {
            l: 200,
            r: 10,
            b: 25,
            t: 25,
            pad: 4
        },
        plot_bgcolor: "rgba(220,220,220 ,1 )",
        paper_bgcolor: "rgba(220,220,220 ,1 )"
    };
    var layout1 = {
        // barmode: 'group',
        title: "Platillos con Costos >28%",
        font: {
            size: 9,
            color: 'black'
        },
        autosize: false,
        width: 700,
        height: 300,
        margin: {
            l: 200,
            r: 10,
            b: 25,
            t: 25,
            pad: 4
        },
        plot_bgcolor: "rgba(220,220,220 ,1 )",
        paper_bgcolor: "rgba(220,220,220 ,1 )"
    };

    Plotly.newPlot('costos_menor_28', datos, layout);
    Plotly.newPlot('costos_mayor_28', datos1, layout1);

    let utilidad = [{
        x: data.utilidad.utilidad_promedio,
        y: data.utilidad.grupo,
        type: "bar",
        name: "Utilidad por grupo",
        orientation: "h",
        marker: {
            color: 'rgba(67, 168, 129, 1)'
        }
    }];
    var layout_utilidad = {
        // barmode: 'group',
        title: "Utilidad promedio por grupo",
        font: {
            size: 9,
            color: 'black'
        },
        autosize: false,
        width: 1500,
        height: 400,
        margin: {
            l: 200,
            r: 10,
            b: 25,
            t: 25,
            pad: 4
        },
        plot_bgcolor: "rgba(220,220,220 ,1 )",
        paper_bgcolor: "rgba(220,220,220 ,1 )"
    };

    Plotly.newPlot('utilidad_max', utilidad, layout_utilidad);


    var venta_format = function(d) { return "$" + d3.format(",.2f")(d); }
    var costo_format = function(d) { return d3.format(",.2f")(d) + "%"; }


    d3.select("#venta_acumulada").text(venta_format(venta_total[0]))

    d3.select("tbody")
        .selectAll("tr")
        .data(promedio_costo)
        .enter()
        .append("tr")
        .html(m => {
            return `<td>${m.grupo}</td><td>${costo_format(m.costo_promedio)}</td>`
        });


});