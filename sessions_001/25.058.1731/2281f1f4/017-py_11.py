import numpy as np

def analyze_example(input_grid, output_grid):
    """
    Analyzes a single input/output pair and returns a dictionary of observations.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    rows, cols = input_grid.shape
    
    border_pixels = []
    border_colors = set()
    
    # Check top and bottom rows
    for col in range(cols):
        if input_grid[0, col] != 0:  # Check top row
            border_pixels.append(((0, col), input_grid[0, col]))
            border_colors.add(input_grid[0, col])
        if input_grid[rows - 1, col] != 0: # Check bottom row
            border_pixels.append(((rows-1, col), input_grid[rows - 1, col]))
            border_colors.add(input_grid[rows-1, col])

    # Check left and right columns (excluding corners already checked)
    for row in range(1, rows - 1):
        if input_grid[row, 0] != 0:  # Check left column
            border_pixels.append(((row, 0), input_grid[row, 0]))
            border_colors.add(input_grid[row, 0])
        if input_grid[row, cols - 1] != 0: #check right column
            border_pixels.append(((row, cols - 1), input_grid[row, cols - 1]))
            border_colors.add(input_grid[row, cols-1])
            
    infill_pixels = []
    for (r,c), color in border_pixels:
        #check down-left
        if r+1 < rows and c - 1 >= 0:
            if output_grid[r+1, c-1] != input_grid[r+1, c-1]:
                infill_pixels.append(((r+1, c-1), output_grid[r+1, c-1], 'down-left'))
        #check down-right
        if r+1 < rows and c + 1 < cols:
            if output_grid[r+1, c+1] != input_grid[r+1, c+1]:
                infill_pixels.append(((r+1, c+1), output_grid[r+1, c+1], 'down-right'))
        #check up-left
        if r-1 >= 0 and c - 1 >= 0:
            if output_grid[r-1, c-1] != input_grid[r-1, c-1]:
                infill_pixels.append(((r-1, c-1), output_grid[r-1, c-1], 'up-left'))
        #check up-right
        if r-1 >= 0 and c + 1 < cols:
            if output_grid[r-1, c+1] != input_grid[r-1, c+1]:
                infill_pixels.append(((r-1, c+1), output_grid[r-1, c+1], 'up-right'))

    return {
        'border_pixels': border_pixels,
        'border_colors': list(border_colors),
        'infill_pixels': infill_pixels,
        'same_shape': input_grid.shape == output_grid.shape
    }

# Example Usage (replace with actual input/output grids from the task)

task_id = "6f8cd79b"

train_input_output_pairs = [
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [0, 0, 0, 0, 0, 0, 0, 0, 5, 5],
    [0, 0, 0, 0, 0, 0, 0, 5, 5, 5],
    [0, 0, 0, 0, 0, 0, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
  ],
  [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
 [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]),
  ([
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
],
[
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 1, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
])
]

results = [analyze_example(inp, out) for inp, out in train_input_output_pairs]

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Border Colors: {result['border_colors']}")
    print(f"  Border Pixels: {result['border_pixels']}")
    print(f"  Infill Pixels: {result['infill_pixels']}")
    print(f"  Shapes are the same?: {result['same_shape']}")
    print("-" * 20)
