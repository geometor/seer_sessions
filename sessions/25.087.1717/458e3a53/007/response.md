```python
import numpy as np
from collections import Counter

"""
Identifies a 'frame' color based on line segments, finds solid rectangular blocks of other colors completely enclosed by a 1-pixel thick border of the frame color, and arranges the colors of these inner blocks into an output grid based on the relative spatial positions of the blocks.

1.  **Determine Frame Color:** Identify the color that forms the most horizontal and vertical line segments of length 3 or more in the input grid. This is the `frame_color`. If no such lines are found, use the most frequent non-background color as a fallback.
2.  **Find Framed Rectangles:** Iterate through the grid to find potential top-left corners (r, c) of inner blocks (pixels not matching the `frame_color`).
3.  **Verify Rectangle and Frame:** For each potential corner:
    a.  Determine the `inner_color`.
    b.  Calculate the `height` and `width` of the contiguous block of `inner_color` starting at (r, c).
    c.  Check if this inner block is fully enclosed by a 1-pixel thick border consisting solely of the `frame_color`. The frame check includes corners and must be within grid bounds.
4.  **Store Rectangle Info:** If a valid framed rectangle is found, store its `inner_color`, and the top-left coordinates `(r, c)` of the inner block.
5.  **Calculate Output Dimensions:** Collect the unique row coordinates and unique column coordinates from the stored top-left positions. Sort them to determine the order. The number of unique rows is the `output_height`, and the number of unique columns is the `output_width`.
6.  **Create Coordinate Maps:** Create mappings from the sorted unique row coordinates to output grid row indices (0, 1, ...) and from sorted unique column coordinates to output grid column indices (0, 1, ...).
7.  **Construct and Populate Output Grid:** Create an output grid of size `output_height` x `output_width`, initialized to white (0). Iterate through the stored rectangle information. For each rectangle, use the coordinate maps to find the corresponding output grid position `(output_r, output_c)` for its `(r, c)` coordinates and place its `inner_color` there.
8.  **Return Output:** Return the populated output grid. If no frame color or no rectangles are found, return a default `[[0]]` grid.
"""

def find_frame_color(grid):
    """
    Identifies the potential frame color by finding the color that forms
    the most horizontal and vertical line segments of length 3 or more.
    Includes a fallback to most frequent non-background or overall most frequent color.
    """
    rows, cols = grid.shape
    line_colors = Counter()
    min_line_length = 3

    # Horizontal lines
    for r in range(rows):
        c = 0
        while c < cols:
            color = grid[r, c]
            if color == 0: # Skip background for line counting? Maybe not necessary
                c+=1
                continue
            length = 0
            while c + length < cols and grid[r, c + length] == color:
                length += 1

            if length >= min_line_length:
                line_colors[color] += 1
            c += length # Move past the segment regardless of length


    # Vertical lines
    for c in range(cols):
        r = 0
        while r < rows:
            color = grid[r, c]
            if color == 0: # Skip background for line counting?
                 r+=1
                 continue
            length = 0
            while r + length < rows and grid[r + length, c] == color:
                length += 1

            if length >= min_line_length:
                line_colors[color] += 1
            r += length # Move past the segment regardless of length

    if line_colors:
        # Return the most common color found in lines
        frame_color = line_colors.most_common(1)[0][0]
        return frame_color
    else:
        # Fallback: If no lines >= 3, find the most frequent non-background color
        all_colors = Counter(grid.flatten())
        if 0 in all_colors:
            del all_colors[0] # Remove background color count

        if all_colors:
             # Return most frequent non-background color
             return all_colors.most_common(1)[0][0]
        else:
            # If only background exists or grid is empty, maybe return background or -1
            # Let's try returning the overall most frequent if non-background failed
            all_colors_inc_bg = Counter(grid.flatten())
            if all_colors_inc_bg:
                 return all_colors_inc_bg.most_common(1)[0][0]
            else:
                 return -1 # Indicate no plausible color found


def find_framed_rectangles(grid, frame_color):
    """
    Finds all rectangles perfectly framed by a specific frame_color.
    This version removes the `visited` array to avoid issues with adjacent frames.

    Args:
        grid (np.ndarray): The input grid.
        frame_color (int): The color of the frame.

    Returns:
        list: A list of tuples, where each tuple contains:
              (inner_color, top_row, left_col)
              representing the inner color and the top-left coordinates
              of the inner rectangle. Returns an empty list if none found.
    """
    rectangles = []
    rows, cols = grid.shape
    processed_inner_coords = set() # Keep track of inner blocks already found

    # Iterate through potential top-left corners of the *inner* rectangle
    # The inner rectangle must start at least at (1, 1) and end at most at (rows-2, cols-2)
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            
            # If this coordinate is part of an already identified inner block, skip
            if (r, c) in processed_inner_coords:
                continue

            # Potential inner block must not be the frame color
            if grid[r, c] == frame_color:
                continue

            inner_color = grid[r, c]

            # Basic check: Immediate top and left must be frame color
            if grid[r - 1, c] != frame_color or grid[r, c - 1] != frame_color:
                 continue
                 
            # Determine the dimensions of the solid inner rectangle starting at (r,c)
            height = 0
            for h_offset in range(rows - r):
                if grid[r + h_offset, c] == inner_color:
                    height += 1
                else:
                    break

            width = 0
            # Check first row consistency to find width
            for w_offset in range(cols - c):
                 if r + height > rows : # Ensure we don't go out of bounds when checking rows below
                     width=0
                     break
                 # Check if the entire column segment within the potential rect has the inner color
                 is_solid_column = True
                 for h_check in range(height):
                     if c + w_offset >= cols or grid[r + h_check, c + w_offset] != inner_color:
                         is_solid_column = False
                         break
                 if is_solid_column:
                    width +=1
                 else:
                    break
            
            if height == 0 or width == 0:
                continue # Not a valid rectangle start

            # Define inner block boundaries
            inner_r_start, inner_c_start = r, c
            inner_r_end, inner_c_end = r + height - 1, c + width - 1

            # --- Verification Step ---
            is_valid = True

            # 1. Verify the inner area is indeed solid inner_color (redundant given width calc, but safe)
            # if not np.all(grid[inner_r_start : inner_r_end + 1, inner_c_start : inner_c_end + 1] == inner_color):
            #     is_valid = False
            #     continue # This check should be inherently passed by how width/height were found

            # 2. Verify the surrounding frame (1-pixel thick) is solid frame_color
            frame_r_start, frame_c_start = inner_r_start - 1, inner_c_start - 1
            frame_r_end, frame_c_end = inner_r_end + 1, inner_c_end + 1

            # Check if frame goes out of bounds
            if frame_r_start < 0 or frame_c_start < 0 or frame_r_end >= rows or frame_c_end >= cols:
                is_valid = False
                continue # Frame extends beyond grid boundaries

            try:
                # Check Top frame row
                if not np.all(grid[frame_r_start, frame_c_start : frame_c_end + 1] == frame_color):
                    is_valid = False
                # Check Bottom frame row
                elif not np.all(grid[frame_r_end, frame_c_start : frame_c_end + 1] == frame_color):
                    is_valid = False
                # Check Left frame column (excluding corners already checked by rows)
                elif not np.all(grid[frame_r_start + 1 : frame_r_end, frame_c_start] == frame_color):
                    is_valid = False
                # Check Right frame column (excluding corners already checked by rows)
                elif not np.all(grid[frame_r_start + 1 : frame_r_end, frame_c_end] == frame_color):
                    is_valid = False
            except IndexError:
                 # Should be caught by boundary check above, but as safety
                is_valid = False

            # If all checks passed, it's a valid framed rectangle
            if is_valid:
                # Add to list
                rectangles.append((inner_color, inner_r_start, inner_c_start))
                
                # Mark all pixels within this inner block as processed
                # This prevents redundant checks starting within this block
                for row_idx in range(inner_r_start, inner_r_end + 1):
                    for col_idx in range(inner_c_start, inner_c_end + 1):
                        processed_inner_coords.add((row_idx, col_idx))

    return rectangles


def transform(input_grid):
    """
    Transforms the input grid by finding framed rectangles, extracting their
    inner colors, and arranging them spatially in an output grid.
    """
    # Convert input list of lists to numpy array
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # Handle grids too small to contain a framed rectangle (inner 1x1 + frame = 3x3)
    if rows < 3 or cols < 3:
        return [[0]] # Default output for small grids

    # Step 1: Identify the frame color
    frame_color = find_frame_color(grid_np)

    # If no plausible frame color identified, return default
    if frame_color == -1:
         # print("Warning: Could not reliably determine frame color.")
         return [[0]]

    # Step 2, 3 & 4: Find all framed rectangles using the identified frame color
    # and record their inner color and top-left inner coordinate.
    # Uses the revised find_framed_rectangles without the problematic visited array.
    found_rectangles = find_framed_rectangles(grid_np, frame_color)

    # Handle case where no rectangles are found
    if not found_rectangles:
        return [[0]] # Return default if no framed rectangles found

    # Step 5: Determine output dimensions and coordinate mapping
    # Collect unique row and column coordinates of the *inner* top-left corners
    rows_coords = sorted(list(set(r for _, r, _ in found_rectangles)))
    cols_coords = sorted(list(set(c for _, _, c in found_rectangles)))

    # Calculate output grid dimensions
    output_rows = len(rows_coords)
    output_cols = len(cols_coords)

    # Handle case where dimensions might be zero (shouldn't happen if rectangles were found)
    if output_rows == 0 or output_cols == 0:
         return [[0]]

    # Step 6: Create mappings from actual grid coordinates to output grid indices
    row_map = {r: i for i, r in enumerate(rows_coords)}
    col_map = {c: i for i, c in enumerate(cols_coords)}

    # Step 7: Create the output grid, initialized with white (0)
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Step 8: Populate the output grid
    for inner_color, r, c in found_rectangles:
        # Find the corresponding output grid indices using the maps
        # Check if the coordinates exist in the map (they should)
        if r in row_map and c in col_map:
            output_r = row_map[r]
            output_c = col_map[c]
            # Place the inner color at the calculated position
            output_grid[output_r, output_c] = inner_color
        # else:
            # This case indicates an issue, perhaps in how rectangles were recorded or maps created.
            # print(f"Warning: Coordinate ({r}, {c}) not found in maps.")


    # Step 9: Return the populated output grid as a list of lists
    return output_grid.tolist()
```