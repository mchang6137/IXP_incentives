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
        weight_rand = Random.randint(0,9) + 1
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

#Generate a number yes/no with probability in weights
def weighted_random(weights):
    number = random.random() * sum(weights.values())
    for k,v in weights.iteritems():
        if number < v:
            break
        number -= v
    return k

def calculate_target_function(graph, w):
    all_nodes = nx.nodes(graph)
    pair_set = findsubsets(all_nodes,2)

    summation = 0 

    for pair in pair_set:
        i = pair[0]
        j = pair[1]

        path = nx.shortest_path(graph, source=i, target=j)
        path_weight = 0
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

def algorithm_dual(MST_proposed, complete_graph, w):
    all_nodes = nx.nodes(MST_proposed)
    pair_set = findsubsets(all_nodes,2)

    #Starting the algorithm_dual algorithm with MST_proposed as the starting graph
    while True:
        #very big number
        min_over_edges = 9999999999
        min_edge = (0,0)

        num_edges = nx.number_of_edges(complete_graph)

        #Create a random list
        random_list = range(1, num_edges)
        Random.shuffle(random_list)

        all_edges = complete_graph.edges()
        #Minimize over all the edges in the complete graph
        #for edge in complete_graph.edges():
        for index in random_list:

            edge_src = all_edges[index][0]
            edge_dst = all_edges[index][1]

            local_summation = 0

            #Iterate through powerset of size 2
            for pair in pair_set:
                src = pair[0]
                dst = pair[1]

                #Try on the graph E_proposed
                E_proposed_paths = nx.shortest_path(MST_proposed, source=src, target=dst)
                E_proposed_path_weight = 0
                for i in range(0,len(E_proposed_paths) - 1):
                    step_src = E_proposed_paths[i]
                    step_dst = E_proposed_paths[i+1]
                    E_proposed_path_weight += complete_graph[step_src][step_dst]['weight']

                #Now try with the edge removed
                try:
                    MST_proposed.remove_edge(edge_src, edge_dst)
                except nx.NetworkXError:
                    continue
                try:
                    incomplete_paths = nx.shortest_path(MST_proposed, source=src, target=dst)
                except nx.NetworkXNoPath:
                    #Indicates that graph would be disconnected, so break.
                    MST_proposed.add_edge(edge_src, edge_dst, weight=complete_graph[edge_src][edge_dst]['weight'])
                    continue
                incomplete_path_weight = 0
                for i in range(0,len(incomplete_paths) - 1):
                    step_src = incomplete_paths[i]
                    step_dst = incomplete_paths[i+1]
                    incomplete_path_weight += complete_graph[step_src][step_dst]['weight']

                #Add the edge back 
                MST_proposed.add_edge(edge_src, edge_dst, weight=complete_graph[edge_src][edge_dst]['weight'])

                #if(incomplete_path_weight != complete_path_weight):
                #    print str(edge_src) + " : " + str(edge_dst)
                #    print "incomplete summation: " + str(incomplete_path_weight)
                #    print "complete summation: " + str(complete_path_weight)

                #if(incomplete_path_weight - complete_path_weight == 0):
                #    print str(edge_src) + " : " + str(edge_dst)
                local_summation += (incomplete_path_weight - E_proposed_path_weight) * w[src][dst]

            if local_summation < min_over_edges:
                min_over_edges = local_summation
                min_edge = (edge_src, edge_dst)
                print 'minimum edge found is ' + str(min_edge)
                print 'weight is ' + str(min_over_edges)

        if(min_over_edges - complete_graph[min_edge[0]][min_edge[1]]['weight'] < 0):
            try:
                MST_proposed.remove_edge(min_edge[0], min_edge[1])
            except nx.NetworkXError:
                MST_proposed.add_edge(min_edge[0], min_edge[1], weight=complete_graph[min_edge[0]][min_edge[1]]['weight'])

            if nx.is_connected(MST_proposed) is False:
                MST_proposed.add_edge(min_edge[0], min_edge[1], weight=complete_graph[min_edge[0]][min_edge[1]]['weight'])
            print min_edge
        else:
            break

    return MST_proposed

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
    complete_graph = generate_complete_weighted_graph(p_length)

    draw(complete_graph, 'completetest')
    exit()

    #Generate Complete Graph
    current_MST = kruskal(complete_graph)

    original_MST = current_MST.copy()

    smallest_target = 999999999
    smallest_target_MST = original_MST.copy()

    #TODO: Reduce number of shortest path calculations
    #complete_graph_shortest_path = [[0 for x in range(p_length)] for x in range(p_length)]

    T = 100
    for t in range(1, T):

        all_nodes = nx.nodes(complete_graph)
        pair_set = findsubsets(all_nodes,2)

        MST_proposed = current_MST.copy()

        for pair in pair_set:
            probability = 1 / (2 * (math.log(t,10)+1))
            weights = {'add_vertex': probability,
                       'leave_alone': 1-probability}

            #Add them to the set of E_proposed with a certain probability
            if weighted_random(weights) is 'add_vertex':
                complete_paths = nx.shortest_path(complete_graph, source=pair[0], target=pair[1])
                for i in range(0,len(complete_paths) - 1):
                    step_src = complete_paths[i]
                    step_dst = complete_paths[i+1]
                    if(MST_proposed.has_edge(step_src, step_dst) is False):
                        print 'Added ' + str(step_src) + " : " + str(step_dst)
                        MST_proposed.add_edge(step_src, step_dst, weight=complete_graph[step_src][step_dst]['weight'])

        MST_proposed = algorithm_dual(MST_proposed, complete_graph, w)

        target_value = calculate_target_function(current_MST, w)
        accept_probability = calculate_target_function(current_MST, w)/calculate_target_function(MST_proposed, w)
        if accept_probability <= 1:
            weights = {'accept': accept_probability,
                            'decline': 1 - accept_probability}
            if weighted_random(weights) == 'accept':
                current_MST = MST_proposed
        #Otherwise, do with probability 1
        else:
            current_MST = MST_proposed

        if(target_value < smallest_target):
            smallest_target = target_value
            smallest_target_MST = current_MST.copy()

    print 'done'
    print 'The smallest target function found was: ' + str(smallest_target)
    #draw(smallest_target_MST, 'annealedMST')

if __name__ == "__main__":
    sys.exit(main())