import numpy as np
from collections import Counter
import copy

"""
Mirrors foreground patterns from the left half of a grid onto the right half across a vertical separator line, 
preserving the right half's original background color where the left half had its background color.

The transformation involves the following steps:
1. Identify the vertical separator column, typically sharing the color of the grid's border.
2. Determine the background colors of the source (left) and target (right) regions.
3. Iterate through the target region. For each cell, find its mirrored counterpart in the source region.
4. If the mirrored source cell contains a foreground color (not the source background), copy that color to the target cell.
5. If the mirrored source cell contains the source background color, the target cell retains the target region's original background color.
6. The source region, separator column, and borders remain unchanged.
"""

def find_separator_column(grid_np: np.ndarray) -> int | None:
    """
    Finds the index of the vertical separator column.
    Assumes the separator uses the same color as the border and is a solid line
    within the non-border area of the grid.
    """
    rows, cols = grid_np.shape
    if rows <= 2 or cols <= 2:
        return None # Not enough space for a separator within borders

    border_color = grid_np[0, 0]

    # Look for a column (excluding outer borders) that matches the border color
    for c in range(1, cols - 1):
        is_separator = True
        for r in range(1, rows - 1): # Check only within inner grid
             if grid_np[r, c] != border_color:
                 is_separator = False
                 break
        if is_separator:
             # Check if this column separates two distinct background colors
             # (Simple check: look at colors immediately adjacent in a middle row)
             mid_row = rows // 2
             if c > 1 and c < cols - 2: # Ensure there are cells to check on both sides
                 left_neighbor = grid_np[mid_row, c - 1]
                 right_neighbor = grid_np[mid_row, c + 1]
                 # A potential separator should ideally have different colors next to it,
                 # and these colors shouldn't be the border color itself.
                 if left_neighbor != border_color and \
                    right_neighbor != border_color and \
                    left_neighbor != right_neighbor:
                     return c

    # Fallback or alternative strategy if no solid border-color line found?
    # For this specific problem, the examples show a clear separator.
    # Let's try finding the first column from the left (after col 0)
    # that contains the border color anywhere within the inner grid.
    for c in range(1, cols - 1):
        if np.any(grid_np[1:-1, c] == border_color):
             # Crude check if it looks like a separator based on example structure
             if c > cols // 4 and c < 3 * cols // 4: # Must be somewhat central
                 # Check if the column consists *only* of border color (stronger check)
                 if np.all(grid_np[:, c] == border_color):
                     return c

    print("Warning: Separator column not clearly identified based on border color match.")
    # Default guess if no clear separator found (might be brittle)
    return cols // 2


def get_region_background(region: np.ndarray) -> int:
    """
    Determines the most frequent color in a region, assuming it's the background.
    Handles empty regions.
    """
    if region.size == 0:
        return -1 # Or raise an error, indicates issue with region definition
    colors, counts = np.unique(region, return_counts=True)
    if colors.size > 0:
        return colors[np.argmax(counts)]
    return -1 # Should not happen if region is not empty


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the pattern mirroring transformation to the input grid.
    """
    # Convert to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = copy.deepcopy(input_np) # Initialize output as a copy of input
    rows, cols = input_np.shape

    if rows <= 2 or cols <= 2:
        return input_grid # Grid too small to have distinct regions/separator

    # --- Identify Separator ---
    separator_index = find_separator_column(input_np)
    if separator_index is None or separator_index <= 0 or separator_index >= cols - 1:
        print(f"Error: Could not reliably find separator column. Guessing middle: {cols // 2}")
        # Fallback, might be incorrect for some cases
        separator_index = cols // 2 
        # A better fallback might be needed depending on task variations

    # --- Define Regions ---
    # Source region: columns to the left of the separator (excluding border and separator)
    # Target region (in input): columns to the right of the separator (excluding border and separator)
    # Note: indices are [start:stop], stop is exclusive.
    # We need the background colors *within* the active area (excluding borders)
    source_region_indices = (slice(1, rows - 1), slice(1, separator_index))
    target_region_indices = (slice(1, rows - 1), slice(separator_index + 1, cols - 1))

    source_region = input_np[source_region_indices]
    target_region_input = input_np[target_region_indices] # Use input to find original target bg

    # --- Determine Background Colors ---
    source_background_color = get_region_background(source_region)
    # Target background is uniform in examples, take first element if available
    target_background_color = -1
    if target_region_input.size > 0:
        target_background_color = target_region_input[0,0] # Assume uniform background in target input
        # More robust: check uniformity or use get_region_background
        # confirmed_target_bg = get_region_background(target_region_input)
        # if confirmed_target_bg != target_background_color:
        #     print("Warning: Target region background in input is not uniform.")
        #     target_background_color = confirmed_target_bg # Use most frequent anyway

    if source_background_color == -1 or target_background_color == -1:
         print("Error: Could not determine background colors.")
         return input_grid # Return original if backgrounds are unclear

    # --- Process Target Region for Output ---
    # Iterate through each cell in the target region of the output grid
    for r in range(1, rows - 1): # Exclude top/bottom borders
        for c in range(separator_index + 1, cols - 1): # Exclude side borders and separator
            # Calculate mirrored source coordinates
            # Distance from target cell 'c' to separator = c - separator_index
            # Mirrored column = separator_index - distance
            mirrored_c = separator_index - (c - separator_index)

            # Ensure mirrored column is within valid source region bounds (should be > 0)
            if mirrored_c >= 1: # Check it's not the left border
                source_color = input_np[r, mirrored_c]

                # Apply Transformation Rule
                if source_color != source_background_color:
                    # If the source color is a foreground pattern, copy it
                    output_np[r, c] = source_color
                else:
                    # If the source color is the background, keep the target background
                    # Since output_np started as a copy of input_np, the target cells
                    # already have the target_background_color. Explicitly setting for clarity:
                    output_np[r, c] = target_background_color
            else:
                # This case shouldn't typically happen with a central separator
                # but handle it defensively - keep target background
                 output_np[r, c] = target_background_color


    # Convert back to list of lists for the final output
    output_grid = output_np.tolist()
    return output_grid