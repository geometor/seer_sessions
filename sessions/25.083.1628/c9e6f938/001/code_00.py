"""
1.  **Identify Objects:** Recognize the background (white, 0) and the primary object (orange, 7).

2.  **Determine Output Dimensions:** The output grid's width is double the input grid's width. The output grid's height is the same as the input grid's height.

3. **Expand the grid:** create an output grid that is double in width.

4.  **Replicate and Position:**
    *   For each orange (7) pixel in the input grid, place an orange pixel in the corresponding position in the output grid. The row number should be the same. The new column number is calculated with: `output_col= input_col * 2`. Place additional orange pixels to "connect" the shapes, ensuring the new shape contains all pixels from the original, plus newly added pixels, all contiguous.

5.  **Fill Background:** Fill all remaining cells in the output grid with the background color (white, 0).
"""

import numpy as np

def get_objects(grid):
    # returns a dictionary of objects, where each object is a list of coordinates
    objects = {}
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell not in objects:
                objects[cell] = []
            objects[cell].append((row_index, col_index))
    return objects

def transform(input_grid):
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros((height, width * 2), dtype=int)

    # Get objects
    objects = get_objects(input_grid)

    # Replicate and position the primary object (orange, 7)
    if 7 in objects:
        for row, col in objects[7]:
            output_grid[row, col * 2] = 7

        # connect the orange pixels
        min_col = min(col * 2 for _, col in objects[7])
        max_col = max(col * 2 for _, col in objects[7])
        
        for row in range(height):
            has_orange = False
            for col in range(min_col, max_col+1):
                if output_grid[row,col] == 7:
                    has_orange = True

            if has_orange:
                for col in range(min_col, max_col + 1):
                    if output_grid[row,col] == 7 or any(output_grid[row,c] == 7 for c in range(min_col,col)):
                        output_grid[row,col] = 7

    return output_grid