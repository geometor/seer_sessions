import numpy as np
from collections import Counter

"""
This module defines a function to transform an input grid based on color patterns.
The transformation identifies three key colors: background, line_color, and scatter_color.
Vertical lines composed of the line_color divide the grid into horizontal regions.
The function counts the occurrences of the scatter_color within each region.
The output grid is the region containing the highest count of scatter_color pixels.

Transformation Steps:
1.  Identify the most frequent color (background) and the two other unique colors present.
2.  Determine which non-background color forms full-height vertical lines (line_color) 
    and find the columns (line_columns) where these occur. The remaining 
    non-background color is the scatter_color.
3.  Define horizontal regions based on the spaces between/around the line_columns. 
    Regions are defined by column ranges: [0, c1), [c1+1, c2), ..., [clast+1, width).
4.  For each region, count the number of pixels matching the scatter_color.
5.  Identify the region with the maximum count of scatter_color pixels. If there's a tie,
    the leftmost region (smallest starting column index) is chosen.
6.  Create the output grid by extracting the columns defined by the selected region 
    from the input grid, maintaining the original height.
"""

def _is_vertical_line(grid, col_idx, color):
    """Checks if a column consists entirely of a specific color."""
    # Helper function to check if all pixels in a given column match the specified color.
    height = grid.shape[0]
    return np.all(grid[:, col_idx] == color)

def transform(input_grid):
    """
    Extracts a horizontal section of the input grid based on vertical line delimiters
    and the density of a specific 'scatter' color within the delimited regions.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Step 1: Identify background, potential line, and potential scatter colors.
    unique_elements, counts = np.unique(grid, return_counts=True)

    # Basic validation: Need at least 3 colors for the described logic.
    if len(unique_elements) < 3:
        # print(f"Warning: Expected at least 3 unique colors, found {len(unique_elements)}. Returning original grid.")
        # According to ARC task constraints and examples, this case might not occur in valid tasks.
        # Returning an empty list or original grid might be options depending on expected behavior for invalid inputs.
        return [] # Or return input_grid

    # Sort colors by frequency to find the background color.
    color_counts = sorted(zip(unique_elements, counts), key=lambda x: x[1], reverse=True)
    background_color = color_counts[0][0]
    # The remaining colors are candidates for line and scatter colors.
    potential_colors = [c[0] for c in color_counts[1:]]

    # Step 2: Identify Line Color, Scatter Color, and Line Columns.
    line_color = None
    scatter_color = None
    line_columns = []
    found_line_color = False

    # Iterate through the potential non-background colors to find the one forming vertical lines.
    for p_color in potential_colors:
        cols_for_this_color = []
        is_this_color_lines = False
        for c in range(width):
            if _is_vertical_line(grid, c, p_color):
                cols_for_this_color.append(c)
                is_this_color_lines = True

        # If this color forms lines AND we haven't assigned a line color yet
        if is_this_color_lines:
            if found_line_color:
                 # Ambiguity: More than one non-background color forms lines.
                 # This case is not observed in the training examples.
                 # Behavior is undefined; returning empty list for now.
                 # print(f"Warning: Ambiguous case - multiple colors form vertical lines. Found {p_color} and {line_color}.")
                 return []
            line_color = p_color
            line_columns = cols_for_this_color
            found_line_color = True

    # Check if a line color was successfully identified.
    if not found_line_color:
        # print("Warning: No color found forming complete vertical lines.")
        return [] # Cannot proceed without line delimiters.

    # Identify the scatter color (the non-background, non-line color).
    # It assumes exactly one line color and one scatter color among non-backgrounds.
    for p_color in potential_colors:
        if p_color != line_color:
            scatter_color = p_color
            break # Found the scatter color

    if scatter_color is None:
        # This might happen if there were only 2 colors total, or if the line color was the only non-background color.
        # print("Warning: Could not determine a distinct scatter color.")
        return []


    # Step 3: Define Regions based on line columns.
    regions = []
    # Use implicit boundaries at -1 (before column 0) and width (after column width-1).
    boundaries = [-1] + sorted(line_columns) + [width]
    for i in range(len(boundaries) - 1):
        # Define region columns: start is inclusive, end is exclusive.
        start_col = boundaries[i] + 1
        end_col = boundaries[i+1]
        # Add region only if it has a positive width.
        if start_col < end_col:
            regions.append({'start': start_col, 'end': end_col, 'scatter_count': 0})

    # Handle case where no regions could be defined (e.g., lines at edges or adjacent)
    if not regions:
         # If no lines were found, the logic above would have returned already.
         # This means lines exist but don't create separable regions.
         # print("Warning: No regions defined between lines.")
         return []


    # Step 4: Count Scatter Pixels in each Region.
    max_scatter_count = -1
    target_region_index = -1

    for i, region in enumerate(regions):
        start, end = region['start'], region['end']
        # Extract the subgrid for the current region.
        subgrid = grid[:, start:end]
        # Count pixels matching the scatter color.
        count = np.count_nonzero(subgrid == scatter_color)
        regions[i]['scatter_count'] = count

        # Step 5: Track the region with the maximum count.
        # Tie-breaking: The first region (leftmost) with the max count is chosen.
        if count > max_scatter_count:
            max_scatter_count = count
            target_region_index = i

    # Check if any scatter pixels were found or if any region was selected.
    if target_region_index == -1:
        # This could happen if no scatter pixels exist or if all regions had 0 count.
        # The examples imply the target region always exists.
        # If no scatter pixels, the rule isn't well-defined. Return empty?
        # Or return the first region? Let's return empty if max count remains <= 0 and regions exist.
        if max_scatter_count <= 0 and regions:
            # print("Warning: No scatter pixels found in any region. Cannot determine target region.")
            # If needed, could default to the first region: target_region_index = 0
             return []
        elif not regions:
            # Should have been caught earlier, but double-checking.
            return []
        # If max_scatter_count is > 0, target_region_index should have been set.

    # Step 6: Select the Target Region details.
    target_region = regions[target_region_index]
    target_start_col = target_region['start']
    target_end_col = target_region['end']

    # Step 7: Extract the subgrid corresponding to the target region.
    output_grid = grid[:, target_start_col:target_end_col]

    # Return the result as a list of lists.
    return output_grid.tolist()