import numpy as np

def find_object(grid, color):
    # Find the coordinates of a single pixel of the specified color.
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        return coords[0]  # Return the first occurrence
    return None

def find_block(grid, color):
    # Find coordinates of a block, assume its solid rectangle, find top left and bottom right
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
      min_row, min_col = np.min(coords, axis=0)
      max_row, max_col = np.max(coords, axis=0)
      return (min_row, min_col), (max_row, max_col)
    return None, None

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = input_grid.copy()
    
    # 1. Maroon Pixel Duplication
    maroon_pos = find_object(input_grid, 9)
    if maroon_pos is not None:
        output_grid[maroon_pos[0], maroon_pos[1]] = 9  # Keep original
        new_maroon_row = min(maroon_pos[0] + 1, output_grid.shape[0] - 1)
        output_grid[new_maroon_row, maroon_pos[1]] = 9  # Duplicate below

    # 2. Azure Block Modification
    (top_left_8, _), _ = find_block(input_grid, 8)
    if top_left_8 is not None and maroon_pos is not None:
      if top_left_8[0] <= maroon_pos[0]: # check if block begins before maroon
        target_row = maroon_pos[0] + 1
      else:
        target_row = top_left_8[0]
      
      if target_row < input_grid.shape[0]:  # Check for out-of-bounds access
          if input_grid[target_row, maroon_pos[1]] == 8:  # find azure pixel in the same column.
            output_grid[target_row, maroon_pos[1]] = 9 # make it maroon

    # 3. Magenta Pixel Repositioning
    magenta_pos = find_object(input_grid, 6)
    (top_left_8, _), (bottom_right_8, _) = find_block(input_grid, 8)

    if magenta_pos is not None and top_left_8 is not None:
      # Try to place it below the block
      target_row = bottom_right_8[0] + 1
      target_col = top_left_8[1]
      
      if target_row >= output_grid.shape[0]:
        # Not enough space below, try sides
        target_row = bottom_right_8[0]
        
        #try left first
        target_col = top_left_8[1] - 1
        if target_col < 0: #try right
            target_col = bottom_right_8[1] + 1

      if 0 <= target_row < output_grid.shape[0] and 0 <= target_col < output_grid.shape[1]: #check if valid position
        output_grid[target_row, target_col] = 6
        if (target_row != magenta_pos[0]) or (target_col != magenta_pos[1]):  # remove only if moved
          output_grid[magenta_pos[0], magenta_pos[1]] = 0 # Remove original
      else:
        output_grid[magenta_pos[0], magenta_pos[1]] = 0 # remove and don't put down


    # 4. Yellow Pixel Invariance (already handled by copying)
    
    # 5. Blank spaces remain 0 - they are 0 by default.
    
    return output_grid

task_id = "3b5a0e7f"

train_examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 0, 0, 6, 0], [0, 8, 8, 8, 0, 0, 0, 0], [0, 8, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 9, 0, 0, 0, 0, 4]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 0, 0, 0, 0], [0, 8, 8, 8, 0, 0, 0, 0], [0, 8, 8, 8, 0, 0, 0, 0], [0, 0, 9, 0, 0, 0, 6, 0], [0, 0, 9, 0, 0, 0, 0, 4]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 9, 0, 0, 0, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 8, 8, 8, 8, 8, 8, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 9, 0, 0, 0, 4, 0], [0, 0, 0, 9, 0, 0, 0, 0, 0], [0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 6]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 8, 8, 8, 9, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 9, 0], [0, 0, 0, 0, 8, 8, 8, 9, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0], [0, 0, 0, 6, 0, 0, 0, 0, 0]]
    }
]

def compare_grids(grid1, grid2):
    """Compares two grids and returns a detailed report."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"

    diff = grid1 != grid2
    num_diffs = np.sum(diff)
    diff_indices = np.argwhere(diff)

    report = f"Number of differences: {num_diffs}\n"
    for i, (row, col) in enumerate(diff_indices):
        report += f"Difference {i+1}: at ({row}, {col}), expected {grid2[row, col]}, got {grid1[row, col]}\n"
    return report

for i, example in enumerate(train_examples):
  input_grid = np.array(example['input'])
  expected_output = np.array(example['output'])
  predicted_output = transform(input_grid)
  print(f"Example {i+1}:")
  print(compare_grids(predicted_output, expected_output))
  print("-" * 20)