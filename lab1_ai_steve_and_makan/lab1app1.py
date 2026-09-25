#AI Lab A1 Part 1
#Game of Thrones kings battle graph

import pandas as pd
from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components


#page title
st.title("Game of Thrones Kings Battle Graph")


#Loading the data
data = pd.read_csv("data/game-of-thrones-battles.csv")


#select required columns
battles_df = data.loc[:, [
    "name",
    "attacker_king",
    "defender_king",
    "attacker_size",
    "defender_size"
]]


#remove rows with any missing values (NaN)
battles_df_cleaned = battles_df.dropna()


#Task 1.1
print(f"Attacking kings: {battles_df_cleaned['attacker_king'].unique()}")


#Task 1.2
print(f"Defending kings: {battles_df_cleaned['defender_king'].unique()}")


#Task 2
net5kings = Network(
    heading="Task1. Building Interactive Network of battles of the War of 5 Kings",
    bgcolor ="#242020",
    font_color = "white",
    height = "1000px",
    width = "100%",
    directed = True,
    notebook=False,
    cdn_resources = "in_line"
)


#Task 2.1
nodes = set(
    battles_df_cleaned["attacker_king"].tolist() +
    battles_df_cleaned["defender_king"].tolist()
)

print(f"Kings list (nodes names): {nodes}")


#Task 2.2
#add the nodes
net5kings.add_nodes(list(nodes))

print(f"Nodes of net5kings properties: {net5kings.nodes}")


#Task 2.3
edges = battles_df_cleaned.loc[:, [
    "attacker_king",
    "defender_king"
]].values.tolist()

print("Potential Edges of net5kings:")

for edge in edges:
    print(edge)


#Task 2.3
unique_edges = set()

for edge in edges:
    unique_edges.add(tuple(edge))

print("Real (unique) directed Edges of net5kings:")

for edge in unique_edges:
    print(edge)


#Task 2.4
edges_w = battles_df_cleaned.groupby(
    ["attacker_king", "defender_king"]
)["name"].count()

print(edges_w)


#Task 2.4
edges_titles = battles_df_cleaned.groupby(
    ["attacker_king", "defender_king"]
)["name"].agg(", ".join)

print(edges_titles)


#Task 2.5
edges_weights = []

for index in unique_edges:

    print(
        f"Attackin king: {index[0]}, "
        f"Defending king: {index[1]}, "
        f"N of battles: {edges_w[index]}, "
        f"battles: {edges_titles[index]}"
    )

    edges_weights.append(int(edges_w[index]))

print(f"edges_weights: {edges_weights}")


#Task 2.6
for index, edge in enumerate(unique_edges):

    net5kings.add_edge(
        edge[0],
        edge[1],
        value=int(edges_w[edge]),
        title=edges_titles[edge]
    )

    print(
        f"The edge from {edge[0]} to {edge[1]} "
        f"with weight {edges_w[edge]}, "
        f"title: '{edges_titles[edge]}' was added"
    )


#Task 2.7
print(net5kings.edges)


#Task 3.1
enemies_map = net5kings.get_adj_list()

print(enemies_map)


#Task 3.2
for king, enemies in enemies_map.items():

    print(
        f"King: {king} has attacked: {enemies}, "
        f"N of enemies: {len(enemies)}, "
        f"node's value: {1 + len(enemies)}"
    )


#Task 3.3.1
nodeColors={
    0:"blue",
    1:"green",
    2:"orange",
    3:"purple",
    4:"gold",
    5:"red"
}


#Task 3.3.2
for node in net5kings.nodes:

    node["value"] = 1 + len(enemies_map[node["id"]])

    node["color"] = nodeColors[node["value"]]


#Task 3.4
print(net5kings.nodes)


#show some information on the streamlit page
st.write("Number of battles:", len(battles_df_cleaned))
st.write("Number of kings:", len(nodes))
st.write("Number of edges:", len(unique_edges))


#generate the html
html = net5kings.generate_html()


#save the html using utf-8
HtmlFile = open(
    "Lab1-task1-net5kings.html",
    "w",
    encoding="utf-8"
)

HtmlFile.write(html)

HtmlFile.close()


#open the html file
HtmlFile = open(
    "Lab1-task1-net5kings.html",
    "r",
    encoding="utf-8"
)


#display the graph on streamlit
components.html(
    HtmlFile.read(),
    height=1050,
    scrolling=True
)


#close the file
HtmlFile.close()