var buildInteractionsProfilePlot = function(canvasId, data){
    
    var width = 500;
    var height = 500;

    var margin = {
        top: 40,
        right: 40,
        bottom: 40,
        left: 40
    };

    var x = d3.scaleLinear().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    x.domain([0,1]);
    y.domain([0,1]);

    var xAxis = d3.axisTop(x);

    var yAxis = d3.axisRight(y);

    var svg = d3.select("#"+canvasId)
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(" + 0 + "," + height / 2 + ")")
            .call(xAxis);

    svg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + width / 2 + "," + 0 + ")")
            .call(yAxis)
            .append("text");
              

  var dots =  svg.selectAll("g.dot")
            .data(data)
            .enter().append('g');
            
            dots.append("circle")
            .attr("class", "dot")
            .attr("r", 5)
            .attr("cx", function (d) {
                return x(d.K_i);
            })
            .attr("cy", function (d) {
                return y(d.K_cp);
            })
            .style("fill", function (d) {
                return "#50C2E3";
            });
            // gdots.append("text").text(function(d){
            // 	return d.name;
            // })
            // .attr("x", function (d) {
            //     return x(d.K_i);
            // })
            // .attr("y", function (d) {
            //     return y(d.K_cp);
            // });
}


var buildStatePlot = function(canvasId, data){

    var margin = {
        top: 15,
        right: 25,
        bottom: 15,
        left: 60
    };
    console.log(data)

    var width = 960 - margin.left - margin.right;
    var height = 500 - margin.top - margin.bottom;

    var svg = d3.select("#"+canvasId).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var x = d3.scaleLinear()
        .range([0, width])
        .domain([0,1]);

    var y = d3.scaleBand()
        .range([0, height])
        .domain(data.map(function(d) {
            return d.name;
        }))

    var xAxis = d3.axisTop(x)
        .tickSize(0);

    var yAxis = d3.axisLeft(y)
        .tickSize(0);


    var bars = svg.selectAll(".bar")
        .data(data)
        .enter()
        .append("g")


    bars.append("rect")
        .attr("class", "bar")
        .attr("y", function (d) {
            return y(d.name)+y.bandwidth()*3/16;
        })
        .attr("height", y.bandwidth()*3/4)
        .attr("x", 0)
        .attr("width", function (d) {
            return x(d.value);
        })
        .attr("fill", "#50C2E3");

    var gy = svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
    var gy = svg.append("g")
        .attr("class", "x axis")
        .call(xAxis)
}