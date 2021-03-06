"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        try:
            self.vertices[v2]
            self.vertices[v1].add(v2)
        except KeyError:
            print(
                f'At least one of the vertices you supplied ({v1}, {v2}) does not exist in the graph.')

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # Check for a valid starting vertex
        try:
            self.vertices[starting_vertex]
        except KeyError:
            return f'The starting vertex you supplied ({starting_vertex}) does not exist in the graph.'
        # Set up traversal record, queue, and color record for visited vertices
        traversal = []
        q = Queue()
        visited = {i: 'white' for i in self.vertices}
        # Seed the queue with the starting vertex and color it grey
        q.enqueue(starting_vertex)
        visited[starting_vertex] = 'grey'
        # Once the queue is empty, we're done. NOTE: This implementation will only traverse the graph component of which the starting vertex is a member.
        while q.size() > 0:
            # unvisited = the set of valid neighbors minus the set of already visited vertices
            unvisited = self.vertices[
                q.queue[0]] - set(k for k, v in visited.items() if v != 'white')
            # Put each unvisited neighbor vertex in the queue and color it grey.
            for i in unvisited:
                q.enqueue(i)
                visited[i] = 'grey'
            # Now we're finished with the current vertex. Put it in the traversal record, then remove it from the queue and color it black.
            traversal.append(q.queue[0])
            visited[q.dequeue()] = 'black'
        # Return the traversal record
        return traversal

    def bft_brady(self, starting_vertex):
        visited = set()
        q = Queue()
        q.enqueue(starting_vertex)
        while q.size() > 0:
            v = q.dequeue()
            if v not in visited:
                visited.add(v)
                for neighbor in self.vertices[v]:
                    q.enqueue(neighbor)
        return visited

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # Check for a valid starting vertex
        try:
            self.vertices[starting_vertex]
        except KeyError:
            return f'The starting vertex you supplied ({starting_vertex}) does not exist in the graph.'
        # Set up traversal record, stack, and color record for visited vertices
        traversal = []
        s = Stack()
        visited = {i: 'white' for i in self.vertices}
        # Seed the stack with the starting vertex and color it grey
        s.push(starting_vertex)
        visited[starting_vertex] = 'grey'
        # Once the stack is empty, we're done. NOTE: This implementation will only traverse the graph component of which the starting vertex is a member.
        while s.size() > 0:
            # Since the stack is LIFO, we note the index of the current vertex.
            current = len(s.stack) - 1
            # unvisited = the set of valid neighbors minus the set of already visited vertices
            unvisited = self.vertices[
                s.stack[len(s.stack) - 1]] - set(k for k, v in visited.items() if v != 'white')
            # Put each unvisited neighbor vertex in the stack and color it grey.
            for i in unvisited:
                s.push(i)
                visited[i] = 'grey'
            # If the current vertex is still on top of the stack, then it has no unvisited neighbors, and therefore has reached the full depth. We add it to the front of the traversal record (since the vertices are completed in reverse order), then remove it from the stack and color it black.
            if current == len(s.stack) - 1:
                traversal.insert(0, s.stack[len(s.stack) - 1])
                visited[s.pop()] = 'black'
        # Return the traversal record
        return traversal

    def dft_brady(self, starting_vertex):
        visited = set()
        s = Stack()
        s.push(starting_vertex)
        while s.size() > 0:
            v = s.pop()
            if v not in visited:
                visited.add(v)
                for neighbor in self.vertices[v]:
                    s.push(neighbor)
        return visited

    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        This should be done using recursion.
        """
        # Check for a valid starting vertex
        try:
            self.vertices[starting_vertex]
        except KeyError:
            return f'The starting vertex you supplied ({starting_vertex}) does not exist in the graph.'
        # Set up traversal record and color record for visited vertices
        traversal = []
        visited = {i: 'white' for i in self.vertices}

        # Recursive function nested within main function
        def recurse(vertex):
            # Color each visited vertex grey
            visited[vertex] = 'grey'
            # Determine unvisited neighbors
            unvisited = self.vertices[vertex] - \
                set(k for k, v in visited.items() if v != 'white')
            # Call this function on each unvisited neighbor
            for i in unvisited:
                recurse(i)
            # Once all neighbors have been visited, color vertex black and add it to the front of the traversal record (see explanation in DFT, above)
            visited[vertex] = 'black'
            traversal.insert(0, vertex)
        # Start the recursion with the starting vertex
        recurse(starting_vertex)
        # Return the traversal record
        return traversal

    def dft_recursive_brady(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        This should be done using recursion.
        """
        if visited == None:
            visited = set()
        # If the node hasn't been visited
        if starting_vertex not in visited:
            # Mark the node as visited
            print(starting_vertex)
            visited.add(starting_vertex)
            for neighbor in self.vertices[starting_vertex]:
                self.dft_recursive_brady(neighbor, visited)

        # Then call dft_recursive_brady on each child

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        try:
            self.vertices[starting_vertex]
            self.vertices[destination_vertex]
        except KeyError:
            return f'At least one of the vertices you supplied ({starting_vertex}, {destination_vertex}) does not exist in the graph.'

        # Since full paths are stored in the queue, no separate traversal record is needed.
        q = Queue()
        visited = {i: 'white' for i in self.vertices}

        q.enqueue([starting_vertex])
        visited[starting_vertex] = 'grey'

        while q.size() > 0:
            # This time, unvisited = the set of valid neighbors _of the last vertex in first path in the queue_ minus the set of already visited vertices
            unvisited = self.vertices[
                q.queue[0][len(q.queue[0]) - 1]] - set(k for k, v in visited.items() if v != 'white')
            for i in unvisited:
                # (I think) we need to make a deep copy (copy by value) of the path in order to append each new vertex to their own copy of the path.
                path_copy = list(map(lambda i: i, q.queue[0]))
                path_copy.append(i)
                # As soon as the destination vertex is found, the path is returned:
                if i == destination_vertex:
                    return path_copy
                # Otherwise, the new (longer) path is added to the queue to check for a connection to the destination vertex
                q.enqueue(path_copy)
                visited[i] = 'grey'
            visited[q.queue[0][len(q.queue[0]) - 1]] = 'black'
            q.dequeue()

    def bfs_brady(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create an empty set to store visited nodes
        visited = set()
        # Create an empty Queue and enqueue A PATH TO the starting vertex
        q = Queue()
        q.enqueue([starting_vertex])
        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue the first PATH
            path = q.dequeue()
            # GRAB THE VERTEX FROM THE END OF THE PATH
            v = path[-1]
            # IF VERTEX == TARGET, RETURN PATH
            if v == destination_vertex:
                return path
            # If that vertex has not been visited...
            if v not in visited:
                # Mark it as visited
                visited.add(v)
                # Then add A PATH TO all of its neighbors to the back of the queue
                for neighbor in self.vertices[v]:
                    # Copy the path
                    path_copy = list(path)
                    # Append neighbor to the back of the copy
                    path_copy.append(neighbor)
                    # Enqueue copy
                    q.enqueue(path_copy)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        try:
            self.vertices[starting_vertex]
            self.vertices[destination_vertex]
        except KeyError:
            return f'At least one of the vertices you supplied ({starting_vertex}, {destination_vertex}) does not exist in the graph.'

        path = []
        visited = {i: 'white' for i in self.vertices}

        def recurse(vertex):
            # Once the destination vertex is found, don't visit any new vertices (i.e., don't color them grey).
            if visited[destination_vertex] == 'white':
                visited[vertex] = 'grey'
                unvisited = self.vertices[vertex] - \
                    set(k for k, v in visited.items() if v != 'white')
                for i in unvisited:
                    recurse(i)
                visited[vertex] = 'black'
            # A vertex is not added to the path unless it's part of the path that leads to the destination vertex.
            if visited[destination_vertex] != 'white' and visited[vertex] != 'white':
                path.insert(0, vertex)

        recurse(starting_vertex)
        return path

    # dfs() is already recursive, but I nested the recursive function in the larger function. Here I refactored so it passes path and visited along instead of relying on path and visited being outside of the recursive function.
    def dfs_recursive(self, starting_vertex, destination_vertex, path=None, visited=None):
        try:
            self.vertices[starting_vertex]
            self.vertices[destination_vertex]
        except KeyError:
            return f'At least one of the vertices you supplied ({starting_vertex}, {destination_vertex}) does not exist in the graph.'

        if path == None:
            path = []
        if visited == None:
            visited = {i: 'white' for i in self.vertices}

        if visited[destination_vertex] == 'white':
            visited[starting_vertex] = 'grey'
            unvisited = self.vertices[starting_vertex] - \
                set(k for k, v in visited.items() if v != 'white')
            for i in unvisited:
                self.dfs_recursive(i, destination_vertex, path, visited)
            visited[starting_vertex] = 'black'
        # A vertex is not added to the path unless it's part of the path that leads to the destination vertex.
        if visited[destination_vertex] != 'white' and visited[starting_vertex] != 'white':
            path.insert(0, starting_vertex)

    def dfs_brady(self, starting_vertex, destination_vertex):
        # Create an empty set to store visited nodes
        visited = set()
        # Create an empty Stack and push A PATH TO the starting vertex
        s = Stack()
        s.push([starting_vertex])
        # While the stack is not empty...
        while s.size() > 0:
            # Pop the first PATH
            path = s.pop()
            # GRAB THE VERTEX FROM THE END OF THE PATH
            v = path[-1]
            # IF VERTEX == TARGET, RETURN PATH
            if v == destination_vertex:
                return path
            # If that vertex has not been visited...
            if v not in visited:
                # Mark it as visited
                visited.add(v)
                # Then add A PATH TO all of its neighbors to the top of the stack
                for neighbor in self.vertices[v]:
                    # Copy the path
                    path_copy = list(path)
                    # Append neighbor to the back of the copy
                    path_copy.append(neighbor)
                    # Enqueue copy
                    s.push(path_copy)


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    # Adding these vertices (and the edges below) caused my previous implementation of DFS to fail (DFS is working now).
    graph.add_vertex(8)
    graph.add_vertex(9)
    graph.add_vertex(10)

    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)
    # Adding these edges (and the vertices above) caused my previous implementation of DFS to fail (DFS is working now).
    graph.add_edge(1, 8)
    graph.add_edge(1, 9)
    graph.add_edge(1, 10)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print('vertices and edges: ', graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    print('bft:       ', graph.bft(1))
    print('bft_brady: ', graph.bft_brady(1))

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    print('dft:       ', graph.dft(1))
    print('dft_brady: ', graph.dft(1))

    '''
    Valid DFT recursive paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    print('dft_recursive:       ', graph.dft_recursive(1))
    print('dft_recursive_brady: ', graph.dft_recursive(1))

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print('bfs:       ', graph.bfs(1, 6))
    print('bfs_brady: ', graph.bfs_brady(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print('dfs:           ', graph.dfs(1, 6))
    print('dfs_recursive: ', graph.dfs(1, 6))
    print('dfs_brady:     ', graph.dfs(1, 6))
