class PointDatabase:

    class _XTreeNode:
        __slots__ = "val",'left','right','ytree'
        def __init__(self,val,ytree,left=None,right=None):
            """Node for X-Tree"""
            self.val = val
            self.left = left 
            self.right = right 
            self.ytree = ytree
        


    class _YTreeNode:
        __slots__ = "val",'left','right'
        def __init__(self,val,left=None,right=None):
            """Node for Y-Tree"""
            self.val = val
            self.left = left 
            self.right = right 
        
    

    # -------------------- Utility functions ------------------------------------------
        
        
    def _check_in_range(self,pt,rng):
        """Return True if the given pt is in the range, False otherwise"""
        # TIME COMPLEXITY : O(1)

        if (abs(pt[0]-rng[0])<=rng[2] and abs(pt[1]-rng[1])<=rng[2]):
            return True
        return False
    

    def _check_x_range(self,x_coord,rng):
        """Return True if x_coord is within the range, False otherwise"""
        # TIME COMPLEXITY : O(1)

        return abs(x_coord-rng[0])<=rng[2]
    

    def _check_y_range(self,y_coord,rng):
        """Return True if y_coord is within the range, False otherwise"""
        # TIME COMPLEXITY : O(1)

        return abs(y_coord-rng[1])<=rng[2]


    def _check_leaf_node(self,node):
        """Return True if the node is None or it is a leaf node, False otherwise"""
        # TIME COMPLEXITY : O(1)

        if node == None:
            return True
        if node.left == None and node.right==None:
            return True
        return False


    def _inorder(self,root,arr):
        """Returns the inorder traversal of the given tree and stores it in arr."""
        # TIME COMPLEXITY : O(n)

        if root:
            self._inorder(root.left,arr)
            arr.append(root.val)
            self._inorder(root.right,arr)

    
    def _merge_sorted_arr(self, arr1, arr2):
        """Merge two sorted arrays arr1 and arr2 store it in arr and then return arr"""
        # TIME COMPLEXITY : O(n)

        arr = []
        i = j = 0
        while i < len(arr1) and j < len(arr2):
            if arr1[i][1] <= arr2[j][1]:
                arr.append(arr1[i])
                i += 1
            else:
                arr.append(arr2[j])
                j += 1
        while i < len(arr1):
            arr.append(arr1[i])
            i += 1
        while j < len(arr2):
            arr.append(arr2[j])
            j += 1
        return arr


    def _arr_to_bst(self,arr):
        """Create a Y-Tree (Balanced BST) from given sorted arr and return the root of the BST."""
        # TIME COMPLEXITY : O(n)

        if not arr:
            return None
        mid = len(arr) // 2
        root = self._YTreeNode(arr[mid])                            # create a node at median
        root.left = self._arr_to_bst(arr[:mid])                     # recursively call the function to create left subtree for points smaller than median
        root.right = self._arr_to_bst(arr[mid + 1:])                # recursively call the function to create right subtree for points greater than median
        return root                                                 # return root


    # ---------------- Utility functions completed ------------------------------------

    # ----------------- Balanced BST creation functions -------------------------------


    def _merge_tree(self,median,t1,t2 = None):
        """Merge two BST and create a new Balanced BST"""
        # TIME COMPLEXITY : O(n)

        arr1 = []
        self._inorder(t1,arr1)                                      # get the inorder traversal of tree t1
        arr2 = []
        self._inorder(t2,arr2)                                      # get the inorder traversal of tree t2
        arr = self._merge_sorted_arr(arr1,arr2)                     # merge the two sorted arrays

        # insert median in this arr by insert() function
        median_inserted = False
        for i in range(len(arr)):
            if arr[i][1]> median[1]:
                arr.insert(i,median)
                median_inserted = True
                break
        if not median_inserted:
            arr.append(median)

        root = self._arr_to_bst(arr)                                # convert the array to Balanced BST
        return root                                                 # return root of merged tree


    def _build_x_tree(self,data):
        """Build the X-Tree (2d Range Tree) on given data"""
        # TIME COMPLEXITY : O(nlog(n))

        if len(data)==0:                                            # Base Case
            return None

        if len(data)==1:                                            # Base Case
            return self._XTreeNode(data[0],self._YTreeNode(data[0]))

        else:
            # divide the data into two halves
            mid = len(data)//2
            x_median = data[mid]
            ltreedata = data[:mid]
            rtreedata = data[mid+1:]

            # recursively create X-Tree on left and right halves
            ltree = self._build_x_tree(ltreedata)
            rtree = self._build_x_tree(rtreedata)

            # Merge the Y-Trees of left and right subtrees
            merged_y_tree = None

            if ltree != None and rtree != None:
                merged_y_tree = self._merge_tree(x_median,ltree.ytree,rtree.ytree)

            elif ltree == None and rtree != None:
                merged_y_tree = self._merge_tree(x_median, rtree.ytree)

            elif ltree != None and rtree == None:
                merged_y_tree = self._merge_tree(x_median, ltree.ytree)

            # create the node having x_median as val, and the the given Y-Tree, left and right subtrees
            root = self._XTreeNode(x_median,merged_y_tree,ltree,rtree)
            return root                                         # return root
    

    # ---------------------- bst creation function completed -----------------------------
    
    # ------------------------- Search functions -----------------------------------------

    def _find_split_node(self, root, mid, d, param):
        """Find the split node for the given range (mid,d)"""
        # Used for both X and Y Trees
        # TIME COMPLEXITY : O(log(n))

        snode = root                                                    # start the search from root
        while snode != None:
            if snode.val[param]>=mid-d and snode.val[param]<=mid+d:     # if the val at this point lies within the range then break as this is the split node
                break

            elif mid + d < snode.val[param]:                            # if the val lies to the right of range then move left
                snode = snode.left
            
            elif  mid - d > snode.val[param]:                           # if the val lies to the left of range then move right
                snode = snode.right

        return snode                                                    # return the split node


    def _search_y_tree(self,root,rng,nodes):
        """Range query for Y-Tree (1d Range Query)"""
        # TIME COMPLEXITY : O(m + log(n))

        s_node = self._find_split_node(root,rng[1],rng[2],1)            # find the split node

        if s_node == None:                                              # Base case
            return
        
        if self._check_y_range(s_node.val[1],rng):                      # if val at split node lies within the range then append it to nodes list
            nodes.append(s_node.val)
        
        v = s_node.left                                                 # search in left subtree of split_node
        while not self._check_leaf_node(v):
            if self._check_y_range(v.val[1],rng):                       # if current point lies in y range then search the right subtree of Y-Tree
                nodes.append(v.val)
                self._search_y_tree(v.right,rng,nodes)
                v = v.left                                              # and then move left
            else:                                                       # else move right
                v = v.right
        
        if v != None and self._check_y_range(v.val[1],rng):             # check leaf node
            nodes.append(v.val)
        
        v = s_node.right                                                # search in right subtree of split_node
        while not self._check_leaf_node(v):
            if self._check_y_range(v.val[1],rng):                       # if current point lies in y range then search the left subtree of Y-Tree
                nodes.append(v.val)
                self._search_y_tree(v.left,rng,nodes)
                v = v.right                                             # and then move right
            else:                                                       # else move left
                v = v.left
        
        if v != None and self._check_y_range(v.val[1],rng):              # check leaf node
            nodes.append(v.val)


    def _search_x_tree(self,root,rng,ans):
        """Range Query for X-Tree(2d Range Query)"""
        # TIME COMPLEXITY : O(m + log^2(n))

        s_node = self._find_split_node(root,rng[0],rng[2],0)            # find the split node

        if s_node == None:                                              # Base case
            return 

        if self._check_leaf_node(s_node):                               # Base case
            if self._check_in_range(s_node.val,rng):
                ans.append(s_node.val)
            return
        
        if self._check_in_range(s_node.val,rng):                        # if val at split node is in range then append it to ans
            ans.append(s_node.val)

        # Search in the left subtree of split node
        v = s_node.left

        while not self._check_leaf_node(v):
            # if current point is greater than the lower limit of x then check if this point is in range and then search the right subtree of this node
            if rng[0]-rng[2]<=v.val[0]:
                if self._check_in_range(v.val,rng):
                    ans.append(v.val)
                # Search on Y- Tree for the right subtree of v
                if v.right != None:
                    self._search_y_tree(v.right.ytree,rng,ans)
                v = v.left                                  # move towards left
            
            else:                               # else move right
                v = v.right
        
        # check if the leaf node is within range
        if v != None and self._check_in_range(v.val,rng):
            ans.append(v.val)
        

        # Search in the right subtree of split node
        v = s_node.right

        while not self._check_leaf_node(v):
            # if current point is lesser than the upper limit of x then check if this point is in range and then search the left subtree of this node
            if rng[0]+rng[2]>=v.val[0]:
                if self._check_in_range(v.val,rng):
                    ans.append(v.val)
                # Search on Y- Tree for the left subtree of v
                if v.left != None:
                    self._search_y_tree(v.left.ytree,rng,ans)
                v = v.right                             # move towards right
            
            else:                               # else move left
                v = v.left
        # check if the leaf node is within range
        if v != None and self._check_in_range(v.val,rng):
            ans.append(v.val)


    # ---------------------- Search functions completed --------------------------------------

    # --------------------------- PUBLIC METHODS ----------------------------------------------


    def __init__(self,pointlist):
        """Creates a 2d Range Tree based on given pointlist"""

        # -----------------------------------------------------------------------------------
        # | INPUT                                                                           |
        # | pointlist : List[tuple()] - list of points (x,y)                                |
        # |                                                                                 |
        # | OUTPUT  : None                                                                  |
        # |                                                                                 |
        # | TIME COMPLEXITY : O(nlog(n))                                                    |
        # -----------------------------------------------------------------------------------

        pointlist.sort()                                        # sort the given pointlist based on x coordinates
        self.tree = self._build_x_tree(pointlist)               # build the 2d range tree and store its root at self.tree


    def searchNearby(self,q,d):
        """Return the points within distance d of q from the pointlist."""

        # -----------------------------------------------------------------------------------
        # | INPUT                                                                           |
        # | q : (x,y) - tuple (x,y)                                                         |
        # | d : int   - distance d                                                          |
        # |                                                                                 |
        # | OUTPUT                                                                          |
        # | results : List[tuple()] - List of points (x,y) which are within l-infinite      |
        # | distance d from q                                                               |
        # |                                                                                 |
        # | TIME COMPLEXITY : O(m + log^2(n))                                               |
        # -----------------------------------------------------------------------------------

        rng = (q[0],q[1],d)                                 # store the parameters of range in a tuple
        results = []                                        # initialize a empty list

        self._search_x_tree(self.tree, rng, results)        # query the range tree

        return results                                      # return results
