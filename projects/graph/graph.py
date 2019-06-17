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
        self.vertices.update({vertex: set()})

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

    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        This should be done using recursion.
        """
        pass  # TODO

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        pass  # TODO

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        pass  # TODO


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

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print('Vertices and edges: ', graph.vertices)

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
    print('BFT: ', graph.bft(1))

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    print('DFT: ', graph.dft(1))

    '''
    Valid DFT recursive paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    # print('DFT (recursive): ', graph.dft_recursive(1))

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    # print('BFS: ', graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    # print('DFS: ', graph.dfs(1, 6))
