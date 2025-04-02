import numpy as np

"""
Transforms a 1D grid by moving a contiguous block of a single color (not white or green) 
so that its right end is immediately adjacent to the left of a single green pixel. 
The green pixel's position remains unchanged. The background is white.
"""

def find_pixel(grid, color):
  """Finds the index of the first occurrence of a specific color in the grid."""
  for i, pixel in enumerate(grid):
    if pixel == color:
      return i
  return -1 # Should not happen based on task description

def find_block(grid, exclude_colors):
  """
  Finds the first contiguous block of pixels whose color is not in exclude_colors.
  Returns the color, start index, and length of the block.
  """
  block_color = -1
  block_start = -1
  block_length = 0
  in_block = False

  for i, pixel in enumerate(grid):
    if pixel not in exclude_colors:
      if not in_block:
        # Start of a new block
        in_block = True
        block_color = pixel
        block_start = i
        block_length = 1
      elif pixel == block_color:
        # Continuing the current block
        block_length += 1
      else:
        # Found a different non-excluded color, but the task implies only one block
        # Assuming the first block found is the target
        break 
    elif in_block:
      # End of the block
      break 
      
  if block_start != -1:
      return block_color, block_start, block_length
  else:
      # Should not happen if a block always exists
      return None, -1, 0 

def transform(input_grid):
    """
    Moves a colored block to be adjacent to a fixed green pixel in a 1D grid.

    Args:
        input_grid: A list or numpy array representing the 1D input grid.

    Returns:
        A numpy array representing the transformed 1D output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid)
    grid_size = len(grid_np)

    # Initialize output_grid with background color (white, 0)
    output_grid = np.zeros(grid_size, dtype=int)

    # 1. Find the index of the anchor pixel (green, 3)
    green_index = find_pixel(grid_np, 3)
    if green_index == -1:
        # Handle error: green pixel not found (though problem implies it exists)
        return output_grid # Or raise an error

    # 2. Find the main block (non-white, non-green)
    # Define colors to exclude when searching for the main block
    exclude_colors = {0, 3} 
    block_color, _, block_length = find_block(grid_np, exclude_colors)

    if block_color is None:
        # Handle error: main block not found (though problem implies it exists)
        # Place only the green pixel if no block is found
        if green_index != -1:
             output_grid[green_index] = 3
        return output_grid

    # 3. Calculate the new position for the main block
    # The right end of the block should be at green_index - 1
    new_block_end_index = green_index - 1
    # The start index is calculated from the end index and length
    new_block_start_index = new_block_end_index - block_length + 1

    # 4. Place the main block in the output grid
    # Ensure indices are within bounds (although problem constraints might guarantee this)
    if 0 <= new_block_start_index < grid_size and 0 <= new_block_end_index < grid_size:
         output_grid[new_block_start_index : new_block_end_index + 1] = block_color

    # 5. Place the anchor pixel (green, 3) in the output grid at its original position
    if 0 <= green_index < grid_size:
        output_grid[green_index] = 3

    return output_grid.tolist() # Return as list to match typical ARC format if needed
