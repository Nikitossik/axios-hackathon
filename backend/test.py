import osmnx as ox

# Define the place name for which you want to download the street network
place_name = "Cracow, Poland"

# Download the street network graph
# You can change network_type to 'walk', 'bike', or 'all' depending on your needs
print(f"Downloading graph for {place_name}...")
G = ox.graph_from_place(place_name, network_type='drive')

# Print some basic information about the graph
print(f"Graph imported with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")


def value_preview(value, max_len=120):
	text = repr(value)
	if len(text) > max_len:
		return text[: max_len - 3] + "..."
	return text


def print_graph_structure(graph):
	print("\n" + "=" * 80)
	print("GRAPH STRUCTURE")
	print("=" * 80)

	print("\n[GROUP] graph (global metadata)")
	if graph.graph:
		for key in sorted(graph.graph.keys()):
			value = graph.graph[key]
			print(f"- {key}: type={type(value).__name__}, value={value_preview(value)}")
	else:
		print("- No global graph attributes")

	print("\n[GROUP] nodes")
	nodes_data = list(graph.nodes(data=True))
	print(f"- Total nodes: {len(nodes_data)}")

	node_fields = sorted({field for _, attrs in nodes_data for field in attrs.keys()})
	print(f"- Node fields ({len(node_fields)}):")
	for field in node_fields:
		example = next((attrs[field] for _, attrs in nodes_data if field in attrs), None)
		print(f"  - {field}: type={type(example).__name__}, example={value_preview(example)}")

	print("\n- Sample nodes (first 3):")
	for node_id, attrs in nodes_data[:3]:
		print(f"  - node_id={node_id}")
		for key in sorted(attrs.keys()):
			print(f"      {key}: {value_preview(attrs[key])}")

	print("\n[GROUP] edges")
	edges_data = list(graph.edges(keys=True, data=True))
	print(f"- Total edges: {len(edges_data)}")

	edge_fields = sorted({field for _, _, _, attrs in edges_data for field in attrs.keys()})
	print(f"- Edge fields ({len(edge_fields)}):")
	for field in edge_fields:
		example = next((attrs[field] for _, _, _, attrs in edges_data if field in attrs), None)
		print(f"  - {field}: type={type(example).__name__}, example={value_preview(example)}")

	print("\n- Sample edges (first 3):")
	for u, v, k, attrs in edges_data[:3]:
		print(f"  - edge=({u} -> {v}, key={k})")
		for key in sorted(attrs.keys()):
			print(f"      {key}: {value_preview(attrs[key])}")


print_graph_structure(G)
