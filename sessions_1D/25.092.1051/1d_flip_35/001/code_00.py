import numpy as np
from collections import Counter

"""
Identifies a contiguous horizontal block of non-white pixels in a single-row input grid.
This block consists of a sequence of pixels of one color (main color) and a single pixel of another color (singleton color) located at one end of the sequence.
The transformation moves the singleton pixel to the opposite end of the main color sequence, maintaining the relative order of the main sequence pixels and the block's overall position within the row.
"""

def find_non_white_block(grid_row):
    """Finds the start index, end index (exclusive), and content of the non-white block."""
    start_index = -1
    end_index = -1
    block = []
    for i, pixel in enumerate(grid_row):
        if pixel != 0 and start_index == -1:
            start_index = i
        if pixel != 0:
            block.append(pixel)
        if pixel == 0 and start_index != -1 and end_index == -1:
            end_index = i
            break
    # Handle case where the block extends to the end of the row
    if start_index != -1 and end_index == -1:
        end_index = len(grid_row)
        
    if start_index == -1: # No block found
        return -1, -1, []
        
    return start_index, end_index, block

def transform(input_grid):
    """
    Transforms the input grid according to the rule: move the singleton pixel
    at the end of a sequence to the other end.
    """
    # Assuming input_grid is a list of lists, but the examples are 1xN
    # Convert to numpy array for easier handling if needed, but list operations are fine for 1D
    if isinstance(input_grid, np.ndarray):
      input_row = input_grid.tolist()[0] # Extract the first (and only) row as a list
    elif isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
        input_row = input_grid[0]
    elif isinstance(input_grid, list) and all(isinstance(x, int) for x in input_grid):
         # Handle case where input might be just a flat list representing the row
        input_row = input_grid
    else:
         raise ValueError("Input grid format not recognized or not a single row.")

    # Initialize output_grid as a copy of the input row
    output_row = list(input_row)
    grid_width = len(input_row)

    # Find the non-white block
    start_index, end_index, block = find_non_white_block(input_row)

    # If no block is found, return the original grid
    if start_index == -1:
        # Ensure output format matches typical ARC format (list of lists)
        return [output_row] if not isinstance(input_grid, np.ndarray) else np.array([output_row])


    # Count pixel occurrences in the block to find the singleton
    pixel_counts = Counter(block)
    singleton_color = -1
    main_color = -1
    
    if len(pixel_counts) != 2:
        # This case shouldn't happen based on examples, but good to handle
        print(f"Warning: Expected 2 distinct non-white colors in the block, found {len(pixel_counts)}. Returning original.")
        return [output_row] if not isinstance(input_grid, np.ndarray) else np.array([output_row])

    for color, count in pixel_counts.items():
        if count == 1:
            singleton_color = color
        else:
            main_color = color
            
    if singleton_color == -1 or main_color == -1:
        # This also shouldn't happen if len(pixel_counts) == 2
        print("Warning: Could not identify singleton or main color. Returning original.")
        return [output_row] if not isinstance(input_grid, np.ndarray) else np.array([output_row])


    # Reconstruct the block based on the singleton's position
    new_block = []
    if block[0] == singleton_color:
        # Singleton was at the start, move it to the end
        new_block = [p for p in block if p == main_color] + [singleton_color]
    elif block[-1] == singleton_color:
        # Singleton was at the end, move it to the start
        new_block = [singleton_color] + [p for p in block if p == main_color]
    else:
        # Singleton is somehow in the middle? This contradicts the perceived pattern.
        print("Warning: Singleton color not found at either end of the block. Returning original.")
        return [output_row] if not isinstance(input_grid, np.ndarray) else np.array([output_row])


    # Place the new block back into the output row
    for i in range(len(new_block)):
        output_row[start_index + i] = new_block[i]
        
    # Ensure output format matches typical ARC format (list of lists) or numpy array
    return [output_row] if not isinstance(input_grid, np.ndarray) else np.array([output_row])