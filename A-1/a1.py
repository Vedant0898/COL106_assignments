class Stack:

    def __init__(self):
        """Stack implementation with Dynamic list resizing"""
        self._elem = [None]*8
        self._len = 0
        self._capacity = 8
    
    def is_empty(self):
        # returns true is stack is empty else false
        return self._len==0

    def _resize(self,capacity):
        # resize internal list (_elem) to given capacity and update _capacity
        new_lst = [None]*capacity
        for i in range(self._len):
            new_lst[i] = self._elem[i]
        
        self._elem = new_lst
        self._capacity = capacity

    def pop(self):
        # removes last element and returns its value
        # raises ValueError if Stack is Empty
        if self.is_empty():
            raise ValueError('Stack is empty')
        else:
            val = self._elem[self._len-1]
            self._elem[self._len-1] = None
            self._len-=1
            if self._len*4<self._capacity and self._capacity>8:
                self._resize(self._capacity//2)         # resize to half capacity 
            return val
    
    def push(self,val):
        # add given val to end of stack and resize to double capacity if required
        if self._len==self._capacity:
            self._resize(2*self._capacity)              # resize to double capacity
        
        self._elem[self._len] = val
        self._len+=1

    def top(self):
        # returns the last element of stack
        if self.is_empty():
            raise ValueError('Stack is empty')
        
        else:
            val = self._elem[self._len-1]
            return val

    def __str__(self):
        return f"Cap:{self._capacity}\tLen:{self._len}\nElem:{self._elem}\n"



class Vector:

    def __init__(self):
        """Represent position vector and distance moved"""
        # first 3 elements denote X,Y,Z coordinates
        # last element denotes distance moved
        self._vect = [0,0,0,0]

    def move(self,direction,axis):
        """Move according to direction and axis"""
        # Direction can be '+' or '-'
        # Axis can be 'X','Y' or 'Z'

        if (direction=="+"):
            if axis=="X":
                self[0]+=1
            elif axis=="Y":
                self[1]+=1
            elif axis=="Z":
                self[2]+=1
            else:
                return
            
            self[3]+=1
            
        elif (direction=="-"):
            if axis=="X":
                self[0]-=1
            elif axis=="Y":
                self[1]-=1
            elif axis=="Z":
                self[2]-=1
            else:
                return
            
            self[3]+=1

    def to_list(self):
        # converts vector to list
        return self._vect

    def __getitem__(self,pos):
        # operator overloading for syntax like vector[i]
        return self._vect[pos]
    
    def __setitem__(self,pos,val):
        # operator overloading for syntax like vector[i] = val
        self._vect[pos] = val

    def __mul__(self,factor):
        # operator overloading to multiply a vector by given factor
        result = Vector()
        if isinstance(factor,int):
            for i in range(4):
                result[i]=self[i]*factor
            return result
        else:
            raise ValueError("factor must be int")
    
    def __rmul__(self,factor):
        # operator overloading
        return self*factor
    
    def __add__(self,other):
        # operator overlaoding to add two vectors
        result = Vector()
        for i in range(4):
            result[i] = self[i]+other[i]
        return result
    
    def __radd__(self,other):
        # operator overloading
        return self + other
    
    def __str__(self):
        s = "Pos. vector is ({},{},{})\nDist. moved is {}".format(*self._vect)
        return s



def is_dir(c)->bool:
    """Check if given character 'c' is + or -"""
    if c in ["+","-"]:
        return True
    return False
    

def is_axis(c)->bool:
    """Check if given character 'c' is an axis('X','Y','Z')"""
    if c in ["X","Y","Z"]:
        return True
    return False


def is_num(c)->bool:
    """Check if given character 'c' is a number"""
    asc = ord(c)
    if asc>=48 and asc<=57:
        return True
    return False


def extract_number(s_arr,start_index)->int:
    """Finds the number starting from start_index until a non-numeric char is found"""

    # -------------------------------------------------------------------
    # | INPUT:                                                          |
    # | s_arr(List[]) : input string converted to array for             |
    # |                  pass by reference                              |
    # | start_index(List[]) : a list containing 1 int for               |
    # |                       pass by reference                         |
    # |                                                                 |
    # | OUTPUT:                                                         |
    # | val(int) : value of number before a bracket                     |
    # -------------------------------------------------------------------

    val = 0
    while start_index[0]<len(s_arr) and is_num(s_arr[start_index[0]]):
        d = int(s_arr[start_index[0]])
        start_index[0]+=1
        val = val*10+d
    
    return val


def movement(s_arr)-> Vector:
    """Return the final position and distance travelled in form of Vector"""

    # -------------------------------------------------------------------
    # | INPUT:                                                          |
    # | s_arr(List[]) : input string converted to array for             |
    # |                  pass by reference                              |
    # |                                                                 |
    # | OUTPUT:                                                         |
    # | ans(Vector()) : object of class Vector                          |
    # -------------------------------------------------------------------

    bracket_level = 0
    vect_stack = Stack()                        # to store object of class Vector
    factor_stack = Stack()                      # to store the factors m of m(P)

    pos = [0]                                   # stores current index in list for pass by referenece to other functions
    n = len(s_arr)                              

    while pos[0]<n:
        if is_num(s_arr[pos[0]]):
            # extract number and save in fact_stack
            num = extract_number(s_arr,pos)
            factor_stack.push(num)
        
        elif s_arr[pos[0]]=="(":
            # create a new vector for bracket opening
            bracket_level+=1
            vect_stack.push(Vector())
            pos[0]+=1
        
        elif pos[0]<n-1 and is_dir(s_arr[pos[0]]) and is_axis(s_arr[pos[0]+1]):
            # make the movement for drone
            dir = s_arr[pos[0]]
            axis = s_arr[pos[0]+1]

            vect = vect_stack.top()        # get reference to modify vector
            vect.move(dir,axis)             # since move method changes the vector inplace
            
            pos[0]+=2
        
        elif s_arr[pos[0]]==")":
            # multiply top vector in vect_stack with topmost factor in factor_stack 
            # and add it to previous vector
            bracket_level-=1
            pos[0]+=1
            vect = vect_stack.pop()         # need to pop and push again as mul returns new vector
            fact = factor_stack.pop()
            vect = fact*vect                # use of operator overloading in Vector class
            if bracket_level!=0:
                prev_vect = vect_stack.pop()
                prev_vect = prev_vect+vect
                vect_stack.push(prev_vect)
            else:
                vect_stack.push(vect)       # if it is last vector push it in stack
        else:
            raise ValueError("Invalid syntax for Drone programme")

    ans = Vector()                          # create an empty vector for blank case

    if not vect_stack.is_empty():
        ans = vect_stack.pop()              # get ans from vect_stack

    return ans                              # return ans in vector form


def findPositionandDistance(P):
    
    if type(P)!=str:
        raise ValueError("Drone programme must be a string")

    s = "1("+P+")"                          # change 'P' to 1(P)
    s_arr = list(s)                         # convert string to char array for pass by reference

    vect = movement(s_arr)                  # get ans in vector form

    return vect.to_list()                   # return ans in list form
