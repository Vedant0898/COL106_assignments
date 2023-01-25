
# --------------------------- CLASS DEFINITION --------------------------------------------------
class Object:
    """Class for details of each object"""
    def __init__(self,i,m,x,v,t=0):
        self._index = i     # index of object
        self.m = m          # mass of object
        self.x = x          # position of object
        self.v = v          # velocity of object
        self._t = t         # time at which position of object is recorded
    
    def get_projected_pos(self,new_time):
        """return the position of object at given time"""
        # helper function for calculating time of collision
        delta_t = new_time-self._t
        if(delta_t<=0):
            return self.x
        
        new_x = self.x + delta_t * self.v
        return new_x

    def update_time(self,new_time):
        """update time and calculate new position of the object"""
        delta_t = new_time-self._t
        if(delta_t<=0):
            return
        
        self.x = self.x + delta_t * self.v
        self._t = new_time
    
    def update_pos_and_time(self,new_time,new_pos):
        """update both position and time by given value"""
        # using this function when objects collide instead of "update_time" to 
        # avoid precision issue in floats 
        delta_t = new_time-self._t
        if(delta_t<=0):
            return
        self._t = new_time
        self.x = new_pos
    
    def __str__(self):
        return f'i:{self._index}\tm:{self.m}\tx:{self.x}\tv:{self.v}\tt:{self._t}'



class Time:
    """Class for storing time and index"""

    def __init__(self,i,time):
        self._time = time           # time of collision between objects with index i and i+1
        self._index = i             # index i
    
    def get_key(self):
        return self._index          # getter method for index/key
    
    def get_time(self):
        return self._time           # getter method for time
    
    def set_time(self,new_time):
        self._time = new_time       # setter method for time

    def __lt__(self,other):
        # less than operator overloading to compare with other time objects
        # return true if time is lower or if it is equal then returns true for object 
        # with smaller index else returns false
        return (self._time < other._time) or (self._time==other._time and self._index < other._index)
    
    def __gt__(self,other):
        # greater than operator overloading to compare with other time objects
        return (self._time > other._time) or (self._time==other._time and self._index > other._index)
    
    def __str__(self):
        return f'i:{self._index}\t\ttime:{self._time}'



