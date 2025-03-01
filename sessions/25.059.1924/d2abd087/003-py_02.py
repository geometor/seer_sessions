import numpy as np
from collections import deque

def find_objects(grid, color):
    """Finds contiguous regions of the specified color in the grid."""
    visited = set()
    objects = []

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, current_object):
        if (x, y) in visited or not is_valid(x, y) or grid[x, y] != color:
            return
        visited.add((x, y))
        current_object.append((x, y))

        # Check adjacent cells (not diagonally)
        dfs(x + 1, y, current_object)
        dfs(x - 1, y, current_object)
        dfs(x, y + 1, current_object)
        dfs(x, y - 1, current_object)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == color and (x, y) not in visited:
                current_object = []
                dfs(x, y, current_object)
                objects.append(current_object)
    return objects

def build_adjacency_graph(objects):
    """Builds an adjacency graph of the objects."""
    graph = {i: [] for i in range(len(objects))}
    for i, obj1 in enumerate(objects):
        for j, obj2 in enumerate(objects):
            if i != j:
                for x1, y1 in obj1:
                    for x2, y2 in obj2:
                        # Check for adjacency (not diagonally)
                        if abs(x1 - x2) + abs(y1 - y2) == 1:
                            if j not in graph[i]:
                                graph[i].append(j)
                            if i not in graph[j]:
                                graph[j].append(i)
                            break  # Move to the next object pair
                    else:
                        continue
                    break
    return graph

def color_graph(graph, objects):
    """Colors the graph using a BFS traversal, alternating colors."""
    colors = {}  # object index -> color
    q = deque()

    for start_node in graph:
        if start_node not in colors:
          q.append((start_node, 1))  # Start with blue (1)
          colors[start_node] = 1

          while q:
              node, color = q.popleft()
              for neighbor in graph[node]:
                  if neighbor not in colors:
                      colors[neighbor] = 3 - color  # Alternate between 1 and 2
                      q.append((neighbor, 3 - color))
    return colors

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # 1. Identify Gray Shapes
    gray_objects = find_objects(input_grid, 5)

    # 2. Construct a Connectivity Graph
    adjacency_graph = build_adjacency_graph(gray_objects)

    # 3. Color the graph
    object_colors = color_graph(adjacency_graph, gray_objects)

    # 4. Replace with Colored Shapes
    for i, obj in enumerate(gray_objects):
        color = object_colors.get(i,0) # get assigned color
        for x, y in obj:
            output_grid[x, y] = color

    return output_grid.tolist()

def analyze_example(input_grid, output_grid):
    """Analyzes a single example and returns relevant metrics."""
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    gray_objects = find_objects(input_grid, 5)
    num_gray_objects = len(gray_objects)
    adjacency_graph = build_adjacency_graph(gray_objects)
    object_colors = color_graph(adjacency_graph, gray_objects)
    predicted_output_grid = np.array(transform(input_grid))

    comparison = (predicted_output_grid == output_grid)
    differences = []
    if not np.all(comparison):
       #find all differences
       for x in range(comparison.shape[0]):
          for y in range(comparison.shape[1]):
             if not comparison[x,y]:
                differences.append( (x,y, predicted_output_grid[x,y], output_grid[x,y]))

    return {
        "num_gray_objects": num_gray_objects,
        "adjacency_graph": adjacency_graph,
        "object_colors": object_colors,
        "differences": differences,
        "success": np.all(comparison)
    }

# Example Usage with the Training Data:

task_data = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0, 0, 5, 5, 0], [0, 5, 5, 5, 0, 0, 0, 5, 5, 0], [0, 5, 5, 5, 0, 0, 0, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 2, 2, 0], [0, 1, 1, 1, 0, 0, 0, 2, 2, 0], [0, 1, 1, 1, 0, 0, 0, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 5, 5, 5, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0, 2, 2, 2, 0]]
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 0, 0, 5, 5, 5, 5], [5, 5, 5, 0, 0, 0, 0, 5, 5, 5], [5, 5, 5, 0, 0, 0, 0, 5, 5, 5], [5, 5, 5, 5, 0, 0, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 0, 0, 1, 1, 1, 1], [2, 2, 2, 0, 0, 0, 0, 1, 1, 1], [2, 2, 2, 0, 0, 0, 0, 1, 1, 1], [2, 2, 2, 2, 0, 0, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
        }
    ]
}

results = {}
for i, example in enumerate(task_data["train"]):
  results[i] = analyze_example(example["input"], example["output"])

for ex_num, result in results.items():
  print (f'example {ex_num}:')
  print (result)