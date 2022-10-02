//source: https://www.geeksforgeeks.org/best-way-to-make-a-d3-js-visualization-layout-responsive/
var responsivefy = function(svg, targetWidthClamp, leftPaddingRatio) {
    // Container is the DOM element, svg is appended.
    // Then we measure the container and find its
    // aspect ratio.
    const container = d3.select(svg.node().parentNode),
        width = parseInt(svg.style('width'), 10),
        height = parseInt(svg.style('height'), 10),
        aspect = width / height;
         
    // Add viewBox attribute to set the value to initial size
    // add preserveAspectRatio attribute to specify how to scale
    // and call resize so that svg resizes on page load
    svg.attr('viewBox', `0 0 ${width} ${height}`).
    attr('preserveAspectRatio', 'xMinYMid');
    svg.call(resize);
     
    d3.select(window).on('resize.' + container.attr('id'), resize);

    function resize() {
        var targetWidth = parseInt(container.style('width'));
        svg.attr('transform', 'translate('+targetWidth*leftPaddingRatio+','+0+')');
        if(targetWidth > targetWidthClamp){
            targetWidth = targetWidthClamp;
        }

        // console.log(targetWidth);
        svg.attr('width', targetWidth);
        svg.attr('height', Math.round(targetWidth / aspect));
        
    }
}









groupsPlotNodeElements = undefined;
groupsPlotScaleType = undefined;

// used to correctly generate user colors
var abMax = 0;
var engMax = 0; 

var abMin = Infinity;
var engMin = Infinity; 

var generateGroupColor = function(profile) {
    var focus = profile.dimensions.Focus;
    var challenge = profile.dimensions.Challenge;

    if (focus >= 0 && focus < 0.33){
        if (challenge >= 0 && challenge < 0.33){
            return '#dd6c02'
        }
        else if (challenge >= 0.33 && challenge < 0.66){
            return '#ddb502'
        }
        else if (challenge >= 0.66 && challenge <= 1.0){
            return '#b5dd02'
        }
    }
    else if (focus >= 0.33 && focus < 0.66){
        if (challenge >= 0 && challenge < 0.33){
            return '#dd1402'
        }
        else if (challenge >= 0.33 && challenge < 0.66){
            return '#a3a1a1'
        }
        else if (challenge >= 0.66 && challenge <= 1.0){
            return '#19c151'
        }
    }
    else if (focus >= 0.66 && focus <= 1.0){
        if (challenge >= 0 && challenge < 0.33){
            return '#89150b'
        }
        else if (challenge >= 0.33 && challenge < 0.66){
            return '#cd7dce'
        }
        else if (challenge >= 0.66 && challenge <= 1.0){
            return '#7724d6'
        }
    }
    return '#a3a1a1'
}



var generatePlayerColor = function(node){
    var userChar = node.userState.characteristics;
    
    //groupsPlotScaleType == 'absolute'
    var abRatio = userChar.ability;
    var engRatio = userChar.engagement;
    if(groupsPlotScaleType =='relative'){
        abRatio = abMax > 0.0? ((userChar.ability - abMin) / (abMax - abMin)): 0.0;
        engRatio = engMax > 0.0? ((userChar.engagement - engMin) / (engMax - engMin)): 0.0;
    }

    ratio = (abRatio + engRatio) / 2.0;

    return d3.scaleLinear()
    .domain([0.0, 0.5, 1.0])
    .range(['#FF0000', '#FFFF00', '#00FF00'])(ratio)
}
    
var updateGroupsPlotNodeColors = function(canvasId, newScaleType){
    groupsPlotScaleType = newScaleType;
    
    var nodes = groupsPlotNodeElements._groups[0];
    for(var i=0; i<nodes.length; i++){
        d3.select(nodes[i])
            .transition()
            .duration(1000)
            .attr('fill', function(){
                    return nodes[i].isForStudent? colors[0]: generatePlayerColor(nodes[i].__data__);
                });
    }
    
}
    

