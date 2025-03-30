import numpy as np
from collections import deque

"""
Transforms the input grid based on identifying two main regions: a large, solid-colored rectangular 'canvas' and a 'stamps' area containing other non-white patterns. The transformation involves:
1. Identifying the largest contiguous rectangular area of a single non-white color (the 'Canvas Area'). Determine its color ('Canvas Color') and dimensions.
2. Identifying all other non-white pixels in the input grid that are *not* part of the Canvas Area. These constitute the 'Stamps Area'.
3. Determining the bounding box of the Stamps Area.
4. Creating an output grid with the dimensions of the Canvas Area, filled entirely with the Canvas Color.
5. Iterating through the cells within the bounding box of the Stamps Area in the input grid.
6. For each cell within the Stamps Area bounding box:
    a. If the input cell's color is non-white (not 0) AND it's not part of the identified Canvas Area rectangle:
        i. Calculate the cell's relative row and column position within the Stamps Area bounding box (relative to its top-left corner).
        ii. If these relative coordinates fall within the bounds of the output grid:
            - Set the corresponding cell in the output grid to azure (8).
7. Return the modified output grid.
"""

def find_largest_monochromatic_rect(grid):
    """
    Finds the largest contiguous rectangular area of a single non-white color.

    Args:
        grid (np.array): The input grid.

    Returns:
        dict: A dictionary containing the 'r', 'c', 'h', 'w', and 'color'
              of the largest rectangle, or None if no non-white pixels exist.
    """
    rows, cols = grid.shape
    max_area = 0
    best_rect = None

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color == 0:  # Skip white background
                continue

            # Check for largest possible rectangle starting at (r, c) with this color
            max_w = cols - c
            for h in range(1, rows - r + 1):
                current_w = max_w
                for w in range(1, max_w + 1):
                    # Check if the rectangle (r, c) to (r+h-1, c+w-1) is monochromatic
                    is_monochromatic = True
                    # Check the new row/column being added
                    if w == current_w: # check new row only
                        for check_c in range(c, c + w):
                             if grid[r + h - 1, check_c] != color:
                                is_monochromatic = False
                                break
                    if h==1: # check new column only if it's the first row check
                        if grid[r + h - 1, c + w - 1] != color:
                                is_monochromatic = False

                    # More thorough check if needed (though optimized checks above should suffice)
                    # This simplified check might be faster if assumptions hold
                    # Check the bottom row of the potential rectangle expansion
                    if h > 1:
                         for check_c in range(c, c + w):
                             if grid[r + h - 1, check_c] != color:
                                 is_monochromatic = False
                                 current_w = w -1 # Max width possible for this height
                                 break
                         if not is_monochromatic: break # Stop increasing width for this height

                    # Check the rightmost column of the potential rectangle expansion
                    if is_monochromatic and w > 1:
                         for check_r in range(r, r + h):
                              if grid[check_r, c + w - 1] != color:
                                  is_monochromatic = False
                                  break # stop checking width
                         if not is_monochromatic:
                             current_w = w - 1 # update max width
                             break # Stop increasing width for this height


                    if not is_monochromatic:
                         break # Stop increasing width for this height


                    # Update best rectangle if this one is larger
                    area = h * w
                    if area > max_area:
                        max_area = area
                        best_rect = {'r': r, 'c': c, 'h': h, 'w': w, 'color': color}
                max_w = current_w # Update the max width possible for next height iteration

    return best_rect


def get_bounding_box(pixels):
    """
    Calculates the bounding box for a list of pixel coordinates.

    Args:
        pixels (list): A list of (row, col) tuples.

    Returns:
        tuple: (min_r, min_c, max_r, max_c) or None if pixels is empty.
    """
    if not pixels:
        return None
    min_r = min(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_r = max(r for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return min_r, min_c, max_r, max_c


def transform(input_grid):
    """
    Applies the transformation described above to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Identify the Canvas Area
    canvas_info = find_largest_monochromatic_rect(grid)
    if canvas_info is None:
        # Handle case with no non-white pixels or only stamps?
        # Based on examples, there's always a canvas. Assume it exists.
        # If it could be missing, we'd need different logic.
        # For now, assume it's found. If not, maybe return empty or original?
        # Let's assume it's always found based on training data.
         return [] # Or raise error, depends on spec for invalid input

    canvas_r, canvas_c = canvas_info['r'], canvas_info['c']
    canvas_h, canvas_w = canvas_info['h'], canvas_info['w']
    canvas_color = canvas_info['color']

    # 4. Create the initial output grid
    output_grid = np.full((canvas_h, canvas_w), canvas_color, dtype=int)

    # 2. Identify Stamps Area pixels
    stamp_pixels_coords = []
    for r in range(rows):
        for c in range(cols):
            # Check if pixel is non-white
            if grid[r, c] != 0:
                # Check if pixel is outside the canvas rectangle bounds
                is_outside_canvas = not (
                    canvas_r <= r < canvas_r + canvas_h and
                    canvas_c <= c < canvas_c + canvas_w
                )
                if is_outside_canvas:
                    stamp_pixels_coords.append((r, c))

    # If there are no stamp pixels, return the canvas as is
    if not stamp_pixels_coords:
        return output_grid.tolist()

    # 3. Determine the bounding box of the Stamps Area
    stamp_box = get_bounding_box(stamp_pixels_coords)
    if stamp_box is None: # Should not happen if stamp_pixels_coords is not empty
         return output_grid.tolist()

    min_r_stamp, min_c_stamp, max_r_stamp, max_c_stamp = stamp_box

    # 5. & 6. Iterate through the Stamps Area bounding box and transfer patterns
    for r in range(min_r_stamp, max_r_stamp + 1):
        for c in range(min_c_stamp, max_c_stamp + 1):
            # Check if the pixel is within the original grid bounds (might not be if box extends)
            if 0 <= r < rows and 0 <= c < cols:
                 input_color = grid[r, c]
                 # Check if it's a non-white pixel AND truly part of the stamps (not canvas)
                 is_stamp_pixel = (
                     input_color != 0 and
                     not (canvas_r <= r < canvas_r + canvas_h and canvas_c <= c < canvas_c + canvas_w)
                 )

                 if is_stamp_pixel:
                    # Calculate relative position within the stamp bounding box
                    rel_r = r - min_r_stamp
                    rel_c = c - min_c_stamp

                    # Check if relative position is within the output grid bounds
                    if 0 <= rel_r < output_grid.shape[0] and 0 <= rel_c < output_grid.shape[1]:
                        # Set the output pixel to azure (8)
                        output_grid[rel_r, rel_c] = 8

    # 7. Return the final grid
    return output_grid.tolist()