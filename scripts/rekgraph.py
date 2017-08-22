"""
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance with the License. 
A copy of the License is located at

    http://aws.amazon.com/asl/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
express or implied. See the License for the specific language governing permissions and limitations under the License.
"""


from IPython.display import IFrame
import json
import uuid
from py2neo import cypher



def graphbacon(noded,linkd):	
    html = """
		<html>
		<head>


		<style>
		.links line {{
		stroke: #aaa;
		}}

		.nodes circle {{
		pointer-events: all;
		stroke: none;
		stroke-width: 40px;
		}}

		</style>
		</head>
		<body>
		<svg width="600" height="400"></svg>
		<div id=\"{id}\"></div>
		<script type="text/javascript" src="../lib/d3.v4.min.js"></script>

		<script type="text/javascript">
		var loc = 20;
		var svg = d3.select("svg"),
		width = +svg.attr("width"),
		height = +svg.attr("height");

		var simulation = d3.forceSimulation()
		.force("link", d3.forceLink().id(function(d) {{ return d.id; }}))
		.force("charge", d3.forceManyBody())
		.force("center", d3.forceCenter(width /2 , height / 2));


		var nodes = {nodedata};
		var links = {linkdata};



		var link = svg.append("g")
		.attr("class", "links")
		.selectAll("line")
		.data(links)
		.enter().append("line");

		var node = svg.append("g")
		.attr("class", "nodes");

		var circles = node
		.selectAll("circle")
		.data(nodes)
		.enter().append("circle")
		.attr("r", 20)
		.attr("fill", function (d){{
		if (d.label == 'Movie')
		return "Aqua"
		else 
		return "Grey"
		}})
		.call(d3.drag()
		.on("start", dragstarted)
		.on("drag", dragged)
		.on("end", dragended));


		var text = node
		.selectAll("text")
		.data(nodes)
		.enter().append("text")
		.attr("text-anchor","middle")
		.text(function(d){{
		return d.title
		}});




		simulation
		.nodes(nodes)
		.on("tick", ticked);

		simulation.force("link")
		.links(links);

		function ticked() {{
		link
		.attr("x1", function(d) {{ return d.source.x; }})
		.attr("y1", function(d) {{ return d.source.y; }})
		.attr("x2", function(d) {{ return d.target.x; }})
		.attr("y2", function(d) {{ return d.target.y; }});


		circles
		.attr("cx", function(d) {{ return d.x; }})
		.attr("cy", function(d) {{ return d.y; }})
		// .selectAll("text")
		// .attr("x", function(d) {{return d.x}})
		// .attr("y", function(d) {{return d.y}});

		text
		.attr("x", function(d) {{return d.x}})
		.attr("y", function(d) {{return d.y}})

		}};

		function dragstarted(d) {{
		if (!d3.event.active) simulation.alphaTarget(0.01).restart();
		d.fx = d.x;
		d.fy = d.y;
		}}

		function dragged(d) {{
		d.fx = d3.event.x;
		d.fy = d3.event.y;
		}}

		function dragended(d) {{
		if (!d3.event.active) simulation.alphaTarget(0);
		d.fx = null;
		d.fy = null;
		}}

		function idIndex(a,id) {{
		for (var i=0;i<a.length;i++) {{
		if (a[i].id == id) return id;
		}}
		return null;
		}}

		</script>
		</body>
		</html>
	"""
    
    unique_id = str(uuid.uuid4())

    html = html.format(id=unique_id,nodedata=json.dumps(noded, indent=1),linkdata=json.dumps(linkd, indent=1))
    filename = "figure/relationships-{}.html".format(unique_id)
    file = open(filename, "w")
    file.write(html)
    file.close()
    return IFrame(filename, width="600%", height="400")

def rekrelationships(graph, actor1, actor2):
	query = """
	MATCH p=shortestPath((bacon:Person {{name:\"{actor1}\"}})-[*]-(meg:Person {{name:\"{actor2}\"}}) ) RETURN p
	"""
	query = query.format(actor1=actor1,actor2=actor2)
	#result = graph.run(query)
	result = graph.cypher.execute(query)
	subg = result.to_subgraph()
	relRes= subg.relationships
	nodesRes = subg.nodes

	nodes = []
	links = []

	for node in nodesRes:
		labelList = node.labels
		label = l = labelList.pop()
		if l =='Movie' :
			title = node.properties.get("title","")
		else:
			title = node.properties.get("name","")
		id = node.properties.get("id","")
		nodes.append({"title":title,"label":label,"id":id})

		for rel in relRes:
			links.append({"source":rel.start_node.properties.get("id",""),"target":rel.end_node.properties.get("id",""),"type":rel.type})

	return graphbacon(nodes,links)



