import numpy as np

def code_execution(input_grid, output_grid, transformed_grid):
    """
    Executes the code and compares the transformed output with the expected output.

    Args:
      input_grid: The input grid.
      output_grid: The expected output grid.
      transformed_grid: the result of running the transform function on the input_grid
    """

    print(f"Input Grid:\n{input_grid}")
    print(f"Expected Output Grid:\n{output_grid}")
    print(f"Transformed Output Grid:\n{transformed_grid}")
    print(f"Shapes - Input: {input_grid.shape}, Expected: {output_grid.shape}, Transformed: {transformed_grid.shape}")
    print(f"Matches Expected Output: {np.array_equal(output_grid, transformed_grid)}")
    print("---")
# re-create the function here so it is available
def find_colored_bands(grid):
    rows, cols = grid.shape
    horizontal_bands = []
    vertical_bands = []

    # Find horizontal bands
    for r in range(rows):
        row = grid[r]
        is_horizontal_band = False
        if row[0] == 1 or row[0] == 2:  # Check start of band
            is_horizontal_band = True
            for i in range(cols - 1):
                if row[i] == row[i + 1] or (row[i] != 1 and row[i] != 2):
                    is_horizontal_band = False
                    break
        if is_horizontal_band:
            horizontal_bands.append(r)

    # Find vertical bands (transpose the grid for easier processing)
    transposed_grid = grid.T
    rows_t, cols_t = transposed_grid.shape
    for r in range(rows_t):
        row = transposed_grid[r]
        is_vertical_band = False

        if row[0] == 1 or row[0] == 2:  # Check start of band
            is_vertical_band = True
            for i in range(cols_t - 1):
                if row[i] == row[i+1] or (row[i]!=1 and row[i] != 2):
                    is_vertical_band = False
                    break

        if is_vertical_band:
            vertical_bands.append(r)
    return horizontal_bands, vertical_bands
def transform(input_grid):
    rows, cols = input_grid.shape

    horizontal_bands, vertical_bands = find_colored_bands(input_grid)

    # Initialize output_grid based on whether there are horizontal or vertical bands
    if horizontal_bands:
      output_grid = np.zeros((rows, cols * 2), dtype=int)
    elif vertical_bands:
      output_grid = np.zeros((rows*2, cols), dtype=int)
    else: # handles edge case if not band is found - no stretching
      return input_grid


    # Handle horizontal stretching
    if horizontal_bands:
        for r in range(rows):
            if r not in horizontal_bands:
              # Copy background rows directly, doubling the width
              for c in range(cols):
                output_grid[r, c*2] = input_grid[r,c]
                output_grid[r, c*2 + 1] = input_grid[r,c]
            else:
                # Stretch the colored band rows
                for c in range(cols):
                    output_grid[r, 2 * c] = input_grid[r, c]
                    output_grid[r, 2 * c + 1] = input_grid[r, c]

    # Handle vertical stretching
    if vertical_bands:
      for c in range(cols):
        if c not in vertical_bands:
          for r in range(rows):
            output_grid[r*2,c] = input_grid[r,c]
            output_grid[r*2+1, c] = input_grid[r,c]
        else:
          for r in range(rows):
            output_grid[2*r, c] = input_grid[r,c]
            output_grid[2*r + 1, c] = input_grid[r,c]


    return output_grid
# Example Usage (replace with your actual task data)
task_id = "6e82a1ae"  #Task ID
train_examples = [
    {
        "input": [[5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [1, 2, 1, 2, 1, 2, 1, 2], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5]],
        "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
    },
        {
        "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [1, 2, 1, 2, 1, 2, 1, 2, 1], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]],
        "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
    },
    {
        "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [1, 2, 1, 2, 1, 2, 1, 2, 1, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
        "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
    },
        {
        "input": [[5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 1, 2, 1, 2, 1], [5, 5, 5, 5, 5, 5]],
        "output": [[5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 1, 2, 1, 2, 1], [5, 5, 5, 5, 5, 5]]
    },
    {
        "input" : [[1,2,1,2,1,2],[5,5,5,5,5,5],[5,5,5,5,5,5],[5,5,5,5,5,5]],
        "output": [[1,2,1,2,1,2],[1,2,1,2,1,2],[5,5,5,5,5,5],[5,5,5,5,5,5],[5,5,5,5,5,5],[5,5,5,5,5,5]]
    }
]

for i, example in enumerate(train_examples):
  transformed_grid = transform(np.array(example["input"]))
  print(f"Example {i+1}:")
  code_execution(np.array(example["input"]), np.array(example["output"]), transformed_grid)