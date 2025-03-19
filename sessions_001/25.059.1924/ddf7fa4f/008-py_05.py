"""
1.  **Identify the Gray Region:** Locate the contiguous block of gray (5) pixels within the input grid. This region is the target for replacement.
2.  **Identify All Unique Colors (Except White):** Determine all unique colors present in the entire input grid, excluding white (0).
3.  **Determine Replacement Dimensions and Proportions:**
    *   The height of the replacement region is the same as the height of the gray region.
    *   The width of each color's segment within the replacement region is proportional to its total horizontal span (contiguous width) in the *entire input grid*, relative to the sum of the widths of all unique colors (excluding white).
4.  **Replace the Gray Region:** Replace the gray region with the identified colors, maintaining their proportional widths. The order of colors is determined by their left-to-right appearance in the input grid. If a color's calculated width rounds down to zero, but the color *does* exist in the input, give it a minimum width of 1 to ensure it's represented.
5. **Remainder of the Image:** All other pixels in the image remain unchanged.
"""

import numpy as np

def find_object(grid, color):
    """Finds the bounding box of a contiguous region of the specified color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Color not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def get_color_width(grid, color):
    """Calculates the total contiguous width of a color in the grid."""
    bounds = find_object(grid, color)
    if bounds is None:
        return 0
    _, min_col = bounds[0]
    _, max_col = bounds[1]
    return max_col - min_col + 1

def get_color_order(grid, colors):
    """Determines the left-to-right order of colors based on their first appearance."""
    color_positions = []
    for color in colors:
        bounds = find_object(grid, color)
        if bounds:
            _, min_col = bounds[0]
            color_positions.append((min_col, color))
    color_positions.sort()  # Sort by column (left-to-right)
    return [color for _, color in color_positions]

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)

    # 1. Identify the Gray Region
    gray_bounds = find_object(input_grid, 5)
    if gray_bounds is None:
        return output_grid  # No gray region, return input as is

    gray_min_row, gray_min_col = gray_bounds[0]
    gray_max_row, gray_max_col = gray_bounds[1]
    gray_width = gray_max_col - gray_min_col + 1
    gray_height = gray_max_row - gray_min_row + 1

    # 2. Identify All Unique Colors (excluding 0)
    unique_colors = [color for color in np.unique(input_grid) if color != 0]

    # 3. Determine Replacement Dimensions and Proportions
    replacement_height = gray_height
    color_widths = [get_color_width(input_grid, color) for color in unique_colors]
    total_non_white_width = sum(color_widths)

    # Determine color order
    ordered_colors = get_color_order(input_grid, unique_colors)

    # 4. Replace the Gray Region
    current_col = gray_min_col
    for color in ordered_colors:
        color_index = unique_colors.index(color) # get index to use with color_widths
        if total_non_white_width > 0:
            proportional_width = int(round((color_widths[color_index] / total_non_white_width) * gray_width))

            # Ensure color is represented if it exists
            if color_widths[color_index] > 0 and proportional_width == 0:
                proportional_width = 1
        else:
          proportional_width = 0

        # last color gets the remaining width
        if color == ordered_colors[-1]:
            proportional_width = gray_max_col - current_col + 1


        output_grid[gray_min_row:gray_min_row + replacement_height,
                    current_col:current_col + proportional_width] = color
        current_col += proportional_width

    # 5. Remainder of the Image: No changes needed, already copied

    return output_grid