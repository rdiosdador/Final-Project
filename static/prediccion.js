d3.select("#calculando").text("Analizando Información...")
d3.json("/MLPRED", { method: "POST", headers: { "Content-type": "application/json" } }).then(function(data) {

    let trace = {
        x: data.total_sales.Fecha,
        y: data.total_sales.cantidad,
        name: "Ventas totales",
        marker: {
            color: 'rgba(93, 29, 0, 1)'
        }
    };

    let datos = [trace]

    var layout = {
        title: "Ventas Totales",
        font: {
            size: 9,
            color: 'black'
        },
        autosize: false,
        width: 1000,
        height: 700,
        plot_bgcolor: "rgba(220,220,220 ,1 )",
        paper_bgcolor: "rgba(220,220,220 ,1 )"
    };

    Plotly.newPlot('historico_ventas', datos, layout);

    d3.select("#calculando").text("")
    d3.select("#prediccion_ventas").text(data.predictor)
    console.log(data.predictor)

    d3.select("#confiabilidad").text(data.confiabilidad)
    console.log(data.confiabilidad)

});