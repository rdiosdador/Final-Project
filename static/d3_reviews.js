d3.json("/API-REVIEWS", { method: "POST", headers: { "Content-type": "application/json" } }).then(function(data) {


    console.log(data)

    var reviews = [{
        values: data.reviews.count,
        labels: data.reviews.classification,
        type: 'pie'
    }];

    var layout = {
        title: "Total de Reviews",
        height: 650,
        width: 600,
        font: {
            size: 15,
            color: 'black'
        },
        plot_bgcolor: "rgba(220,220,220 ,1 )",
        paper_bgcolor: "rgba(220,220,220 ,1 )"
    };
    Plotly.newPlot('reviews', reviews, layout);

    console.log(data)



});