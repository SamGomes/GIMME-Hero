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

    var svg = d3.select('#'+canvasId)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    svg.append('g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(' + 0 + ',' + height / 2 + ')')
            .call(xAxis);

    svg.append('g')
            .attr('class', 'y axis')
            .attr('transform', 'translate(' + width / 2 + ',' + 0 + ')')
            .call(yAxis)
            .append('text');
              

  var dots =  svg.selectAll('g.dot')
            .data(data)
            .enter().append('g');
            
            dots.append('circle')
                .attr('class', 'dot')
                .attr('r', 5)
                .attr('cx', function (d) {
                    return x(d.K_i);
                })
                .attr('cy', function (d) {
                    return y(d.K_cp);
                })
                .style('fill', function (d) {
                    return '#50C2E3';
                })
                .on('mouseover',function(d){
                    d3.select(this).append('text').text(function(d){
                                return d.name;
                            })
                            .attr('x', function (d) {
                                return x(d.K_i);
                            })
                            .attr('y', function (d) {
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

    var svg = d3.select('#'+canvasId).append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

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


    var bars = svg.selectAll('.bar')
        .data(data)
        .enter()
        .append('g')


    bars.append('rect')
        .attr('class', 'bar')
        .attr('y', function (d) {
            return y(d.name)+y.bandwidth()*3/16;
        })
        .attr('height', y.bandwidth()*3/4)
        .attr('x', 0)
        .attr('width', function (d) {
            return x(d.value);
        })
        .attr('fill', '#50C2E3');

    var gy = svg.append('g')
        .attr('class', 'y axis')
        .call(yAxis)
    var gy = svg.append('g')
        .attr('class', 'x axis')
        .call(xAxis)
}


var buildGroupsPlot = function(canvasId, data, selectedUsersStates){
    
    // from http://bl.ocks.org/mbostock/7555321
    function wrap(text, width) {
        text.each(function () {
            var text = d3.select(this),
                words = text.text().split(/\s+/).reverse(),
                word,
                line = [],
                lineNumber = 0,
                lineHeight = 1.1, // ems
                x = text.attr("x"),
                y = text.attr("y"),
                dy = 0, //parseFloat(text.attr("dy")),
                tspan = text.text(null)
                            .append("tspan")
                            .attr("x", x)
                            .attr("y", y)
                            .attr("dy", dy + "em");
            while (word = words.pop()) {
                line.push(word);
                tspan.text(line.join(" "));
                if (tspan.node().getComputedTextLength() > width) {
                    line.pop();
                    tspan.text(line.join(" "));
                    line = [word];
                    tspan = text.append("tspan")
                                .attr("x", x)
                                .attr("y", y)
                                .attr("dy", ++lineNumber * lineHeight + dy + "em")
                                .text(word);
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

    function sqrDistBetweenVectors(vec1, vec2){
        return (Math.pow(vec1.ability - vec2.ability, 2) + Math.pow(vec1.engagement - vec2.engagement, 2));
    }

    const width = 1400;
    const height = 500;
    svg = d3.select('#'+canvasId).append('svg')
      .attr('width', width)
      .attr('height', height);

    var userNodes = [];
    var groupIndicatorNodes = [];
    var colors = [];

    var currPlotIndex = 0;
 
    for (i=0; i<data.groups.length; i++){
        var group = data.groups[i]
        var avgCharacteristics = data.avgCharacteristics[i]
        var profile = data.profiles[i]
        var adaptedTaskId = data.adaptedTaskId[i]
        var groupCenterOfMass = {'x': 100 + Math.random()*(width - 300), 'y': 100 + Math.random()*(height - 300)};

        groupIndicatorNodes.push({'groupId': i, 'characteristics': avgCharacteristics,  'profile': profile, 'adaptedTaskId': adaptedTaskId, 'centerOfMass': groupCenterOfMass});
        
        for(var j=0;j<group.length; j++){
            //TODO: add user characteristics
            var userId = group[j];
            userState = selectedUsersStates[userId];
            console.log(userState)
            userNodes.push({'plotIndex': currPlotIndex++, 'userId': userId, 'userState': userState, 'groupId': i, 'groupCharacteristics': avgCharacteristics, 'centerOfMass': groupCenterOfMass});
            // userNodes.push({'userId': userId, 'userState': fetchPlayerStateCallback(userId), 'groupId': i, 'groupCharacteristics': avgCharacteristics, 'centerOfMass': groupCenterOfMass});
        }
        colors[i] = getRandomColor();
    } 

    

    var groupIndicators =
        svg.append('g')
          .selectAll('circle')
          .data(groupIndicatorNodes)
          .enter().append('circle')
            .attr('r', node => {
                var group = userNodes;
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
           



    function clamp(num, min, max) {
      return num <= min ? min : num >= max ? max : num;
    }

    var generatePlayerColor = function(node){
        var userChar = node.userState.characteristics;
        var baseColor = colors[node.groupId].split('#')[1];
        var transparency = 50 + Math.round(175*(1 - sqrDistBetweenVectors(node.groupCharacteristics, userChar)/2));
        return '#' +  baseColor + transparency.toString(16);
    }

    var nodeElements =
        svg.append('g')
          .selectAll('circle')
          .data(userNodes)
          .enter().append('circle')
            .attr('r', 10)
            .attr('fill', function(node){
                                return generatePlayerColor(node);
                            });


    // var textElements =
    //     svg.append('g')
    //       .selectAll('text')
    //       .data(userNodes)
    //       .enter().append('text')
    //         .text(function (d) {
    //             return d.userId.toString();
    //         })
    //         .attr('font-size', 10)
    //         .attr('dx', -5)
    //         .attr('dy', 5);






    var groupInfoTooltips =
        svg.append('g')
            .selectAll('text')
            .data(groupIndicatorNodes)
            .enter()
            .append('g')
            .style('visibility','hidden');

    groupInfoTooltips.append('rect')
        .attr('x', 15)
        .attr('y', 4)
        .attr('rx', '15px')
        // .attr('ry', '35px')
        .attr('width', 400)
        .attr('height', 300)
        .attr('fill', function(node){
                                var baseColor = colors[node.groupId].split('#')[1];
                                transparency = 127;
                                return '#' +  baseColor + transparency.toString(16);
                            })
        .attr('stroke', 'black');
    

    groupInfoTooltips.append('text')
        .attr('x', 30)
        .attr('y', 30)
        
        .attr('font-size', 15)
        .attr('fill','black')
        .text(node => { 
            if(node.adaptedTaskId == -1){
                alert('Could not compute task for group'+node.groupId+'... Maybe no tasks are available?')
            }
            return 'Group Info\n '+JSON.stringify({ 'group Id': node.groupId, 'characteristics': node.characteristics, 
            'profile': node.profile, 'adaptedTaskId': node.adaptedTaskId == -1 ? node.adaptedTaskId : '<Could not compute task>' } ,  undefined, 2);

        })
        .call(wrap, 300);


    groupIndicators.on('mouseover', function(d){ d3.select(groupInfoTooltips._groups[0][d.groupId]).style('visibility', 'visible');})
            .on('mouseout', function(d){ d3.select(groupInfoTooltips._groups[0][d.groupId]).style('visibility', 'hidden');});        





    var userInfoTooltips =
        svg.append('g')
            .selectAll('text')
            .data(userNodes)
            .enter()
            .append('g')
            .style('visibility','hidden');

    userInfoTooltips.append('rect')
        .attr('x', 15)
        .attr('y', 4)
        .attr('rx', '15px')
        // .attr('ry', '35px')
        .attr('width', 400)
        .attr('height', 300)
        .attr('fill', function(node){
                                return generatePlayerColor(node);
                            })
        .attr('stroke', 'black');
    

    console.log(wrap)
    userInfoTooltips.append('text')
        .attr('x', 30)
        .attr('y', 30)
        
        .attr('font-size', 15)
        .attr('fill','black')
        .text(node => { 
                    return 'User Info '+ JSON.stringify({'userId': node.userId, 'userState': node.userState},  undefined, 2);
                })
        .call(wrap, 300);

     nodeElements.on('mouseover', function(d){ d3.select(userInfoTooltips._groups[0][d.plotIndex]).style('visibility', 'visible');})
            .on('mouseout', function(d){ d3.select(userInfoTooltips._groups[0][d.plotIndex]).style('visibility', 'hidden');});        

            





    var simulation = d3.forceSimulation();
    var resetSim = function(){
        simulation.nodes(userNodes)
        .force('collide', d3.forceCollide(15)
            .strength(0.2))
        .force('attract', d3.forceAttract()
                    .target((node) => {return [node.centerOfMass.x, node.centerOfMass.y];})
                    .strength(3)
                    );
    }


    resetSim();
    simulation.on('tick', () => {
            nodeElements
                .attr('cx', node => node.x)
                .attr('cy', node => node.y);

            groupIndicators
                .attr('cx', node => node.centerOfMass.x)
                .attr('cy', node => node.centerOfMass.y)
                .attr('r', node => {
                    var group = userNodes;
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
                

            groupInfoTooltips
                .attr('transform', node => 'translate('+node.centerOfMass.x+' '+node.centerOfMass.y+')');

            // textElements
            //     .attr('x', node => node.x)
            //     .attr('y', node => node.y);

            userInfoTooltips
                .attr('transform', node => 'translate('+node.x+' '+node.y+')');

        });



    const dragDrop = d3.drag()
        .on('start', node => {
            if (!d3.event.active)
                simulation.alphaTarget(0.3).restart();

            node.centerOfMass.x = d3.event.x;
            node.centerOfMass.y = d3.event.y;
            node.fx = node.centerOfMass.x;
            node.fy = node.centerOfMass.y;
            for(i=0; i<userNodes.length; i++){
                var currNode = userNodes[i];
                if(currNode.groupId == node.groupId){
                    currNode.centerOfMass.x = d3.event.x;
                    currNode.centerOfMass.y = d3.event.y;

                    currNode.fx = currNode.centerOfMass.x;
                    currNode.fy = currNode.centerOfMass.y;
                }
            }
        })
        .on('drag', node => {
            simulation.alphaTarget(1.0).restart();
            node.centerOfMass.x = d3.event.x;
            node.centerOfMass.y = d3.event.y;
            node.fx = node.centerOfMass.x;
            node.fy = node.centerOfMass.y;
            for(i=0; i<userNodes.length; i++){
                var currNode = userNodes[i];
                if(currNode.groupId == node.groupId){
                    currNode.centerOfMass.x = d3.event.x;
                    currNode.centerOfMass.y = d3.event.y;

                    currNode.fx = currNode.centerOfMass.x;
                    currNode.fy = currNode.centerOfMass.y;
                }
            }
        })
        .on('end', node => {
            if (!d3.event.active) {
                simulation.alphaTarget(0);
            }
            node.fx = null;
            node.fy = null;
            for(i=0; i<userNodes.length; i++){
                var currNode = userNodes[i];
                if(currNode.groupId == node.groupId){
                    currNode.centerOfMass.x = d3.event.x;
                    currNode.centerOfMass.y = d3.event.y;

                    currNode.fx = null;
                    currNode.fy = null;
                }
            }
            resetSim();
        });

    groupIndicators.call(dragDrop);
    



}