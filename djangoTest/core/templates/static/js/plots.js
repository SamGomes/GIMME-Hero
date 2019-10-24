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
    
    function getRandomColor() {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    const width = 960;
    const height = 500;
    svg = d3.select("#"+canvasId).append('svg')
      .attr('width', width)
      .attr('height', height);

    const simulation = d3.forceSimulation()
      .force('charge', d3.forceManyBody().strength(-20)) 
      .force('center', d3.forceCenter(width / 2, height / 2))

    var allGroups = []
    var colors = []
    for (i=0; i<data.length; i++){
        var group = data[i].playerIds
        for(var j=0;j<group.length; j++){
            allGroups.push({"playerId": group[j], "groupId": i});
        }
        colors[i]=getRandomColor();
    } 
    console.log(allGroups)
    var nodeElements =
        svg.append('g')
          .selectAll('circle')
          .data(allGroups)
          .enter().append('circle')
            .attr('r', 10)
            .attr('fill', function(d){
                return colors[d.groupId]
            });
    
    var textElements =
        svg.append('g')
          .selectAll('text')
          .data(allGroups)
          .enter().append('text')
            .text(function (d) {
                return d.playerId.toString();
            })
            .attr('font-size', 15)
            .attr('dx', 15)
            .attr('dy', 4);


    simulation.nodes(allGroups).on("tick", () => {
            nodeElements
                .attr("cx", node => node.x)
                .attr("cy", node => node.y)
            textElements
                .attr("x", node => node.x)
                .attr("y", node => node.y)
        })

    const dragDrop = d3.drag()
        .on('start', node => {
            node.fx = node.x
            node.fy = node.y
        })
        .on('drag', node => {
            simulation.alphaTarget(0.7).restart()
            node.fx = d3.event.x
            node.fy = d3.event.y
        })
        .on('end', node => {
            if (!d3.event.active) {
                simulation.alphaTarget(0)
            }
            node.fx = null
            node.fy = null
        })

    nodeElements.call(dragDrop)
}