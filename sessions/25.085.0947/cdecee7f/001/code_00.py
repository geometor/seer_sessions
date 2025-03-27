import numpy as np

"""
Identify all non-white (non-zero) pixels in the 10x10 input grid.
Collect the color values of these pixels by scanning the input grid column by column (left-to-right), and then row by row within each column (top-to-bottom). Store these collected colors in a list.
If the number of collected colors is 6 or more, swap the color at index 3 with the color at index 5 in the list.
Create a new 3x3 output grid, initialized with white (0).
Fill the 3x3 output grid row by row (top-to-bottom), and then column by column within each row (left-to-right), using the colors from the (potentially modified) list.
If the list runs out of colors before the 3x3 grid is full, the remaining cells stay white (0).
Return the filled 3x3 grid.
"""

def transform(input_grid):
    """
    Transforms the input grid based on collecting non-white pixels column-wise,
    conditionally swapping elements, and populating a 3x3 grid row-wise.

    Args:
        input_grid (list of lists): The input 10x10 grid.

    Returns:
        list of lists: The transformed 3x3 grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize an empty list to store collected colors
    collected_colors = []

    # 1. Iterate through columns, then rows (column-major)
    for j in range(width):
        for i in range(height):
            # 2. Collect non-white pixel colors
            pixel_value = input_np[i, j]
            if pixel_value != 0:
                collected_colors.append(pixel_value)

    # 3. Conditional swap if length is 6 or more
    if len(collected_colors) >= 6:
        # Ensure indices are valid before swapping (though check >= 6 covers this)
        if len(collected_colors) > 5: # Redundant check, but safe
             collected_colors[3], collected_colors[5] = collected_colors[5], collected_colors[3]

    # 4. Create a new 3x3 output grid initialized with white (0)
    output_grid_np = np.zeros((3, 3), dtype=int)
    output_height, output_width = output_grid_np.shape

    # 5. Populate the output grid row by row (row-major)
    color_index = 0
    for r in range(output_height):
        for c in range(output_width):
            # Check if there are still colors left to place
            if color_index < len(collected_colors):
                output_grid_np[r, c] = collected_colors[color_index]
                color_index += 1
            else:
                # No more colors, leave remaining cells as 0 (already initialized)
                break # Optimization: break inner loop if no more colors
        if color_index >= len(collected_colors):
            break # Optimization: break outer loop if no more colors

    # Convert numpy array back to list of lists for the final output
    output_grid = output_grid_np.tolist()

    return output_grid