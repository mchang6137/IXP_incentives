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
import random as Random


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
        (src, dst): "%.4f" %d['weight'] for src, dst, d in
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

def generate_complete_weighted_graph(size, costs):
    complete_graph = nx.complete_graph(size)
    weighted_complete_graph = nx.Graph()
    count = 0
    for (u,v) in complete_graph.edges():
        weight_prefix = (costs[u] + costs[v])/2
        weighted_complete_graph.add_edge(u,v, weight=weight_prefix)
        count += 1
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

def calculate_target_function(graph, w):
    all_nodes = nx.nodes(graph)
    pair_set = findsubsets(all_nodes,2)

    summation = 0 

    for pair in pair_set:
        i = pair[0]
        j = pair[1]

        path_weight = 0

        try:
            path = nx.shortest_path(graph, source=i, target=j)
        except nx.NetworkXNoPath:
            #Set to an arbitrary large number
            path_weight = 10000
            path = [0]
      
        for i in range(0,len(path) - 1):
            step_src = path[i]
            step_dst = path[i+1]
            path_weight += graph[step_src][step_dst]['weight']

        summation += path_weight * w[i][j]

    total_cost = 0
    #find the total cost of the edges
    for edges in graph.edges():
        total_cost += graph[edges[0]][edges[1]]['weight']

    return summation + total_cost

#Generates a cost distribution
def generate_costs(p):
    p_length = len(p)
    costs = []

    average_prefixes = sum(p) / len(p)

    #Cost is based on inbalance of traffic
    for i in range(0,p_length):
        costs.append((math.log(p[i],10) + 1 ) / (average_prefixes))

    return costs


#Main body of algorithm located here
def main():

    prefixes_advertised = [1, 1603, 9, 5, 1, 28, 1, 1, 4234, 17, 9, 1, 81, 288, 1607, 2, 1, 13, 139, 90, 78, 164, 35]
    p_length = len(prefixes_advertised)
    total_prefixes = sum(prefixes_advertised)

    #Calculation of w_(i,j)
    w = [[0 for x in range(p_length)] for x in range(p_length)] 
    for i in range(0,p_length):
        for j in range(0,p_length):
            if(i == j):
                w[i][j] = 0
            else:
                w[i][j] = prefixes_advertised[i] / (total_prefixes - prefixes_advertised[j])

    #Generate some complete graph with arbitrary weights
    costs = generate_costs(prefixes_advertised)
    complete_graph = generate_complete_weighted_graph(p_length, costs)

    #Saving the Minimum Spanning tree
    current_MST = kruskal(complete_graph)
    last_MST = current_MST.copy()
  
    #TODO: Reduce number of shortest path calculations
    #complete_graph_shortest_path = [[0 for x in range(p_length)] for x in range(p_length)]

    while True:
        ###########################################################################################################
        #Part 2: Add edges as necessary
        all_nodes = nx.nodes(complete_graph)
        pair_set = findsubsets(all_nodes,2)

        local_summation = 0
        best_e_union_P = current_MST.copy()
        overall_minimum = 9999999

        #Iterate through powerset of size 2
        for pair in pair_set:
            e_union_P = current_MST.copy()

            src = pair[0]
            dst = pair[1]

            #Find the shortest path on the complete graph
            complete_paths = nx.shortest_path(complete_graph, source=src, target=dst)
            complete_path_weight = 0
            for i in range(0,len(complete_paths) - 1):
                step_src = complete_paths[i]
                step_dst = complete_paths[i+1]
                if(e_union_P.has_edge(step_src, step_dst) is False):
                    e_union_P.add_edge(step_src, step_dst, weight=complete_graph[step_src][step_dst]['weight'])

            difference = calculate_target_function(e_union_P,w) - calculate_target_function(current_MST,w)
            if difference < overall_minimum:
                overall_minimum = difference
                best_e_union_P = e_union_P.copy()

        if(calculate_target_function(best_e_union_P,w) - calculate_target_function(current_MST,w) < 0):
            current_MST = best_e_union_P.copy()

        ###########################################################################################################
        #Part 3: Remove edges as necessary

        part_3_minimum = 999999999
        edge_to_remove = [0,0]
        original_MST_target = calculate_target_function(current_MST, w)

        for edges in current_MST.edges():

            src = edges[0]
            dst = edges[1]
           
            current_MST.remove_edge(src, dst)
            difference = calculate_target_function(current_MST, w) - original_MST_target
            current_MST.add_edge(src, dst, weight=complete_graph[src][dst]['weight'])

            if(difference < part_3_minimum):
                part_3_minimum = difference
                edge_to_remove = [src, dst]

        remove_edge_src = edge_to_remove[0]
        remove_edge_dst = edge_to_remove[1]

        #Remove the edge that is determined to be the satisfy the equation
        current_MST.remove_edge(remove_edge_src, remove_edge_dst)


        #If condition is UNsatisified, need to add the edge back.
        if calculate_target_function(current_MST, w) - original_MST_target >= 0:
            current_MST.add_edge(remove_edge_src, remove_edge_dst, weight=complete_graph[remove_edge_src][remove_edge_dst]['weight'])

        ############################################################################################################
        if(current_MST==last_MST):
            break
        else:
            last_MST = current_MST

        print 'The target function is: ' + str(calculate_target_function(current_MST,w))

    print 'done'
    draw(current_MST, 'modified_complete')
    print 'The target function is: ' + str(calculate_target_function(current_MST,w))
    
if __name__ == "__main__":
    sys.exit(main())