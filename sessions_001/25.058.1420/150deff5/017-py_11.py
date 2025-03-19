import numpy as np

def analyze_results(input_grid, output_grid, expected_output_grid):
    """Analyzes the results and provides metrics."""

    # Check if output matches expected output
    match = np.array_equal(output_grid, expected_output_grid)

    # Find shapes in input, output, and expected output
    input_shapes = find_shapes(input_grid, 5)
    output_shapes_2 = find_shapes(output_grid, 2)
    output_shapes_8 = find_shapes(output_grid, 8)

    expected_output_shapes_2 = find_shapes(expected_output_grid, 2)
    expected_output_shapes_8 = find_shapes(expected_output_grid, 8)

    print(f"  Match: {match}")
    print(f"  Input shapes (5s): {len(input_shapes)}")
    print(f"  Output shapes (2s): {len(output_shapes_2)}")
    print(f"  Output shapes (8s): {len(output_shapes_8)}")
    print(f"  Expected output shapes (2s): {len(expected_output_shapes_2)}")
    print(f"  Expected output shapes (8s): {len(expected_output_shapes_8)}")

def find_shapes(grid, color):
    """
    Finds contiguous shapes of the specified color and returns as list where
    one item contains coordinates for one shape
    """
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return []

    shapes = []
    visited = set()

    def dfs(row, col, current_shape):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_shape.append((row, col))
        dfs(row + 1, col, current_shape)
        dfs(row - 1, col, current_shape)
        dfs(row, col + 1, current_shape)
        dfs(row, col - 1, current_shape)

    for r, c in coords:
        if (r, c) not in visited:
            current_shape = []
            dfs(r, c, current_shape)
            shapes.append(current_shape)

    return shapes

# Example grids (replace with your actual grid data)
task_examples = [
  {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 5, 5, 5, 5, 0],
                           [0, 5, 5, 5, 5, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0],
                            [0, 2, 2, 8, 8, 0],
                            [0, 2, 2, 8, 8, 0],
                            [0, 0, 0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 5, 5, 5, 0, 0, 0],
                           [0, 0, 5, 5, 5, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 5, 5, 0],
                           [0, 0, 0, 0, 5, 5, 5, 0],
                           [0, 0, 0, 0, 5, 5, 5, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 2, 2, 8, 0, 0, 0],
                            [0, 0, 2, 2, 8, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 2, 2, 8, 0],
                            [0, 0, 0, 0, 2, 2, 8, 0],
                            [0, 0, 0, 0, 2, 2, 8, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 5, 5, 5, 5, 0, 0, 0, 0],
                           [0, 5, 5, 5, 5, 0, 0, 0, 0],
                           [0, 5, 5, 5, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 5, 5, 0],
                           [0, 0, 0, 0, 0, 0, 5, 5, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 2, 2, 8, 8, 0, 0, 0, 0],
                            [0, 2, 2, 8, 8, 0, 0, 0, 0],
                            [0, 2, 2, 8, 8, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 2, 8, 0],
                            [0, 0, 0, 0, 0, 0, 2, 8, 0]]),
    },
]

for i, example in enumerate(task_examples):
    print(f"Example {i+1}:")
    output_grid = transform(example["input"])
    analyze_results(example["input"], output_grid, example["output"])
    print("-" * 20)