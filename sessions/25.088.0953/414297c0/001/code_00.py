import numpy as np
from collections import deque

"""
Identifies the largest solid, single-colored, non-white rectangle in the input grid.
This rectangle defines the background color and dimensions of the output grid.
Then, iterates through the input grid. Any pixel that is not white (0) and not part of the identified background rectangle is overlaid onto the output grid, maintaining its position relative to the top-left corner of the background rectangle found in the input.
"""

def find_largest_rectangle(grid):
    """
    Finds the largest solid rectangle of a single non-white color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        dict or None: A dictionary containing the rectangle's color, top-left row 'r',
                      top-left column 'c', height 'h', and width 'w',
                      or None if no such rectangle is found.
    """
    height, width = grid.shape
    max_area = 0
    best_rect_info = None

    # Iterate through all possible top-left corners (r1, c1)
    for r1 in range(height):
        for c1 in range(width):
            # Iterate through all possible bottom-right corners (r2, c2)
            for r2 in range(r1, height):
                for c2 in range(c1, width):
                    # Extract the subgrid
                    sub_grid = grid[r1:r2+1, c1:c2+1]

                    # Check if the subgrid is valid and potentially a candidate
                    if sub_grid.size == 0:
                        continue

                    # Get the potential color from the top-left of the subgrid
                    color = sub_grid[0, 0]

                    # Rule out white background color
                    if color == 0:
                        continue

                    # Check if all elements in the subgrid are the same color
                    if np.all(sub_grid == color):
                        # Calculate area
                        current_height = r2 - r1 + 1
                        current_width = c2 - c1 + 1
                        area = current_height * current_width

                        # Update if this is the largest rectangle found so far
                        if area > max_area:
                            max_area = area
                            best_rect_info = {
                                'color': color,
                                'r': r1,
                                'c': c1,
                                'h': current_height,
                                'w': current_width
                            }
    return best_rect_info


def transform(input_grid):
    """
    Transforms the input grid based on overlaying elements onto the largest rectangle.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Find the largest solid non-white rectangle (the canvas)
    canvas_info = find_largest_rectangle(grid_np)

    if canvas_info is None:
        # Handle case where no suitable rectangle is found (e.g., return empty or input)
        # Based on examples, this shouldn't happen, but good practice.
        return [] # Or perhaps return input_grid

    canvas_color = canvas_info['color']
    canvas_r, canvas_c = canvas_info['r'], canvas_info['c']
    canvas_h, canvas_w = canvas_info['h'], canvas_info['w']

    # Initialize the output grid with the canvas color and dimensions
    output_grid_np = np.full((canvas_h, canvas_w), canvas_color, dtype=int)

    # Iterate through the input grid to find overlay pixels
    for r in range(height):
        for c in range(width):
            pixel_color = grid_np[r, c]

            # Check if the pixel is part of the canvas rectangle area
            is_in_canvas_area = (canvas_r <= r < canvas_r + canvas_h and
                                 canvas_c <= c < canvas_c + canvas_w)

            # A pixel is an overlay if it's not white AND
            # EITHER it's outside the canvas area
            # OR it's inside the canvas area but has a DIFFERENT color than the canvas
            # Simplified: If pixel is not white (0) and not the canvas color itself at that location
            # More precisely: We need to copy any non-white pixel that ISN'T part of the original canvas block
            # Let's check if the pixel should be considered for overlaying
            if pixel_color != 0: # Must not be white
                 # If the pixel is within the bounds of where the canvas *was* in the input...
                 if is_in_canvas_area:
                     # ...but its color is different from the canvas color, it's an overlay
                     if pixel_color != canvas_color:
                         # Calculate its position relative to the canvas top-left
                         out_r = r - canvas_r
                         out_c = c - canvas_c
                         # Place it on the output grid
                         output_grid_np[out_r, out_c] = pixel_color
                 # If the pixel is *outside* the canvas area in the input, it's also potentially an overlay
                 # but we only care if its corresponding position *would* fall inside the output grid dimensions
                 else:
                     # Calculate its hypothetical position relative to the canvas top-left
                     out_r = r - canvas_r
                     out_c = c - canvas_c
                     # Check if this position is valid within the output grid bounds
                     if 0 <= out_r < canvas_h and 0 <= out_c < canvas_w:
                         # Place it on the output grid
                         output_grid_np[out_r, out_c] = pixel_color


    # Convert the final numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid