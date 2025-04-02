```python
import numpy as np

"""
Transformation Rule:
1. Identify the contiguous horizontal block of non-white (0), non-red (2) color (the main color block). Record its color and the column index of its rightmost pixel.
2. Identify the column index of the single red pixel (color 2).
3. Starting from the column immediately to the right of the main color block's rightmost pixel, change all pixels to the color of the main color block, up to (but not including) the column containing the red pixel.
4. Leave all other pixels in the grid unchanged.
"""

def find_main_block(row):
    """Finds the main color block's color and rightmost index."""
    main_color = -1
    block_end_index = -1
    for i, pixel in enumerate(row):
        if pixel != 0 and pixel != 2:
            # Found a potential start or continuation of the block
            if main_color == -1:
                main_color = pixel # Set the color on first encounter
            elif pixel != main_color:
                 # This shouldn't happen based on examples, but good to handle
                 # If colors change, we stick with the first block found
                 break 
            block_end_index = i # Update the end index
        elif main_color != -1:
            # If we were in a block and encountered 0 or 2, the block ended
            break
            
    # Alternative using numpy - potentially cleaner if only one block guaranteed
    # main_indices = np.where((row != 0) & (row != 2))[0]
    # if len(main_indices) > 0:
    #     main_color = row[main_indices[0]]
    #     block_end_index = np.max(main_indices)
    # else:
    #     main_color = -1
    #     block_end_index = -1
        
    return main_color, block_end_index

def find_boundary_pixel(row, boundary_color=2):
    """Finds the index of the first boundary pixel."""
    try:
        # Find the first occurrence of the boundary color
        boundary_index = np.where(row == boundary_color)[0][0]
        return boundary_index
    except IndexError:
        # Boundary color not found
        return -1

def transform(input_grid):
    """
    Extends a horizontal block of color rightwards until it reaches a 
    boundary pixel (red, color 2).
    """
    # Make a copy to modify
    output_grid = input_grid.copy()
    
    # Assuming the grid is always 1 row high based on examples
    if input_grid.shape[0] != 1:
        # Handle unexpected input dimension if necessary
        # For now, assume it's always 1 row
        pass 
        
    row = output_grid[0] # Work with the first (and only) row

    # 1. Identify the main color block and its properties
    main_color, block_end_index = find_main_block(row)

    # 2. Identify the boundary pixel's location
    boundary_index = find_boundary_pixel(row, 2) # 2 is red

    # 3. Perform the extension if both block and boundary are found
    #    and the block ends before the boundary
    if main_color != -1 and boundary_index != -1 and block_end_index < boundary_index - 1:
        # Define the start and end columns for filling
        fill_start_col = block_end_index + 1
        fill_end_col = boundary_index # Slice goes up to, but not including, this index
        
        # Change the pixels in the output grid
        row[fill_start_col:fill_end_col] = main_color
        
    # 4. Return the modified grid
    return output_grid
```