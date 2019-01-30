import networkx
import matplotlib.pyplot as plot
import random
import math

"""This module is a graph-based social network model using networkx with a dictionaries of dictionaries
    implementation. Please make sure to install the following dependencies before running:
        - networkx: pip3 install networkx
        - matplotlib: pip3 install matplotlib
        - tkinter: apt install pyton3-tk or equivalent for non-debian linux or mac
        - scipy: pip3 install scipy
    The code is uses Python 3 features. 
        """


class SocialNetwork:

    """This class models a social network of connected people. This is a graph-based model with each
    node representing a person and each edge representing a connection between two people. The default
    instance of this class uses a simple small network of people with random connections. The constructor
    provides for the ability to specify the people and the connections in two separate lists or sets. A
    third argument "gov" is provided in the case that no connections are provided and simple designates one
    of two algorithms for creating connections between people in the network. The two possible values
    are "random" which creates random connections, this is to be used whenever you want to provide only a
    list of people and still create a meaningful social network, the other option is "full" which exists
    only for graph testing purposes and shouldn't be used. If a connections list is provided, a gov argument
    has no effect"""

    __test_people = ["Ahmed", "Mohamed", "Mahmoud", "Moaz", "Amr", "Omar", "Mai", "Hoda"]

    def __init__(self, people=__test_people, connections=None, gov=None):
        self.people = people
        self.connections = []
        self.graph = networkx.MultiGraph()
        self.plot = plot
        # the default connection creation between people is random. They're also a full connection
        # implementation that connects all nodes to all other nodes. It's there but not useful for this model
        if connections is None:
            if gov is None:
                self.create_connections_random()
            elif gov == "random":
                self.create_connections_random()
            elif gov == "full":
                self.create_connections_full()
        else:
            self.connections = connections
        # create the graph with nodes and connections
        self.populate_graph()

    def create_connections_full(self):
        """Create a list of connections that connect all nodes to all other nodes in the network,
            not useful for our needs and don't use it for purposes of testing this model as it creates
            a meaningless social network.
            Note: This function should not be called from outside but for testing
            purposes external invocation is allowed"""
        # This little devilish loop here creates lots of connections
        for i in self.people:
            for j in self.people:
                # self connections are actually handled by networkx by I want a clean connection list
                if i is j:
                    continue
                self.connections.append((i, j))

    def create_connections_random(self):
        """Create a list of connections that randomly connect nodes to other nodes in the network,
            this is the recommended way of creating a meaningful network for our model.
            Note: This function should not be called from outside but for testing
            purposes external invocation is allowed"""
        for i in self.people:
            for j in self.people:
                # self connections are actually handled by networkx by I want a clean connection list
                if i is j:
                    continue
                # this creates connections at a random boolean-like decision
                m = random.randint(0, 1)
                if m == 0:
                    continue
                else:
                    self.connections.append((i, j))
                # this loop only executes one for each person to create less and easier connections
                break

    def populate_graph(self):
        """Populate the graph object with the nodes and the edges.
        Note: This function should not be called from outside but for testing
            purposes external invocation is allowed"""
        # add the nodes to the graph
        self.graph.add_nodes_from(self.people)
        # add the edges to the graph
        self.graph.add_edges_from(self.connections)

    def draw_graph(self):
        """Create the plot of the network graph.
        Note: this function doesn't display the plot, to do that call show_graph() afterwards"""
        # this is the matplotlib plot object, this subplot full height and left-most occupying
        self.plot.subplot(121)
        # draw the network graph on the subplot
        networkx.draw_networkx(self.graph, with_labels=True, font_weight='bold')

    def draw_graph_shell(self):
        """Create the plot of the network graph shell.
        Note: this function doesn't display the plot, to do that call show_graph() afterwards"""
        # this is the matplotlib plot object, this subplot full height and right-most occupying
        self.plot.subplot(122)
        # draw the shell of network graph on the subplot for an easier outside-in view
        networkx.draw_shell(self.graph, with_labels=True, font_weight='bold')

    def show_graph(self):
        """Show the drawn plots for this network"""
        self.plot.show()

    def get_adjacency_with_separation_degree(self, degree):
        """Get a list of all nodes in the network and for each node a set of nodes that are exactly
        degree degrees of separation away from the node"""
        # store the adjacency list
        adjacency = {}
        # iterate over the iterable for all shortest path lengths in the graph
        # each i is a dictionary containing with the person's name and a dictionary
        # of degrees of separation from each other node in the network
        for i in networkx.all_pairs_shortest_path_length(self.graph):
            # holder for the set of people that are exactly degree degrees away from the current node
            temp = set()
            # a dictionary to hold the separation dictionary in i
            dic = dict(i[1])
            # iterate over the separation dictionary for the current node
            for j in dic:
                # if the current node of the separation dictionary is exactly degree degrees of separation
                # add it to the current set of nodes
                if dic.get(j) == degree:
                    temp.add(j)
            # after iterating over all separations add the person and the set of people that are exactly
            # degree degrees away from that person
            adjacency.update({i[0]: temp})
        # return the adjacency dictionary
        return adjacency

    def get_friends(self):
        """Friends of a node are the people who are exactly 1 degree of separation away.
            Note: this notation is not consistent with social theory degree of separation,
            it is consistent with graph theory degree of separation that uses edges"""
        return self.get_adjacency_with_separation_degree(1)

    def get_friends_of_friends(self):
        """Friends of friends of a node are the people who are exactly 2 degrees of separation away.
            Note: this notation is not consistent with social theory degree of separation,
            it is consistent with graph theory degree of separation that uses edges"""
        return self.get_adjacency_with_separation_degree(2)

    def get_most_popular(self):
        """Get a set of all the most popular people in the network, the node(s) with the highest connectivity"""
        # a unique set of popular people
        populars = set({})
        # a placeholder for a comparable object representing a person
        person = None
        for i in self.graph.degree:
            # this is for the first iteration to cast person from None to a comparable object type
            if person is None:
                person = i
                continue
            # if the current person object's connectivity level (how many people they're connected to)
            # is higher than the place holder, replace the placeholder with the current person
            if i[1] > person[1]:
                person = i
        # add the most popular person to the set of most popular people
        populars.add(person[0])
        # this loops adds other people who are equally popular to the most popular person
        for i in self.graph.degree:
            # if the current person object's connectivity level is equal than the place holder,
            # this person is as popular to the most popular person and add them to the set
            if i[1] == person[1]:
                populars.add(i[0])
        # return the set of most popular people
        return populars

    def get_least_popular(self):
        """Get a set of the least popular people in the network, the node(s) with the least connectivity.
        Note: Certain variable names contained in this method may trigger people who were triggered by
        certain historic python terminology. Please open a PEP if you wish to rectify this issue."""
        # placeholder for a unique set of least popular people
        unpopulars = set({})
        # placeholder for a comparable person object
        person = None
        for i in self.graph.degree:
            if person is None:
                person = i
                continue
            if i[1] < person[1]:
                person = i
        unpopulars.add(person[0])
        for i in self.graph.degree:
            if i[1] == person[1]:
                unpopulars.add(i[0])
        return unpopulars

    def get_average(self, gov=None):
        """Get the average level of connectivity in the network.
        Note: averages are floating points but to be meaningful this function returns an integer,
        for this reason you may specify a governor for rounding. Possible governors are "ceiling", "floor",
        "cast"  which uses python's int() casting for rounding, or unspecified which returns floating point"""
        # the summation of all degrees and the count of nodes
        summation, count = 0, 0
        # iterate over the degrees of connectivity of all nodes in the network
        for i in self.graph.degree:
            # increase the number of nodes
            count += 1
            # sum the values of node degrees
            summation += i[1]
        # do rounding according to the governor argument
        if gov == "floor":
            return math.floor(summation/count)
        elif gov == "ceiling":
            return math.ceil(summation/count)
        elif gov == "cast":
            return int(summation/count)
        else:
            return summation/count

    def get_more_than_four(self):
        """Get a set of people who have four or more friends in the network"""
        # a unique set of people with more than four friends
        populars = set({})
        # iterate over the degrees of separation of all nodes in the network
        for i in self.graph.degree:
            if i[1] > 4:
                populars.add(i[0])
        if len(populars) == 0:
            return "No one has more than four friends"
        return populars


# create the social network mode
social_network = SocialNetwork()
# draw the graph for the network
social_network.draw_graph()
# draw the network graph shell
social_network.draw_graph_shell()
# show the graph plots
social_network.show_graph()
# print the friends of everyone in the network
print("Friends:", social_network.get_friends())
# print the friends of friends of everyone in the network
print("Friends of friends:", social_network.get_friends_of_friends())
# print the most popular people in the network
print("Most popular:", social_network.get_most_popular())
# print the least popular people in the network
print("Least popular:", social_network.get_least_popular())
# print the average popularity of people in the network
print("Average popularity:", social_network.get_average())
# print people in the network with more than four friends
print("More than 4 friends:", social_network.get_more_than_four())
