```python
import numpy as np

"""
Maps the non-white pixel from each 3x3 block of the input grid to the corresponding cell in a 3x3 output grid.

1. Determines the dimensions of the input grid.
2. Calculates the dimensions of the sub-blocks based on a 3x3 output grid.
3. Initializes a 3x3 output grid.
4. Iterates through each of the 9 conceptual blocks in the input grid.
5. For each block, finds the single non-white pixel.
6. Places the color of that non-white pixel into the corresponding cell of the 3x3 output grid.
7. Returns the resulting 3x3 grid.
"""

def find_non_white_pixel_in_block(block):
  """Finds the value of the first non-white pixel in a given block."""
  for r in range(block.shape[0]):
    for c in range(block.shape[1]):
      if block[r, c] != 0:
        return block[r, c]
  return 0 # Should not happen based on problem description, but good practice

def transform(input_grid):
    """
    Transforms the input grid by mapping non-white pixels from 3x3 blocks
    to a 3x3 output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Define output dimensions
    output_height = 3
    output_width = 3

    # Calculate block dimensions
    # Use integer division // as block dimensions must be whole numbers
    block_height = input_height // output_height
    block_width = input_width // output_width

    # Initialize the 3x3 output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the 3x3 block structure
    for block_r in range(output_height):
        for block_c in range(output_width):
            # Define the boundaries of the current block in the input grid
            start_row = block_r * block_height
            end_row = start_row + block_height
            start_col = block_c * block_width
            end_col = start_col + block_width

            # Extract the current block from the input grid
            current_block = input_np[start_row:end_row, start_col:end_col]

            # Find the non-white pixel color within the current block
            pixel_color = find_non_white_pixel_in_block(current_block)

            # Place the found color into the corresponding cell of the output grid
            output_grid[block_r, block_c] = pixel_color

    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()
```