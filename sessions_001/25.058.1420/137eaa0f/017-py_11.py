import numpy as np

def code_execution(input_grid, predicted_output, target_output):
    """Executes code and provides both visual and exact match comparisons."""

    # Convert to numpy arrays for easier handling
    input_grid = np.array(input_grid)
    target_output = np.array(target_output)
    predicted_output = np.array(predicted_output)

    # 1. Visual Comparison (first 5 rows and columns if large)
    print("Input Grid (Snippet):\n", input_grid[:5, :5] if input_grid.size > 25 else input_grid)
    print("\nPredicted Output (Snippet):\n", predicted_output[:5, :5] if predicted_output.size > 25 else predicted_output)
    print("\nTarget Output (Snippet):\n", target_output[:5, :5] if target_output.size > 25 else target_output)

    # 2. Exact Match Check
    match = np.array_equal(predicted_output, target_output)
    print("\nExact Match:", match)

    # 3. Non-zero pixel counts
    input_nonzero = np.count_nonzero(input_grid)
    predicted_nonzero = np.count_nonzero(predicted_output)
    target_nonzero = np.count_nonzero(target_output)

    print("\nNon-zero Pixels - Input:", input_nonzero, "Predicted:", predicted_nonzero, "Target:", target_nonzero)
    
    # 4. Shape Comparison
    
    print("\nShapes - Input:",input_grid.shape, "Predicted:", predicted_output.shape, "Target:", target_output.shape)

    return match

#Example Usage for Task Training Data

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[5, 0], [0, 5]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[8]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[7, 0], [0, 7]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 9, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[9]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[6, 0], [1, 0]],
        },
    ]
}

import numpy as np

def get_nonzero_pixels(grid):
    """
    Finds the coordinates and values of all non-zero pixels in a grid.

    Args:
        grid: A 2D numpy array representing the input grid.

    Returns:
        A list of tuples, where each tuple contains (row, column, value)
        of a non-zero pixel.
    """
    nonzero_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                nonzero_pixels.append((r, c, grid[r, c]))
    return nonzero_pixels

def transform(input_grid):
    """
    Transforms the input grid by extracting non-zero pixels and arranging
    them in a condensed output grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # 1. Identify Non-Zero Pixels and their locations.
    nonzero_pixels = get_nonzero_pixels(input_grid)

    # 2. Create a new output grid, enough to fit non-zero pixels
    output_grid = np.zeros((len(nonzero_pixels), len(nonzero_pixels)), dtype=int)

    #3. Extract, and Position:
    output_row = 0
    output_col = 0

    for _, _, value in nonzero_pixels:
          output_grid[output_row,output_col] = value
          output_col += 1
          if output_col >= output_grid.shape[1]:
            output_col = 0
            output_row +=1

    #4. Determine the required size, trimming the grid

    #find dimensions needed
    max_row = 0
    max_col = 0

    for r in range(output_grid.shape[0]):
      for c in range(output_grid.shape[1]):
        if output_grid[r,c] != 0:
          if r > max_row:
            max_row = r
          if c > max_col:
            max_col = c

    trimmed_output_grid = output_grid[:max_row+1,:max_col+1]
    return trimmed_output_grid


for i, example in enumerate(task["train"]):
    input_grid = example["input"]
    target_output = example["output"]
    predicted_output = transform(input_grid)

    print(f"\n--- Example {i+1} ---")
    code_execution(input_grid, predicted_output, target_output)