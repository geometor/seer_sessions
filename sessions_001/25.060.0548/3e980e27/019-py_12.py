import numpy as np

def find_objects(grid):
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_coords):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                objects.append({"color": grid[r, c], "coords": obj_coords})
    return objects

def analyze_example(input_grid, output_grid, predicted_output):
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)
    predicted_objects = find_objects(predicted_output)

    print("Input Objects:", input_objects)
    print("Output Objects:", output_objects)
    print("Predicted Objects", predicted_objects)
    print("Input Grid:\n", input_grid)
    print("Output Grid:\n", output_grid)
    print("Predicted Output:\n", predicted_output)
    print("Differences (Output - Predicted):\n", output_grid - predicted_output)

# Example usage with the provided training data (replace with actual data)
#example index and data from the file

examples = [
  (0,
    np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,0,0,0,0],[0,0,0,0,2,0,0,0,0],[0,0,0,0,2,0,0,0,0],[0,0,0,0,2,0,0,4,0],[3,0,0,0,2,0,0,4,0],[3,0,0,0,0,0,0,4,0],[3,0,0,0,0,0,0,0,0]]),
    np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,0,0,0,0],[0,0,0,0,2,0,0,0,0],[0,0,0,0,2,0,0,0,0],[4,4,4,0,2,0,0,0,0],[4,4,4,0,0,0,0,0,0],[4,4,4,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])
 ),(1,
  np.array([[0,0,0,0,0,0,0,0],[8,0,0,0,2,0,0,0],[8,0,0,0,2,0,0,0],[8,0,0,0,2,0,0,4],[0,0,0,0,2,0,0,4],[0,0,0,0,2,0,0,4],[0,0,0,0,0,0,0,0]]),
  np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,0,0,0,0,0]])
), (2,
   np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,0,0,0,0],[8,0,0,0,2,0,0,0,0],[8,0,0,0,2,0,0,4,0],[8,8,0,0,2,0,0,4,0],[8,8,0,0,0,0,0,4,0],[0,0,0,0,0,0,0,0,0]]),
   np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,0,0,0,0],[0,0,0,0,2,0,0,0,0],[0,0,0,0,2,0,0,0,0],[4,4,4,0,2,0,0,0,0],[4,4,4,0,0,0,0,0,0],[4,4,4,0,0,0,0,0,0]])
), (3,
  np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,0,2,0,4,0],[3,0,0,0,2,0,4,0],[3,0,0,0,2,0,4,0],[3,3,0,0,2,0,4,0],[3,3,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]),
  np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,0,2,0,0,0],[4,4,4,0,2,0,0,0],[4,4,4,0,0,0,0,0],[4,4,4,0,0,0,0,0]])
)
]

from previous_code_store import transform

for i, example in enumerate(examples):
    input_grid = example[1][0]
    output_grid = example[1][1]
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid, predicted_output)
    print("-" * 20)