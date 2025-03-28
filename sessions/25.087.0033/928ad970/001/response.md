```python
import numpy as np

"""
Locate all gray pixels (color 5) in the input grid. Determine the bounding 
box enclosing these gray pixels (min/max row and column). Identify the color 
(C) of the single non-gray, non-background object. Create a copy of the input 
grid. Define an inner rectangle one unit inwards from the gray pixel bounding 
box. Draw the perimeter of this inner rectangle onto the copied grid using 
color C, but only overwrite background pixels (color 0).
"""

def transform(input_grid):
    """
    Draws a hollow rectangle based on the bounding box of gray pixels, 
    using the color of another object in the grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid with the added rectangle.
    """
    # Convert input list of lists to a NumPy array for easier processing
    grid = np.array(input_grid, dtype=int)
    
    # Initialize output grid as a copy of the input grid
    output_grid = grid.copy()
    
    # Find coordinates of all gray pixels (color 5)
    gray_pixels = np.argwhere(grid == 5)
    
    # If no gray pixels are found, return the original grid (edge case)
    if gray_pixels.size == 0:
        return output_grid.tolist()
        
    # Determine the bounding box of the gray pixels
    min_row = np.min(gray_pixels[:, 0])
    max_row = np.max(gray_pixels[:, 0])
    min_col = np.min(gray_pixels[:, 1])
    max_col = np.max(gray_pixels[:, 1])
    
    # Find the color of the non-gray, non-background object
    object_color = -1 # Initialize with an invalid color
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0 and color != 5:
            object_color = color
            break
            
    # If no such object color is found, return the original grid (edge case)
    if object_color == -1:
         return output_grid.tolist()

    # Define the coordinates for the inner hollow rectangle
    # Ensure coordinates stay within grid boundaries and the box has valid dimensions
    top_row = min_row + 1
    bottom_row = max_row - 1
    left_col = min_col + 1
    right_col = max_col - 1

    # Check if the inner rectangle dimensions are valid
    if top_row > bottom_row or left_col > right_col:
        # If the bounding box is too small to draw an inner rectangle, return the original grid
        return output_grid.tolist()

    # Draw the top edge of the rectangle
    for c in range(left_col, right_col + 1):
        if grid[top_row, c] == 0: # Only overwrite background pixels
            output_grid[top_row, c] = object_color
            
    # Draw the bottom edge of the rectangle
    for c in range(left_col, right_col + 1):
         if grid[bottom_row, c] == 0: # Only overwrite background pixels
            output_grid[bottom_row, c] = object_color

    # Draw the left edge of the rectangle (excluding corners already drawn)
    for r in range(top_row + 1, bottom_row):
        if grid[r, left_col] == 0: # Only overwrite background pixels
            output_grid[r, left_col] = object_color
            
    # Draw the right edge of the rectangle (excluding corners already drawn)
    for r in range(top_row + 1, bottom_row):
        if grid[r, right_col] == 0: # Only overwrite background pixels
            output_grid[r, right_col] = object_color

    # Convert the NumPy array back to a list of lists before returning
    return output_grid.tolist()

```