import numpy as np

def find_pixel_by_color(grid, color):
    """Finds the coordinates of the first pixel of a given color."""
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color:
                return (r, c)
    return None

def transform(input_grid):
    # Find the yellow pixel.
    yellow_pos = find_pixel_by_color(input_grid, 4)
    if yellow_pos is None:  # Handle cases where yellow might be missing.
      yellow_pos = (0,0)

    # Extract the 2x2 subgrid.
    row_start = yellow_pos[0]
    col_start = yellow_pos[1]
   
    output_grid = []
    for r in range(row_start, min(row_start + 2, len(input_grid))):
        row = []
        for c in range(col_start, min(col_start + 2, len(input_grid[0]))):
            #filter out green
            if input_grid[r][c] != 3:
              row.append(input_grid[r][c])
            else:
              #if green, don't append it
              pass
        #fill in the rest with azure if needed
        while len(row) < 2:
          row.append(8)

        output_grid.append(row)
    
    #make sure we have 2 rows, fill with azure if needed
    while len(output_grid) < 2:
      output_grid.append([8,8])
    
    return output_grid

# Example Data (replace with actual data from the task)
examples = [
    {
        "input": [[6, 1, 1, 1, 1, 1, 1, 1, 6, 6], [1, 1, 1, 1, 1, 1, 1, 1, 1, 6], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 4, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [6, 1, 1, 1, 1, 1, 1, 1, 6, 6], [6, 6, 1, 1, 1, 1, 1, 1, 6, 6]],
        "output": [[4, 1], [1, 1]]
    },
    {
        "input": [[6, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 4, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 6], [6, 6, 1, 1, 1, 1, 1, 1, 6, 6]],
        "output": [[4, 1], [1, 1]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[4, 0], [0, 0]]
    },
    {
        "input" : [[6, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 4, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 3, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [6, 1, 1, 1, 1, 1, 1, 1, 6, 6], [6, 6, 1, 1, 1, 1, 1, 1, 6, 6]],
        "output": [[4, 1], [1, 1]]
    },
    {
        "input": [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 4, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]],
        "output": [[4, 6], [6, 6]]
    }

]

for i, example in enumerate(examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    print(f"  Input:\n{np.array(input_grid)}")
    print(f"  Expected Output:\n{np.array(expected_output)}")
    print(f"  Predicted Output:\n{np.array(predicted_output)}")
    print(f"  Yellow Position: {find_pixel_by_color(input_grid, 4)}")
    print("---")