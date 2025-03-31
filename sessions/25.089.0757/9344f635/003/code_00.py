import numpy as np
from collections import Counter

"""
Transforms the input grid based on row-level analysis and a global pattern template.

1. Identify the background color (assumed to be 7/gray).
2. Determine the pattern template row:
   - Iterate through the entire input grid.
   - Collect all unique non-background pixels (color and column index).
   - Create a template row (width of the grid) filled with the background color.
   - Place the collected unique non-background pixel colors into their corresponding columns in the template row. Handle potential conflicts in columns if necessary (though examples suggest none).
3. Analyze each row of the input grid to determine its type:
   - Count non-background colors in the row.
   - If any non-background color appears 2 or more times, mark the row as a "fill row" with that color.
   - Otherwise, mark the row as a "pattern row".
4. Construct the output grid:
   - Initialize an output grid of the same dimensions as the input.
   - For rows marked as "fill rows", fill the corresponding output row entirely with the designated fill color.
   - For rows marked as "pattern rows", copy the pattern template row into the corresponding output row.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    output_grid = np.zeros_like(input_grid_np)

    # --- Configuration ---
    # Determine background color dynamically or assume based on examples
    # Assuming gray (7) based on previous observation, but could check most frequent
    background_color = 7
    # If we need dynamic background detection:
    # unique_colors, counts = np.unique(input_grid_np, return_counts=True)
    # background_color = unique_colors[np.argmax(counts)]


    # --- Step 2: Determine the global pattern template row ---
    pattern_template_row = np.full(width, background_color, dtype=int)
    pattern_pixels_map = {} # Store {col_index: color}

    # Iterate through the entire grid to find all non-background pixels
    for r in range(height):
        for c in range(width):
            pixel_color = input_grid_np[r, c]
            if pixel_color != background_color:
                # If a column already has a pattern pixel, the examples don't show conflicts.
                # If a conflict arose, we might need a rule (e.g., last seen wins).
                # For now, assume no conflicts or simple overwrite is fine.
                pattern_pixels_map[c] = pixel_color

    # Populate the template row from the map
    for c, color in pattern_pixels_map.items():
        pattern_template_row[c] = color

    # --- Step 3 & 4: Analyze rows and construct the output grid ---
    for r in range(height):
        row = input_grid_np[r, :]
        non_background_pixels = row[row != background_color]

        is_fill_row = False
        fill_color = None

        if len(non_background_pixels) > 0:
            color_counts = Counter(non_background_pixels)
            for color, count in color_counts.items():
                if count >= 2:
                    is_fill_row = True
                    fill_color = color
                    break # Assume only one color triggers fill per row

        # Construct the output row based on type
        if is_fill_row:
            output_grid[r, :] = fill_color
        else:
            # This includes rows that were originally all background
            output_grid[r, :] = pattern_template_row

    # Convert back to list of lists if required by the framework
    return output_grid.tolist()