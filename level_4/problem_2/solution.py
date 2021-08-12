from copy import deepcopy

"""
The problem is of the max flow problem in graph theory and to solve it we used the 
Edmonds-Karp Algorithm the algorithm is as follows

algorithm Edmonds-Karp is
    input:
        graph   (graph[v] should be the list of edges coming out of vertex v in the
                 original graph and their corresponding constructed reverse edges
                 which are used for push-back flow.
                 Each edge should have a capacity, flow, source and sink as parameters.)
        s       (Source vertex)
        t       (Sink vertex)
    output:
        flow    (Value of maximum flow)
    
    flow := 0   (Initialize flow to zero)
    repeat
        (Run a breadth-first search (bfs) to find the shortest s-t path.
         We use 'pred' to store the edge taken to get to each vertex,
         so we can recover the path afterwards)
        q := queue()
        q.push(s)
        pred := array(graph.length)
        while not empty(q)
            cur := q.pull()
            for Edge e in graph[cur] do
                if pred[e.t] = null and e.t != s and e.cap > e.flow then
                    pred[e.t] := e
                    q.push(e.t)

        if not (pred[t] = null) then
            (We found an augmenting path.
             See how much flow we can send) 
            df := inf
            for (e := pred[t]; e != null; e := pred[e.s]) do
                df := min(df, e.cap - e.flow)
            (And update edges by that amount)
            for (e := pred[t]; e != null; e := pred[e.s]) do
                e.flow  := e.flow + df
            flow := flow + df

    until pred[t] = null  (i.e., until no augmenting path was found)
    return flow


The running time of O(|V||E|^{2}) is found by showing that each augmenting path can be found in O(|E|) time, 
that every time at least one of the E edges becomes saturated (an edge which has the maximum possible flow), 
that the distance from the saturated edge to the source along the augmenting path must be longer than last time it was saturated,
and that the length is at most |V|. 
Another property of this algorithm is that the length of the shortest augmenting path increases monotonically
"""



class EdgeFlow:
    """
    Edge object containing flow, capacity and its start and end
    """
    def __init__(self,start, end, capacity):
        self.flow = 0
        self.capacity = capacity
        self.start = start
        self.end = end

class FlowGraph:
    
    def __init__(self, entries, exits, adj_mat):
        self.adj_mat = adj_mat
        self.entries = entries
        self.exits = exits
        self.total_flow = 0
        
        self.total_nodes = len(self.adj_mat[0])
        self.add_source() # adding source
        self.add_sink() # adding sink
        self.create_edge_list() # creating edge objects
    
    def add_sink(self):
        """
        adds the sink(t) at the last place
        with infinite capacity corridor
        """
        sinks = [0 for _ in range(self.total_nodes+1)]
        for pos in range(self.total_nodes):
            current_val = self.adj_mat[pos]
            to_add = float('inf') if pos in self.exits else 0
            current_val.append(to_add)
            self.adj_mat[pos] = deepcopy(current_val)
        self.total_nodes += 1
        
        self.adj_mat.append(sinks)
        
    
    def add_source(self):
        """
        adds the source(s) in the first place
        with infinite capacity corridor
        
        and adjusts the positions of entries and exits
        """
        self.total_nodes += 1
        
        self.exits = [e+1 for e in self.exits]
        self.entries = [e+1 for e in self.entries]
        
        source = [float('inf') if pos in self.entries else 0 for pos in range(self.total_nodes)]
        self.adj_mat = [source] + self.adj_mat
        
        for pos in range(1,self.total_nodes):
            current_val = self.adj_mat[pos]
            current_val = [0] + current_val
            self.adj_mat[pos] = deepcopy(current_val)
            
    def create_edge_list(self):
        """
        Creates edge object
        """
        self.edge_flow = []
        for start_node in range(self.total_nodes):
            edge_list = [EdgeFlow(start_node, end_node, self.adj_mat[start_node][end_node])
                             for end_node in range(self.total_nodes)]
            self.edge_flow.append(deepcopy(edge_list))
        
        
    def get_neighbors(self,node):
        """
        Returns the neighbors of an node
        """
        connections = self.adj_mat[node]
        neigh = [node for node,val in enumerate(connections) if val > 0]
        
        return neigh
    
    def path_edges(self,path):
        """
        Returns edges in the said path
        """
        edge_list = list(zip(path[:-1],path[1:]))
        return edge_list
    
    def bfs_search(self):
        """
        Runs a BFS search from source 0th node to sink node
        it returns the least length path using non-saturated nodes
        """

        queue = [(0,0)] # level and the position of the sink
        aug_path = {(0,0):[0]} # level,last_index store to path storage
        min_path = [] # one storing the min path
        visited = set()
        while len(queue) > 0:
            prev_level, queue_node = queue[0]
            queue = queue[1:]
            visited.add(queue_node)
            neigh = self.get_neighbors(queue_node)
            neigh = [i for i in neigh if i not in visited]
            level = prev_level + 1 # current level of the bfs
            path = aug_path[(prev_level,queue_node)]
            for node in neigh:
                edge = self.edge_flow[queue_node][node]
                if edge.capacity > edge.flow:
                    aug_path[(level,node)] = path + [node]
                    
                    if node+1 == self.total_nodes:
                        queue = []
                        min_path = path +[node]
                    else:
                        
                        queue.append((level, node))
        
        return self.path_edges(min_path)
    
    def get_flow(self):
        """
        Run a breadth-first search (bfs) to find the shortest s-t path.
         We use 'aug_path' to store the edge taken to get to each vertex,
         so we can recover the path afterwards
        """
        
        # run until no improvement in the self.total_flow can be made
        while True:
            
            aug_path = self.bfs_search()
            
            if len(aug_path) > 0:
                edges = [self.edge_flow[edge[0]][edge[1]]
                             for edge in aug_path]
                min_flow = min([(e.capacity - e.flow) for e in edges])
                for e in edges:
                    e.flow = e.flow + min_flow
            else:
                break
            self.total_flow += min_flow
                
        return self.total_flow
    

def solution(entrances, exits, path):
    obj = FlowGraph(entrances, exits, path)
    return int(obj.get_flow())

if __name__ == "__main__":

    print(solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
    print(solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]]))