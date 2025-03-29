import numpy as np
from collections import defaultdict

"""
Identify all distinct rectangular regions within the input grid where a solid block 
of one color (inner color) is completely enclosed by a one-pixel-thick frame of 
a different, uniform color (frame color). Determine the relative grid layout 
(rows and columns) formed by these framed rectangles based on their top-left 
corner positions. Create an output grid with dimensions matching this layout. 
Populate the output grid cells with the inner colors of the identified rectangles, 
maintaining their relative spatial arrangement.
"""

def find_framed_rectangles(grid):
    """
    Finds all framed rectangles in the grid.

    A framed rectangle is defined as a solid rectangular block of an inner color
    completely surrounded by a 1-pixel thick frame of a different, uniform frame color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple contains:
              (inner_color, top_row, left_col)
              representing the inner color and the top-left coordinates 
              of the inner rectangle. Returns an empty list if no such
              rectangles are found.
    """
    rectangles = []
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(rows - 2):
        for c in range(cols - 2):
            if visited[r, c]:
                continue

            frame_color = grid[r, c]
            potential_inner_color = grid[r+1, c+1]

            # Basic check: frame and inner must be different, and potential frame corners must match
            if frame_color == potential_inner_color:
                continue
            if grid[r+1, c] != frame_color or grid[r, c+1] != frame_color:
                 continue


            # Find the potential extent of the inner rectangle
            inner_r, inner_c = r + 1, c + 1
            height = 0
            width = 0

            # Find height
            for h in range(inner_r, rows -1):
                 # Check left frame pixel and first inner pixel
                if grid[h, inner_c -1] == frame_color and grid[h, inner_c] == potential_inner_color:
                    height += 1
                else:
                    break # Stop if left frame or inner color breaks pattern

            # Find width
            for w in range(inner_c, cols -1):
                 # Check top frame pixel and first inner pixel
                if grid[inner_r -1, w] == frame_color and grid[inner_r, w] == potential_inner_color:
                    width += 1
                else:
                    break # Stop if top frame or inner color breaks pattern
            
            if height == 0 or width == 0:
                continue # Not a valid rectangle start


            bottom_r = inner_r + height - 1
            right_c = inner_c + width - 1
            
            # --- Verification ---
            
            # 1. Check if the inner area is solid potential_inner_color
            inner_area = grid[inner_r : bottom_r + 1, inner_c : right_c + 1]
            if not np.all(inner_area == potential_inner_color):
                continue

            # 2. Check the surrounding frame
            is_framed = True
            # Top row frame check
            if not np.all(grid[inner_r - 1, inner_c -1 : right_c + 2] == frame_color):
                 is_framed = False
            # Bottom row frame check
            if not np.all(grid[bottom_r + 1, inner_c -1 : right_c + 2] == frame_color):
                 is_framed = False
            # Left column frame check
            if not np.all(grid[inner_r : bottom_r + 1, inner_c - 1] == frame_color):
                is_framed = False
            # Right column frame check
            if not np.all(grid[inner_r : bottom_r + 1, right_c + 1] == frame_color):
                 is_framed = False
                 
            if is_framed:
                rectangles.append((potential_inner_color, inner_r, inner_c))
                # Mark the entire framed rectangle area (including frame) as visited
                visited[inner_r - 1 : bottom_r + 2, inner_c - 1 : right_c + 2] = True
                
    return rectangles


def transform(input_grid):
    """
    Identifies framed rectangles in the input grid, determines their relative
    layout, and creates an output grid containing their inner colors arranged
    according to that layout.
    """
    
    # 1. Find all framed rectangles and their inner colors/positions
    #    Each element is (inner_color, top_row, left_col)
    found_rectangles = find_framed_rectangles(np.array(input_grid))

    if not found_rectangles:
        # Handle cases where no rectangles are found if necessary
        # Depending on task specifics, might return empty grid, error, etc.
        # For now, assume at least one rectangle will be found based on examples.
        # Let's return a 1x1 grid with 0 if none are found to avoid errors.
         return np.array([[0]], dtype=int)


    # 2. Determine the grid layout based on unique row and column coordinates
    rows_coords = sorted(list(set(r for _, r, _ in found_rectangles)))
    cols_coords = sorted(list(set(c for _, _, c in found_rectangles)))
    
    output_rows = len(rows_coords)
    output_cols = len(cols_coords)

    # Create mappings from actual coordinates to output grid indices
    row_map = {r: i for i, r in enumerate(rows_coords)}
    col_map = {c: j for i, c in enumerate(cols_coords)}

    # 3. Initialize the output grid
    output_grid = np.zeros((output_rows, output_cols), dtype=int) # Use 0 (white) as default/background

    # 4. Populate the output grid
    for inner_color, r, c in found_rectangles:
        output_r = row_map[r]
        output_c = col_map[c]
        output_grid[output_r, output_c] = inner_color

    return output_grid.tolist() # Return as list of lists per ARC format