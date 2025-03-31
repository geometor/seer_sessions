import numpy as np
from collections import Counter

"""
Transforms the input grid based on row-level analysis.

1. Identify the background color (assumed to be 7/gray).
2. Analyze each row of the input grid:
   - Count non-background colors in the row.
   - If any non-background color appears 2 or more times, mark the row as a "fill row" with that color.
   - Otherwise, mark the row as a "pattern row".
3. Determine the pattern template:
   - Collect all non-background pixels (color and column index) from all "pattern rows".
   - Create a template row (width of the grid) filled with the background color.
   - Place the collected unique pattern pixel colors into their corresponding columns in the template row.
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
    input_grid = np.array(input_grid, dtype=int)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    
    # --- Configuration ---
    background_color = 7

    # --- Step 1 & 2: Analyze rows and determine action type ---
    row_info = {} # Stores type ('fill' or 'pattern') and fill color for each row
    pattern_pixels = [] # Stores (color, col_index) for pixels in pattern rows

    for r in range(height):
        row = input_grid[r, :]
        non_background_pixels = row[row != background_color]
        
        if len(non_background_pixels) == 0:
            # If the row is entirely background, treat it as a pattern row
            row_info[r] = {'type': 'pattern', 'fill_color': None}
            continue # No pattern pixels to collect from this row itself

        color_counts = Counter(non_background_pixels)
        
        fill_color_found = None
        for color, count in color_counts.items():
            if count >= 2:
                fill_color_found = color
                break # Assume only one color triggers fill per row based on examples
        
        if fill_color_found is not None:
            row_info[r] = {'type': 'fill', 'fill_color': fill_color_found}
        else:
            row_info[r] = {'type': 'pattern', 'fill_color': None}
            # Collect pixels for the pattern template from this pattern row
            for c in range(width):
                pixel_color = input_grid[r, c]
                if pixel_color != background_color:
                    pattern_pixels.append((pixel_color, c))

    # --- Step 3: Create the pattern template row ---
    pattern_template_row = np.full(width, background_color, dtype=int)
    
    # Use a set to keep track of columns already filled to handle multiple pixels in the same column
    # Although the logic implies unique locations based on examples, this makes it robust.
    # Prioritize based on iteration order if duplicates exist (not explicitly defined, but likely sufficient).
    filled_cols = set() 
    for color, col_index in pattern_pixels:
         # Only fill if not already filled by a previous pattern pixel in the same column
         # Note: The problem description doesn't specify precedence if multiple pattern
         # pixels map to the same column. We use the first encountered.
         # Alternatively, could collect all possibilities and decide, but sticking to simpler interpretation first.
         if col_index not in filled_cols:
              pattern_template_row[col_index] = color
              filled_cols.add(col_index)


    # --- Step 4: Construct the output grid ---
    for r in range(height):
        info = row_info[r]
        if info['type'] == 'fill':
            output_grid[r, :] = info['fill_color']
        elif info['type'] == 'pattern':
            output_grid[r, :] = pattern_template_row
        else:
             # Fallback or error case - should not happen with current logic
             # Fill with background just in case
             output_grid[r, :] = background_color


    return output_grid.tolist() # Convert back to list of lists if required by the framework