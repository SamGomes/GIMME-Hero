var buildInteractionsProfilePlot = function(data){
	// var data = [
 //        {"x": 0.5, "y": 0.7, "c": "#50C2E3", "name": "A"},
 //        {"x": 0, "y": 0.25, "c": "#50C2E3", "name": "B"},
 //        {"x": 0.45, "y": 0.77, "c": "#50C2E3", "name": "C"},
 //        {"x": 0.6, "y": 0.90, "c": "#50C2E3", "name": "D"},
 //        {"x": -17, "y": 0.56, "c": "#50C2E3", "name": "D"},
 //        {"x": 0.57, "y": 0.58, "c": "#50C2E3", "name": "E"},
 //        {"x": 0.84, "y": 0.75, "c": "#50C2E3", "name": "F"}
 //    ];
    console.log(data);
    
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

    var svg = d3.select("#interactionsProfilePlot")
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
              

  var gdots =  svg.selectAll("g.dot")
            .data(data)
            .enter().append('g');
            
            gdots.append("circle")
            .attr("class", "dot")
            .attr("r", 10)
            .attr("cx", function (d) {
                return x(d.K_i);
            })
            .attr("cy", function (d) {
                return y(d.K_cp);
            })
            .style("fill", function (d) {
                return d.c;
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
