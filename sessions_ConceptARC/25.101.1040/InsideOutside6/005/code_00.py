import numpy as np
from typing import List, Tuple

"""
Filters a grid based on pixel adjacency rules derived from examples.

The transformation identifies three color roles: background (assumed to be 0), 
'target', and 'context'. 
If exactly two non-background colors exist, the 'target' color is the one 
with the lower frequency count, and the 'context' color is the one with the 
higher frequency count. If only one non-background color exists, it's treated 
as the 'target' color, and there is no 'context' color.

The rule is to keep 'target' color pixels in the output grid *only if* they 
are NOT adjacent (horizontally, vertically, or diagonally - 8-connectivity) 
to any 'context' color pixel in the input grid. 

All 'context' color pixels, as well as 'target' color pixels that *are* 
adjacent to 'context' pixels, are replaced with the background color in the 
output. Pixels that are already the background color remain so.

If zero, more than two non-background colors exist, or if the two 
non-background colors have equal frequency (making the target/context roles 
ambiguous based on the frequency heuristic), the function returns a grid 
filled entirely with the background color.

The grid dimensions remain unchanged.

Note: This rule implementation matches most transformations in the provided 
examples but differs for a few specific target pixels that are removed in the 
expected output despite not being adjacent to any context pixel (e.g., 
T1(3,5), T1(4,5), T1(6,6), T2(10,7)). The exact rule for these exceptions is 
not captured here.
"""

def _identify_colors(grid: np.ndarray) -> Tuple[int, int, int]:
    """
    Identifies background, target, and context colors based on frequency.
    Assumes background=0. Finds non-background colors.
    Hypothesis: If two non-background colors exist, Target color is less 
                frequent than context color.
    Returns: (background_color, target_color, context_color)
             target_color or context_color can be -1 if not applicable/found.
             Special negative codes (-2, -3) indicate ambiguity or errors.
    """
    unique_colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    background_color = 0
    # Filter out the background color to find non-background colors and their counts
    non_background_colors = {c: count for c, count in color_counts.items() if c != background_color}
    num_non_background = len(non_background_colors)

    target_color = -1  # Default: No target color found
    context_color = -1 # Default: No context color found

    if num_non_background == 0:
        # Only background color present in the input grid
        pass # target/context remain -1
    elif num_non_background == 1:
        # Exactly one non-background color exists, treat it as the target color
        target_color = list(non_background_colors.keys())[0]
        context_color = -1 # No context color in this case
    elif num_non_background == 2:
        # Exactly two non-background colors exist, determine roles by frequency
        colors = list(non_background_colors.keys())
        counts_list = list(non_background_colors.values())

        # Assign target to the less frequent color, context to the more frequent
        if counts_list[0] < counts_list[1]:
            target_color = colors[0]
            context_color = colors[1]
        elif counts_list[1] < counts_list[0]:
            target_color = colors[1]
            context_color = colors[0]
        else:
             # Frequencies are equal, roles are ambiguous based on this heuristic
             target_color = -2 # Indicate ambiguity
             context_color = -2
    else: 
        # More than two non-background colors found, roles are ambiguous
        target_color = -3 # Indicate >2 colors issue
        context_color = -3

    return background_color, target_color, context_color

def _check_neighbors_for_color(grid: np.ndarray, r: int, c: int, color_to_find: int) -> bool:
    """
    Checks the 8 neighbors (Moore neighborhood) of cell (r, c) in the grid
    to see if any neighbor has the specified color_to_find.
    Returns True if a neighbor with the color is found, False otherwise.
    Handles boundary conditions gracefully.
    """
    rows, cols = grid.shape
    # Iterate through the 3x3 neighborhood centered at (r, c)
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue

            # Calculate neighbor coordinates
            nr, nc = r + dr, c + dc

            # Check if the neighbor coordinates are within the grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor has the color we're looking for
                if grid[nr, nc] == color_to_find:
                    return True # Found the color in a neighbor, no need to check further

    # If the loop completes without finding the color in any neighbor
    return False

def transform(input_grid_list: list[list[int]]) -> list[list[int]]:  
    # Convert input list of lists to a numpy array for efficient processing
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # Step 1: Identify background, target, and context colors using the frequency heuristic
    background_color, target_color, context_color = _identify_colors(input_grid)

    # Step 2: Handle edge cases or ambiguous color roles
    # If no target color identified, or roles are ambiguous, return a grid filled with background color
    if target_color < 0: # Covers -1 (no target), -2 (ambiguous tie), -3 (>2 colors)
        output_grid = np.full((rows, cols), background_color, dtype=int)
        return output_grid.tolist()

    # Step 3: Initialize the output grid with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # Step 4: Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Step 5: Check if the current pixel is the target color
            if input_grid[r, c] == target_color:

                # Step 6: Assume the target pixel should be kept, unless proven otherwise
                keep_pixel = True 

                # Step 7: Check for adjacent context pixels ONLY if a context color exists
                if context_color != -1: # A context color exists (i.e., exactly 2 non-bg colors found)
                    is_near_context = _check_neighbors_for_color(input_grid, r, c, context_color)
                    # If any neighbor is the context color, mark this pixel for removal
                    if is_near_context:
                        keep_pixel = False 

                # Step 8: If the pixel is marked to be kept, place its color in the output grid
                if keep_pixel:
                    output_grid[r, c] = target_color
            
            # Step 9: Pixels that are not the target color (background or context) 
            # remain as the background color in the output grid (due to initialization).

    # Step 10: Convert the final numpy array grid back to a list of lists and return
    return output_grid.tolist()