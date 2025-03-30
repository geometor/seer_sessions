import numpy as np
import collections

"""
Identify two distinct colors in the input grid. One color forms complete horizontal and vertical lines (separator color), dividing the grid into regions filled with the other color (region color). Count the number of horizontal separator lines (H) and vertical separator lines (V). Create an output grid with dimensions (H+1) x (V+1) filled entirely with the region color.
"""

def find_separator_and_region_colors(grid):
    """Identifies the separator and region colors."""
    unique_colors = np.unique(grid)
    if len(unique_colors) != 2:
        # This case might indicate an issue or a different pattern,
        # but based on examples, we expect exactly two colors.
        # Handle potential errors or return None if needed.
        # For now, assume valid input based on examples.
        # Let's tentatively pick the most frequent as region color if needed,
        # but ideally, identification relies on line formation.
        counts = collections.Counter(grid.flatten())
        region_color = counts.most_common(1)[0][0]
        separator_color = [c for c in unique_colors if c != region_color][0]
        # print(f"Warning: Expected 2 colors, found {len(unique_colors)}. Guessing separator={separator_color}, region={region_color}")

    else:
        color1, color2 = unique_colors
        
        # Check color1 for separator properties
        is_sep1_h = np.any(np.all(grid == color1, axis=1))
        is_sep1_v = np.any(np.all(grid == color1, axis=0))

        # Check color2 for separator properties
        is_sep2_h = np.any(np.all(grid == color2, axis=1))
        is_sep2_v = np.any(np.all(grid == color2, axis=0))

        if is_sep1_h and is_sep1_v:
            separator_color = color1
            region_color = color2
        elif is_sep2_h and is_sep2_v:
            separator_color = color2
            region_color = color1
        else:
            # Fallback or error handling if neither color forms both H and V lines
            # Based on examples, one color *will* be the separator.
            # Let's assume the color forming lines is the separator,
            # prioritizing the one forming both if possible.
            # A simple fallback could be to check which color forms *any* line.
            if is_sep1_h or is_sep1_v:
                separator_color = color1
                region_color = color2
            elif is_sep2_h or is_sep2_v:
                 separator_color = color2
                 region_color = color1
            else:
                 # If neither forms lines, maybe pick based on frequency?
                 # This scenario shouldn't occur based on the task description derived.
                 counts = collections.Counter(grid.flatten())
                 region_color = counts.most_common(1)[0][0]
                 separator_color = [c for c in unique_colors if c != region_color][0]
                 # print(f"Warning: Neither color forms full lines. Guessing separator={separator_color}, region={region_color}")


    return separator_color, region_color

def count_separator_lines(grid, separator_color):
    """Counts the horizontal and vertical separator lines."""
    num_rows, num_cols = grid.shape

    # Count horizontal lines
    h_lines = 0
    for r in range(num_rows):
        if np.all(grid[r, :] == separator_color):
            h_lines += 1

    # Count vertical lines
    v_lines = 0
    for c in range(num_cols):
        if np.all(grid[:, c] == separator_color):
            v_lines += 1

    return h_lines, v_lines

def transform(input_grid):
    """
    Transforms the input grid based on identifying separator lines and region color.

    1. Converts the input list of lists to a numpy array.
    2. Identifies the separator color (forms full rows and columns) and the region color.
    3. Counts the number of horizontal (H) and vertical (V) separator lines.
    4. Creates an output grid of size (H+1) x (V+1).
    5. Fills the output grid with the region color.
    6. Returns the output grid as a numpy array.
    """
    # Convert input to numpy array
    input_np = np.array(input_grid, dtype=int)

    # Identify the separator and region colors
    separator_color, region_color = find_separator_and_region_colors(input_np)
    if separator_color is None:
         # Handle error case if colors couldn't be determined as expected
         print("Error: Could not determine separator and region colors definitively.")
         # Return a default or empty grid, or raise an exception
         return np.array([[]], dtype=int)


    # Count the number of horizontal and vertical separator lines
    H, V = count_separator_lines(input_np, separator_color)

    # Determine the dimensions of the output grid
    output_height = H + 1
    output_width = V + 1

    # Create the output grid filled with the region color
    output_grid = np.full((output_height, output_width), region_color, dtype=int)

    # Return the output grid (can be converted back to list of lists if required by framework)
    return output_grid.tolist()