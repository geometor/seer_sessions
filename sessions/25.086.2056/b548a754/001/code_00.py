import numpy as np

"""
Identifies a primary shape (contiguous non-white, non-azure pixels) and a single azure marker pixel (8) in the input grid.
The azure pixel indicates how to extend the primary shape.
If the azure pixel is to the right of the shape's rightmost edge, the shape is extended horizontally to the right. The rightmost column of the shape is copied into the columns between the original right edge and the column of the azure pixel.
If the azure pixel is below the shape's bottom edge, the shape is extended vertically downwards. The bottom row of the shape is copied into the rows between the original bottom edge and the row of the azure pixel.
The azure marker pixel is removed (set to white 0) in the output grid.
"""

def find_marker(grid):
    """Finds the coordinates of the azure (8) pixel."""
    marker_coords = np.where(grid == 8)
    if len(marker_coords[0]) > 0:
        return marker_coords[0][0], marker_coords[1][0]
    return None

def find_shape_bounds(grid):
    """Finds the bounding box of non-white (0) and non-azure (8) pixels."""
    shape_coords = np.where((grid != 0) & (grid != 8))
    if len(shape_coords[0]) > 0:
        min_row = np.min(shape_coords[0])
        max_row = np.max(shape_coords[0])
        min_col = np.min(shape_coords[1])
        max_col = np.max(shape_coords[1])
        return min_row, max_row, min_col, max_col
    return None

def transform(input_grid):
    """
    Extends a shape based on the position of an azure marker pixel.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    
    # Find the marker pixel
    marker_pos = find_marker(grid)
    
    if marker_pos is None:
        # If no marker is found, return the original grid (or handle as error)
        # For this problem, examples suggest a marker always exists.
        return input_grid 
        
    marker_row, marker_col = marker_pos
    
    # Remove the marker from the output grid
    output_grid[marker_row, marker_col] = 0
    
    # Find the bounding box of the shape (excluding the marker itself)
    shape_bounds = find_shape_bounds(grid)
    
    if shape_bounds is None:
         # If no shape is found, return the grid with the marker removed
         return output_grid.tolist()
         
    min_row, max_row, min_col, max_col = shape_bounds

    # Determine extension direction and apply it
    # Check for horizontal extension (marker to the right)
    if marker_col > max_col:
        # Extract the rightmost column of the shape as the pattern
        edge_pattern = grid[min_row:max_row+1, max_col]
        # Fill columns from the end of the shape up to the marker's column
        for c in range(max_col + 1, marker_col):
            # Ensure we don't write out of bounds if marker is beyond grid edge
            if c < output_grid.shape[1]: 
                output_grid[min_row:max_row+1, c] = edge_pattern
                
    # Check for vertical extension (marker below) - use elif assuming only one direction
    elif marker_row > max_row:
        # Extract the bottom row of the shape as the pattern
        edge_pattern = grid[max_row, min_col:max_col+1]
        # Fill rows from the end of the shape up to the marker's row
        for r in range(max_row + 1, marker_row):
             # Ensure we don't write out of bounds if marker is beyond grid edge
            if r < output_grid.shape[0]:
                output_grid[r, min_col:max_col+1] = edge_pattern

    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()
