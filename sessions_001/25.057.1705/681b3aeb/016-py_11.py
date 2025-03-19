import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-zero pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append(
                    {"color": grid[row, col], "pixels": obj_pixels}
                )
    return objects

def analyze_example(input_grid, output_grid):
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    print("Input Objects:")
    for i, obj in enumerate(input_objects):
        print(f"  Object {i+1}: Color={obj['color']}, Pixel Count={len(obj['pixels'])}")

    print("\nOutput Objects:")
    for i, obj in enumerate(output_objects):
        print(f"  Object {i+1}: Color={obj['color']}, Pixel Count={len(obj['pixels'])}")

    print("\nInput Grid Shape:", input_grid.shape)
    print("Output Grid Shape:", output_grid.shape)
    print("-" * 20)

example_grids = [
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0],
              [0, 3, 3, 3, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 8, 0],
              [0, 0, 0, 0, 0, 0, 0, 8, 0],
              [0, 0, 0, 0, 0, 8, 8, 8, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 6, 0, 0, 0],
              [0, 0, 0, 6, 0, 0, 0],
              [0, 0, 0, 6, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 4, 4, 4, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              ])
]
expected_outputs = [
        np.array([[1, 1, 1],
                  [1, 0, 3],
                  [1, 3, 3]]),
        np.array([[0, 0, 0],
                  [0, 0, 8],
                  [8, 8, 8]]),
        np.array([[0, 6, 0],
                  [0, 6, 0],
                  [4, 6, 4]]),
]

for i in range(len(example_grids)):
    print(f"Example {i+1}:")
    analyze_example(example_grids[i], expected_outputs[i])