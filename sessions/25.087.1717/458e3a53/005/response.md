```python
import numpy as np
from collections import Counter

"""
1. **Analyze Input Grid Lines:** Scan the input grid to identify the color that forms the most prominent horizontal and vertical line segments (e.g., segments of length 3 or more). Designate this color as the `frame_color`.
2. **Find Framed Rectangles:** Search the input grid for all occurrences of solid rectangular blocks (`inner_blocks`) where each block consists of a single color (`inner_color`) different from the `frame_color`, and is perfectly enclosed by a 1-pixel thick border composed solely of the `frame_color`.
3. **Record Rectangle Properties:** For each valid `framed_rectangle` found, store its `inner_color` and the grid coordinates (row, column) of the top-left pixel of its `inner_block`.
4. **Determine Output Dimensions and Mapping:**
   - Collect all unique row coordinates from the recorded top-left positions. Sort these unique rows. The number of unique rows is the `output_height`. Create a mapping from each unique row coordinate to its index (0, 1, ...) in the sorted list.
   - Collect all unique column coordinates from the recorded top-left positions. Sort these unique columns. The number of unique columns is the `output_width`. Create a mapping from each unique column coordinate to its index (0, 1, ...) in the sorted list.
5. **Construct Output Grid:** Create a new grid with dimensions `output_height` x `output_width`, initializing all cells to white (0).
6. **Populate Output Grid:** Iterate through the recorded rectangles. For each rectangle, use its stored `inner_color` and its top-left `inner_block` coordinates. Find the corresponding output row index using the row mapping and the output column index using the column mapping. Place the `inner_color` at this (output row, output column) position in the output grid.
7. **Return Output:** Return the fully populated output grid.
"""

def find_frame_color(grid):
    """
    Identifies the potential frame color by finding the color that forms
    the most horizontal and vertical line segments of length 3 or more.
    """
    rows, cols = grid.shape
    line_colors = Counter()
    min_line_length = 3

    # Horizontal lines
    for r in range(rows):
        c = 0
        while c < cols:
            color = grid[r, c]
            length = 0
            while c + length < cols and grid[r, c + length] == color:
                length += 1
            # Check length *after* finding the end of the segment
            if length >= min_line_length:
                line_colors[color] += 1
                # Move counter past this counted segment
                c += length
            else:
                # Move counter by 1 if segment wasn't long enough
                c += 1 # Correctly advance even if line isn't long enough

    # Vertical lines
    for c in range(cols):
         r = 0
         while r < rows:
            color = grid[r, c]
            length = 0
            while r + length < rows and grid[r + length, c] == color:
                length += 1
            # Check length *after* finding the end of the segment
            if length >= min_line_length:
                line_colors[color] += 1
                # Move counter past this counted segment
                r += length
            else:
                 # Move counter by 1 if segment wasn't long enough
                r += 1 # Correctly advance even if line isn't long enough

    # Return the most common color, or a default (e.g., -1) if none found
    if not line_colors:
        # Fallback: If no lines >= 3, maybe check most frequent color overall?
        # Or maybe the task guarantees such lines exist if framing exists.
        # Let's return -1 to indicate failure to find a line-based frame color.
         all_colors = Counter(grid.flatten())
         if all_colors:
             # Heuristic: perhaps the most frequent non-background (non-0) color?
             # Or maybe just the overall most frequent? Let's try most frequent.
             most_common = all_colors.most_common(1)
             if most_common:
                 return most_common[0][0] # Return most frequent color as fallback
         return -1 # Indicate no clear frame color found
    
    # Find the color with the maximum count
    frame_color = line_colors.most_common(1)[0][0]
    return frame_color


def find_framed_rectangles_with_color(grid, frame_color):
    """
    Finds all rectangles framed by a specific frame_color.

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
    visited = np.zeros_like(grid, dtype=bool)

    # Iterate through potential top-left corners of the *inner* rectangle
    # The inner rectangle must start at least at (1, 1)
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # Skip if visited or if this pixel is the frame color itself
            if visited[r, c] or grid[r, c] == frame_color:
                continue

            inner_color = grid[r, c]
            
            # Check if the pixel is potentially framed (immediate neighbors are frame_color)
            # Top, Left, Top-Left must be frame_color
            if not (grid[r - 1, c] == frame_color and
                    grid[r, c - 1] == frame_color and
                    grid[r - 1, c - 1] == frame_color):
                continue

            # Try to determine the dimensions of the inner rectangle
            height = 0
            width = 0

            # Determine height (check downwards)
            for h_offset in range(rows - r):
                if grid[r + h_offset, c] == inner_color:
                    height += 1
                else:
                    break

            # Determine width (check rightwards)
            for w_offset in range(cols - c):
                if grid[r, c + w_offset] == inner_color:
                    width += 1
                else:
                    break

            if height == 0 or width == 0:
                continue # Should not happen if we start on an inner_color pixel

            # Define inner block boundaries
            inner_r_start, inner_c_start = r, c
            inner_r_end, inner_c_end = r + height - 1, c + width - 1
            
            # --- Verification Step ---
            is_valid = True

            # 1. Verify the inner area is solid inner_color
            if not np.all(grid[inner_r_start : inner_r_end + 1, inner_c_start : inner_c_end + 1] == inner_color):
                is_valid = False
                continue # Not a solid inner block

            # 2. Verify the surrounding frame (1-pixel thick) is solid frame_color
            try:
                # Check Top frame row (r-1, c-1 to c+width)
                if not np.all(grid[inner_r_start - 1, inner_c_start - 1 : inner_c_end + 2] == frame_color):
                    is_valid = False
                # Check Bottom frame row (r+height, c-1 to c+width)
                elif not np.all(grid[inner_r_end + 1, inner_c_start - 1 : inner_c_end + 2] == frame_color):
                    is_valid = False
                # Check Left frame column (r to r+height-1, c-1)
                elif not np.all(grid[inner_r_start : inner_r_end + 1, inner_c_start - 1] == frame_color):
                    is_valid = False
                # Check Right frame column (r to r+height-1, c+width)
                elif not np.all(grid[inner_r_start : inner_r_end + 1, inner_c_end + 1] == frame_color):
                    is_valid = False
            except IndexError:
                # If any check goes out of bounds, it's not properly framed within the grid
                is_valid = False

            # If all checks passed, it's a valid framed rectangle
            if is_valid:
                # Add to list
                rectangles.append((inner_color, inner_r_start, inner_c_start))
                # Mark the entire area (inner block + frame) as visited
                # Frame rows: r-1 to r+height
                # Frame cols: c-1 to c+width
                visited[inner_r_start - 1 : inner_r_end + 2, inner_c_start - 1 : inner_c_end + 2] = True

    return rectangles


def transform(input_grid):
    """
    Transforms the input grid by finding framed rectangles, extracting their
    inner colors, and arranging them spatially in an output grid.
    """
    # Convert input list of lists to numpy array
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    
    # Handle trivial case: 1x1 input
    if rows <= 2 or cols <= 2:
        return [[0]] # Cannot contain a framed rectangle

    # Step 1: Identify the frame color
    frame_color = find_frame_color(grid_np)
    
    # If no plausible frame color identified, return default
    if frame_color == -1:
         print("Warning: Could not reliably determine frame color.")
         # Maybe return the input or a small default grid? Let's try default.
         return [[0]] 

    # Step 2 & 3: Find all framed rectangles using the identified frame color
    # and record their inner color and top-left inner coordinate.
    found_rectangles = find_framed_rectangles_with_color(grid_np, frame_color)

    # Handle case where no rectangles are found
    if not found_rectangles:
        return [[0]] # Return default if no framed rectangles matching the criteria exist

    # Step 4: Determine output dimensions and coordinate mapping
    # Collect unique row and column coordinates of the *inner* top-left corners
    rows_coords = sorted(list(set(r for _, r, _ in found_rectangles)))
    cols_coords = sorted(list(set(c for _, _, c in found_rectangles)))

    # Calculate output grid dimensions
    output_rows = len(rows_coords)
    output_cols = len(cols_coords)

    # Create mappings from actual grid coordinates to output grid indices
    row_map = {r: i for i, r in enumerate(rows_coords)}
    col_map = {c: i for i, c in enumerate(cols_coords)}

    # Step 5: Create the output grid, initialized with white (0)
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Step 6: Populate the output grid
    for inner_color, r, c in found_rectangles:
        # Find the corresponding output grid indices using the maps
        output_r = row_map[r]
        output_c = col_map[c]
        # Place the inner color at the calculated position
        output_grid[output_r, output_c] = inner_color

    # Step 7: Return the populated output grid as a list of lists
    return output_grid.tolist()
```