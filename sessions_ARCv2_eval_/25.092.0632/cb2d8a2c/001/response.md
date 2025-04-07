```python
import numpy as np

def find_color_coordinates(grid, color):
    """Finds the coordinates of the first pixel with the specified color."""
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        return coords[0] # Return the first coordinate found (row, col)
    return None

def transform(input_grid):
    """
    Transforms the input grid by first changing all blue (1) pixels to red (2).
    Then, it finds the single green (3) pixel and extends green lines horizontally
    and vertically from it. These lines stop when they hit a grid boundary or
    a red (2) pixel (including those originally blue).
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy()
    height, width = output_grid.shape

    # --- Step 1: Color Transformation (Blue to Red) ---
    # Change all blue (1) pixels to red (2)
    output_grid[output_grid == 1] = 2

    # --- Step 2: Find the Green Pixel ---
    green_coord = find_color_coordinates(grid_np, 3) # Use original grid to find the green pixel
    if green_coord is None:
        # Should not happen based on examples, but good practice to handle
        return output_grid.tolist() 
    
    start_r, start_c = green_coord

    # --- Step 3: Line Extension ---
    
    # Extend Upwards (decrementing row)
    for r in range(start_r - 1, -1, -1):
        if output_grid[r, start_c] == 2: # Stop if red barrier
            break
        if output_grid[r, start_c] == 8: # Overwrite azure background
             output_grid[r, start_c] = 3
        # If it's another color (not red or azure), we also stop (implicit)
        # If it's already green (e.g., from another extension path), leave it.
        elif output_grid[r, start_c] != 3:
            break
            
    # Extend Downwards (incrementing row)
    for r in range(start_r + 1, height):
        if output_grid[r, start_c] == 2: # Stop if red barrier
            break
        if output_grid[r, start_c] == 8: # Overwrite azure background
             output_grid[r, start_c] = 3
        elif output_grid[r, start_c] != 3:
            break
            
    # Extend Leftwards (decrementing column)
    for c in range(start_c - 1, -1, -1):
        if output_grid[start_r, c] == 2: # Stop if red barrier
            break
        if output_grid[start_r, c] == 8: # Overwrite azure background
             output_grid[start_r, c] = 3
        elif output_grid[start_r, c] != 3:
            break

    # Extend Rightwards (incrementing column)
    for c in range(start_c + 1, width):
        if output_grid[start_r, c] == 2: # Stop if red barrier
            break
        if output_grid[start_r, c] == 8: # Overwrite azure background
             output_grid[start_r, c] = 3
        elif output_grid[start_r, c] != 3:
            break

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```