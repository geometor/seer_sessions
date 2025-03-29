import numpy as np

"""
Identifies isolated non-background pixels in the input grid. An isolated pixel 
is one with no neighbors (orthogonally or diagonally) of the same color. 
Each isolated pixel is then expanded into a 3x3 pattern centered on its 
original location in the output grid. The specific 3x3 pattern depends on the 
color of the isolated pixel:
- Color 1 (Blue): Solid 3x3 square.
- Color 2 (Red): 3x3 plus sign (+).
- Color 3 (Green): 3x3 diamond/X shape (center and diagonals).
- Color 6 (Magenta): 3x3 solid square minus horizontal neighbors (vertical bar hollow).
- Color 8 (Azure): 3x3 hollow square (perimeter).
Pixels that are not isolated remain unchanged. Expansions overwrite existing 
pixels in the output grid, potentially overlapping. The background color is 0.
"""

def is_within_bounds(r, c, height, width):
    """Checks if coordinates (r, c) are within the grid boundaries."""
    return 0 <= r < height and 0 <= c < width

def transform(input_grid):
    """
    Transforms the input grid by expanding isolated pixels into specific 3x3 patterns
    based on their color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input grid to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a copy of the input grid
    # Transformations will be applied to this copy
    output_grid = np.copy(input_np)

    # --- Step 1: Identify all isolated pixels using the original input grid ---
    isolated_pixels = []
    for r in range(height):
        for c in range(width):
            pixel_color = input_np[r, c]
            
            # Skip background pixels
            if pixel_color == 0:
                continue

            is_isolated = True
            # Check 8 neighbors (including diagonals)
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    # Skip the center pixel itself
                    if dr == 0 and dc == 0:
                        continue
                    
                    nr, nc = r + dr, c + dc
                    
                    # Check if neighbor is within bounds
                    if is_within_bounds(nr, nc, height, width):
                        # If any neighbor has the same color, it's not isolated
                        if input_np[nr, nc] == pixel_color:
                            is_isolated = False
                            break  # No need to check other neighbors for this pixel
                if not is_isolated:
                    break # Break outer neighbor loop as well
            
            # If the pixel is isolated, store its info
            if is_isolated:
                isolated_pixels.append({'coord': (r, c), 'color': pixel_color})

    # --- Step 2: Apply expansions for isolated pixels onto the output grid ---
    for isolated_info in isolated_pixels:
        r, c = isolated_info['coord']
        color = isolated_info['color']
        
        # Iterate through the 3x3 area centered at (r, c)
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                # Calculate the target coordinates in the output grid
                nr, nc = r + dr, c + dc
                
                # Check if the target coordinate is within bounds
                if is_within_bounds(nr, nc, height, width):
                    # Determine the value to write based on the color and relative position (dr, dc)
                    write_value = -1 # Default to an invalid value

                    if color == 1: # Blue: Solid Square
                        write_value = color
                    
                    elif color == 2: # Red: Plus (+)
                        # Fill center and orthogonal neighbors, corners are background
                        if dr == 0 or dc == 0: 
                            write_value = color
                        else:
                            write_value = 0 # Set corners to background

                    elif color == 3: # Green: Diamond/X
                        # Fill center and diagonal neighbors, orthogonals are background
                        if dr == 0 and dc == 0: # Center
                             write_value = color
                        elif abs(dr) == 1 and abs(dc) == 1: # Diagonals
                            write_value = color
                        else: # Orthogonals
                            write_value = 0 # Set orthogonals to background

                    elif color == 6: # Magenta: Vertical Bar Hollow
                        # Fill all except horizontal neighbors
                        if dc == 0: # Center column
                            write_value = color
                        elif abs(dr) == 1 and abs(dc) == 1: # Corner columns also filled
                            write_value = color
                        else: # Horizontal neighbors (dr=0, dc!=0)
                            write_value = 0 # Set horizontal neighbors to background
                            
                    elif color == 8: # Azure: Hollow Square
                        # Fill perimeter, center is background
                        if dr == 0 and dc == 0: # Center
                            write_value = 0 # Set center to background
                        else:
                            write_value = color # Fill perimeter

                    # If a pattern was defined for the color, write the value
                    if write_value != -1:
                        output_grid[nr, nc] = write_value
                    # If the color wasn't one of the specified patterns (1, 2, 3, 6, 8),
                    # the output_grid remains unchanged in this 3x3 area for this pixel, 
                    # effectively leaving the original pixel as is.

    # Convert back to list of lists for the required output format
    return output_grid.tolist()