import numpy as np
from collections import Counter

"""
Transforms the input grid based on color adjacency rules involving three non-background colors.

1. Identifies the background color (most frequent).
2. Identifies the three unique non-background colors.
3. Sorts the non-background colors numerically to determine roles:
    - Source_Color: Lowest index.
    - Mid_Color: Middle index.
    - Target_Color: Highest index.
4. Iterates through each pixel of the input grid.
5. If a pixel has the Source_Color:
    - Checks its 8 neighbors (including diagonals) in the input grid.
    - If any neighbor has the Target_Color, the output pixel becomes Mid_Color.
    - Otherwise, the output pixel becomes Background_Color.
6. If a pixel has the Mid_Color:
    - Checks its 8 neighbors (including diagonals) in the input grid.
    - If any neighbor has the Target_Color, the output pixel becomes Target_Color.
    - Otherwise, the output pixel becomes Background_Color.
7. Pixels with Target_Color or Background_Color retain their original color in the output grid.
"""

def _get_colors(grid):
    """
    Identifies background color and the three non-background colors, assigning roles.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (background_color, source_color, mid_color, target_color)
               Returns None for colors if fewer than 3 non-background colors are found.
    """
    unique_colors, counts = np.unique(grid, return_counts=True)
    
    # Handle grids with only one color (all background)
    if len(unique_colors) == 1:
        return unique_colors[0], None, None, None
        
    background_color = unique_colors[np.argmax(counts)]
    non_background_colors = sorted([color for color in unique_colors if color != background_color])

    # Assign roles based on sorted order
    source_color = non_background_colors[0] if len(non_background_colors) > 0 else None
    mid_color = non_background_colors[1] if len(non_background_colors) > 1 else None
    target_color = non_background_colors[2] if len(non_background_colors) > 2 else None

    # Basic check if we have the required 3 non-background colors for the core logic
    if len(non_background_colors) < 3:
        print(f"Warning: Expected 3 non-background colors, found {len(non_background_colors)}: {non_background_colors}. Roles assigned: S={source_color}, M={mid_color}, T={target_color}")


    return background_color, source_color, mid_color, target_color

def _is_valid(r, c, rows, cols):
    """Checks if coordinates are within grid bounds."""
    return 0 <= r < rows and 0 <= c < cols

def _has_target_neighbor(r, c, input_grid_np, target_color, rows, cols):
    """Checks if any of the 8 neighbors have the target color."""
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is valid and has the Target_Color
            if _is_valid(nr, nc, rows, cols) and input_grid_np[nr, nc] == target_color:
                return True # Found one
    return False # Checked all neighbors, none found

def transform(input_grid):
    """
    Applies the adjacency-based color transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)

    # 1. Identify colors and roles
    background_color, source_color, mid_color, target_color = _get_colors(input_grid_np)

    # Check if essential colors (especially target) were identified for the logic to proceed
    if target_color is None:
         print("Error: Target color could not be determined. Cannot apply transformation rule.")
         return input_grid # Return original grid if roles cannot be established

    # 2. Iterate through each pixel of the *input* grid
    for r in range(rows):
        for c in range(cols):
            input_color = input_grid_np[r, c]

            # 3. Apply transformation based on input color
            
            # Case 1: Pixel color is Source_Color
            if input_color == source_color:
                # Check adjacency to Target_Color in the *input* grid
                if _has_target_neighbor(r, c, input_grid_np, target_color, rows, cols):
                    output_grid[r, c] = mid_color # Change to Mid_Color
                else:
                    output_grid[r, c] = background_color # Change to Background_Color

            # Case 2: Pixel color is Mid_Color
            elif input_color == mid_color:
                # Check adjacency to Target_Color in the *input* grid
                if _has_target_neighbor(r, c, input_grid_np, target_color, rows, cols):
                    output_grid[r, c] = target_color # Change to Target_Color
                else:
                    output_grid[r, c] = background_color # Change to Background_Color
            
            # Case 3 & 4: Pixel color is Target_Color or Background_Color
            # No action needed, output_grid already holds the correct color from the initial copy.
            # elif input_color == target_color: pass
            # elif input_color == background_color: pass

    # Convert back to list of lists for ARC standard output format
    return output_grid.tolist()