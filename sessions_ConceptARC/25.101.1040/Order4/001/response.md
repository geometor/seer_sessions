```python
import numpy as np
from collections import Counter

"""
Identifies vertical blocks of non-background colors separated by background (0) columns.
For each block, it determines the primary color (MainColor, not 0 or 5) and an impurity color (ImpurityColor, either 0 or 5).
Based on the ImpurityColor, a specific color transformation map is applied to the MainColor to determine the OutputColor.
The output grid is created by filling the spatial extent (min/max rows and columns) of each input block with its corresponding OutputColor.
"""

def find_blocks(grid: np.ndarray) -> list[tuple[int, int, int, int]]:
    """
    Identifies the bounding boxes (min_row, max_row, col_start, col_end) of vertical blocks.
    Blocks are regions containing non-background pixels, separated by columns of only background pixels.

    Args:
        grid: The input grid as a NumPy array.

    Returns:
        A list of tuples, where each tuple represents a block's bounding box:
        (min_row, max_row, col_start, col_end).
    """
    rows, cols = grid.shape
    non_bg_cols = np.any(grid != 0, axis=0)
    blocks = []
    
    col_start = -1
    for c in range(cols):
        if non_bg_cols[c] and col_start == -1:
            # Start of a potential block
            col_start = c
        elif not non_bg_cols[c] and col_start != -1:
            # End of the block
            col_end = c # Exclusive end index initially
            
            # Find min/max rows for this block
            block_cols_grid = grid[:, col_start:col_end]
            non_bg_rows_in_block = np.where(np.any(block_cols_grid != 0, axis=1))[0]
            
            if len(non_bg_rows_in_block) > 0:
                min_row = non_bg_rows_in_block.min()
                max_row = non_bg_rows_in_block.max()
                blocks.append((min_row, max_row, col_start, col_end - 1)) # Inclusive col_end
                
            col_start = -1 # Reset for the next block
            
    # Handle block extending to the last column
    if col_start != -1:
        col_end = cols # Exclusive end index
        block_cols_grid = grid[:, col_start:col_end]
        non_bg_rows_in_block = np.where(np.any(block_cols_grid != 0, axis=1))[0]
        if len(non_bg_rows_in_block) > 0:
             min_row = non_bg_rows_in_block.min()
             max_row = non_bg_rows_in_block.max()
             blocks.append((min_row, max_row, col_start, col_end - 1)) # Inclusive col_end

    return blocks

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying colored blocks, determining their
    main and impurity colors, applying a color transformation rule based on the
    impurity, and filling the block area in the output grid with the new color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize output grid with background color (0)
    output_np = np.zeros_like(input_np)

    # Define the color transformation maps
    map_impurity_5 = {1: 4, 2: 2, 3: 1, 4: 3} # {Blue: Yellow, Red: Red, Green: Blue, Yellow: Green}
    map_impurity_0 = {2: 7, 4: 6, 6: 2, 7: 4} # {Red: Orange, Yellow: Magenta, Magenta: Red, Orange: Yellow}

    # Find all blocks in the input grid
    blocks = find_blocks(input_np)

    # Process each block
    for min_row, max_row, col_start, col_end in blocks:
        # Extract the relevant subgrid for analysis (includes potential impurity 0)
        block_subgrid = input_np[min_row:max_row+1, col_start:col_end+1]
        
        # Find unique colors within the block's bounding box
        unique_colors = np.unique(block_subgrid)
        
        # Determine MainColor and ImpurityColor
        main_color = -1
        impurity_color = -1
        
        # Check for impurity 5 first
        if 5 in unique_colors:
            impurity_color = 5
            # Find the main color (not 0 and not 5)
            for color in unique_colors:
                if color != 0 and color != 5:
                    main_color = color
                    break
        # If impurity is not 5, check if impurity is 0 (within the block bounds)
        elif 0 in unique_colors:
             impurity_color = 0
             # Find the main color (the only non-zero color)
             for color in unique_colors:
                if color != 0:
                    main_color = color
                    break
        else:
            # Should not happen based on examples, but handle defensively
            # If only one non-zero color and it's not 5, treat it as main
             for color in unique_colors:
                if color != 0:
                    main_color = color
                    break
            # This case might need refinement if new examples appear

        # Determine the OutputColor using the appropriate map
        output_color = -1 # Default/error value
        if impurity_color == 5 and main_color in map_impurity_5:
            output_color = map_impurity_5[main_color]
        elif impurity_color == 0 and main_color in map_impurity_0:
            output_color = map_impurity_0[main_color]
        elif impurity_color == -1 and main_color != -1:
             # Fallback if no impurity detected but a main color exists
             # (e.g., a solid block of a single color other than 5)
             # Based on example 1 (red block), it seems the color remains unchanged if impurity 5 isn't present.
             # Let's assume the map_impurity_5 is the default or applies if only one color is present?
             # Example 1's red block (2) becomes red (2) -> Consistent with map_impurity_5.
             # Let's apply map_impurity_5 as default if no impurity 0 is found.
             if main_color in map_impurity_5:
                 output_color = map_impurity_5[main_color]
             else:
                 # If not in map_impurity_5 either, maybe it stays the same?
                 output_color = main_color # Best guess


        # Fill the corresponding area in the output grid
        if output_color != -1:
             output_np[min_row:max_row+1, col_start:col_end+1] = output_color
        else:
             # If we couldn't determine an output color, copy the original block? Or leave as bg?
             # Leaving as background (initial state) seems safer.
             print(f"Warning: Could not determine output color for block at rows {min_row}-{max_row}, cols {col_start}-{col_end}")


    # Convert the NumPy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```