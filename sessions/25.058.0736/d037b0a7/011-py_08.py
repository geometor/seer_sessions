import numpy as np

def _find_nonzero_region(grid):
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle the case where there are no non-zero pixels
        return None, None, None, None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the bounding box of the non-zero region
    min_row, max_row, min_col, max_col = _find_nonzero_region(input_grid)

    # Handle the case where the input grid is all zeros
    if min_row is None:
        return np.copy(input_grid)

    # Extract the source object
    source_object = input_grid[min_row:max_row+1, min_col:max_col+1]

    # Calculate the height of the output grid
    output_height = max_row + (max_row - min_row + 1) +1

     # Determine the starting row for replication
    replication_start_row = max_row + 1
    
    # Create an output grid of appropriate size
    output_grid = np.zeros((output_height, input_grid.shape[1]), dtype=input_grid.dtype)

    # Copy the original non zero region in the correct place
    output_grid[min_row:max_row+1, min_col:max_col + 1] = source_object

    # Replicate the source object downwards
    output_grid[replication_start_row:output_height, min_col:max_col+1] = source_object
   
    return output_grid

def show_grid(grid, title="Grid"):
    print(f"\n--- {title} ---")
    for row in grid:
        print("".join(str(int(cell)) for cell in row))

# Example Data (replace with actual task data)
examples = [
    {
        "input": np.array([[0, 0, 0], [0, 2, 0], [0, 0, 0]]),
        "output": np.array([[0, 0, 0], [0, 2, 0], [0, 2, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0], [0, 3, 3, 0], [0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0], [0, 3, 3, 0], [0, 3, 3, 0]]),
    },
     {
        "input": np.array([[0, 0, 0, 0], [0, 4, 4, 0], [0, 4, 4, 0], [0,0,0,0]]),
        "output": np.array([[0, 0, 0, 0], [0, 4, 4, 0], [0, 4, 4, 0], [0,4,4,0], [0,4,4,0]]),
    },
]

results = []
for i, example in enumerate(examples):
  input_grid = example["input"]
  expected_output = example["output"]
  actual_output = transform(input_grid)
  
  show_grid(input_grid, title=f"Example {i+1} - Input")
  show_grid(expected_output, title=f"Example {i+1} - Expected Output")
  show_grid(actual_output, title=f"Example {i+1} - Actual Output")

  results.append({
        "example": i + 1,
        "input_shape": input_grid.shape,
        "output_shape": actual_output.shape,
        "expected_shape": expected_output.shape,
        "match": np.array_equal(actual_output, expected_output)
    })
  

for result in results:
    print(result)