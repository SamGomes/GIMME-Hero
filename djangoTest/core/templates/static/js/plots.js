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
    // console.log(data)

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
    

    // from http://bl.ocks.org/mbostock/7555321
    function wrap(text, width) {
        
        text.each(function() {
            var text = d3.select(this),
            words = text.text().split(/\n/g).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.2, // ems
            x = text.attr("x"),
            y = text.attr("y"),
            dy = text.attr("dy") ? text.attr("dy") : 0;
            tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em");

            // console.log(words);
            // console.log(words.pop());

            while (words.length > 0) {
                word = words.pop();
                line.push(word);
                tspan.text(line.join(" "));
                // console.log(tspan.node().getComputedTextLength());
                if (tspan.node().getComputedTextLength() > width) {
                    line.pop();
                    tspan.text(line.join(" "));
                    line = [word];
                    tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
                }
            }
        });
    }

    function getRandomColor() {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    const width = 1400;
    const height = 500;
    svg = d3.select("#"+canvasId).append('svg')
      .attr('width', width)
      .attr('height', height);

    console.log(data);
  
    var playerNodes = [];
    var groupIndicatorNodes = [];
    var colors = [];
    for (i=0; i<data.groups.length; i++){
        var group = data.groups[i]
        var avgState = data.avgStates[i]
        var profile = data.profiles[i]
        var groupCenterOfMass = {"x": 100 + Math.random()*(width-300), "y": 100 + Math.random()*(height-300)};

        groupIndicatorNodes.push({"groupId": i, "characteristics": avgState.characteristics, "profile": profile, "centerOfMass": groupCenterOfMass});
        
        for(var j=0;j<group.length; j++){
            playerNodes.push({"playerId": group[j], "groupId": i, "centerOfMass": groupCenterOfMass});
        }
        colors[i]=getRandomColor();
    } 

    const simulation = d3.forceSimulation()
        .nodes(playerNodes)
        .force('attract', d3.forceAttract()
            .target((node) => [node.centerOfMass.x, node.centerOfMass.y])
            .strength(0.8)
            )
        .force('collide', d3.forceCollide(30)
            .strength(0.1))
        .nodes(groupIndicatorNodes)
        .force('collide', d3.forceCollide(30)
            .strength(0.2))


    var nodeElements =
        svg.append('g')
          .selectAll('circle')
          .data(playerNodes)
          .enter().append('circle')
            .attr('r', 10)
            .attr('fill', node => colors[node.groupId]);
  

    var groupIndicators =
        svg.append('g')
          .selectAll('circle')
          .data(groupIndicatorNodes)
          .enter().append('circle')
            .attr('r', node => {
                var group = playerNodes;
                var maxRadius = 0;
                for(var j=0; j< group.length; j++){
                    var currNode = group[j];
                    if(currNode.groupId != node.groupId){
                        continue;
                    }
                    var currRadius = (currNode.x - currNode.centerOfMass.x)**2 + (currNode.y - currNode.centerOfMass.y)**2
                    if(currRadius > maxRadius){
                        maxRadius = currRadius;
                    }
                }
                return Math.sqrt(maxRadius)
            })
            .attr('cx', node => node.centerOfMass.x)
            .attr('cy', node => node.centerOfMass.y)
            .attr('stroke-dasharray', '5,5')
            .attr('stroke', node => colors[node.groupId])
            .attr('fill', 'transparent');
   


    var textElements =
        svg.append('g')
          .selectAll('text')
          .data(playerNodes)
          .enter().append('text')
            .text(function (d) {
                return d.playerId.toString();
            })
            .attr('font-size', 15)
            .attr('dx', 15)
            .attr('dy', 4);


    var tooltipElements =
        svg.append('g')
            .selectAll('text')
            .data(groupIndicatorNodes)
            .enter()
            .append('g')
            .style('visibility','hidden');

    tooltipElements.append('rect')
        .attr('x', 15)
        .attr('y', 4)
        .attr('rx', '15px')
        // .attr('ry', '35px')
        .attr('width', 300)
        .attr('height', 200)
        .attr('fill', 'rgba(0, 0, 0, 0.59)')
        .attr('stroke', 'black');
    

    tooltipElements.append('text')
        .attr('x', 30)
        .attr('y', 30)
        
        // .attr('width', 200)
        // .attr('height', 160)

        .attr('font-size', 15)
        .attr('fill','white')
        .text(node => { return "Group Characteristics:\n "+JSON.stringify({ "characteristics": node.characteristics, "profile": node.profile} ,  undefined, 2);})
        .call(wrap, 80);



    //events
    groupIndicators
        .on("mouseover", function(d){ d3.select(tooltipElements._groups[0][d.index]).style("visibility", "visible");})
        .on("mouseout", function(d){ d3.select(tooltipElements._groups[0][d.index]).style("visibility", "hidden");});

    
    simulation.nodes(playerNodes).on("tick", () => {
            nodeElements
                .attr("cx", node => node.x)
                .attr("cy", node => node.y);

            groupIndicators
                .attr('cx', node => node.centerOfMass.x)
                .attr('cy', node => node.centerOfMass.y)
                .attr('r', node => {
                    var group = playerNodes;
                    var maxRadius = 0;
                    for(var j=0; j< group.length; j++){
                        var currNode = group[j];
                        if(currNode.groupId != node.groupId){
                            continue;
                        }
                        var currRadius = (currNode.x - currNode.centerOfMass.x)**2 + (currNode.y - currNode.centerOfMass.y)**2
                        if(currRadius > maxRadius){
                            maxRadius = currRadius;
                        }
                    }
                    return Math.sqrt(maxRadius) + 30 
                });

            tooltipElements
                .attr('transform', node => 'translate('+node.centerOfMass.x+' '+node.centerOfMass.y+')')

            textElements
                .attr("x", node => node.x)
                .attr("y", node => node.y);
        });

    const dragDrop = d3.drag()
        .on('start', node => {
            node.fx = node.x;
            node.fy = node.y;
        })
        .on('drag', node => {
            simulation.alphaTarget(1).restart();
            node.fx = d3.event.x;
            node.fy = d3.event.y;
        })
        .on('end', node => {
            if (!d3.event.active) {
                simulation.alphaTarget(0);
            }
            node.fx = null
            node.fy = null
        });

    groupIndicators.call(dragDrop)



}