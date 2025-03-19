import numpy as np

def find_objects(grid, color):
    """Finds all disconnected objects of a specified color."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                if current_object:
                    # Calculate bounding box
                    min_row = min(current_object, key=lambda p: p[0])[0]
                    max_row = max(current_object, key=lambda p: p[0])[0]
                    min_col = min(current_object, key=lambda p: p[1])[1]
                    max_col = max(current_object, key=lambda p: p[1])[1]
                    objects.append(((min_row, min_col), (max_row, max_col)))
    return objects

# Example Data (replace with actual data from the task)
example_inputs = [
    np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 4, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8]
    ]),
    np.array([
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
       [1, 1, 1, 1, 4, 1, 1, 1, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 8, 4, 0, 0, 0, 0],
       [0, 0, 0, 0, 8, 0, 0, 0, 0, 0]
    ]),
    np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 8, 8, 0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 0],
        [8, 4, 8, 0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 0],
        [8, 8, 8, 0, 0, 0, 0, 0, 0, 8, 4, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
]
example_outputs = [
   np.array([
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
      [1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 0, 0],
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
      [0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 0, 0, 4, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 0, 0, 8, 8, 8, 8, 8],
      [0, 0, 0, 0, 8, 0, 0, 8, 8, 8, 4, 8],
      [0, 0, 0, 0, 8, 0, 0, 8, 8, 8, 8, 8]
   ]),
   np.array([
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
      [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
      [1, 1, 1, 1, 4, 1, 1, 1, 0, 0],
      [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
      [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
      [0, 0, 0, 0, 8, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 4, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 8, 0, 0, 0, 0]
   ]),
   np.array([
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
      [0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
      [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
      [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
      [0, 0, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 0, 0],
      [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
      [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
      [0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
      [0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
      [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
      [8, 4, 8, 8, 8, 8, 8, 8, 8, 8, 4, 8, 0, 0],
      [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
      [0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
      [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   ])
]

for i, input_grid in enumerate(example_inputs):
    print(f"Example {i+1}:")
    print("Input:")
    print(input_grid)
    azure_objects = find_objects(input_grid, 8)
    yellow_objects = find_objects(input_grid, 4)
    blue_objects = find_objects(input_grid, 1)
    print("Azure Objects (Bounding Boxes):", azure_objects)
    print("Yellow Objects (Bounding Boxes):", yellow_objects)
    print("Blue Objects (Bounding Boxes):", blue_objects)
    print("Output:")
    print(example_outputs[i])
    print("-" * 30)