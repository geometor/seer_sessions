import numpy as np

def find_uppermost_nonzero(grid):
    """Finds the row and column index of the uppermost non-zero pixel."""
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                return r, c
    return None  # Return None if no non-zero pixel is found

def find_lowermost_nonzero(grid):
    """Finds the row and column index of the lowermost non-zero pixel."""
    for r in range(len(grid) - 1, -1, -1):
        for c in range(len(grid[0])):
            if grid[r][c] != 0:
                return r, c
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find uppermost and lowermost non-zero pixels
    uppermost = find_uppermost_nonzero(input_grid)
    lowermost = find_lowermost_nonzero(input_grid)
    
    # change output pixels 
    if uppermost is not None and lowermost is not None and uppermost != lowermost :
      # Swap their positions
      output_grid[uppermost[0], uppermost[1]], output_grid[lowermost[0], lowermost[1]] = \
      output_grid[lowermost[0], lowermost[1]], output_grid[uppermost[0], uppermost[1]]

    return output_grid

task = task_data[4]

for i, example in enumerate(task['train']):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_output = transform(input_grid)
    
    print(f"--- Example {i+1} ---")
    print("Input Grid:\n", input_grid)
    print("Output Grid:\n", output_grid)
    print("Predicted Output:\n", predicted_output)

    uppermost = find_uppermost_nonzero(input_grid)
    lowermost = find_lowermost_nonzero(input_grid)

    print("Uppermost Non-zero Pixel (Input):", uppermost)
    if uppermost:
        print("Color of Uppermost Row (Input):", input_grid[uppermost[0]])
    print("Lowermost Non-zero Pixel (Input):", lowermost)
    if lowermost:
        print("Color of Lowermost Row (Input):", input_grid[lowermost[0]])

    if uppermost:
        print("Uppermost Row in Output:", output_grid[uppermost[0]])
    if lowermost:
      print("Lowermost Row in Output:", output_grid[lowermost[0]])
        
    print("Correct:", np.array_equal(output_grid, predicted_output))
    print("\n")