import subprocess
import os

import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

import matplotlib.pyplot as plt

import math



n = 7


def display_and_save_graph(G, n, e, g_index, outdir="graphs"):
	os.makedirs(f"{n}-{outdir}/size-{e}", exist_ok=True)

	pos = nx.circular_layout(G)

	plt.figure(figsize=(4, 4))
	nx.draw(
		G,
		pos,
		with_labels=True,
		node_color="black",
		edge_color="black",
		font_color="white",
		font_size=12,
		node_size=600,
	)

	filename = f"{n}-{outdir}/size-{e}/({n}, {e})-graph({g_index}).png"
	plt.savefig(filename, dpi=300, bbox_inches="tight")
	plt.close()

	print(f"Saved {filename}")


def display_grid_graph(g_list, filename="grid.png"):
	k = len(g_list)
	cols = 3 # customize number of columns
	rows = math.ceil(k / cols)

	plt.figure(figsize=(4*cols, 4*rows))

	for idx, g in enumerate(g_list, 1):
		pos = nx.circular_layout(g)

		plt.subplot(rows, cols, idx)
		nx.draw(
			g,
			pos,
			with_labels=True,
			node_color="black",
			edge_color="black",
			font_color="white",
			font_size=12,
			node_size=500,
		)
		plt.title(f"Size {len(g.edges)}")

	plt.tight_layout()
	plt.savefig(filename, dpi=300)
	plt.close()

	print(f"Saved {filename}")


def compute_vertex_maps(G, turn_on=False):
	if not turn_on:
		return

	GM = GraphMatcher(G, G)
	automorphisms = list(GM.isomorphisms_iter()) # automorphism group of G

	print("\nAutomorphism group (vertex mappings):")
	for auto in automorphisms:
		print(auto) # display automorphisms as mappings


def compute_orbits(G, turn_on=False):
	if not turn_on:
		return

	GM = GraphMatcher(G, G)
	automorphisms = list(GM.isomorphisms_iter()) # automorphism group of G

	orbits = {v: set() for v in G.nodes()} # create dict for orbits
	for auto in automorphisms:
		for v, u in auto.items(): 
			orbits[v].add(u) 

		orbits = {v: sorted(list(s)) for v, s in orbits.items()}
		print("\nOrbits of vertices:")
		for v, orbit in orbits.items():
			print(f"Vertex {v}: {orbit}")



total_classes = 0
max_edges = math.comb(n, 2) # nChoose2, max edges of an n-order graph
g_list = []

for e in range(max_edges+1):
	proc = subprocess.Popen(
		["./geng", str(n), str(e)],
		stdout=subprocess.PIPE,
		text=True
	) # process ./geng inside python
	# ./geng outputs non-isomorphic graphs in graph6 string format

	equiv_classes = 0
	g_index = 1

	for line in proc.stdout: #read lines from ./geng	
		g6 = line.strip()
		if g6 == '':
			continue
		G = nx.from_graph6_bytes(g6.encode())

		display_and_save_graph(G, len(G.nodes), len(G.edges), g_index) #produce individual graph .png files
		g_list.append(G)
		g_index += 1

		#uncomment to show edge pairs of each graph in cmd
		# print("Edges:", G.edges)
		# print("Edge count:", len(G.edges))

		# compute automorphisms
		compute_vertex_maps(G,) # enter True to compute vertex maps

		# compute orbits
		compute_orbits(G,) # enter True to compute orbits

		equiv_classes += 1
		# print(f"Automorphism Count: {len(automorphisms)}")

	print(f"Equivalence Classes Count: {equiv_classes} on {len(G.edges)} edges\n")
	total_classes += equiv_classes

print(f"Total equivalence classes: {total_classes}")
#display_grid_graph(g_list) # display all graphs on one grid