var buildGroupsPlot = function(isForStudent, canvasId, data, userStates, scaleType){
    abMax = 0;
    engMax = 0; 

    abMin = Infinity;
    engMin = Infinity; 
    
    groupsPlotScaleType = scaleType;
    
    $('#adaptationIssues_professor_dash').hide();
    $('#adaptationIssuesText_professor_dash').html('');

    // from http://bl.ocks.org/mbostock/7555321
    var wrap = function (text, width) {
        text.each(function () {
            var text = d3.select(this),
                words = text.text().split(/\s+/).reverse(),
                word,
                line = [],
                lineNumber = 0,
                lineHeight = 1.1, // ems
                x = text.attr('x'),
                y = text.attr('y'),
                dy = 0, //parseFloat(text.attr('dy')),
                tspan = text.text(null)
                            .append('tspan')
                            .attr('x', x)
                            .attr('y', y)
                            .attr('dy', dy + 'em');
            while (word = words.pop()) {
                line.push(word);
                tspan.text(line.join(' '));
                if (tspan.node().getComputedTextLength() > width) {
                    line.pop();
                    tspan.text(line.join(' '));
                    line = [word];
                    tspan = text.append('tspan')
                                .attr('x', x)
                                .attr('y', y)
                                .attr('dy', ++lineNumber * lineHeight + dy + 'em')
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
        return '#' + padZero(r) + padZero(g) + padZero(b);
    }

    //source: https://campushippo.com/lessons/how-to-convert-rgb-colors-to-hexadecimal-with-javascript-78219fdb
    var rgbToHex = function (rgb) { 
        var hex = Number(rgb).toString(16);
        if (hex.length < 2) {
            hex = "0" + hex;
        }
        return hex;
    };
    var fullColorHex = function(r,g,b) {   
        var red = rgbToHex(r);
        var green = rgbToHex(g);
        var blue = rgbToHex(b);
        return red+green+blue;
    };

    var padZero = function(str, len) {
        len = len || 2;
        var zeros = new Array(len).join('0');
        return (zeros + str).slice(-len);
    }

    var sqrDistBetweenVectors = function(vec1, vec2){
        return (Math.pow(vec1.ability - vec2.ability, 2) + Math.pow(vec1.engagement - vec2.engagement, 2));
    }

    svg = d3.select('#'+canvasId).append('svg');

    var canvas = svg;
    var canvasContainer = canvas.node().parentNode;
    width = canvasContainer.getBoundingClientRect().width;
 
    if(isForStudent){
        aspect = 2.5 / 1.0;
    }else{
        aspect = 2.5/ 1.5;
    }
   
    height = width/ aspect;
    
    canvas.attr('width', width);
    canvas.attr('height', height);
    

    var userNodes = [];
    var groupIndicatorNodes = [];
    var colors = [];

    var currPlotIndex = 0;

    svg.call(responsivefy, 5000, 0);

    for (i=0; i<data.groups.length; i++){
        var group = data.groups[i];
        var groupCenterOfMass = {'x': 100 + Math.random()*(width*0.8), 'y': 10 + Math.random()*(height*0.8)};
        
        if(isForStudent){
            groupIndicatorNodes.push({'groupId': i, 'tasks': tasks, 'centerOfMass': groupCenterOfMass});
            
            for(var j=0;j<group.length; j++){
                var userId = group[j];
                userState = userStates[userId];
                userNodes.push({'plotIndex': currPlotIndex++, 'userId': userId, 'userState': unformattedStringToObj(userState), 'groupId': i, 'centerOfMass': groupCenterOfMass});
            }
            colors[i] = "#778caa";
        }else{
            var avgCharacteristics = $.extend({}, data.avgCharacteristics[i]);
            delete avgCharacteristics.profile;
            var profile = data.profiles[i];
            var tasks = data.tasks[i];

            groupIndicatorNodes.push({'groupId': i, 'characteristics': avgCharacteristics, 'profile': profile, 'tasks': tasks, 'centerOfMass': groupCenterOfMass});
            
            for(var j=0;j<group.length; j++){
                var userId = group[j];
                userState = userStates[userId];
                userNodes.push({'plotIndex': currPlotIndex++, 'userId': userId, 'userState': unformattedStringToObj(userState), 'groupId': i, 'groupCharacteristics': avgCharacteristics, 'centerOfMass': groupCenterOfMass});
            }
            colors[i] = generateGroupColor(profile);
        }

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
            .attr('stroke-dasharray', '1%')
            .attr('stroke', function(node){
                return colors[node.groupId];
            })
            .attr('stroke-width', '0.25%') 
            .attr('fill', 'transparent');
           



    var clamp = function(num, min, max) {
      return num <= min ? min : num >= max ? max : num;
    }

    
    
    
    var nodeElements =
        svg.append('g')
            .selectAll('circle')
            .data(userNodes)
            .enter()
            .append('circle')
            .attr('r', '1%')
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
                    return isForStudent? colors[0]: generatePlayerColor(node);
                })
            .attr('stroke', function(node){
                    return isForStudent? (data.myStudentId == node.userId? "red": colors[0]): colors[node.groupId];
                })
            .attr('stroke-width', '0.3%');
         
    groupsPlotNodeElements = nodeElements;
            
    var nodeTextElements = 
        svg.append('g')
        .selectAll('text')
        .data(userNodes)
        .enter()
        .append('text')
        .attr('dy', 7)
//         .attr('class', 'fancy-plot-text')
        .attr('font-family', 'Calibri,sans-serif')
        .attr('text-anchor', 'middle')
        .style("stroke-width", 0.5)
        .style("stroke", "black")
        .style("fill", "white")
        .text('');


    var groupInfoTooltips =
        svg.append('g')
            .selectAll('text')
            .data(groupIndicatorNodes)
            .enter()
            .append('g')
            .style('visibility','hidden');


    var getJSONLength = function(json){
        if(typeof json == 'string'|| json == undefined){
            return 0;
        }
        var keys = Object.keys(json);
        var totalLength = keys.length;
        for(var i=0; i < keys.length; i++){
            if(currKey=='0'){
                continue;
            }
            var currKey = keys[i];
            var currJson = json[currKey];
            totalLength += getJSONLength(currJson);
        }
        return totalLength;
    }

    var htmlFromJSON = function(json, fatherElem, currX, currY, paddingX, paddingY, j){
        
        if(typeof json == 'string' || typeof json == 'number' || json == undefined){
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
            
            if(currKey=='0'){
                continue;
            }

            if(typeof currJson != 'string' && typeof currJson != 'number'){
                currKey+=' ↴';
            }

            fatherElem
            .append('text')
            .attr('x', x)
            .attr('y', y + 10)
            .attr('font-size', 18)
            .attr('font-family', 'Calibri,sans-serif')
            .attr('color', function(node){ return isForStudent? invertColor(colors[0], true): invertColor(colors[node.groupId], true); })
            .call(wrap, 150)
            .text(currKey);

            if(typeof currJson == 'string' || typeof currJson == 'number'){

                fatherElem
                .append('rect')
                .attr('x', x + 140)
                .attr('y', y - 5)
                .attr('width', 250)
                .attr('height', 20)
                .attr('fill', function(node){ return 'white'; })
                .attr('stroke', 'black');

                fatherElem
                .append('text')
                .attr('x', x + 145)
                .attr('y', y + 10)
                .attr('font-size', 15)
                .attr('font-family', 'Calibri,sans-serif')
                .attr('color', function(node){ return 'black'; })
                .call(wrap, 150)
                .text(currJson);
            }

            htmlFromJSON(currJson, fatherElem, x, y, paddingX, paddingY, ++j);

            y += 35*(1+getJSONLength(currJson));
        }

    };



    
    
    var mouseX = 0;
    var mouseY = 0;

    var studentForChange = undefined;
    var groupForChange = undefined;

    var resetChangeState = function(){
        nodeElements.attr('r', '1%');

        studentForChange = undefined;
        groupForChange = undefined;

        d3.select('#'+canvasId).select('line').remove();
    }
    
    
    var canNodeBeExpanded = function(selection, node){
        return (node.groupId == selection.groupId || (studentForChange != undefined && node.userId == studentForChange.userId))
    };
    
//     var mouseOverCallbacks = 0;
   
    var expandNodeViz = function(d){
//         if(mouseOverCallbacks == 0){
//             simulation.alpha(0.1).restart();
//         }
//         mouseOverCallbacks++;
        
        $(groupIndicators._groups[0])
            .each(function(i,e){
                d3.select(e).attr('opacity', node => canNodeBeExpanded(d, node)? '1.0': '0.2');
            });
        $(nodeElements._groups[0])
            .each(function(i,e){
                d3.select(e).attr('r', node => canNodeBeExpanded(d, node)? '1.5%': '1%');
                d3.select(e).attr('opacity', node => canNodeBeExpanded(d, node)? '1.0': '0.2');
            });
        $(nodeTextElements._groups[0])
            .each(function(i,e){
                d3.select(e).text(node => {
                    if(canNodeBeExpanded(d, node)){
                        var fullName = node.userState.fullName.split(' ');
                        var nameInitials = '';
                        if(fullName.length == 1){
                            nameInitials = fullName[0][0];
                        }else{
                            nameInitials = fullName[0][0] + fullName[fullName.length - 1][0];
                        }
                        return nameInitials;
                    }
                    else{
                        return '';
                    }
                    
                });
            });
    };
    
    var contractNodeViz = function(d){
        if(studentForChange!=undefined){
            return;
        }
        
        
        $(groupIndicators._groups[0])
            .each(function(i,e){
                d3.select(e).attr('opacity', '1.0');
            });
            
        $(nodeElements._groups[0])
            .each(function(i,e){
                d3.select(e).attr('r', '1%');
                d3.select(e).attr('opacity', '1.0');
            });
            
        $(nodeTextElements._groups[0])
            .each(function(i,e){
                d3.select(e).text('');
            });
    };

    
    
    
    
    
    if(!isForStudent){
        groupIndicators.on('mouseover', function(d){
            d3.select(groupInfoTooltips._groups[0][d.groupId]).style('visibility', 'visible');
            expandNodeViz(d);
            
            if(studentForChange != undefined){

                thisElem = d3.select(this);
                
                groupForChange = d;

                d3.select('#' + canvasId).select('line')
                    .attr('x2', thisElem.attr('cx'))
                    .attr('y2', thisElem.attr('cy'));
                
               
            }
            d3.event.stopPropagation();
            
        });
        groupIndicators.on('mouseout', function(d){
            d3.select(groupInfoTooltips._groups[0][d.groupId]).style('visibility', 'hidden');
            contractNodeViz(d);
            d3.event.stopPropagation();
        });
        
        d3.select('#'+canvasId).on('click',function(d){
            resetChangeState();
            contractNodeViz(d);
            d3.event.stopPropagation();
        });

    }


    

    // define arrow points paths
    var defs = svg.append('defs');

    defs.append('marker')
        .attr('id', 'arrow')
        .attr('viewBox', '0 -10 20 20')
        .attr('refX', 10)
        .attr('refY', 0)
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('orient', 'auto')
        .attr('stroke', 'black')
        .attr('fill', 'black')

        .append('path')
            .attr('d', 'M0,-5 L10,0 L0,5')
            .attr('class', 'arrowHead');





    // only professors can perform changes in groups
    if(!isForStudent){
        
        var nodeClickCallback = function(d, i){
            resetChangeState();
            
            var elem = nodeElements._groups[0][i];
            
            var coordinates = d3.mouse(elem);
            var mouseX = coordinates[0];
            var mouseY = coordinates[1];

            var thisElem = d3.select(elem);
            thisElem.attr('r', '2%');
            studentForChange = d;
            
            d3.select(elem.parentNode.parentNode)

                .append('line')
                .attr('class', 'arrow')
//                 .attr('marker-start', 'url(#arrowFront)')
                .attr('marker-end', 'url(#arrow)')
                .attr('x1', thisElem.attr('cx'))
                .attr('y1', thisElem.attr('cy'))
                .attr('x2', mouseX)
                .attr('y2', mouseY)
                .attr('stroke-width', '0.5%')
                .attr('stroke-dasharray', '2%')
                .attr('stroke', 'black');
            
            d3.event.stopPropagation();
        }
        
        nodeTextElements.on('click', function(d, i){
            nodeClickCallback(d, i);
        });
        nodeElements.on('click', function(d){ 
            nodeClickCallback(d, i);
        });
    }

    
    

    
    
    
    
    
    // adapted from: https://stackoverflow.com/questions/12115691/svg-d3-js-rounded-corner-on-one-corner-of-a-rectangle
    // Returns path data for a rectangle with rounded right corners.
    // The top-left corner is ⟨x,y⟩.
    function rightRoundedRect(x, y, width, height, radius) {
        return 'M' + x + ',' + y
            + 'l' + (width*0.1) + ',' + (height*0.1)
            + 'h' + (width*0.9)
            + 'a' + radius + ',' + radius + ' 0 0 1 ' + radius + ',' + radius
            + 'v' + (height - 2 * radius)
            + 'a' + radius + ',' + radius + ' 0 0 1 ' + -radius + ',' + radius
            + 'h' + (radius - width*0.95)
            + 'a' + radius + ',' + -radius + ' 0 0 1 ' + -radius + ',' + -radius
            + 'l' + 0.0 + ',' + -height*0.9
            + 'z';
    }


    groupInfoTooltips
        .append('path')
        .attr('d', function(d) {
          return rightRoundedRect(15, 15, 600, 280, 7);
        })
        .attr('fill', function(node){
                                var baseColor = colors[node.groupId].split('#')[1];
                                transparency = 200;
                                return '#' +  baseColor + transparency.toString(16);
                            })
        .attr('stroke', 'gray')
        .attr('stroke-width', '0.15%')
        .attr('z-index','7000');
    

    var warningMsg = 'Could not compute task for group(s) ';
    var displayWarn = false;
    groupInfoTooltips.each(function(originalNode){ 

        var currTooltip = d3.select(groupInfoTooltips._groups[0][originalNode.groupId]);
        if(originalNode.tasks == -1){
            displayWarn = true;
            warningMsg += originalNode.groupId + ',';
        }
        node = $.extend({}, originalNode); //performs a shallow copy
        node.tasks = originalNode.tasks == -1 ? '<No computed tasks>' : originalNode.tasks;

        node['Group ID'] = node.groupId;


        if(!isForStudent){
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

            node['Characteristics'] = {};
            node['Characteristics']['Ability'] = characteristics.ability;
            node['Characteristics']['Engagement'] = characteristics.engagement;
            node['Profile'] = dimensions;

            //delete undisplayed attributes
            delete node.profile;
            delete node.characteristics;
        }
        delete node.tasks;
        delete node.centerOfMass;
        delete node.groupId;

        htmlFromJSON(node, currTooltip, 0, 0, 0, 40, 0);
    });
    if(displayWarn){
        generatePlotWarningMessage(
            warningMsg.slice(0, -2) + ' and ' + warningMsg.slice(-2, -1)  + '... Maybe no tasks are selected?',
            3000
        );
    }
    
    
    
    
    
    
    var userInfoTooltips =
        svg.append('g')
            .selectAll('text')
            .data(userNodes)
            .enter()
            .append('g')
            .style('visibility','hidden')
            .attr('z-index','7000');

    userInfoTooltips
        .append('path')
        .attr('d', function(d) {
            if(!isForStudent){
                return rightRoundedRect(5, 5, 600, 280, 7);
//                 return rightRoundedRect(5, 5, 600, 320, 7);
            }else{
                return rightRoundedRect(5, 5, 500, 200, 7);
            }
        })
        .attr('fill', function(node){
            var baseColor = {}
            transparency = 200;
            if(isForStudent){
                baseColor = colors[0];
                return baseColor + transparency.toString(16);
            }else{
                var playerColor = generatePlayerColor(node).split(/,|\(|\)/);
                baseColor = fullColorHex(playerColor[1], playerColor[2], playerColor[3]);
                return '#' +  baseColor + transparency.toString(16);
            }
        })
        .attr('stroke', 'gray')
        .attr('stroke-width', '0.15%');
    
    userInfoTooltips.each(function(originalNode){

        //change displayed attributes to be more friendly and easy to read
        var currTooltip = d3.select(userInfoTooltips._groups[0][originalNode.plotIndex]);

        node = {}
        node['Student ID'] = originalNode.userId;
        node['Student Name'] = originalNode.userState.fullName;
        node['Email'] = originalNode.userState.email;

        if(!isForStudent){
            characteristics = originalNode.userState.characteristics;
            // dimensions = originalNode.userState.preferencesEst.dimensions;

            cKeys = Object.keys(characteristics);
            dKeys = Object.keys(dimensions);
            for (i=0; i<cKeys.length; i++){
                key = cKeys[i];
                currC = characteristics[key]; 
                characteristics[key] = Number((currC).toFixed(2));
            }

            node['Characteristics'] = {};
            node['Characteristics']['Ability'] = characteristics.ability;
            node['Characteristics']['Engagement'] = characteristics.engagement;
            node['(External) Grade'] = originalNode.userState.grade;
        }

        htmlFromJSON(node, currTooltip, 0, 0, 0, 50, 0);
    });

    
    var nodeMouseOverCallback = function(i){
        node = userNodes[i];
        expandNodeViz(node);
        d3.select(userInfoTooltips._groups[0][node.plotIndex]).style('visibility', 'visible');
        d3.event.stopPropagation();
    }
    var nodeMouseOutCallback = function(i){
        node = userNodes[i];
        contractNodeViz(node);
        d3.select(userInfoTooltips._groups[0][node.plotIndex]).style('visibility', 'hidden');
        d3.event.stopPropagation();
    }
    
    nodeTextElements.on('mouseover', function(_, i){
        nodeMouseOverCallback(i);
    });
    nodeElements.on('mouseover', function(_, i){
        nodeMouseOverCallback(i);
    });
    nodeTextElements.on('mouseout', function(_, i){ 
        nodeMouseOutCallback(i);
    });
    nodeElements.on('mouseout', function(_, i){
        nodeMouseOutCallback(i);
    });


    

    var simulation = d3.forceSimulation();
    var resetSim = function(){
        simulation.nodes(userNodes)
        .force('collide', d3.forceCollide()
            .radius(width*0.015)
//             .radius((_, i) => {
//                 return (d3.select(nodeElements._groups[0][i]).attr('r') == '1%')? width*0.015: width*0.03;
//             })
            .strength(0.1)
        )
        .force('attract', d3.forceAttract()
            .target((node) => {return [node.centerOfMass.x, node.centerOfMass.y];})
            .strength(5)
        );
    }


    resetSim();
    simulation.on('tick', () => {
            resetSim();
            
//             console.log(simulation.alpha());

            nodeElements
                .attr('cx', node => node.x)
                .attr('cy', node => node.y);

            nodeTextElements
                .attr('x', node => node.x)
                .attr('y', node => node.y);
                
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
                    sqrtMR = Math.sqrt(maxRadius);
                    return 2*sqrtMR; 
                });
                

            groupInfoTooltips
                .attr('transform', node => 'translate('+node.centerOfMass.x+' '+node.centerOfMass.y+')');

            userInfoTooltips
                .attr('transform', node => 'translate('+node.x+' '+node.y+')');

        });



    const dragDrop = d3.drag()
        .on('start', node => {
            if (!d3.event.active)
                simulation.alphaTarget(0.1).restart();

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
            
            if(studentForChange != undefined){
                if(studentForChange.groupId != node.groupId){
                    //perform change
                    //deploy confirmation box?
                    $.ajax({
                        type: 'POST',
                        url: '/manuallyChangeStudentGroup/',
                        data: {'student': studentForChange, 'group': groupForChange},
                        complete: 
                        function(response){
                            if(response.responseText == 'error'){
                                generatePlotErrorMessage(
                                    'Adaptation Error! Group size violation. Maintaining old state...',
                                    3000
                                );
                            }
                        }
                    });
                }
                resetChangeState();
            }
        })
        
        .on('drag', node => {
            if (!d3.event.active)
                simulation.alphaTarget(0.1).restart();
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
            if (!d3.event.active)
                simulation.alphaTarget(0);
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

    var canvas = d3.select('#'+canvasId);
    var width = 500;
    var height = 500;

    
    // append the svg object to the body of the page
    svg = canvas
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .style('background', 'url("../media/images/plots/interactionSpaceBckgrd.png") no-repeat')
        .style('background-size', '100%')
        .style('background-position', 'center')
        .attr('display', 'block')
        .attr('margin', 'auto')
        .call(responsivefy, 500, 0.25);
    
    svg.append('g')
        .append('text') 
        .attr('class', 'x label')
        .attr('x', width* 0.5)
        .attr('y', height* 0.94)
        .attr('text-anchor', 'middle')
        .style('font-size', width*0.05 +'px')
        .text(' Self      ← Focus →     Others');

    svg.append('g')
        .append('text') 
        .attr('class', 'y label')
        .attr('text-anchor', 'middle')
        .attr('x', -width* 0.48)
        .attr('y', height* 0.04)
        .style('font-size', height*0.05 +'px')
        .attr('transform', 'rotate(-90)')
        .text('Complicate ← Challenge → Facilitate ');


    // Add X axis
    var x = d3.scaleLinear()
        .domain([-3, 3])
        .range([35, width-30]);


    // Add Y axis
    var y = d3.scaleLinear()
        .domain([-3, 3])
        .range([height-65, 30]);

    // Add dots
    svg.append('g')
        .selectAll('dot')
        .data(data)
        .enter()
        .append('circle')
        .attr('cx', function (d) { return x(d.focus); } )
        .attr('cy', function (d) { return y(d.challenge); } )
        .attr('r', height * 0.015)
        .style('fill', '#5afcf4')
        .style('stroke', 'black')
        .style('stroke-width', '1%');

    
}


var buildStatePlot = function(canvasId, data, minValue=0, maxValue=undefined, step=undefined){

    var canvas = d3.select('#'+canvasId);

    var width = 1000;
    var height = 150;

    var margin = {
        top: height * 0.1,
        right: width * 0.1,
        bottom: height * 0.1,
        left: width * 0.3
    };

    var svg = canvas.append('svg');

    svg.attr('width', width + margin.left + margin.right)
        .attr('display', 'block')
        .attr('margin', 'auto')
        .attr('height', height + margin.top + margin.bottom + 200)
        .call(responsivefy, 1000, 0.15);


    if(maxValue == undefined){
        for(var i=0; i < data.length; i++){
            var currValue = parseFloat(data[i].value);
            if(maxValue == undefined || currValue > maxValue){
                maxValue = currValue;
            }
        }
        maxValue += 0.1*maxValue;
    }

    var x = d3.scaleLinear()
        .range([margin.left, width])
        .domain([minValue, maxValue]);

    var y = d3.scaleBand()
        .range([margin.bottom, height])
        .domain(data.map(function(d) {
            return d.name;
        }));

    var xAxis = d3.axisBottom(x);
        
    xAxis.tickSize(-width);
    if(step != undefined){
        xAxis.ticks(maxValue - minValue / step);
    }

    var yAxis = d3.axisLeft(y)
        .tickSize(0);


    var bars = svg.selectAll('.bar')
        .data(data)
        .enter()
        .append('g');


    bars.append('rect')
        .attr('class', 'bar')
        .attr('y', function (d) {
            return y(d.name) + y.bandwidth()*3/16;
        })
        .attr('height', y.bandwidth()*1/2)
        .attr('x', margin.left)
        .attr('width', function (d) {
            return  x(d.value) - margin.left;
        })
        .attr('fill', '#50C2E3');

    var gy = svg.append('g')
                .attr('class', 'y axis label')
                .call(yAxis) 
                .attr('transform', 'translate(' + margin.left + ',0)')
                    .style('font-size','30px');

    gy.selectAll("text")
        .attr("transform", "translate(-35,0)");

    
    var gx = svg.append('g')
                .attr('class', 'x axis')
                .call(xAxis)
                .attr('transform', 'translate(0,' + height + ')')
                .style('font-size','25px');
    
    gx.selectAll('.tick line')
        .attr('opacity', 0.5)
     
    gx.selectAll("text")
        .attr("transform", "rotate(70), translate(35,-15)");
        
    
    svg.append('g')
        .call(xAxis)
        .selectAll("text")
            .attr("visibility","hidden");
}


var buildPieChart = function(canvasId, numWeeks, currWeek = 0, changeSimulationDisplayCallback){

    
    // set the dimensions and margins of the graph
    var width = 300
    height = 600;
    
    var margin = {
        top: height * 0.1,
        right: width * 0.1,
        bottom: height * 0.1,
        left: width * 0.1
    };
    
    // var svg = canvas.append('svg');
    
    // // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
    var radius = Math.min(width, height) / 2 
    
    // svg.attr('width', width + margin.left + margin.right)
    //     .attr('display', 'block')
    //     .attr('margin', 'auto')
    //     .attr('height', height + margin.top + margin.bottom + 200)
    //     .call(responsivefy, 1000, 0.15);
    
    var svg = d3.select('#'+canvasId)
        .append('svg');

    svg.attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.bottom + margin.top)
        .attr('display', 'block')
        .attr('margin', 'auto')
        .call(responsivefy, 300, 0.65);
    
    // Create dummy data
    var weekValue = 100 / numWeeks;
    var data = {};
    for(i=0; i<numWeeks; i++)
        data[i] = weekValue;

    var leftXPosition = -document.getElementById("storylineLog_professor_dash").parentElement.clientWidth / 2;

    var positionArray = [[0,-70],[0,0],[0,70],[leftXPosition,70],[leftXPosition,0],[leftXPosition,-70]];
    var currSelectedWeek = currWeek;
    $("#storylineLog_professor_dash").css({'transform': 'translate(' + positionArray[currSelectedWeek][0] + 'px,' + positionArray[currSelectedWeek][1] + 'px)'});


    // Compute the position of each group on the pie:
    var pie = d3.pie()
    .value(function(d) {return d.value; })
    var data_ready = pie(d3.entries(data))

    var arcGenerator = d3.arc()
    .innerRadius(radius*0.3)
    .outerRadius(radius);


    var g = svg.append('g');    
    g.style("transform", "translate(" + width / 2 + "px," + height / 2 + "px)");
    
    // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
    g
    .selectAll('mySlices')
    .data(data_ready)
    .enter()
    .append('path')
    .attr('d', arcGenerator)
    .attr('fill', 
        function(d){
            week = d.data.key;
            if (week < currWeek)
                return '#91f4ff';
            else if (week == currWeek || week == currSelectedWeek)
                return '#1ce9ff';
            return '#808080';
        })
    .attr("stroke", "white")
    .style("stroke-width", "10px")
    .style("opacity", 0.7)
    .on("mouseover", function (d) {
        currSelectedWeek = d.data.key;
        changeSimulationDisplayCallback(currWeek, currSelectedWeek);
    })
    .on("mouseout", function (d) {
        currSelectedWeek = currWeek;
        changeSimulationDisplayCallback(currWeek, currSelectedWeek);

    })

}