class MinHeap:
    """Min Heap class"""       
    # -------------------------- NON PUBLIC METHODS -------------------------------

    def _parent_index(self,m):
        # returns index of parent
        return (m-1)//2
    
    def _left_child_index(self,m):
        # returns index of left child
        return (2*m+1)
    
    def _right_child_index(self,m):
        # returns index of right child
        return (2*m+2)
    
    def _has_parent(self,m):
        # returns False if the given node is root else True
        return self._parent_index(m)>=0
    
    def _has_left(self,m):
        # returns True if node has left child else False
        return self._left_child_index(m)<len(self._elem)
    
    def _has_right(self,m):
        # returns True if node has right child else False
        return self._right_child_index(m)<len(self._elem)
    
    def _swap(self,x,y):
        # swap node at position x and y
        self._locator[self._elem[x].get_key()] = y
        self._locator[self._elem[y].get_key()] = x
        self._elem[x],self._elem[y] = self._elem[y],self._elem[x]

    def _bubble_up(self,m):
        # swap the element with its parent to get it to correct position
        while self._has_parent(m):
            par = self._parent_index(m)
            if self._elem[m]<self._elem[par]:
                self._swap(m,par)
                m = par
            else:
                break
    
    def _bubble_down(self,m):
        # swap the element with child having minimum value to get it to correct position
        while self._has_left(m):
            left = self._left_child_index(m)
            min_child = left

            if self._has_right(m):
                right = self._right_child_index(m)
                if self._elem[right]<self._elem[left]:
                    min_child = right
            
            if self._elem[m]>self._elem[min_child]:
                self._swap(m,min_child)
                m = min_child
            else:
                break
    

    def _heapify(self):
        # heapify the given data
        start  = self._parent_index(len(self._elem)-1)
        for i in range(start,-1,-1):
            self._bubble_down(i)
        
    # ----------------------- PUBLIC METHODS -------------------------------


    def __init__(self,data = []):
        self._elem = data                                   # internal array of minheap
        self._locator = {}                                  # dictionary for changing time
        for obj in data:
            self._locator[obj.get_key()] = obj.get_key()    # add keys in dictionary
        if len(data)>1:
            self._heapify()                                 # heapify the given data


    def is_empty(self):
        # return true if heap is empty
        return len(self._elem)==0

    def add(self,val):
        """add val in the heap"""

        self._elem.append(val)                              # add new val in array

        self._locator[val.get_key()] = len(self._elem)-1    # add new value in locator
        self._bubble_up(len(self._elem)-1)                  # move the node up
    
    def min(self):
        """returns the minimum value"""
        # this function does not remove the minimum from the heap
        # TIME COMPLEXITY : O(1)

        if self.is_empty():
            raise ValueError("Heap is Empty")
        return self._elem[0]

    def remove_min(self):
        """Remove and return the minimum value from the heap"""
        # TIME COMPLEXITY : O(logn)

        if self.is_empty():
            raise ValueError("Heap is Empty")
        
        self._swap(0,len(self._elem)-1)
        val =  self._elem.pop()
        self._locator.pop(val.get_key())                    # remove val from locator
        
        self._bubble_down(0)
        return val
    
    def change_time(self,new_t_obj):
        """update the time of a given key"""
        # TIME COMPLEXITY : O(logn)
        
        key = new_t_obj.get_key()
        new_time = new_t_obj.get_time()
        if self.is_empty():
            raise ValueError("Heap is Empty")
        
        if self._locator.get(key)==None:
            raise ValueError(f"Key not present key={key}")

        pos = self._locator[key]
        t_obj = self._elem[pos]
        prev_time = t_obj.get_time()
        t_obj.set_time(new_time)

        if prev_time> new_time:
            self._bubble_up(pos)                    # bubble up if value of time decreases
        else:
            self._bubble_down(pos)                  # bubble down if value of time increases

    def __str__(self):
        return f'Heap is {self._elem}\nLocator: {self._locator}'


# constants
INF = float('inf')                                  # infinite time if collision does not take place
PRECISION = 4                                       # precision of round function

# global variables
curr_time = 0                                       # time elapsed
object_lst = []                                     # global list of all objects


# ----------------------- UTILITY Functions ----------------------------------------------------

def calculate_time_for_collision(i):
    """Calculate time for collision between i and i+1 object"""
    # -----------------------------------------------------------------------------------
    # | INPUT - i                                                                       |
    # |     i : index (int)                                                             |
    # |                                                                                 |
    # | OUTPUT - Time(i,t)                                                              |
    # |     t : time of collision                                                       |
    # |                                                                                 |
    # | TIME COMPLEXITY : O(1)                                                          |
    # -----------------------------------------------------------------------------------
    
    o1 = object_lst[i]
    o2 = object_lst[i+1]

    x1 = o1.get_projected_pos(curr_time)
    x2 = o2.get_projected_pos(curr_time)

    if o1.v==o2.v:
        return Time(i,INF)
    
    t = (x2-x1)/(o1.v-o2.v)
    if t<=0:
        return Time(i,INF)
    return Time(i,curr_time+t)


def calculate_position_of_collision(i):
    """Calculate the position at which objects i and i+1 will collide"""
    # -----------------------------------------------------------------------------------
    # | INPUT - i                                                                       |
    # |     i : index (int)                                                             |
    # |                                                                                 |
    # | OUTPUT - x                                                                      |
    # |     x : position of collision                                                   |
    # |                                                                                 |
    # | TIME COMPLEXITY : O(1)                                                          |
    # -----------------------------------------------------------------------------------
    
    o1 = object_lst[i]                                  # get object i
    o2 = object_lst[i+1]                                # get object i+1
    x = o1.v * (o2.x - o1.x)/(o1.v - o2.v) + o1.x       # find position of collision
    return x


