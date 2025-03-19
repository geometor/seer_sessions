"""
1. Preserve Gray Lines: The gray (value 5) grid lines, both horizontal and vertical, are preserved in the output.

2. Identify Target Section: A specific section of the grid is defined.(Currently assumed as bottom-right, but need clarification.)

3. Green Pixel Removal (Outside Target Section): All green (value 3) pixels *outside* of the target section are removed (changed to 0/white).

4. Green Pixel Consolidation (Inside Target Section):
    *   Count the number of green pixels remaining within the identified target section.
    *   Remove all of existing green pixels in that section.
    *   If the count is greater than or equal to 9, arrange green pixels in a 3x3 square at the bottom-right corner of that section.
    *   If the count is less than 9 and greater than 0, arrange the green pixels as a horizontal line along the bottom edge of that section, starting from the right. The line's length equals the green pixel count.
    * If no green pixels are remained, leave the section unchanged.

5. Target Section Identification logic: (needs improvement)
    *   Currently: Assumes the last horizontal and vertical gray line defines the bottom-right section. - Incorrect assumption.
    *   Improved: Should focus on section that could contain a 3x3 square.
"""

import numpy as np

def _find_target_section(grid):
    """Identifies the target section based on potential for 3x3 square."""
    rows, cols = grid.shape
    
    # Iterate through potential top-left corners of a 3x3 square
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Check if a 3x3 square can exist at this location
            valid_section = True
            for i in range(r, r + 3):
                for j in range(c, c + 3):
                    if grid[i,j] == 5 :
                        valid_section= False
                        break;
                if not valid_section:
                    break
            
            if valid_section:
                return r, r + 3, c, c + 3

    # Fallback: return the entire grid if no suitable section is found
    return 0, rows, 0, cols

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Preserve Gray Lines: (Implicitly handled by copying the input grid)

    # 2. Identify Target Section:
    target_row_start, target_row_end, target_col_start, target_col_end = _find_target_section(input_grid)

    # 3. Green Pixel Removal (Outside Target Section):
    for r in range(rows):
        for c in range(cols):
            if not (target_row_start <= r < target_row_end and target_col_start <= c < target_col_end):
                if output_grid[r, c] == 3:
                    output_grid[r, c] = 0

    # 4. Green Pixel Consolidation (Inside Target Section):
    num_green = 0
    for r in range(target_row_start, target_row_end):
        for c in range(target_col_start, target_col_end):
            if output_grid[r, c] == 3:
                num_green += 1

    for r in range(target_row_start, target_row_end):
        for c in range(target_col_start, target_col_end):
            output_grid[r,c] = 0 if output_grid[r,c] == 3 else output_grid[r,c] #reset all greens in section to zero

    if num_green > 0:
        if num_green >= 9:
            for r in range(target_row_end - 3, target_row_end):
                for c in range(target_col_end - 3, target_col_end):
                    output_grid[r, c] = 3
        else:
            for c in range(target_col_end - num_green, target_col_end):
                output_grid[target_row_end - 1, c] = 3

    return output_grid