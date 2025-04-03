import numpy as np
from collections import Counter

"""
Transforms the input grid based on color adjacency rules.

1. Identifies the background color (most frequent) and the three unique non-background colors.
2. Sorts the non-background colors numerically:
    - Lowest index = Source_Color
    - Middle index = Unaffected_Color
    - Highest index = Target_Color
3. Iterates through each pixel of the input grid.
4. If a pixel has the Source_Color:
    - Checks its 8 neighbors (including diagonals) in the input grid.
    - If any neighbor has the Target_Color, the corresponding pixel in the output grid is set to Target_Color.
    - Otherwise (no Target_Color neighbors), the output pixel is set to the Background_Color.
5. Pixels with colors other than Source_Color (Background, Unaffected, Target) retain their original color in the output grid.
"""

def get_colors(grid):
    """Identifies background and non-background colors."""
    unique_colors, counts = np.unique(grid, return_counts=True)
    background_color = unique_colors[np.argmax(counts)]
    non_background_colors = sorted([color for color in unique_colors if color != background_color])
    if len(non_background_colors) != 3:
        # This case might indicate an issue with the problem assumption or the specific input
        # For robustness, handle it, perhaps by returning None or raising an error
        # Or, if it's possible only a subset exist, adapt logic. Assuming 3 based on examples.
        print(f"Warning: Expected 3 non-background colors, found {len(non_background_colors)}: {non_background_colors}")
        # Decide on handling: maybe return placeholders or raise error?
        # Returning placeholders for now to avoid crashing during tests if input deviates.
        source, unaffected, target = (None, None, None)
        if len(non_background_colors) > 0: source = non_background_colors[0]
        if len(non_background_colors) > 1: unaffected = non_background_colors[1]
        if len(non_background_colors) > 2: target = non_background_colors[2]
        return background_color, source, unaffected, target
        
    source_color = non_background_colors[0]
    unaffected_color = non_background_colors[1]
    target_color = non_background_colors[2]
    
    return background_color, source_color, unaffected_color, target_color

def is_valid(r, c, rows, cols):
    """Checks if coordinates are within grid bounds."""
    return 0 <= r < rows and 0 <= c < cols

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # 1. Identify colors and roles
    background_color, source_color, unaffected_color, target_color = get_colors(input_np)

    # Handle cases where exactly 3 non-background colors might not be found
    if source_color is None or target_color is None:
         # If crucial colors are missing, maybe return the input unchanged or handle error
         print("Error: Could not determine Source or Target color. Returning input.")
         return input_grid # Or output_grid which is currently a copy

    # 3. Iterate through each pixel of the *input* grid
    for r in range(rows):
        for c in range(cols):
            # 4. Check if the current pixel has the Source_Color
            if input_np[r, c] == source_color:
                is_adjacent_to_target = False
                # Check 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue # Skip the cell itself
                        
                        nr, nc = r + dr, c + dc
                        
                        # Check if neighbor is valid and has the Target_Color
                        if is_valid(nr, nc, rows, cols) and input_np[nr, nc] == target_color:
                            is_adjacent_to_target = True
                            break # Found one, no need to check further
                    if is_adjacent_to_target:
                        break # Exit outer loop too
                
                # Update the output grid based on adjacency check
                if is_adjacent_to_target:
                    output_grid[r, c] = target_color
                else:
                    output_grid[r, c] = background_color
            
            # 5. Else (pixel is Background, Unaffected, or Target):
            # No action needed as output_grid started as a copy.

    # Convert back to list of lists if necessary for ARC standard
    return output_grid.tolist()