function buildInteractionsProfilePlot(data){
	var data = [
        {"x": -123, "y": 63, "c": "#50C2E3", "name": "A"},
        {"x": 71, "y": 0, "c": "#50C2E3", "name": "B"},
        {"x": 3845, "y": 77, "c": "#50C2E3", "name": "C"},
        {"x": 3176, "y": 90, "c": "#50C2E3", "name": "D"},
        {"x": -17, "y": 56, "c": "#50C2E3", "name": "D"},
        {"x": 1357, "y": 58, "c": "#50C2E3", "name": "E"},
        {"x": 7684, "y": 75, "c": "#50C2E3", "name": "F"}
    ];

    var width = 500;
    var height = 500;

    var margin = {
        top: 40,
        right: 40,
        bottom: 40,
        left: 40
    };

    var x = d3.scale.linear().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);

    var minX = _(data).orderBy('x').first().x;
    var maxX = _(data).orderBy('x').last().x;

    x.domain([minX - 500, maxX + 500]);
    y.domain([0, 100]);

    var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

    var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

    var svg = $("#interactionsProfilePlot")
            .select("#d3")
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
                return x(d.x);
            })
            .attr("cy", function (d) {
                return y(d.y);
            })
            .style("fill", function (d) {
                return d.c;
            });
            gdots.append("text").text(function(d){
            	return d.name;
            })
            .attr("x", function (d) {
                return x(d.x);
            })
            .attr("y", function (d) {
                return y(d.y);
            });
}
