#AI Lab A1 Part 2
#Game of Thrones Houses Graph

import json
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components

from pyvis.network import Network


#page title
st.title("Task2: infographic of relationships between characters in the Game of Thrones")


#load json data
with open(
    "data/game-of-thrones-characters-groups.json",
    "r",
    encoding="utf-8"
) as file:

    json_data = json.load(file)


#Task 1
class Dynasty:

    def __init__(self, name):

        self._name = name
        self.characters = []


    @property
    def name(self):

        return self._name


    @name.setter
    def name(self, value):

        if value != "":

            self._name = value


    def append(self, ch):

        if isinstance(ch, str):

            self.characters.append(ch)

        else:

            raise TypeError("Character must be a string")


    def __iter__(self):

        return iter(self.characters)


    def __contains__(self, ch):

        return ch in self.characters


    def __str__(self):

        return self._name


    def getStrength(self):

        return len(self.characters)


#Task 2
class GameOfThronesGraph:

    def __init__(self, corpus):

        #dictionary to store houses
        self.houses = {}


        #load house data
        for data_item in corpus:

            house = Dynasty(data_item["name"])


            for character in data_item["characters"]:

                house.append(character)


            self.houses[house.name] = house


    def __iter__(self):

        return iter(self.houses.values())


    def __contains__(self, h):

        return h in self.houses


#load groups from json
corpusData = json_data["groups"]


#create Game of Thrones houses object
GameOfThronesHouses = GameOfThronesGraph(corpusData)


#Task 2.2
visualisationData = {}

legendData = []


for house in GameOfThronesHouses:

    visualisationData[house.name] = house.getStrength()

    legendData.append(house.name)


#Task 3
g = nx.Graph()


#number of houses
N_houses = 0

colorKeys = []


for house in GameOfThronesHouses:

    if house.name != "Include":

        N_houses += 1

        colorKeys.append(house.name)


#create colors
nodeColors = dict(
    zip(
        colorKeys,

        [
            tuple(int(c * 255) for c in cs)

            for cs in sns.color_palette(
                "husl",
                N_houses
            )
        ]
    )
)


#add house nodes
for house in GameOfThronesHouses:

    if house.name != "Include":

        g.add_node(
            house.name,
            size=house.getStrength()
        )


#add family member nodes
for house in GameOfThronesHouses:

    if house.name != "Include":

        for person in house:

            g.add_node(person)


#add edges
myEdges = []


for house in GameOfThronesHouses:

    if house.name != "Include":

        for person in house:

            myEdges.append(
                (person, house.name)
            )


g.add_edges_from(myEdges)


#create pyvis network
GameOfThronesNet = Network(
    bgcolor="#242020",
    font_color="white",
    height="1000px",
    width="100%",
    notebook=False,
    cdn_resources="in_line"
)


#convert NetworkX graph to Pyvis
GameOfThronesNet.from_nx(g)


#assign colors
for node in GameOfThronesNet.nodes:

    if node["id"] in GameOfThronesHouses:

        #convert RGB to hexadecimal
        node["color"] = '#%02x%02x%02x' % nodeColors[node["id"]]


    else:

        for house in GameOfThronesHouses:

            if house.name != "Include":

                #apply house color to family member
                if node["id"] in house:

                    node["color"] = '#%02x%02x%02x' % nodeColors[house.name]


#generate html
html = GameOfThronesNet.generate_html()


#--------------------------------------------------
#STREAMLIT TABS
#--------------------------------------------------

tab1, tab2, tab3 = st.tabs([
    "Game Of Thrones Houses",
    "Members of Houses",
    "Graph for Game Of Throne Houses"
])


#--------------------------------------------------
#TAB 1
#--------------------------------------------------

with tab1:

    st.write("Game ofThrones Houses:")


    for house in GameOfThronesHouses:

        st.write(
            f"- This is a House of {house.name}!: "
            f"Strength: {house.getStrength()}"
        )


    #bar graph
    x = list(visualisationData.keys())

    y = list(visualisationData.values())


    fig, ax = plt.subplots()


    sns.barplot(
        x=x,
        y=y,
        ax=ax
    )


    #legend
    ax.legend(legendData)

    sns.move_legend(
        ax,
        "upper left",
        bbox_to_anchor=(1.05, 1)
    )


    #axis labels
    ax.set(
        xlabel="Houses",
        ylabel="Strength (N family members)",
        title="Strength of GameOfThronesHouses"
    )


    plt.xticks(rotation=45)


    st.pyplot(fig)


#--------------------------------------------------
#TAB 2
#--------------------------------------------------

with tab2:

    for house in GameOfThronesHouses:

        st.write(
            f"This is a House of {house.name}!. "
            f"Our members:"
        )


        for person in house:

            st.write(f"- {person}")


        st.write(
            f"We have {house.getStrength()} family members!!!"
        )


        st.write("")


#--------------------------------------------------
#TAB 3
#--------------------------------------------------

with tab3:

    st.header("Lab1. Task2.")


    components.html(
        html,
        height=1050,
        scrolling=True
    )