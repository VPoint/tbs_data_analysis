import json
import requests
import networkx as nx
import matplotlib.pyplot as plt

personas = 'http://story-chronicles.herokuapp.com/storyobjects/'

target = requests.get(personas)

x = target.json()


relationship = "Kaeso Messor >> Ally Legio VII - Victrix (Kaeso is a veteran of the 7th) - weight: 6)"

story_objects = {}
labels = {}
node_shapes = {}
node_colors = {}

for character in x:
    name = character["name"]
    story = character["story"]
    c_type = character["c_type"]
    story_objects[name] = {}
    story_objects[name]['name'] = name
    story_objects[name]['story'] = story
    story_objects[name]['c_type'] = c_type
    story_objects[name]['to_relationships'] = []
    if character['c_type'] == "Character":
        story_objects[name]['node_shape'] = 'o'
        story_objects[name]['node_color'] = (0,.5,0)
    elif character['c_type'] == "Organization":
        story_objects[name]['node_shape'] = 's'
        story_objects[name]['node_color'] = (.5,.5,0)
    elif character['c_type'] == "Creature":
        story_objects[name]['node_shape'] = '^'
        story_objects[name]['node_color'] = (0,.5,.5)
    elif character['c_type'] == "Force":
        story_objects[name]['node_shape'] = 'v'
        story_objects[name]['node_color'] = (.5,.5,.5)
    elif character['c_type'] == "Thing":
        story_objects[name]['node_shape'] = 'd'
        story_objects[name]['node_color'] = (.25,0,0)

    for relationship in character["to_relationships"]:
        break_1 = relationship.find(">>")
        break_2 = relationship.find("weight:")
        sub_1 = relationship[0:break_1].strip()
        context = relationship[break_1:break_2]
        weight = relationship[break_2+8:-1]
        story_objects[name]['to_relationships'].append([sub_1, context, weight])

G=nx.MultiDiGraph()

for sub in story_objects:
    s = story_objects[sub]
    if s['story'] == "http://story-chronicles.herokuapp.com/story/1/":
        G.add_node(s['name'])
        labels[s['name']] = s['name']
        node_colors[s['name']] = s['node_color']
        node_shapes[s['name']] = s['node_shape']
        print("***", s['name'], "***", s['c_type'])
        print("details:", s['node_color'], s['node_shape'])
        for i in s['to_relationships']:
            print('target:', i[0])
            print('context:', i[1])
            print('weight:', i[2])
            G.add_edge(s['name'], i[0], weight=int(i[2]))
        print("")

pos=nx.spring_layout(G)
G.degree(weight=weight)

nx.draw_networkx_nodes(G, pos) # node_color=node_colors, node_shape=node_shapes)
nx.draw_networkx_edges(G, pos, arrows=True)
nx.draw_networkx_labels(G, pos, labels)
plt.show()
plt.savefig("test.png")
