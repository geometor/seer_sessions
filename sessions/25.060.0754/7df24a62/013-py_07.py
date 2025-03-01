import numpy as np

def find_yellow_pixels(grid):
    """Finds the coordinates of all yellow (4) pixels in the grid."""
    return np.argwhere(grid == 4)

def get_blue_block_center(grid):
    """
    Find the yellow center of blue block.
    Returns the x, y coordinate as ints, or None, None if no center is found.
    """
    yellow_pixels = np.argwhere(grid == 4)
    for y, x in yellow_pixels:
      #check to see if it might be the center of a blue box
      #blue box is 3x4
      blues_found = 0
      for yy in range(y-2,y+2):
        for xx in range(x-1, x+2):
          if 0 <= yy < grid.shape[0] and 0 <= xx < grid.shape[1]:
            if grid[yy,xx] == 1:
              blues_found +=1
      if blues_found == 12:
        return x,y
    return None, None

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair and returns relevant metrics."""
    input_yellow_pixels = find_yellow_pixels(input_grid)
    output_yellow_pixels = find_yellow_pixels(output_grid)
    blue_block_center_x, blue_block_center_y = get_blue_block_center(output_grid)

    return {
        'input_yellow_count': len(input_yellow_pixels),
        'input_yellow_positions': input_yellow_pixels.tolist() if len(input_yellow_pixels) > 0 else [],
        'output_yellow_count': len(output_yellow_pixels),
        'output_yellow_positions': output_yellow_pixels.tolist() if len(output_yellow_pixels) > 0 else [],
        'blue_block_center_x': blue_block_center_x,
        'blue_block_center_y': blue_block_center_y,
    }

def analyze_task(task):
    results = []
    for example in task['train']:  # Assuming 'train' contains input-output pairs
         results.append(analyze_example(np.array(example['input']), np.array(example['output'])))
    return results

# Example usage (replace with the actual task data structure)
task = {
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[1, 1, 1, 0, 0, 0, 4, 0], [1, 1, 1, 0, 0, 0, 0, 0], [1, 4, 1, 0, 0, 0, 4, 0], [1, 1, 1, 0, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0, 0]], 'output': [[1, 1, 1, 0, 0, 4, 0, 0, 0], [1, 4, 1, 0, 0, 4, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]}
    ]
}
results = analyze_task(task)
for i,r in enumerate(results):
  print(f"Example {i+1}:")
  print(r)
