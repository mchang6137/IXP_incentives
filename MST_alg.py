#!/usr/bin/env python
# encoding: utf-8

'''
Find MST for facilities problem.

'''
import glob
import json
import itertools
from operator import attrgetter
import os
import random
import sys
import math
import networkx as nx
import numpy
from random import randint

#Returns an array of the shortest path between any two pairs of nodes
def floydWarshall(graph):
    return nx.floyd_warshall(graph, weight='weight')

#Returns a graph of Kruskal's MST
def kruskal(graph):
    return (nx.minimum_spanning_tree(graph))


def draw(graph, name):
    # plt.show()
    #elarge=[(u,v) for (u,v,d) in graph.edges(data=True)
               # if  > 3]
    #esmall=[(u,v) for (u,v,d) in graph.edges(data=True)
             #   if 5 <= 3]

    import matplotlib.pyplot as plt
    pos=nx.spring_layout(graph) # positions for all nodes

    nx.draw_networkx_nodes(graph, pos, node_size=700)
    nx.draw_networkx_edges(graph, pos, width=6, label=True)
    nx.draw_networkx_edges(graph, pos, 
                           width=6, alpha=0.5, edge_color='b',style='dashed',
                           label=True)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={
        (src, dst): "%.1f" %d['weight'] for src, dst, d in
            graph.edges(data=True)
        })
    # labels
    nx.draw_networkx_labels(graph, pos, font_size=20,font_family='sans-serif')
    plt.savefig("%s.png" % name)

def output_graph(filename, results):
    with open(filename, "w") as json_file:
        json.dump([r.__dict__ for r in results], json_file, sort_keys=True, indent=4)


def add_edge_to_tree(tree, graph):
    # TODO: Move to Kruskal function?
    pass

def generate_complete_weighted_graph(size):
    complete_graph = nx.complete_graph(size)
    weighted_complete_graph = nx.Graph()
    for (u,v) in complete_graph.edges():
        weight_rand = randint(0,9) + 1
        weighted_complete_graph.add_edge(u,v, weight=weight_rand)
    return weighted_complete_graph


#Finds subsets of S with exactly m elements
def findsubsets(S,m):
    return set(itertools.combinations(S, m))

class Edge:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self,other):
        return ((self.x == other.x) and (self.y == other.y)) or ((self.x == other.y) and (self.y == other.x))

    def __str__(self):
        return "%s - %s (%d%s)" % \
               (self.x, self.y, self.weight,
                ", bw=%d" % self.bandwidth if self.bandwidth else "")


#Main body of algorithm located here
def main():

    prefixes_advertised = [4234, 1603, 9, 5, 1, 28, 1, 1, 59, 17, 9, 1, 81, 288, 1607, 2, 1, 13, 139, 90, 78, 164, 35]
    p_length = len(prefixes_advertised)
    total_prefixes = sum(prefixes_advertised)
    print total_prefixes

    #Calculation of w_(i,j)
    w = [[0 for x in range(p_length)] for x in range(p_length)] 
    for i in range(0,p_length):
        for j in range(0,p_length):
            if(i == j):
                w[i][j] = 0
            else:
                w[i][j] = prefixes_advertised[i] / (total_prefixes - prefixes_advertised[j])

    #Generate some complete graph with arbitrary weights
    complete_graph = generate_complete_weighted_graph(p_length)

    #TODO: Reduce number of shortest path calculations
    #complete_graph_shortest_path = [[0 for x in range(p_length)] for x in range(p_length)]

    #Find the MST of the graph
    #Returns (u,v,w) where w is the weight
    MST_graph = kruskal(complete_graph)

    #To see if the graph is still changing
    previous_MST = MST_graph.copy()

    while True:
        
        all_nodes = nx.nodes(complete_graph)
        pair_list = findsubsets(all_nodes,2)
    
        #Iterate through powerset of size 2
        for pair in pair_list:

            union_summation = 0

            MST_paths = nx.shortest_path(MST_graph, source=pair[0], target=pair[1])
            MST_path_weight = 0
            for i in range(0,len(MST_paths) - 1):
                src = MST_paths[i]
                dst = MST_paths[i+1]

                #for n1,n2,attr in MST_graph.edges(data=True):
                    #print n1,n2,attr
                MST_path_weight += MST_graph[src][dst]['weight']
                union_summation += MST_graph[src][dst]['weight']

            complete_paths = nx.shortest_path(complete_graph, source=pair[0], target=pair[1])
            complete_path_weight = 0
            for i in range(0,len(complete_paths) - 1):
                src = complete_paths[i]
                dst = complete_paths[i+1]
                complete_path_weight += complete_graph[src][dst]['weight']
                #Check if complete this part of the complete path is in the MST; if not, add it to the union summation
                if MST_graph.has_edge(src, dst) is False:
                    union_summation += complete_graph[src][dst]['weight']

            if (complete_path_weight - MST_path_weight) * (w[pair[0]][pair[1]] + w[pair[1]][pair[0]] + union_summation - MST_path_weight < 0:
                #Add the edge in the complete graph to the MST graph
                for i in range(0,len(complete_paths) - 1):
                    src = complete_paths[i]
                    dst = complete_paths[i+1]
                    if(MST_graph.has_edge(src,dst) is False):
                        print 'ABOUT TO ADD A LINK'
                        MST_graph.add_edge(src, dst, weight=complete_graph[src][dst]['weight'])

        
        #Now iterate through all elements of E
        for edge in MST_graph.edges():
            total_summation = 0

            for pair in pair_list:
                try:
                    MST_paths = nx.shortest_path(MST_graph, source=pair[0], target=pair[1])
                except nx.NetworkXNoPath:
                    #not an option so continue
                    break
                MST_path_weight = 0
                for i in range(0,len(MST_paths) - 1):
                    src = MST_paths[i]
                    dst = MST_paths[i+1]
                    MST_path_weight += MST_graph[src][dst]['weight']
    
                MST_graph.remove_edge(edge[0], edge[1])
                try:
                    MST_except_e_paths = nx.shortest_path(MST_graph, source=pair[0], target=pair[1])
                except nx.NetworkXNoPath:
                    #not an option so continue
                    MST_graph.add_edge(edge[0], edge[1], weight=1)
                    break
                MST_except_e_path_weight = 0
                for i in range(0,len(MST_except_e_paths) - 1):
                    src = MST_except_e_paths[i]
                    dst = MST_except_e_paths[i+1]
                    MST_except_e_path_weight += MST_graph[src][dst]['weight']
                MST_graph.add_edge(edge[0], edge[1], weight=1)

                total_summation += (MST_except_e_path_weight - MST_path_weight) * w[pair[0]][pair[1]]

            #Add back the removed edge, else leave it removed form the modified MST
            if total_summation - complete_graph[edge[0]][edge[1]]['weight'] >= 0:
                MST_graph.add_edge(edge[0], edge[1], weight=1)

        if (MST_graph == previous_MST):
            print 'exiting'
            break
        else:
            print previous_MST.edges()
            break
            previous_MST = MST_graph.copy()

    print 'done'
    draw(MST_graph, 'newMST')




    
if __name__ == "__main__":
    sys.exit(main())