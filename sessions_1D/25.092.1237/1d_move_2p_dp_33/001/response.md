```python
import numpy as np

def find_contiguous_block(row, exclude_colors=(0, 9)):
    """
    Finds the start index, end index (exclusive), and color of the first 
    contiguous block of a single color, excluding specified colors.
    Returns (start_idx, end_idx, color) or (None, None, None) if not found.
    """
    start_idx = None
    block_color = None
    for i, pixel in enumerate(row):
        if start_idx is None:
            # Look for the start of a potential block
            if pixel not in exclude_colors:
                start_idx = i
                block_color = pixel
        elif pixel == block_color:
            # Continue the current block
            continue
        elif pixel != block_color:
            # Block ended just before this pixel
            return start_idx, i, block_color
            
    # If the loop finishes and we were in a block, the block ends at the end of the row
    if start_idx is not None:
        return start_idx, len(row), block_color
        
    return None, None, None

def find_first_occurrence(row, target_color):
    """Finds the index of the first occurrence of target_color."""
    for i, pixel in enumerate(row):
        if pixel == target_color:
            return i
    return None

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    1. Identify the main contiguous block (not white 0 or maroon 9).
    2. Identify the single maroon (9) pixel.
    3. Identify white pixels before the main block (prefix).
    4. Identify white pixels between the main block and the maroon pixel (separator).
    5. Identify white pixels after the maroon pixel (suffix).
    6. Reconstruct the grid as: prefix + separator + main_block + maroon + suffix.
    
    Assumes the input is a 1xN grid.
    """
    
    # Since grids are 1xN, work with the first row directly
    # Convert to list for easier slicing and concatenation
    input_row = list(input_grid[0]) 
    
    # 1. Identify the main contiguous block
    block_start, block_end, block_color = find_contiguous_block(input_row, exclude_colors=(0, 9))
    if block_start is None:
        # Should not happen based on examples, but handle defensively
        return input_grid 
    main_block = input_row[block_start:block_end]

    # 2. Identify the single maroon (9) pixel
    maroon_idx = find_first_occurrence(input_row, 9)
    if maroon_idx is None:
         # Should not happen based on examples
        return input_grid
    target_pixel = [input_row[maroon_idx]] # Keep as a list

    # 3. Identify prefix whites (pixels before the main block)
    prefix_whites = input_row[0:block_start]

    # 4. Identify separator whites (pixels between main block end and maroon index)
    separator_whites = input_row[block_end:maroon_idx]

    # 5. Identify suffix whites (pixels after the maroon index)
    suffix_whites = input_row[maroon_idx+1:]

    # 6. Construct the output row by concatenating in the new order
    output_row_list = prefix_whites + separator_whites + main_block + target_pixel + suffix_whites
    
    # Convert back to the expected 2D numpy array format (1xN)
    output_grid = np.array([output_row_list], dtype=int)

    return output_grid
```