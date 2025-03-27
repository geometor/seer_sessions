```python
"""
Transformation Rule:
1. Identify all orange (7) pixels in the input grid.
2. Determine the bounding box enclosing these orange pixels (min/max row and column).
3. Find all instances of a 3x3 "hollow square" pattern within the input grid. 
   This pattern has the structure:
   [[C, C, C],
    [C, 5, C],
    [C, C, C]]
   where C is any non-gray color (not 5) and the center pixel is gray (5).
4. Select the unique hollow square pattern instance whose 3x3 area is entirely 
   contained within the bounding box defined by the orange pixels.
5. Output this selected 3x3 pattern.
"""

import numpy as np

def find_bounding_box(grid, color):
    """
    Finds the minimum bounding box (min_row, min_col, max_row, max_col) 
    containing all pixels of the specified color.
    Returns None if the color is not found.
    """
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_r, max_r = np.min(rows), np.max(rows)
    min_c, max_c = np.min(cols), np.max(cols)
    return min_r, min_c, max_r, max_c

def is_hollow_square(subgrid):
    """
    Checks if a 3x3 subgrid matches the hollow square pattern.
    Returns the border color C if it matches, otherwise None.
    """
    if subgrid.shape != (3, 3):
        return None
    
    # Check center pixel is gray (5)
    if subgrid[1, 1] != 5:
        return None
        
    # Get the potential border color C from the top-left corner
    border_color = subgrid[0, 0]
    
    # Border color must not be gray (5) or background (0)
    if border_color == 5 or border_color == 0:
        return None
        
    # Check all 8 border pixels match the border_color
    if (subgrid[0, 0] == border_color and
        subgrid[0, 1] == border_color and
        subgrid[0, 2] == border_color and
        subgrid[1, 0] == border_color and
        subgrid[1, 2] == border_color and
        subgrid[2, 0] == border_color and
        subgrid[2, 1] == border_color and
        subgrid[2, 2] == border_color):
        return border_color
    else:
        return None

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    
    # 1. & 2. Find the bounding box of orange (7) pixels
    orange_bbox = find_bounding_box(input_grid, 7)
    
    # If no orange pixels found, cannot determine the region (handle as error or default)
    if orange_bbox is None:
        # Based on the task structure, we expect orange pixels.
        # If not found, we might return an empty grid or raise an error.
        # Let's assume for now this won't happen in valid test cases.
        # Or perhaps return the input unchanged or a default small grid.
        # For now, let's raise an error for clarity during testing.
        raise ValueError("No orange (7) pixels found to define the bounding box.")
        
    min_r, min_c, max_r, max_c = orange_bbox
    
    # 3. & 4. & 5. Search for the hollow square pattern within the orange bounding box
    grid_height, grid_width = input_grid.shape
    found_pattern = None
    
    # Iterate through all possible top-left corners (r, c) for a 3x3 subgrid
    for r in range(grid_height - 2):
        for c in range(grid_width - 2):
            # Extract the 3x3 subgrid
            subgrid = input_grid[r:r+3, c:c+3]
            
            # Check if it's a hollow square pattern
            border_color = is_hollow_square(subgrid)
            
            if border_color is not None:
                # Check if this pattern is fully contained within the orange bbox
                # Condition: min_r <= r AND r + 2 <= max_r AND min_c <= c AND c + 2 <= max_c
                if (min_r <= r and r + 2 <= max_r and
                    min_c <= c and c + 2 <= max_c):
                    # Found the unique pattern within the box
                    found_pattern = subgrid
                    # Assuming uniqueness, we can stop searching
                    break # Exit inner loop (cols)
        if found_pattern is not None:
            break # Exit outer loop (rows)

    # 6. Return the found pattern
    if found_pattern is not None:
        return found_pattern
    else:
        # This case implies a hollow square pattern exists but none are inside the bbox,
        # or no hollow square patterns exist at all. This shouldn't happen based on examples.
        raise ValueError("Could not find a hollow square pattern within the orange bounding box.")

```