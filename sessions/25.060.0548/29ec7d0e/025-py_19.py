import numpy as np

def find_2x2_blocks(grid):
    """Finds all 2x2 blocks of ones in the grid."""
    rows, cols = grid.shape
    blocks = []
    for i in range(rows - 1):
        for j in range(cols - 1):
            if grid[i, j] == 1 and grid[i + 1, j] == 1 and grid[i, j + 1] == 1 and grid[i + 1, j + 1] == 1:
                blocks.append((i, j))
    return blocks

def find_changed_zeros(input_grid, output_grid):
    """Finds the locations of zeros that are changed to ones."""
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    changed_zeros = []
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 0 and output_grid[i, j] == 1:
                changed_zeros.append((i, j))
    return changed_zeros

def find_unchanged_zeros(input_grid, output_grid):
     """Finds the locations of zeros that remain unchanged."""
     input_grid = np.array(input_grid)
     output_grid = np.array(output_grid)
     unchanged_zeros = []
     rows, cols = input_grid.shape
     for i in range(rows):
        for j in range(cols):
            if input_grid[i,j] == 0 and output_grid[i,j] == 0:
                unchanged_zeros.append((i,j))
     return unchanged_zeros

def transform(input_grid):
    """Transforms the input grid by changing zeros to ones if they are inside a 2x2 block of ones."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find 2x2 blocks of ones
    blocks = find_2x2_blocks(input_grid)

    # Iterate through the blocks
    for block_row, block_col in blocks:
      # Check surrounding zero pixels
      if input_grid[block_row+1, block_col ] == 0:
          output_grid[block_row+1, block_col] = 1
      if input_grid[block_row, block_col+1 ] == 0:
          output_grid[block_row, block_col+1] = 1
      if input_grid[block_row-1, block_col ] == 0:
          output_grid[block_row-1, block_col] = 1
      if input_grid[block_row, block_col -1] == 0:
          output_grid[block_row, block_col - 1] = 1

      if input_grid[block_row + 1, block_col+1] == 0:
        output_grid[block_row+1,block_col+1] = 1
      if input_grid[block_row - 1, block_col -1] == 0:
        output_grid[block_row - 1,block_col - 1] = 1
      if input_grid[block_row-1, block_col+1 ] == 0:
          output_grid[block_row-1, block_col+1] = 1
      if input_grid[block_row+1, block_col -1] == 0:
          output_grid[block_row+1, block_col - 1] = 1

    return output_grid.tolist()

task = {
    "train": [
        {
            "input": [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 0, 1]],
            "output": [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
        },
        {
            "input": [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]],
        },
        {
            "input": [[1, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 1], [1, 1, 1, 0]],
            "output": [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 0]],
        },
    ],
    "test": [{"input": [[0, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 0]], "output": []}],
}

for example_index, example in enumerate(task["train"]):
  input_grid = example["input"]
  output_grid = example["output"]

  print(f"Example {example_index + 1}:")

  predicted_output = transform(input_grid)
  print(f"  Predicted Output: {predicted_output}")

  blocks = find_2x2_blocks(input_grid)
  print(f"  2x2 Blocks: {blocks}")

  changed_zeros = find_changed_zeros(input_grid, output_grid)
  print(f"  Changed Zeros: {changed_zeros}")

  unchanged_zeros = find_unchanged_zeros(input_grid, output_grid)
  print(f"Unchanged Zeros: {unchanged_zeros}")