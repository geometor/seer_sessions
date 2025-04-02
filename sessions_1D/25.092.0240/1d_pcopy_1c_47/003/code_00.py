import numpy as np

def find_primary_color(grid_array):
  """Finds the single non-zero color in the grid."""
  unique_colors = np.unique(grid_array)
  for color in unique_colors:
    if color != 0:
      return color
  # Return 0 if only white is present or grid is empty
  return 0

def find_block_starts(grid_array, color):
    """Finds the starting column indices of contiguous blocks of a given color in a 1D array."""
    starts = []
    if color == 0: # Cannot search for blocks of background color
        return starts
        
    # Assuming grid_array is 2D, get the first (and only) row
    if grid_array.ndim == 2:
        row = grid_array[0] 
    else: # If somehow it's already 1D
        row = grid_array
        
    width = len(row)
    for c in range(width):
        # Check if current pixel is the target color
        is_target_color = (row[c] == color)
        
        # Check if it's the start of a block:
        # Either it's the first column (c == 0) 
        # OR the previous column (c-1) was white (0)
        is_start_of_block = (c == 0) or (row[c-1] == 0)
        
        if is_target_color and is_start_of_block:
            starts.append(c)
    return starts

def place_block(grid_array, start_col, color, length=3):
    """Places a block of the specified color and length in the grid, handling boundaries."""
    height, width = grid_array.shape
    for i in range(length):
        col_idx = start_col + i
        # Ensure we don't write outside the grid's width
        if 0 <= col_idx < width: 
            # Assuming a 1-row grid based on examples
            grid_array[0, col_idx] = color
            
"""
Transforms the input grid according to the following rules:
1. Initialize an output grid with the same dimensions as the input, filled with white (0).
2. Identify the primary color (the single non-white color) in the input grid.
3. Find the starting column index of every contiguous block of the primary color in the input grid.
4. If no blocks are found, return the initialized white grid.
5. Place a block of three pixels of the primary color in the output grid starting at the same index as the *first* found input block.
6. For every *subsequent* input block found, place a block of three pixels of the primary color in the output grid starting at the index *one less* than the corresponding input block's start index.
7. Handle boundary conditions during placement.
"""
def transform(input_grid):
    # Convert input list of lists to numpy array
    input_array = np.array(input_grid, dtype=int)
    
    # Get grid dimensions
    height, width = input_array.shape
    
    # Initialize output_grid with the same dimensions, filled with white (0)
    output_array = np.zeros_like(input_array)
    
    # Find the primary color
    primary_color = find_primary_color(input_array)
    
    # If no primary color found (e.g., all white input), return the white grid
    if primary_color == 0:
        return output_array.tolist()
        
    # Find the start indices of all blocks of the primary color in the input
    block_starts = find_block_starts(input_array, primary_color)
    
    # If no blocks were found, return the white grid
    if not block_starts:
        return output_array.tolist()
        
    # Process the first block
    first_start_index = block_starts[0]
    place_block(output_array, first_start_index, primary_color, length=3)
    
    # Process subsequent blocks (if any)
    if len(block_starts) > 1:
        for start_index in block_starts[1:]:
            # Calculate the shifted start index for the output
            output_start_index = start_index - 1
            # Ensure the shifted index is not negative before placing
            if output_start_index >= 0:
                 place_block(output_array, output_start_index, primary_color, length=3)
            # If the shifted index would be negative, the block effectively disappears 
            # or potentially overlaps differently, but based on examples, 
            # we just place starting from index 0 if shift results in < 0.
            # Re-evaluating: The examples don't show blocks starting at index 0 being shifted left.
            # Let's stick to the literal interpretation: place at index-1 if index-1 >= 0.
            
    # Convert the numpy array back to a list of lists for the expected output format
    return output_array.tolist()