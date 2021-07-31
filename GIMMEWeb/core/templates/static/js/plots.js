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
            .call(xAxis)
    

    svg.append('g')
        .attr('class', 'y axis')
        .attr('transform', 'translate(' + width / 2 + ',' + 0 + ')')
        .call(yAxis)
            

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
        top: 20,
        right: 30,
        bottom: 30,
        left: 150
    };

    var width = 960 - margin.left - margin.right;
    var height = 100 - margin.top - margin.bottom;

    var svg = d3.select('#'+canvasId).append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    var maxValue = Math.max(data[0].value, data[1].value);
    var x = d3.scaleLinear()
        .range([0, width])
        .domain([0, maxValue + 0.5]);

    var y = d3.scaleBand()
        .range([0, height])
        .domain(data.map(function(d) {
            return d.name;
        }));

    var xAxis = d3.axisBottom(x)
        .tickSize(maxValue / 5.0);

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
        .attr('class', 'y axis label')
        .call(yAxis) 
        .style("font-size","20px");


    var gx = svg.append('g')
        .attr('class', 'x axis')
        .call(xAxis)
        .attr('transform', 'translate(0,' + height + ')')
        .style("font-size","20px");
}


var buildGroupsPlot = function(canvasId, data, selectedUsersStates){

    // used to correctly generate user colors
    var abMax = 0;
    var engMax = 0; 

    var abMin = Infinity;
    var engMin = Infinity; 


    $("#adaptationIssues_professor_dash").hide();
    $("#adaptationIssuesText_professor_dash").html('');

    // from http://bl.ocks.org/mbostock/7555321
    var wrap = function (text, width) {
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

    var getRandomColor = function() {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }


    var generateGroupColor = function(profile) {
        var focus = profile.dimensions.Focus;
        var challenge = profile.dimensions.Challenge;

        if (focus >= 0 && focus < 0.33){
            if (challenge >= 0 && challenge < 0.33){
                return "#b5dd02"
            }
            else if (challenge >= 0.33 && challenge < 0.66){
                return "#ddb502"
            }
            else if (challenge >= 0.66 && challenge <= 1.0){
                return "#dd6c02"
            }
        }
        else if (focus >= 0.33 && focus < 0.66){
            if (challenge >= 0 && challenge < 0.33){
                return "#dd1402"
            }
            else if (challenge >= 0.33 && challenge < 0.66){
                return "#a3a1a1"
            }
            else if (challenge >= 0.66 && challenge <= 1.0){
                return "#19c151"
            }
        }
        else if (focus >= 0.66 && focus <= 1.0){
            if (challenge >= 0 && challenge < 0.33){
                return "#7724d6"
            }
            else if (challenge >= 0.33 && challenge < 0.66){
                return "#cd7dce"
            }
            else if (challenge >= 0.66 && challenge <= 1.0){
                return "#89150b"
            }
        }
        return "#a3a1a1"
    }
    


    var generatePlayerColor = function(node){

        var userChar = node.userState.characteristics;
        abRatio = abMax > 0.0? ((userChar.ability - abMin) / (abMax - abMin)): 0.0;
        engRatio = engMax > 0.0? ((userChar.engagement - engMin) / (engMax - engMin)): 0.0;


        ratio = (abRatio + engRatio) / 2.0;

        return d3.scaleLinear()
        .domain([0.0, 0.5, 1.0])
        .range(["#FF0000", "#FFFF00", "#00FF00"])(ratio)

    }


    // from: https://stackoverflow.com/questions/35969656/how-can-i-generate-the-opposite-color-according-to-current-color
    var invertColor = function(hex, isBW) {
        if (hex.indexOf('#') === 0) {
            hex = hex.slice(1);
        }
        // convert 3-digit hex to 6-digits.
        if (hex.length === 3) {
            hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
        }
        if (hex.length !== 6) {
            throw new Error('Invalid HEX color.');
        }
        var r = parseInt(hex.slice(0, 2), 16),
            g = parseInt(hex.slice(2, 4), 16),
            b = parseInt(hex.slice(4, 6), 16);
        if (isBW) {
            // http://stackoverflow.com/a/3943023/112731
            return (r * 0.299 + g * 0.587 + b * 0.114) > 186
                ? '#000000'
                : '#FFFFFF';
        }
        // invert color components
        r = (255 - r).toString(16);
        g = (255 - g).toString(16);
        b = (255 - b).toString(16);
        // pad each with zeros and return
        return "#" + padZero(r) + padZero(g) + padZero(b);
    }

    var padZero = function(str, len) {
        len = len || 2;
        var zeros = new Array(len).join('0');
        return (zeros + str).slice(-len);
    }

    var sqrDistBetweenVectors = function(vec1, vec2){
        return (Math.pow(vec1.ability - vec2.ability, 2) + Math.pow(vec1.engagement - vec2.engagement, 2));
    }

    var resizeCanvas = function(canvas, aspect){
        var targetWidth = canvasContainer.getBoundingClientRect().width;
        canvas.attr("width", targetWidth);
        canvas.attr("height", targetWidth/aspect);
    }

    svg = d3.select('#'+canvasId).append('svg');

    var canvas = svg;
    var canvasContainer = canvas.node().parentNode;

    width = canvasContainer.getBoundingClientRect().width;
    height = canvasContainer.getBoundingClientRect().height;

    aspect = 2.5 / 1.0;

    resizeCanvas(canvas, aspect);


    var userNodes = [];
    var groupIndicatorNodes = [];
    var colors = [];

    var currPlotIndex = 0;

    d3.select(window)
        .on("resize", function() {
            resizeCanvas(canvas);
        });

    for (i=0; i<data.groups.length; i++){
        var group = data.groups[i];
        var avgCharacteristics = $.extend({}, data.avgCharacteristics[i]);
        delete avgCharacteristics.profile;
        var profile = data.profiles[i];
        var tasks = data.tasks[i];
        var groupCenterOfMass = {'x': 100 + Math.random()*(width*0.8), 'y': 10 + Math.random()*(height*0.8)};

        groupIndicatorNodes.push({'groupId': i, 'characteristics': avgCharacteristics, 'profile': profile, 'tasks': tasks, 'centerOfMass': groupCenterOfMass});
        
        for(var j=0;j<group.length; j++){
            //TODO: add user characteristics
            var userId = group[j];
            userState = selectedUsersStates[userId];
            userNodes.push({'plotIndex': currPlotIndex++, 'userId': userId, 'userState': unformattedStringToObj(userState), 'groupId': i, 'groupCharacteristics': avgCharacteristics, 'centerOfMass': groupCenterOfMass});
        }
        colors[i] = generateGroupColor(profile);
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
            .attr('stroke-dasharray', '8,5')
            .attr('stroke', node => colors[node.groupId])
            .attr('stroke-width', '3.5') 
            .attr('fill', 'transparent');
           



    var clamp = function(num, min, max) {
      return num <= min ? min : num >= max ? max : num;
    }

    var nodeElements =
        svg.append('g')
            .selectAll('circle')
            .data(userNodes)
            .enter().append('circle')
            .attr('r', 15)
            .each(function(node){
                //update caps before treating nodes for print
                var currAb = node.userState.characteristics.ability;
                if(currAb > abMax){
                    abMax = currAb;
                }
                if(currAb < abMin){
                    abMin = currAb;
                }
                var currEng = node.userState.characteristics.engagement;
                if(currEng > engMax){
                    engMax = currEng; 
                }
                if(currAb < engMin){
                    engMin = currAb;
                }
            })
            .attr('fill', function(node){
                    return generatePlayerColor(node);
                })
            .attr('stroke', node => colors[node.groupId])
            .attr('stroke-width', '3');


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


    var getJSONLength = function(json){
        if(typeof json == "string"|| json == undefined){
            return 0;
        }
        var keys = Object.keys(json);
        var totalLength = keys.length;
        for(var i=0; i < keys.length; i++){
            if(currKey=="0"){
                continue;
            }
            var currKey = keys[i];
            var currJson = json[currKey];
            totalLength += getJSONLength(currJson);
        }
        return totalLength;
    }

    var htmlFromJSON = function(json, fatherElem, currX, currY, paddingX, paddingY, j){
        
        if(typeof json == "string" || typeof json == "number" || json == undefined){
            return;
        }


        var keys = Object.keys(json)
        var x = currX + 100;
        var y = currY + 30;

        if(j==0){
            x += paddingX;
            y += paddingY;
        }

        for(var i=0; i < keys.length; i++){
            var currKey = keys[i];
            var currJson = json[currKey];
            
            if(currKey=="0"){
                continue;
            }

            if(typeof currJson != "string" && typeof currJson != "number"){
                currKey+=" ↴";
            }

            fatherElem
            .append('text')
            .attr('x', x)
            .attr('y', y + 20)
            .attr('font-size', 20)
            .attr('font-family', 'Calibri,sans-serif')
            .attr('color', function(node){ return invertColor(colors[node.groupId], true); })
            .call(wrap, 300)
            .text(currKey);

            if(typeof currJson == "string" || typeof currJson == "number"){

                fatherElem
                .append('rect')
                .attr('x', x + 160)
                .attr('y', y)
                .attr('width', 260)
                .attr('height', 30)
                .attr('fill', function(node){ return "white"; })
                .attr('stroke', 'black');

                fatherElem
                .append('text')
                .attr('x', x + 170)
                .attr('y', y + 20)
                .attr('font-size', 20)
                .attr('font-family', 'Calibri,sans-serif')
                .attr('color', function(node){ return "black"; })
                .call(wrap, 300)
                .text(currJson);
            }

            htmlFromJSON(currJson, fatherElem, x, y, paddingX, paddingY, ++j);

            y += 35*(1+getJSONLength(currJson));
        }

    };


    // adapted from: https://stackoverflow.com/questions/12115691/svg-d3-js-rounded-corner-on-one-corner-of-a-rectangle
    // Returns path data for a rectangle with rounded right corners.
    // The top-left corner is ⟨x,y⟩.
    function rightRoundedRect(x, y, width, height, radius) {
        return "M" + x + "," + y
            + "l" + (width*0.1) + "," + (height*0.1)
            + "h" + (width*0.9)
            + "a" + radius + "," + radius + " 0 0 1 " + radius + "," + radius
            + "v" + (height - 2 * radius)
            + "a" + radius + "," + radius + " 0 0 1 " + -radius + "," + radius
            + "h" + (radius - width*0.95)
            + "a" + radius + "," + -radius + " 0 0 1 " + -radius + "," + -radius
            + "l" + 0.0 + "," + -height*0.9
            + "z";
    }


    groupInfoTooltips
        .append("path")
        .attr("d", function(d) {
          return rightRoundedRect(30, 30, 630, 380, 15);
        })
        .attr('fill', function(node){
                                var baseColor = colors[node.groupId].split('#')[1];
                                transparency = 200;
                                return '#' +  baseColor + transparency.toString(16);
                                // return colors[node.groupId];
                            })
        .attr('stroke', 'gray')
        .attr('stroke-width', '3.5');
    

    groupInfoTooltips.each(function(originalNode){ 

        var currTooltip = d3.select(groupInfoTooltips._groups[0][originalNode.groupId]);
        if(originalNode.tasks == -1){
            $('#adaptationIssuesText_professor_dash').html($('#adaptationIssuesText_professor_dash').html() + ('<br></br>Could not compute task for group '+node.groupId+'... Maybe no tasks are available?'));
            $('#adaptationIssues_professor_dash').show(500);
            setTimeout(function(){ $('#adaptationIssues_professor_dash').hide(500); }, 10000);
        }
        node = $.extend({}, originalNode); //performs a shallow copy
        node.tasks = originalNode.tasks == -1 ? '<No computed tasks>' : originalNode.tasks;


        //change displayed attributes to be more friendly and easy to read
        characteristics = $.extend({}, originalNode.characteristics);
        dimensions = $.extend({}, originalNode.profile.dimensions);
        // characteristics = node.characteristics;
        // dimensions = node.profile.dimensions;

        cKeys = Object.keys(characteristics);
        dKeys = Object.keys(dimensions);
        for (i=0; i<cKeys.length; i++){
            key = cKeys[i];
            currC = characteristics[key]; 
            characteristics[key] = Number((currC).toFixed(2));
        }

        //also put profile in range [-3,3]
        for (i=0; i<dKeys.length; i++){
            key = dKeys[i];
            currD = dimensions[key]; 
            dimensions[key] = Number((currD*6.0 - 3.0).toFixed(2));
        }


        node["Group ID"] = node.groupId;
        node["Adapted Task"] = node.tasks;

        node["Characteristics"] = {};
        node["Characteristics"]["Ability"] = characteristics.ability;
        node["Characteristics"]["Engagement"] = characteristics.engagement;
        node["Profile"] = dimensions;


        //delete undisplayed attributes
        delete node.profile;
        delete node.characteristics;
        delete node.centerOfMass;

        delete node.groupId;
        delete node.tasks;

        htmlFromJSON(node, currTooltip, 0, 0, 0, 80, 0);
    });


    groupIndicators.on('mouseover', function(d){ d3.select(groupInfoTooltips._groups[0][d.groupId]).style('visibility', 'visible');})
            .on('mouseout', function(d){ d3.select(groupInfoTooltips._groups[0][d.groupId]).style('visibility', 'hidden');});        



    var userInfoTooltips =
        svg.append('g')
            .selectAll('text')
            .data(userNodes)
            .enter()
            .append('g')
            .style('visibility','hidden');

    userInfoTooltips
        .append("path")
        .attr("d", function(d) {
            return rightRoundedRect(10, 10, 630, 300, 15);
        })
        .attr('fill', function(node){
            return generatePlayerColor(node);
        })
        .attr('stroke', 'gray')
        .attr('stroke-width', '3.5');
    
    userInfoTooltips.each(function(originalNode){

        //change displayed attributes to be more friendly and easy to read
        var currTooltip = d3.select(userInfoTooltips._groups[0][originalNode.plotIndex]);

        characteristics = originalNode.userState.characteristics;
        dimensions = originalNode.userState.preferencesEst.dimensions;

        cKeys = Object.keys(characteristics);
        dKeys = Object.keys(dimensions);
        for (i=0; i<cKeys.length; i++){
            key = cKeys[i];
            currC = characteristics[key]; 
            characteristics[key] = Number((currC).toFixed(2));
        }
        // for (i=0; i<dKeys.length; i++){
        //     key = dKeys[i];
        //     currD = dimensions[key]; 
        //     dimensions[key] = Number((currD).toFixed(2));
        // }

        node = {}
        node["Student ID"] = originalNode.userId;

        node["Student Name"] = originalNode.userState.fullName;

        node["Characteristics"] = {};
        node["Characteristics"]["Ability"] = characteristics.ability;
        node["Characteristics"]["Engagement"] = characteristics.engagement;

        // node["Preferences Est"] = dimensions;

        htmlFromJSON(node, currTooltip, 0, 0, 0, 50, 0);
    });


    // nodeElements.on('click', function(d){ 
    //     var elem = d3.select(userInfoTooltips._groups[0][d.plotIndex]); 
    //     d3.select(d).style('stroke-width','3em');
    //     elem.style('visibility') == 'visible'? elem.style('visibility', 'hidden') : elem.style('visibility', 'visible');});

    var mouseX = 0;
    var mouseY = 0;

    nodeElements.on('mouseover', function(d){ d3.select(userInfoTooltips._groups[0][d.plotIndex]).style('visibility', 'visible');})
        .on('mouseout', function(d){ d3.select(userInfoTooltips._groups[0][d.plotIndex]).style('visibility', 'hidden');})
        .on('click', function(d){ 
            // if(d.isForChange){

            // }else{

            // }

            var coordinates= d3.mouse(this);
            mouseX = coordinates[0];
            mouseY = coordinates[1];

            thisElem = d3.select(this);
            thisElem.attr('r', 20)
            
            d3.select(this.parentNode)
                .append("line")
                .attr("x1", thisElem.attr('cx'))
                .attr("y1", thisElem.attr('cy'))
                .attr("x2", mouseX)
                .attr("y2", mouseY)
                .attr("stroke-width", 5)
                .attr("stroke", "black");

        });        

        



    var simulation = d3.forceSimulation();
    var resetSim = function(){
        simulation.nodes(userNodes)
        .force('collide', d3.forceCollide(20)
            .strength(0.2))
        .force('attract', d3.forceAttract()
                    .target((node) => {return [node.centerOfMass.x, node.centerOfMass.y];})
                    .strength(3)
                    );
    }


    resetSim();
    simulation.on('tick', () => {

            console.log(nodeElements);
            nodeElements.selectAll('.line')
                .attr("x2", mouseX)
                .attr("y2", mouseY);

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

var buildScatterInteractionPlot  = function(canvasId, data){
    //originally from https://www.d3-graph-gallery.com/graph/scatter_basic.html

    // set the dimensions and margins of the graph
    var margin = {top: 50, right: 200, bottom: 100, left: 200},
        width = 1150 - margin.left - margin.right,
        height = 850 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    svg = d3.select('#'+canvasId)
      .append('svg')
        .attr('transform', 'scale(0.75)')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .style('background', 'url("../media/images/plots/interactionSpaceBckgrd.png") no-repeat')
        .style('background-size', '70%')
        .style('background-position', 'center')
      .append('g')
        .attr('transform',
              'translate(' + margin.left + ',' + margin.top + ')');
    
    svg.append('g')
        .append('text') 
        .attr('class', 'x label')
        .attr('x', width/2 + 20)
        .attr('y', height + 80)
        .attr('text-anchor', 'middle')
        .style('font-size','35px')
        .text('Self ←     Focus     → Others');

    svg.append('g')
        .append('text') 
        .attr('class', 'y label')
        .attr('text-anchor', 'middle')
        .attr('y', -60)
        .attr('x', -height/2 + 10)
        .style('font-size','35px')
        .attr('transform', 'rotate(-90)')
        .text('Facilitate ←     Challenge     →  Complicate');


    // Add X axis
    var x = d3.scaleLinear()
        .domain([-3, 3])
        .range([ 0, width ]);
        svg.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(x).ticks(5, "f"))
        .style('font-size','30px');


    // Add Y axis
    var y = d3.scaleLinear()
        .domain([-3, 3])
        .range([ height, 0]);
        svg.append('g')
        .call(d3.axisLeft(y).ticks(5, "f"))
        .style('font-size','30px');

    // Add dots
    svg.append('g')
        .selectAll('dot')
        .data(data)
        .enter()
        .append('circle')
        .attr('cx', function (d) { return x(d.focus); } )
        .attr('cy', function (d) { return y(d.challenge); } )
        .attr('r', 10)
        .style('fill', '#50C2E3')
        .style('stroke', 'black')
        .style('stroker-width', '5');

    
}


