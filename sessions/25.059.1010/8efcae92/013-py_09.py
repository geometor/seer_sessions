import numpy as np

# Provided code (slightly modified for easier data extraction)
def find_bounding_box(grid):
    """Find the bounding box of non-white pixels."""
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    min_row, max_row = np.where(rows)[0][[0, -1]]
    min_col, max_col = np.where(cols)[0][[0, -1]]
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid by extracting a subgrid, removing white pixels,
    and reconstructing a new grid based on relative positions of non-white pixels.
    """
    # 1. Identify the Bounding Box
    min_row, max_row, min_col, max_col = find_bounding_box(input_grid)

    # 2. Extract Subgrid
    subgrid = input_grid[min_row:max_row+1, min_col:max_col+1]

    # 3. Record Positions and Values (relative to the bounding box)
    non_white_indices = np.argwhere(subgrid != 0)
    non_white_values = subgrid[subgrid != 0]

    # 4. Remove White (implicitly done by recording only non-white indices/values)

    # 5. Reconstruct Output: Determine output grid size and populate
    if len(non_white_indices) > 0:  #check if non-white pixels
        #find min/max of non-white indices
        min_output_row = np.min(non_white_indices[:, 0])
        max_output_row = np.max(non_white_indices[:, 0])
        min_output_col = np.min(non_white_indices[:, 1])
        max_output_col = np.max(non_white_indices[:, 1])

        #calc output grid dimensions
        output_height = max_output_row - min_output_row + 1
        output_width = max_output_col - min_output_col + 1

        #initialize output grid filled with white (0)
        output_grid = np.zeros((output_height, output_width), dtype=int)
    
        #adjust non-white indices to be relative to the min row/col
        adjusted_indices = non_white_indices - [min_output_row, min_output_col]
        
        #populate output grid
        for (row, col), value in zip(adjusted_indices, non_white_values):
            output_grid[row, col] = value
    else:
        output_grid = np.array([[]], dtype=int)

    return output_grid

# Task examples (replace with actual data from the task)
train_examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 2, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[1, 2]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 3, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[]])
    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 4, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[]])
    }
]

results = []
for ex in train_examples:
    input_grid = ex["input"]
    expected_output = ex["output"]
    predicted_output = transform(input_grid)
    min_row, max_row, min_col, max_col = find_bounding_box(input_grid)
    results.append({
        "input_shape": input_grid.shape,
        "output_shape": predicted_output.shape,
        "expected_output_shape": expected_output.shape,
        "bounding_box": (min_row, max_row, min_col, max_col),
        "predicted_output": predicted_output.tolist(),
        "expected_output": expected_output.tolist(),
        "match": np.array_equal(predicted_output, expected_output)
    })

for i, res in enumerate(results):
    print(f"--- Example {i+1} ---")
    for k, v in res.items():
        print(f"{k}: {v}")