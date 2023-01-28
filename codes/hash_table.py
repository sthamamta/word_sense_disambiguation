

# Node data structure - essentially a LinkedList node
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
    def __str__(self):
        return "<Node: (%s, %s), next: %s>" % (self.key, self.value, self.next != None)
    def __repr__(self):
        return str(self)

# Hash table with separate chaining
class HashTable:
    # Initialize hash table
    def __init__(self, maxSize):
        self.capacity = maxSize
        self.size = 0
        self.buckets = [None]*self.capacity
    # Generate a hash for a given key
    
    def hash(self, key):
        hashsum = 0
        # For each character in the key
        for idx, c in enumerate(key):
            hashsum += (idx + len(key)) ** ord(c)
            hashsum = hashsum % self.capacity
        return hashsum

    # Insert a key,value pair to the hashtable    
    def insert(self, key, value):
        self.size += 1
        index = self.hash(key)
        node = self.buckets[index]
        if node is None:
            self.buckets[index] = Node(key, value)
            return
        prev = node
        while node is not None:
            prev = node
            node = node.next
        # Add a new node at the end of the list with provided key/value
        prev.next = Node(key, value)

    # Find a data value based on key    
    def find(self, key):
        index = self.hash(key)
        node = self.buckets[index]
        while node is not None and node.key != key:
            node = node.next
        if node is None:
            #insert new bigram and add frequency 1
            self.insert(key, 1)
        else:
            # update this bigram frequency
            node.value = node.value+1
            return node.value
        
    #retrieving all hashtable elements
    def getBgs(self, capacity):
        count = 0
        temp = []
        bgFreq= []
        for index in range(capacity):

            node = self.buckets[index]
            # 3. Traverse the linked list at this node
            while node is not None:
                if node.value > 1:
                    temp.extend([node.key, node.value])
                    bgFreq.append(temp)
                temp = []
                count += node.value
                node = node.next
        return bgFreq
