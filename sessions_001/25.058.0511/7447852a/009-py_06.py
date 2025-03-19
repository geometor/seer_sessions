import numpy as np

# helper function to run transform
def transform(input_grid):
    """
    Transforms the input grid based on red pixel positions.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Conditional Yellow Placement, Row Rule
            if input_grid[r,c] == 0:
                if c + 1 < cols and input_grid[r, c+1] == 0:
                    if r + 1 < rows and c + 2 < cols and input_grid[r+1,c+2] == 2:
                        output_grid[r,c] = 4
            # Conditional Yellow Placement, Column Rule
            if input_grid[r, c] == 0:  # Check if the current cell is white
                if r + 1 < rows and c + 1 < cols and input_grid[r + 1, c + 1] == 2:
                    output_grid[r, c] = 4

    return output_grid

def compare_grids(grid1, grid2):
    """Counts the number of differences between two grids."""
    return np.sum(grid1 != grid2)

# Example data (replace with actual example data from the task)
examples = [
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 0, 0, 5, 5],
                           [5, 5, 5, 5, 2, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 4, 0, 5, 5],
                            [5, 5, 5, 5, 2, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5]])
    },
    {
        "input": np.array([[0, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 0, 5, 5],
                           [5, 5, 5, 2, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[4, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 4, 5, 5],
                            [5, 5, 5, 2, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5]])
    },
    {
         "input": np.array([[5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 0, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 2, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5]]),
         "output": np.array([[5, 5, 5, 5, 5, 5, 5],
                             [5, 5, 5, 4, 5, 5, 5],
                             [5, 5, 5, 5, 5, 5, 5],
                             [5, 5, 5, 5, 5, 5, 5],
                             [5, 5, 5, 2, 5, 5, 5],
                             [5, 5, 5, 5, 5, 5, 5]])
    }
]

for i, example in enumerate(examples):
    transformed_grid = transform(example["input"])
    differences = compare_grids(transformed_grid, example["output"])
    print(f"Example {i+1}: Differences = {differences}")
    if not np.array_equal(transformed_grid, example["output"]):
      print(f"Transformed:\n{transformed_grid}")
      print(f"Expected:\n{example['output']}")
