```python
import numpy as np

"""
Transformation Rule:
1. Identify the single azure (8) colored rectangular object in the input grid.
2. Determine the bounding box of this azure object (minimum row, maximum row, minimum column, maximum column).
3. Create an output grid, initially as a copy of the input grid.
4. Iterate through every cell (row `r`, column `c`) of the grid.
5. Check two conditions for each cell:
   a) Is the cell's original color in the input grid white (0)?
   b) Does the cell's row `r` fall within the azure object's row range (inclusive) OR does the cell's column `c` fall within the azure object's column range (inclusive)?
6. If both conditions (a and b) are true, change the color of the corresponding cell in the output grid to yellow (4).
7. If either condition is false, the cell in the output grid retains its color copied from the input grid.
8. Return the modified output grid.
"""

def find_object_coords(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    coords = np.argwhere(grid == color)
    return coords

def get_bounding_box(coords):
    """
    Calculates the bounding box (min_row, max_row, min_col, max_col) 
    from a list of coordinates. Returns None if no coordinates are provided.
    """
    if coords.size == 0:
        return None
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Fills the background (white) pixels with yellow in a cross-shaped area 
    defined by the bounding box of the single azure object, preserving all 
    original non-white objects.
    
    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    
    # Define target colors
    azure_color = 8
    fill_color = 4 # yellow
    background_color = 0 # white
    
    # Find the coordinates of the azure (8) object
    azure_coords = find_object_coords(input_grid, azure_color)

    # If no azure object is found, return the input grid unchanged.
    # This case might not occur based on examples, but is safe to include.
    if azure_coords.size == 0:
        return input_grid.copy()

    # Calculate the bounding box of the azure object
    azure_bbox = get_bounding_box(azure_coords)
    # This check should not be needed if azure_coords.size > 0, but included for safety
    if azure_bbox is None: 
         return input_grid.copy()
    min_row, max_row, min_col, max_col = azure_bbox
    
    # Initialize the output grid as a copy of the input grid
    output_grid = input_grid.copy()
    
    # Get grid dimensions
    height, width = input_grid.shape

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # Condition a: Check if the original cell was background color
            is_background = (input_grid[r, c] == background_color)

            # Condition b: Check if the cell is within the horizontal or vertical band 
            # defined by the azure object's bounding box.
            in_row_band = (min_row <= r <= max_row)
            in_col_band = (min_col <= c <= max_col)
            in_cross_area = in_row_band or in_col_band
            
            # If the cell was originally background AND it's within the cross area, fill it
            if is_background and in_cross_area:
                output_grid[r, c] = fill_color
                
    return output_grid
```