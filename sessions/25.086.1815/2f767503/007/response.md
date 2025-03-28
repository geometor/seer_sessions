```python
import numpy as np

def find_unique_contiguous_gray_line(grid):
    """
    Finds all gray pixels (5) and checks if they form exactly one
    contiguous vertical OR horizontal line.
    Returns a tuple (type, coord, min_val, max_val) or None.
    - type: 'vertical' or 'horizontal'.
    - coord: The column index (c_gray) if vertical, or row index (r_gray) if horizontal.
    - min_val: The minimum row index (r_min) if vertical, or minimum column index (c_min) if horizontal.
    - max_val: The maximum row index (r_max) if vertical, or maximum column index (c_max) if horizontal.
    Returns None if no gray pixels are found, or if they don't form exactly one
    contiguous vertical or horizontal line.
    """
    rows, cols = grid.shape
    gray_pixels = []
    # Collect coordinates of all gray pixels
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 5:
                gray_pixels.append((r, c))

    # Return None if no gray pixels found
    if not gray_pixels:
        return None

    num_gray = len(gray_pixels)

    # Check if all gray pixels form a single contiguous vertical line
    gray_pixels.sort() # Sort primarily by row, then by column
    first_r, first_c = gray_pixels[0]
    is_vertical = all(c == first_c for r, c in gray_pixels)
    if is_vertical:
        min_r = first_r
        max_r = gray_pixels[-1][0]
        # Check contiguity: number of pixels must match row span,
        # and rows must be sequential.
        is_contiguous_vertical = (num_gray == (max_r - min_r + 1)) and \
                                 all(gray_pixels[i][0] == min_r + i for i in range(num_gray))
        if is_contiguous_vertical:
             return ('vertical', first_c, min_r, max_r)

    # Check if all gray pixels form a single contiguous horizontal line
    # Sort primarily by column, then by row, needed for horizontal check
    gray_pixels.sort(key=lambda x: (x[1], x[0]))
    first_r, first_c = gray_pixels[0] # Potentially different first_r/first_c after resort
    is_horizontal = all(r == first_r for r, c in gray_pixels)
    if is_horizontal:
        min_c = first_c
        max_c = gray_pixels[-1][1]
        # Check contiguity: number of pixels must match col span,
        # and columns must be sequential.
        is_contiguous_horizontal = (num_gray == (max_c - min_c + 1)) and \
                                   all(gray_pixels[i][1] == min_c + i for i in range(num_gray))
        if is_contiguous_horizontal:
            return ('horizontal', first_r, min_c, max_c)

    # If all gray pixels did not form exactly one contiguous vertical or horizontal line
    return None

def find_maroon_pixel(grid):
    """
    Finds the coordinates (row, col) of a single maroon pixel (9).
    Returns (r_m, c_m) if exactly one maroon pixel is found, otherwise returns None.
    """
    rows, cols = grid.shape
    maroon_coords = []
    # Collect coordinates of all maroon pixels
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 9:
                maroon_coords.append((r, c))

    # Return coordinates only if exactly one maroon pixel exists
    if len(maroon_coords) == 1:
        return maroon_coords[0]
    else:
        return None # Zero or multiple maroon pixels found

def transform(input_grid):
    """
    Transforms the input grid based on the relative position of a single contiguous gray line (color 5)
    and a single maroon pixel (color 9). Changes specific yellow pixels (color 4) to orange (color 7).

    Rule Cases:
    1. Vertical Gray Line, Maroon Left: If maroon is one step left (c_m = c_gray - 1) and row-aligned
       (r_min <= r_m <= r_max), change yellow pixels within a calculated bounding box to the right
       of the gray line to orange. The box starts at the top row of the gray line and extends downwards.
       Its width is twice the height of the gray line, starting 2 columns right of the gray line.
    2. Vertical Gray Line, Maroon Right: If maroon is one step right (c_m = c_gray + 1) and row-aligned
       (r_min <= r_m <= r_max), change yellow pixels in the region to the left of the gray line
       (c < c_gray) and between the maroon row and the bottom of the gray line (inclusive, r_m <= r <= r_max)
       to orange.
    3. Horizontal Gray Line, Maroon Below: If maroon is one step below (r_m = r_gray + 1) and col-aligned
       (c_min <= c_m <= c_max), the transformation observed in the examples does not follow a clear
       geometric rule related to the gray/maroon positions analyzed so far. Example 1, which fits this case,
       shows no change between input and output. Therefore, this function returns the input grid unchanged
       for this specific configuration.
    4. Other Cases: If no unique contiguous gray line, no unique maroon pixel, or their relative positions
       don't match cases 1, 2, or 3, the input grid is returned unchanged.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    # Create a copy to modify, ensuring the original input is not changed
    output_grid_np = np.copy(input_grid_np)

    # --- Step 1: Find the required structures ---
    # Find exactly one contiguous gray line (vertical or horizontal)
    gray_line_info = find_unique_contiguous_gray_line(input_grid_np)
    # Find exactly one maroon pixel
    maroon_pos = find_maroon_pixel(input_grid_np)

    # --- Step 2: Check if required structures exist uniquely ---
    # If either structure is missing or not unique, no transformation applies
    if gray_line_info is None or maroon_pos is None:
        return input_grid # Return the original input grid

    # Unpack structure details
    line_type, line_coord, line_min, line_max = gray_line_info
    r_m, c_m = maroon_pos

    # --- Step 3: Apply transformation based on the identified case ---
    transformation_applied = False

    # Case 1: Vertical Gray Line, Maroon Immediately Left
    if line_type == 'vertical':
        c_gray, r_min_gray, r_max_gray = line_coord, line_min, line_max
        # Check relative position: maroon left and row-aligned
        if c_m == c_gray - 1 and r_min_gray <= r_m <= r_max_gray:
            # Calculate bounding box parameters
            height_gray = r_max_gray - r_min_gray + 1
            # Row start is the top of the gray line
            r_start_box = r_min_gray
            # Row end depends on gray line span and maroon row relative position
            r_end_box = r_max_gray + (r_m - r_min_gray + 1)
            # Column start is 2 columns to the right of the gray line
            c_start_box = c_gray + 2
            # Column end depends on gray line column and height * 2
            c_end_box = c_gray + height_gray * 2

            # Apply transformation: Change yellow (4) to orange (7) within the box
            # Iterate safely within grid boundaries
            for r in range(max(0, r_start_box), min(rows, r_end_box + 1)):
                for c in range(max(0, c_start_box), min(cols, c_end_box + 1)):
                    if output_grid_np[r, c] == 4: # If pixel is yellow
                        output_grid_np[r, c] = 7 # Change to orange
            transformation_applied = True

    # Case 2: Vertical Gray Line, Maroon Immediately Right
    elif line_type == 'vertical': # Check vertical type again for clarity
        c_gray, r_min_gray, r_max_gray = line_coord, line_min, line_max
        # Check relative position: maroon right and row-aligned
        if c_m == c_gray + 1 and r_min_gray <= r_m <= r_max_gray:
            # Apply transformation in the specified region to the left
            # Iterate through rows from maroon row down to gray line bottom
            for r in range(max(0, r_m), min(rows, r_max_gray + 1)):
                # Iterate through columns strictly left of the gray line
                for c in range(0, max(0, c_gray)): # c goes from 0 to c_gray-1
                    if output_grid_np[r, c] == 4: # If pixel is yellow
                        output_grid_np[r, c] = 7 # Change to orange
            transformation_applied = True

    # Case 3: Horizontal Gray Line, Maroon Immediately Below
    elif line_type == 'horizontal':
        r_gray, c_min_gray, c_max_gray = line_coord, line_min, line_max
        # Check relative position: maroon below and column-aligned
        if r_m == r_gray + 1 and c_min_gray <= c_m <= c_max_gray:
            # Based on Example 1, no change occurs in this configuration.
            # The 'pass' means transformation_applied remains False.
            pass

    # --- Step 4: Return the result ---
    if transformation_applied:
        # If a transformation was made, return the modified grid
        return output_grid_np.tolist()
    else:
        # If no conditions matched or Case 3 triggered, return the original input grid
        return input_grid
```