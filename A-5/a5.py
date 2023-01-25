
INF = float('inf')                                          # infinity


class HeapNode:
    """Class for storing capacity and node_id"""
    
    def __init__(self, node_id, capacity):
        # node_id is the index of the node
        # capacity is the capacity of the node

        self._max_capacity = capacity                   # maximmum capacity with which the node can be reached
        self._router = node_id                          # index node_id

    def get_key(self):
        return self._router                             # getter method for index/key

    def get_capacity(self):
        return self._max_capacity                       # getter method for capacity

    def set_capacity(self, new_cap):
        self._max_capacity = new_cap                    # setter method for capacity

    def __lt__(self, other):
        # less than operator overloading to compare with other capacity objects
        # return true if capacity is lower else returns false
        return (self._max_capacity < other._max_capacity)

    def __gt__(self, other):
        # greater than operator overloading to compare with other capacity objects
        return (self._max_capacity > other._max_capacity)

    def __str__(self):
        return f'node_id:{self._router}\t\tmax capacity:{self._max_capacity}'


class MaxHeap:
    """Max Heap class"""
    # -------------------------- NON PUBLIC METHODS -------------------------------

    def _parent_index(self, m):
        # returns index of parent
        return (m-1)//2

    def _left_child_index(self, m):
        # returns index of left child
        return (2*m+1)

    def _right_child_index(self, m):
        # returns index of right child
        return (2*m+2)

    def _has_parent(self, m):
        # returns False if the given node is root else True
        return self._parent_index(m) >= 0

    def _has_left(self, m):
        # returns True if node has left child else False
        return self._left_child_index(m) < len(self._elem)

    def _has_right(self, m):
        # returns True if node has right child else False
        return self._right_child_index(m) < len(self._elem)

    def _swap(self, x, y):
        # swap node at position x and y
        # TIME COMPLEXITY : O(1)
        self._locator[self._elem[x].get_key()] = y                      # update locator for x
        self._locator[self._elem[y].get_key()] = x                      # update locator for y
        self._elem[x], self._elem[y] = self._elem[y], self._elem[x]     # swap the nodes

    def _bubble_up(self, m):
        # swap the element with its parent to get it to correct position
        # m is the index of the node which is to be moved up
        # TIME COMPLEXITY : O(logn)
        
        while self._has_parent(m):                          # while node has parent
            par = self._parent_index(m)                     # get parent index
            if self._elem[m] > self._elem[par]:             # if child is greater than parent
                self._swap(m, par)                          # swap the child and parent       
                m = par                                     # update m to parent index
            else:
                break                                       # else break           

    def _bubble_down(self, m):
        # swap the element with child having minimum value to get it to correct position
        # m is the index of the node which is to be moved down
        # TIME COMPLEXITY : O(logn)
        
        while self._has_left(m):                            # while node has left child 
            left = self._left_child_index(m)                # get left child index
            max_child = left                                # set max_child to left child index

            if self._has_right(m):                          # if node has right child
                right = self._right_child_index(m)          # get right child index
                if self._elem[right] > self._elem[left]:    # if right child is greater than left child
                    max_child = right                       # set max_child to right child index

            if self._elem[m] < self._elem[max_child]:       # if parent is less than max_child
                self._swap(m, max_child)                    # swap parent and max_child
                m = max_child                               # update m to max_child index          
            else:
                break                                       # else break


    # ----------------------- PUBLIC METHODS -------------------------------

    def __init__(self, data=[]):
        """Constructor for MaxHeap class"""
        # data is the list of HeapNode objects
        # TIME COMPLEXITY : O(n)
        self._elem = data                                   # internal array of minheap
        self._locator = {}                                  # dictionary for changing capacity
        
        for obj in data:
            # add keys in dictionary
            self._locator[obj.get_key()] = obj.get_key()

    def is_empty(self):
        """returns True if heap is empty else False"""
        # TIME COMPLEXITY : O(1)
        return len(self._elem) == 0

    def add(self, val):
        """add val in the heap"""
        # val is the object of HeapNode class
        # TIME COMPLEXITY : O(logn)

        # add new val in array
        self._elem.append(val)                              # add new val in array

        self._locator[val.get_key()] = len(self._elem) - 1  # add new value in locator
        self._bubble_up(len(self._elem)-1)                  # move the node up

    def max(self):
        """returns the maximum value"""
        # this function does not remove the maximum from the heap
        # TIME COMPLEXITY : O(1)

        if self.is_empty():                                 # if heap is empty
            raise ValueError("Heap is Empty")               # raise error
        return self._elem[0]                                # return the maximum value

    def remove_max(self):
        """Remove and return the maximum value from the heap"""
        # TIME COMPLEXITY : O(logn)

        if self.is_empty():                                 # if heap is empty  
            raise ValueError("Heap is Empty")               # raise error

        self._swap(0, len(self._elem)-1)                    # swap the first and last element
        val = self._elem.pop()                              # remove the last element             
        self._locator.pop(val.get_key())                    # remove val from locator

        self._bubble_down(0)                                # move the root node down    
        return val                                          # return the removed value                    

    def update_capacity(self, new_cap_obj):
        """update the capacity of a given key if it is greater than current value
        and return True if capacity is updated else return False"""
        # new_cap_obj is an object of HeapNode class
        # TIME COMPLEXITY : O(logn)
        
        key = new_cap_obj.get_key()                         # get the key
        new_cap = new_cap_obj.get_capacity()                # get the new capacity
        
        if self.is_empty():                                 # if heap is empty
            self.add(new_cap_obj)                           # add the new capacity object
            return True                                     # return True

        if self._locator.get(key) == None:                  # if key is not present in heap
            self.add(new_cap_obj)                           # add the new capacity object
            return True                                     # return True

        pos = self._locator[key]                            # get the position of key in heap
        cap_obj = self._elem[pos]                           # get the previous capacity object  
        prev_cap = cap_obj.get_capacity()                   # get the previous capacity

        if new_cap > prev_cap:                              # if new capacity is greater than previous capacity
            # bubble up if value of capacity increases
            cap_obj.set_capacity(new_cap)                   # update the capacity
            self._bubble_up(pos)                            # move the node up
            return True                                     # return True

        return False                                        # return False

    def __str__(self):
        return f'Heap is {self._elem}\nLocator: {self._locator}'


