import networkx as nx
import matplotlib.pyplot as plt


def draw_cfg():
    with open(r'CFGS/x/1.txt', mode='r') as f:
        lines = f.readlines()
    lines = lines[0:-1]
    edges = list()
    #print(edges)
    for line_ in lines:
        ab = line_[:-1].split(' ')
        #print(ab)
        edges.append((ab[0], ab[1]))

    print(lines)
    print(edges)
    G = nx.DiGraph(edges)
    #print
    #print(G.nodes(1).keys('1'))
    color_map = []
    #color_map.append('green')
    for node in G:

        if G.in_degree(node) == 0:
            color_map.append('green')
        elif G.out_degree(node) == 0:
            color_map.append('red')
        else:
            color_map.append('orange')

    color_map[0]='green'
    color_map[-1]='red'

    pos = nx.circular_layout(G)



    nx.draw(G, with_labels=True, node_size=1000, pos=pos, node_color=color_map)
    plt.show()

draw_cfg()