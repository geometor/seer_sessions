import numpy as np

def find_objects(grid):
    """Finds all contiguous non-zero blocks of pixels and returns them as a list of (row, col, color) tuples representing the starting pixel of each object."""
    objects = []
    visited = set()

    def dfs(row, col, color):
        """Depth-first search to find contiguous blocks."""
        if (row, col) in visited or row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or grid[row, col] != color:
            return
        visited.add((row, col))
        dfs(row + 1, col, color)
        dfs(row - 1, col, color)
        dfs(row, col + 1, color)
        dfs(row, col - 1, color)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and (r, c) not in visited:
                objects.append((r, c, grid[r, c]))
                dfs(r, c, grid[r, c])  # Mark the entire object as visited.
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.zeros_like(input_grid) # Start with a blank grid
    objects = find_objects(input_grid)

    for r, c, color in objects:
        # Horizontal Expansion with Blocking
        output_grid[r,c] = color
        for c2 in range(c + 1, output_grid.shape[1]):
            if input_grid[r,c2] == 0:
                output_grid[r, c2] = color
            else:
                break # Stop expansion at the next object

    return output_grid

# Example grids (replace with your actual data)
example_inputs = [
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 2, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 2, 2, 2, 2],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 2, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
]
example_outputs = [
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 2, 2],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 2, 2, 2, 2],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 1],
              [0, 0, 0, 0, 0, 0],
              [0, 2, 2, 2, 2, 2],
              [0, 0, 0, 0, 0, 0]]),

]

for i, (input_grid, expected_output) in enumerate(zip(example_inputs, example_outputs)):
    actual_output = transform(input_grid)
    objects = find_objects(input_grid)
    print(f"Example {i+1}:")
    print(f"  Input Objects: {objects}")
    print(f"  Input Grid:\n{input_grid}")
    print(f"  Expected Output:\n{expected_output}")
    print(f"  Actual Output:\n{actual_output}")
    print(f"  Match: {np.array_equal(actual_output, expected_output)}")
    print("-" * 20)