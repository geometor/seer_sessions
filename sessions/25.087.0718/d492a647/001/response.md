```python
import numpy as np

def find_target_pixel(grid):
    """
    Finds the coordinates and color of the target pixel.
    The target pixel is the unique pixel that is not white (0) or gray (5).
    
    Args:
        grid (np.array): The input grid.
        
    Returns:
        tuple: (target_row, target_col, target_color) or (None, None, None) if not found.
    """
    target_indices = np.where((grid != 0) & (grid != 5))
    if len(target_indices[0]) == 1:
        target_row = target_indices[0][0]
        target_col = target_indices[1][0]
        target_color = grid[target_row, target_col]
        return target_row, target_col, target_color
    else:
        # Handle cases where 0 or more than 1 target pixel is found, though ARC examples suggest exactly 1.
        return None, None, None

def transform(input_grid):
    """
    Transforms the input grid based on parity matching with a target pixel.

    1. Finds the single pixel in the input grid that is neither white (0) nor gray (5).
    2. Records its color (target_color) and location (target_row, target_col).
    3. Determines the parity (odd/even) of the target row and column indices.
    4. Creates a copy of the input grid as the output grid.
    5. Iterates through each pixel of the input grid.
    6. If a pixel is white (0) and its row and column parities match the target pixel's row and column parities respectively,
       it changes the color of that pixel in the output grid to the target_color.
    7. Otherwise, the pixel's color remains unchanged.
    8. Returns the modified output grid.
    """
    
    # Convert input list of lists to a numpy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = input_grid_np.copy()
    
    # Find the target pixel's location and color
    target_row, target_col, target_color = find_target_pixel(input_grid_np)
    
    # If no valid target pixel is found, return the original grid (or handle error)
    if target_color is None:
        return output_grid # Or raise an error depending on expected behavior

    # Determine the parity of the target pixel's coordinates
    target_row_parity = target_row % 2
    target_col_parity = target_col % 2
    
    # Get grid dimensions
    height, width = input_grid_np.shape
    
    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the input grid is white (0)
            if input_grid_np[r, c] == 0:
                # Determine the parity of the current pixel's coordinates
                current_row_parity = r % 2
                current_col_parity = c % 2
                
                # Check if both row and column parities match the target's parities
                if current_row_parity == target_row_parity and current_col_parity == target_col_parity:
                    # Change the color of the corresponding pixel in the output grid to the target color
                    output_grid[r, c] = target_color
            
            # If the pixel is not white, or parities don't match, it remains unchanged (already copied)

    # Return the final output grid (convert back to list of lists if necessary, though numpy array is often fine)
    return output_grid.tolist()
```