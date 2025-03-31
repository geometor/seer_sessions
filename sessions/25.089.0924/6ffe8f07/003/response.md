```python
import numpy as np

"""
Identify the single azure (8) colored rectangular object in the input grid.
Calculate its bounding box (minimum/maximum row and column indices).
Create an output grid initialized as a copy of the input grid.
Iterate through every cell (r, c) of the grid.
If the cell's row 'r' falls within the azure object's row range OR the cell's column 'c' falls within the azure object's column range, AND the original color of the cell in the input grid is white (0), then change the color of the corresponding cell in the output grid to yellow (4).
Otherwise, the cell in the output grid retains its original color from the input grid.
"""

def find_object_coords(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    return np.argwhere(grid == color)

def get_bounding_box(coords):
    """Calculates the bounding box from a list of coordinates."""
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
    
    # Find the coordinates of the azure (8) object
    azure_color = 8
    azure_coords = find_object_coords(input_grid, azure_color)

    # If no azure object is found, return the input grid unchanged 
    # (although task implies one exists)
    if azure_coords.size == 0:
        return input_grid.copy()

    # Calculate the bounding box of the azure object
    bbox = get_bounding_box(azure_coords)
    if bbox is None: # Should not happen if azure_coords is not empty
         return input_grid.copy()
    min_row, max_row, min_col, max_col = bbox
    
    # Initialize the output grid as a copy of the input grid
    output_grid = input_grid.copy()
    
    # Define the fill color
    fill_color = 4 # yellow
    background_color = 0 # white

    # Get grid dimensions
    height, width = input_grid.shape

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # Check if the cell is within the horizontal or vertical band of the azure bbox
            in_row_band = (min_row <= r <= max_row)
            in_col_band = (min_col <= c <= max_col)
            
            # Check if the original cell was background color
            is_background = (input_grid[r, c] == background_color)

            # If the cell is within the cross shape and was originally background, fill it
            if (in_row_band or in_col_band) and is_background:
                output_grid[r, c] = fill_color
                
    return output_grid
```