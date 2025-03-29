import numpy as np

"""
Recolor an azure (8) object based on properties (pixel count and internal holes) 
of a blue (1) object, then remove the blue object by setting its pixels to white (0).

1. Identify the blue (1) object.
2. Count the number of pixels (N) in the blue object.
3. Determine if the blue object has internal holes (H=1 if yes, H=0 if no). A hole is a white (0) pixel surrounded by blue (1) pixels on all four sides (up, down, left, right).
4. Determine the target color based on N and H:
    - N=5, H=0 -> target_color = red (2)
    - N=6, H=0 -> target_color = green (3)
    - N=6, H=1 -> target_color = orange (7)
5. Create the output grid by:
    - Replacing all blue (1) pixels with white (0).
    - Replacing all azure (8) pixels with the determined target color.
"""

def _find_pixels(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    return list(zip(*np.where(grid == color)))

def _has_internal_holes(grid, object_color, background_color):
    """Checks if an object of object_color contains internal holes (background_color pixels surrounded by object_color)."""
    rows, cols = grid.shape
    background_pixels = _find_pixels(grid, background_color)
    
    for r, c in background_pixels:
        is_hole = True
        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds and if neighbor is part of the object
            if not (0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == object_color):
                is_hole = False
                break
        if is_hole:
            return True # Found at least one hole
    return False # No holes found


def transform(input_grid):
    """
    Transforms the input grid according to the rules derived from the examples.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    blue_color = 1
    azure_color = 8
    background_color = 0
    
    # Find blue pixels and their count
    blue_pixels = _find_pixels(input_grid, blue_color)
    n_blue = len(blue_pixels)
    
    # If no blue pixels, maybe return original? Based on examples, blue always exists.
    if n_blue == 0:
        # Or should handle this differently? For now, assume blue always present.
        # Let's determine target color anyway, maybe default to something?
        # The rules only cover N=5 and N=6. Let's default to azure if no blue.
         target_color = azure_color 
    else:
        # Determine if the blue object has holes
        h_blue = 1 if _has_internal_holes(input_grid, blue_color, background_color) else 0
        
        # Determine the target color based on N and H
        if n_blue == 5 and h_blue == 0:
            target_color = 2 # red
        elif n_blue == 6 and h_blue == 0:
            target_color = 3 # green
        elif n_blue == 6 and h_blue == 1:
            target_color = 7 # orange
        else:
            # Default or error case if N/H combination is unexpected.
            # Based on training, assume one of the above conditions is always met.
            # For robustness, maybe keep azure color? Or raise error?
            # Let's keep azure if conditions aren't met.
            target_color = azure_color 

    # Apply transformations to the output grid
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == blue_color:
                output_grid[r, c] = background_color # Remove blue
            elif input_grid[r, c] == azure_color:
                output_grid[r, c] = target_color # Recolor azure

    return output_grid