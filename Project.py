import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from collections import Counter
import math

#read the file and load the network into networkx
filename = '/Users/scottye/Desktop/Project/Mar 11/email-EuAll.txt'
f = open(filename, 'r')
edge = list()
for line in f:
    element = line.split()
    temp = []
    for node in element:
        temp.append(node)
    edge.append(temp)
    # if len(edge) > 10000:
    #     break

G = nx.DiGraph()
G.add_edges_from(edge)

def network_info(G):
    print(nx.info(G))

def network_density(G):
    density = nx.density(G)
    print("Network density:", density)

def network_draw(G):
    nx.draw(G)
    plt.show()

def network_details(G): # Graph Properties
    N = G.order()
    K = G.size()
    avg_deg = K / N
    print("Nodes: ", N)
    print("Edges: ", K)
    print("Average degree: ", avg_deg)
    print("SCC: ", nx.number_strongly_connected_components(G))
    print("WCC: ", nx.number_weakly_connected_components(G))

def plot_degree_dist(G):
    degrees = [G.degree(n) for n in G.nodes()]
    plt.hist(degrees)
    plt.show()

def plot_degree_dist2(G):
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    #print(in_degrees)

    in_values = sorted(set(in_degrees.values()))
    out_values = sorted(set(out_degrees.values()))
    in_hist = [list(in_degrees.values()).count(x) for x in in_values]
    out_hist = [list(out_degrees.values()).count(x) for x in out_values]

    plt.figure()
    plt.grid(True)
    plt.plot(in_values, in_hist, 'ro-') # in-degree
    plt.plot(out_values, out_hist, 'bv-') # out-degree
    plt.legend(['In-degree', 'Out-degree'])
    plt.xlabel('Degree')
    plt.ylabel('Number of nodes')
    plt.title('EU email communication network')
    plt.xlim([0, 2*10**3])

    plt.show()



def network_triadic_closure(G):
    triadic_closure = nx.transitivity(G)
    print("Triadic closure:", triadic_closure)

def largest_clustering(G):
    pass
    # G = G.to_undirected()
    # out = float('-inf')
    # for n in range(1, 5):
    #     if nx.clustering(G,'n') > out:
    #         out = nx.clustering(G,'n')
    
    # print(out)


def plot_degree_rank(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    dmax = max(degree_sequence)

    plt.loglog(degree_sequence, "b-", marker="o")
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")

    # draw graph in inset
    plt.axes([0.45, 0.45, 0.45, 0.45])
    Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
    pos = nx.spring_layout(Gcc)
    plt.axis("off")
    nx.draw_networkx_nodes(Gcc, pos, node_size=20)
    nx.draw_networkx_edges(Gcc, pos, alpha=0.4)
    plt.show()

def sorted_clustering(G):
    k = nx.clustering(G)
    sorted_k = sorted(k.items(), key = lambda x: x[1])
    print(sorted_k)

def plot_degree_histogram(g):
    def plot_degree_histogram_inner(g, normalized=True, weight=None):
        
        degree_sequence = sorted([d for n, d in g.degree(weight=weight)], reverse=True)  # degree sequence
        degreeCount = Counter(degree_sequence)
        aux_x, aux_y = zip(*degreeCount.items())

        n_nodes = g.number_of_nodes()
        aux_y = list(aux_y)
        if normalized:
            for i in range(len(aux_y)):
                aux_y[i] = aux_y[i]/n_nodes
        
        return aux_x, aux_y

    (x, y) = plot_degree_histogram_inner(a)
    plt.title('\nDistribution Of Node Linkages (log-log scale)')
    plt.xlabel('Degree\n(log scale)')
    plt.ylabel('Number of Nodes\n(log scale)')
    plt.xscale("log")
    plt.yscale("log")
    plt.plot(x, y, 'o')
    plt.show()

def largest_centrality(G):
    k = nx.eigenvector_centrality(G)
    sorted_k = sorted(k.items(), key = lambda x: x[1], reverse = False)
    print(sorted_k)

def remove_largest_centrality(G, a):
    k = nx.eigenvector_centrality(G)
    sorted_k = sorted(k.items(), key = lambda x: x[1], reverse = False)
    #print(sorted_k)
    print("Before Removing:")
    #network_info(G)
    network_density(G)
    network_details(G)
    #plot_degree_dist_loglog(G)
    for n in sorted_k[-a:]:
        G.remove_node(n[0])

    print('-----------------------')
    print("After Removing")
    #network_info(G)
    network_density(G)
    network_details(G)
    plot_degree_dist_loglog(G)

def largest_connect_component(G1, n):
    G1 = G1.to_undirected()
    Gcc = sorted(nx.connected_components(G1), key=len, reverse=True)
    #print(Gcc)
    G0 = G.subgraph(Gcc[n]) # (n+1)th largest connected component and return to digraph
    print(str(n+1)+"th largest componet:")
    network_info(G0)
    print('-----------------------')
    print("Whole network:")
    network_info(G)
    # nx.draw(G0)
    # plt.show()
    return G0
    
def plot_degree_dist_loglog(G):
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())

    in_values = sorted(set(in_degrees.values()))
    out_values = sorted(set(out_degrees.values()))
    in_hist = [list(in_degrees.values()).count(x) for x in in_values]
    out_hist = [list(out_degrees.values()).count(x) for x in out_values]

    plt.figure()
    plt.grid(True)
    plt.loglog(in_values,in_hist,'ro-') # in-degree
    plt.loglog(out_values, out_hist, 'bv-') # out-degree
    plt.legend(['In-degree', 'Out-degree'])
    plt.xlabel('Degree')
    plt.ylabel('Number of nodes')
    #plt.title('EU email communication network')
    plt.title('200th Largest Component')
    plt.xlim([0, 2*10**4])

    plt.show()

#a = largest_connect_component(G, 0)
#largest_centrality(G)
remove_largest_centrality(G, 5000)

#print(nx.is_connected(a))
#print(nx.diameter(a.to_undirected()))

#plot_degree_dist_loglog(a)



#plot_degree_histogram(a)








# G.remove_node('818')
# G.remove_node('314')
# G.remove_node('1011')
# G.remove_node('599')
# G.remove_node('1118')
# G.remove_node('1014')
# G.remove_node('911')
# G.remove_node('240')
# G.remove_node('1085')
# G.remove_node('192')


#plot_degree_dist_loglog(a)
#largest_centrality(a)
#largest_centrality(G)




#print(nx.average_clustering(G))

#network_draw(G)
#network_info(G)
#plot_degree_dist(G)
#network_density(G)
#network_details(G)



#network_triadic_closure(G)
#plot_degree_dist2(G)
#plot_degree_dist_loglog(G)

# print('Before')
# network_info(G)
# network_density(G)



# print('After')
# network_info(G)
# network_density(G)
# plot_degree_dist_loglog(G)

#network_info(G)