def update_velocity_after_collision(i):
    """Update velocity of objects i and i+1 after collision"""
    # -----------------------------------------------------------------------------------
    # | INPUT - i                                                                       |
    # |     i : index (int)                                                             |
    # |                                                                                 |
    # | OUTPUT - None                                                                   |
    # |                                                                                 |
    # | TIME COMPLEXITY : O(1)                                                          |
    # -----------------------------------------------------------------------------------

    o1 = object_lst[i]                                  # get object i
    o2 = object_lst[i+1]                                # get object i+1
    
    x = calculate_position_of_collision(i)              # find position of collision

    v1 = (o1.m - o2.m) * o1.v/(o1.m + o2.m) + 2 * o2.m * o2.v/(o1.m + o2.m)     # new vel of object i
    v2 = (o2.m - o1.m) * o2.v/(o1.m + o2.m) + 2 * o1.m * o1.v/(o1.m + o2.m)     # new vel of object i+1

    o1.update_pos_and_time(curr_time,x)                 # update object's pos and time
    o2.update_pos_and_time(curr_time,x)                 # update object's pos and time

    o1.v = v1                                           # update vel of object i
    o2.v = v2                                           # update vel of object i+1


# ------------------------- Function Implementation --------------------------------------------
def listCollisions(M,x,v,m,T):
    """Find the collisions for given date"""
    # -----------------------------------------------------------------------------------
    # | INPUT - M,x,v,m,T                                                               |
    # |     M : list of mass of objects                                                 |
    # |     x : list of positions of object                                             |
    # |     v : list of initial veloctiy of objects                                     |
    # |     m : maximum number of collisions to return                                  |
    # |     T : Time upto which collision should be returned                            |
    # |                                                                                 |
    # | OUTPUT - collisions                                                             |
    # |     collisions : list of tuple(t,i,x)                                           |
    # |     t : time of collision                                                       |
    # |     i : index of colliding objects                                              |
    # |     x : position of collision                                                   |
    # |                                                                                 |
    # | TIME COMPLEXITY : O(n+m*logn)                                                   |
    # -----------------------------------------------------------------------------------

    global curr_time,object_lst                         # access global variable
    curr_time = 0                                       # reset global variable initially
    object_lst = []                                     # reset global variable
    
    n = len(M)
    
    if n<2:                                             # handle edge case for n<2
        return []

    # combine M,x,v and i of each object in 'Object' class and append all the objects in 'object_lst'
    for i in range(n):
        obj = Object(i,M[i],x[i],v[i])
        object_lst.append(obj)
    
    # list for storing initial values of collision times for adjacent objects
    initial_collision_times = []

    # find time of collision between adjacent objects
    for i in range(n-1):
        initial_collision_times.append(calculate_time_for_collision(i))
    
    # create a MinHeap from 'initial_collision_times' and heapify the data
    time_heap = MinHeap(initial_collision_times)
    
    coll_counter = 0                                        # current number of collision
    collisions = []                                         # final collision list
    
    while coll_counter<m and time_heap.min().get_time()<=T:
        t_obj = time_heap.remove_min()                      # extract min from 'time_heap'
        index = t_obj.get_key()                             # get index 'i' from 't_obj'
        o1 = object_lst[index]                              # get object i from 'object_lst'
        o2 = object_lst[index+1]                            # get object i+1 from 'object_lst'

        o1.update_time(curr_time)                           # update object's position and time
        o2.update_time(curr_time)                           # to 'curr_time'

        curr_time = t_obj.get_time()                        # update 'curr_time'

        x = calculate_position_of_collision(index)          # calculate x

        current_collision = (round(curr_time,PRECISION),index,round(x,PRECISION))    # collision tuple
        collisions.append(current_collision)                # append in 'collision'
        coll_counter+=1                                     # increase 'coll_counter'
        
        update_velocity_after_collision(index)              # update velocity of object i and i+1
        time_heap.add(calculate_time_for_collision(index))  # add new time in 'time_heap'

        if index>0:                                         # check if there is a left neighbour
            time_heap.change_time(calculate_time_for_collision(index-1))     # update 'time' for objects i-1 and i
        
        if index < n-2:                                     # check if there is a right neighbour
            time_heap.change_time(calculate_time_for_collision(index+1))     # update 'time' for objects i and i+1
        
    return collisions