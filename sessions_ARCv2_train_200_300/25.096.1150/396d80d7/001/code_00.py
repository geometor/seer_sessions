"""
1.  Initialize the output grid as a copy of the input grid.
2.  Identify the background color, which is the most frequent color in the input grid.
3.  Identify the non-background colors present in the input grid.
4.  Determine the "structure" color by finding the most frequent non-background color.
5.  Determine the "frame" color by identifying the other non-background color(s).
6.  Iterate through each cell (at row `r`, column `c`) of the input grid.
7.  If the color of the input cell `input[r][c]` is the background color:
    a.  Examine the 8 neighboring cells of `input[r][c]`.
    b.  If any of these neighbors contain the "structure" color:
        i.  Change the color of the corresponding output cell `output[r][c]` to the "frame" color.
8.  Return the modified output grid.
"""

import numpy as np
from collections import Counter

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a transformation to a grid based on neighbor colors.

    Background cells adjacent (including diagonals) to the most frequent
    non-background color ('structure' color) are changed to the less frequent
    non-background color ('frame' color).
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # --- Identify Colors ---

    # Flatten the grid to count all colors
    all_colors = input_np.flatten()
    color_counts = Counter(all_colors)

    # Find the background color (most frequent)
    background_color = color_counts.most_common(1)[0][0]

    # Find non-background colors and their counts
    non_background_colors = [color for color in all_colors if color != background_color]
    if not non_background_colors:
        # No pattern, return the original grid
        return input_grid
        
    non_background_counts = Counter(non_background_colors)

    # Determine structure and frame colors based on frequency
    # Assumes there are exactly two non-background colors as per examples
    sorted_non_background = non_background_counts.most_common()
    if len(sorted_non_background) < 2:
         # Handle cases with only one non-background color if needed,
         # based on examples, we expect two. If only one, maybe it frames itself?
         # For now, let's assume the task implies two distinct non-bg colors.
         # If only one non-bg color exists, no framing happens based on the logic derived.
         return input_grid # or raise an error, or define behavior

    structure_color = sorted_non_background[0][0]
    frame_color = sorted_non_background[1][0]

    # --- Perform Transformations ---

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is a background cell
            if input_np[r, c] == background_color:
                # Examine the 8 neighbors
                found_structure_neighbor = False
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue  # Skip the cell itself

                        nr, nc = r + dr, c + dc

                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor has the structure color
                            if input_np[nr, nc] == structure_color:
                                found_structure_neighbor = True
                                break  # Found one, no need to check other neighbors
                    if found_structure_neighbor:
                        break # Exit outer neighbor loop too

                # If a structure color neighbor was found, change the output cell
                if found_structure_neighbor:
                    output_np[r, c] = frame_color

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()

    return output_grid