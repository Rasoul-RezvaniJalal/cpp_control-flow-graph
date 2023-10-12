import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import graphviz as gv


def parse_graph(path):
    with open(path, mode='r') as f:
        lines = f.readlines()
    edge_lines = lines[:-2]
    edges = list()
    for line_ in edge_lines:
        ab = line_[:-1].split(' ')
        edges.append((ab[0], ab[1]))


    node_state_lines = lines[-2:]
    node_states = [s.split(":") for s in node_state_lines]
    node_states = [(s[0], int(s[1])) for s in node_states]
    print(node_states)
    return edges, node_states


def draw_CFG(edges, states):
    graph = gv.Digraph(format='png')
    graph.node(str(states[0][1]), style='filled', fillcolor='#c0ffc0')
    graph.node(str(states[1][1]), style='filled', fillcolor='yellow')
    graph.edges(edges)
    graph.render('test-output/round-table.gv', view=True)


def main():
    edges, states = parse_graph('CFGS/x/1.txt')
    draw_CFG(edges, states)


if __name__ == '__main__':
    main()