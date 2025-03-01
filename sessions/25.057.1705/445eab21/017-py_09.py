import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of the same color in a grid.
    Returns a dictionary where keys are colors and values are lists of pixel coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj_pixels):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_pixels.append((r, c))
        dfs(r + 1, c, color, obj_pixels)
        dfs(r - 1, c, color, obj_pixels)
        dfs(r, c + 1, color, obj_pixels)
        dfs(r, c - 1, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                if color != 0:  # Ignore background
                    obj_pixels = []
                    dfs(r, c, color, obj_pixels)
                    if color not in objects:
                        objects[color] = []
                    objects[color].append(obj_pixels)
    return objects

# Example Data (Replace with actual data from the task)
example_inputs = [
    np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 0, 4],
              [4, 4, 4, 4, 4, 4, 4, 0, 4],
              [4, 4, 4, 4, 4, 4, 0, 0, 4],
              [4, 4, 4, 4, 4, 0, 0, 1, 4],
              [4, 4, 4, 4, 4, 0, 0, 0, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4]]),
    np.array([[4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [0, 0, 4, 4, 4, 4, 4, 4, 4, 0, 4],
              [4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 4],
              [4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [4, 4, 4, 0, 0, 1, 0, 0, 0, 4, 4],
              [4, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0],
              [4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 4, 4, 4]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
]
example_outputs = [
    np.array([[4, 4],
              [4, 1]]),
    np.array([[0, 1],
              [0, 0]]),
    np.array([[1]]),
    np.array([[1]])
]

for i, (input_grid, output_grid) in enumerate(zip(example_inputs, example_outputs)):
    print(f"Example {i+1}:")
    print("Input Grid Shape:", input_grid.shape)
    print("Output Grid Shape:", output_grid.shape)
    objects = find_objects(input_grid)
    print("Detected Objects:", objects)
    print("-" * 20)