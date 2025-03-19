import numpy as np

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair and returns relevant metrics."""

    blue_pixels_input = np.sum(input_grid == 1)
    blue_pixels_output = np.sum(output_grid == 1)
    red_pixels_output = np.sum(output_grid == 2)
    white_pixels_input = np.sum(input_grid == 0)
    white_pixels_output = np.sum(output_grid == 0)
    
    blue_blocks_input = get_contiguous_blocks(input_grid, 1)
    
    single_blue_pixels = []
    for r in range(input_grid.shape[0]):
      for c in range(input_grid.shape[1]):
        if input_grid[r,c] == 1:
          is_single = True
          for block in blue_blocks_input:
            if (r,c) in block and len(block) > 1:
              is_single = False
              break
          if is_single:
            single_blue_pixels.append((r,c))
    
    analysis = {
        "blue_pixels_input": int(blue_pixels_input),
        "blue_pixels_output": int(blue_pixels_output),
        "red_pixels_output": int(red_pixels_output),
        "white_pixels_input": int(white_pixels_input),
        "white_pixels_output": int(white_pixels_output),
        "blue_blocks_input": [list(block) for block in blue_blocks_input],  # Convert sets to lists
        "single_blue_pixels": single_blue_pixels
    }
    return analysis

def get_contiguous_blocks(grid, color):
    """
    Finds contiguous blocks of the specified color in the grid.
    Returns a list of sets, where each set contains the coordinates of a contiguous block.
    """
    visited = set()
    blocks = []

    def dfs(row, col, current_block):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_block.add((row, col))
        dfs(row + 1, col, current_block)
        dfs(row - 1, col, current_block)
        dfs(row, col + 1, current_block)
        dfs(row, col - 1, current_block)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_block = set()
                dfs(row, col, current_block)
                blocks.append(current_block)
    return blocks

# Example usage (assuming input_grids and output_grids are defined)
# Replace with the actual input/output grid data
task_examples = [
    (np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 1, 0, 0],
               [0, 1, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 2, 0, 2, 0, 0],
               [0, 2, 0, 0, 0, 2, 0],
               [0, 0, 0, 0, 0, 0, 0]])),

    (np.array([[0, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 1, 0]]),
     np.array([[0, 0, 0, 0],
               [0, 2, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 2, 0]])),
    
        (np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 2, 2, 2, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]])),
]

for i, (input_grid, output_grid) in enumerate(task_examples):
  analysis = analyze_example(input_grid, output_grid)
  print(f"Example {i+1}:")
  print(analysis)
