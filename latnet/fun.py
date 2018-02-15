import networkx as nx

def set_default(obj):
    '''for saving set objects using json'''
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def toNetworkxGraph(agent_manager,relations):
    nodes = agent_manager.toNetworkXFormat()
    edges = relations.toNetworkXFormat()
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return g

def saveToGraphml(graph,filename,**kwargs):
    nx.write_graphml(graph,filename,**kwargs)
