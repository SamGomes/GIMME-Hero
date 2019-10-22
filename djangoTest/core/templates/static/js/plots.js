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
            })
            .on("mouseover",function(d){
                d3.select(this).append("text").text(function(d){
                            return d.name;
                        })
                        .attr("x", function (d) {
                            return x(d.K_i);
                        })
                        .attr("y", function (d) {
                            return y(d.K_cp);
                        });
            });
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


var buildGroupsPlot = function(canvasId, data){

    var svg = d3.select("#"+canvasId).append("svg")
    width = +svg.attr("width"),
    height = +svg.attr("height");

    var color = "rgb(12,240,233)";//d3.scaleOrdinal(d3.schemeCategory20);

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));



    // var link = svg.append("g")
    // .attr("class", "links")
    // .selectAll("line")
    // .data(graph.links)
    // .enter().append("line")
    // .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

    var node = svg.append("g")
    .attr("class", "nodes")
    .selectAll("g")
    .data(data)
    .enter().append("g");

    var circles = node.append("circle")
    .attr("r", 5)
    .attr("fill", function(d) { return color; })
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended));

    var lables = node.append("text")
    .text(function(d) {
            return d.id;
        })
    .attr('x', 6)
    .attr('y', 3);

    node.append("title")
    .text(function(d) { return d.id; });

    simulation
    .on("tick", ticked);

    function ticked() {
        node
        .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
        })
    }
    

    function dragstarted(d) {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    }

    function dragended(d) {
      if (!d3.event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
}