import numpy as np
from collections import defaultdict

"""
The transformation operates on an input grid characterized by a repeating pattern: 3x3 blocks of azure (8) pixels separated by single lines of white (0) pixels, forming a larger structure based on 4x4 meta-units.

1.  **Identify Trigger Pairs:** Locate pairs of identically colored pixels in the input grid, excluding white (0) and azure (8). These are "trigger" pixels. Each distinct color found (other than 0 or 8) will have exactly two pixels.
2.  **Define Bounding Boxes:** For each pair of trigger pixels with color `C` at coordinates `(r1, c1)` and `(r2, c2)`, determine the inclusive bounding rectangle defined by these points: minimum row `min_r = min(r1, r2)`, maximum row `max_r = max(r1, r2)`, minimum column `min_c = min(c1, c2)`, maximum column `max_c = max(c1, c2)`.
3.  **Apply Transformation within Bounding Box:** Iterate through each pixel `(r, c)` within the calculated bounding box (`min_r <= r <= max_r`, `min_c <= c <= max_c`). Apply the following rules based on the pixel's color in the *input* grid:
    *   **If `input_grid[r, c]` is white (0):** Change the corresponding pixel in the output grid to the trigger color `C`.
    *   **If `input_grid[r, c]` is azure (8):**
        *   Determine the pixel's relative position within its local 3x3 azure block. A pixel `(r, c)` is part of an azure block because its indices are not multiples of 4 (i.e., `r % 4 != 0` and `c % 4 != 0`).
        *   Calculate the relative row `rel_r = (r - 1) % 4` and relative column `rel_c = (c - 1) % 4`. These relative coordinates range from 0 to 2 within the 3x3 block.
        *   Change the corresponding pixel in the output grid to the trigger color `C` *only if* the relative coordinates `(rel_r, rel_c)` are `(1, 0)` or `(1, 2)` (i.e., the pixel is in the middle row, and either the first or the third column of its 3x3 azure block).
    *   **If `input_grid[r, c]` is any other color (including the trigger color itself):** Leave the corresponding pixel in the output grid unchanged (it retains the value from the input grid).
4.  **Repeat for all Trigger Pairs:** Perform step 3 for every identified trigger pair and its associated bounding box. If bounding boxes from different trigger colors overlap, the transformations are applied independently based on the input grid's state within each box. The order of processing trigger colors does not affect the final result because changes depend only on the initial input grid state.
5.  **Final Output:** The resulting grid after applying transformations for all trigger pairs is the final output.
"""

def find_trigger_pixels(grid):
    """
    Finds pixels that are not white (0) or azure (8) and groups them by color.
    Assumes each trigger color appears exactly twice.
    Args:
        grid (np.array): The input grid.
    Returns:
        dict: A dictionary where keys are trigger colors (int > 0 and != 8) and
              values are lists containing two (row, col) coordinates for that color.
    """
    triggers = defaultdict(list)
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Trigger colors are non-white (0) and non-azure (8)
            if color != 0 and color != 8:
                triggers[color].append((r, c))
    return triggers


def transform(input_grid):
    """
    Transforms the input grid based on trigger pixel pairs defining rectangles.
    White pixels within the rectangle are changed to the trigger color.
    Specific azure pixels (middle row, 1st/3rd col of their 3x3 block) within the rectangle are changed.
    
    Args:
        input_grid (np.array): The input grid as a NumPy array.
        
    Returns:
        np.array: The transformed output grid.
    """
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Find all trigger pixels and group them by color
    trigger_locations_by_color = find_trigger_pixels(input_grid)
    
    # Process each trigger color
    for color, locations in trigger_locations_by_color.items():
        # Expecting exactly two locations per color based on examples
        if len(locations) == 2:
            (r1, c1), (r2, c2) = locations
            
            # Determine the bounding box coordinates (inclusive)
            min_row = min(r1, r2)
            max_row = max(r1, r2)
            min_col = min(c1, c2)
            max_col = max(c1, c2)
            
            # Iterate through the bounding box
            for r in range(min_row, max_row + 1):
                for c in range(min_col, max_col + 1):
                    # Get the original color from the input grid
                    original_color = input_grid[r, c]
                    
                    # Rule 1: If the pixel is white (0)
                    if original_color == 0:
                        output_grid[r, c] = color
                        
                    # Rule 2: If the pixel is azure (8)
                    elif original_color == 8:
                        # Check if it's actually within an azure block (not on a grid line)
                        # This check is implicitly handled by checking original_color == 8,
                        # as grid lines are color 0.
                        
                        # Calculate relative coordinates within the 3x3 block
                        # The indices are 1-based for the pattern, but 0-based in array.
                        # A pixel at (r,c) is in a block starting visually at row k*4+1, col l*4+1
                        # Relative row within 3x3 block (0, 1, or 2)
                        rel_r = (r - 1) % 4 
                        # Relative col within 3x3 block (0, 1, or 2)
                        rel_c = (c - 1) % 4 
                        
                        # Change color only if in the middle row (rel_r==1) and 
                        # first or third column (rel_c==0 or rel_c==2)
                        if rel_r == 1 and (rel_c == 0 or rel_c == 2):
                            output_grid[r, c] = color
                            
                    # Rule 3: Other colors (including triggers) are left unchanged
                    # This is handled by initializing output_grid as a copy of input_grid
                    # and only modifying white (0) or specific azure (8) pixels.

    # Return the modified grid                
    return output_grid