class Graph:
    """Graph representation using adjacency list"""

    def __init__(self, n):
        # n is number of nodes in graph
        # TIME COMPLEXITY : O(1)
        self.n = n                                      # number of nodes
        self.edges = {}                                 # dictionary for storing edges

    
    def addEdge(self, start, end, capacity):       
        """Add edge from start to end with given capacity"""
        # start and end are integers denoting the id of nodes
        # capacity is the capacity of edge
        # TIME COMPLEXITY : O(1)
        
        if start == end:                                # if start and end are same then don't add edge
            return

        if self.edges.get(start) == None:               # if start node is not present in graph
            self.edges[start] = {}                      # add start node in graph
            self.edges[start][end] = capacity           # add edge from start to end with given capacity

        else:
            prev_cap = self.edges[start].get(end, 0)            # get previous capacity
            self.edges[start][end] = max(prev_cap, capacity)    # update capacity if it is greater than previous capacity


    def dijkstra(self, start, end):
        """Dijkstra's algorithm to find maximum capacity path from start to end"""
        # start and end are integers denoting the id of nodes
        # TIME COMPLEXITY : O(mlogn)
        # m is number of edges in graph and n is number of nodes in graph
        # since O(n)=O(m) so O(mlogn) = O(mlogm)

        # Hence TIME COMPLEXITY : O(mlogm)

        is_explored = [False] * self.n                  # array to check if node is explored or not
        prev_path = [None] * self.n                     # array to store previous node in maximum capacity path
        
        heap = MaxHeap([HeapNode(start, INF)])          # create heap with start node and capacity INF

        while heap.max().get_key() != end:              # loop until end node is not explored
            cur_node = heap.remove_max()                # remove node with maximum capacity from heap
            cur_router = cur_node.get_key()
            is_explored[cur_router] = True              # mark current node as explored

            for conn in self.edges[cur_router].keys():  # loop over all connections of current node
                if not is_explored[conn]:               # if connection is not explored
                    if heap.update_capacity(HeapNode(conn, min(cur_node.get_capacity(), self.edges[cur_router][conn]))):    # update capacity of connection if it is greater than current capacity
                        prev_path[conn] = cur_router    # update previous node in maximum capacity path
        
        # found the max cap path as the end node is on top of heap
        end_node = heap.max()                           # get end node from heap
        FINAL_CAPACITY = end_node.get_capacity()        # get maximum capacity of path
        path = []                                       # array to store nodes in maximum capacity path
        cur = end                                       # start from end node
        while cur is not None:                          # loop until start node is not reached        
            path.append(cur)                            # add current node in path
            cur = prev_path[cur]                        # move to previous node in path

        return FINAL_CAPACITY, path[::-1]               # return maximum capacity and path in reverse order

    def __str__(self) -> str:
        s = ''
        for key in self.edges.keys():
            s += f'{key}: {self.edges[key]}\n'

        return s


def findMaxCapacity(n, links, s, t):
    # -----------------------------------------------------------------------
    # | INPUT                                                               |
    # | n   : int   : number of nodes                                       |
    # | links: list : list of tuples (start, end, capacity)                 |
    # | s   : int   : start node                                            |
    # | t   : int   : end node                                              |
    # |                                                                     |
    # | OUTPUT                                                              |
    # | max_cap: int : maximum capacity of the path from s to t             |
    # | path   : list: list of nodes in the path from s to t                |
    # |                                                                     |
    # | Time Complexity : O(mlogm) where m is the number of links           |
    # -----------------------------------------------------------------------

    network = Graph(n)                                  # initialize graph with n nodes

    for link in links:                                  # add all links in graph
        # add edge in both directions since it is an undirected graph
        network.addEdge(link[0], link[1], link[2])          
        network.addEdge(link[1], link[0], link[2])

    return network.dijkstra(s, t)                       # return maximum capacity and path from s to t
