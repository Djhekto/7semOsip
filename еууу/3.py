def topological_sort(graph, start_node):
    stack = []
    visited = []

    def dfs(node):
        visited.append(node)

        for v in range(len(graph)):
            if graph[node][v] == 1 and v not in visited:
                dfs(v)

        stack.append(node)

    for node in range(len(graph)):
        if node not in visited:
            dfs(node)

    return stack[::-1]

graph = [
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
]

start_node = 0

result = topological_sort(graph, start_node)
print(result)  # Output: [3, 2, 1, 0]
