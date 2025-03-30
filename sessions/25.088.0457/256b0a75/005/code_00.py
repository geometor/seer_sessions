import numpy as np
from collections import defaultdict

"""
Transformation Rule:

1.  **Identify L-Shapes:** Scan the input grid to find all "L-shapes". An L-shape consists of exactly three pixels of the same non-white color (1-9) occupying three out of the four cells in any 2x2 square. Record the color and the set of three coordinate pairs for each distinct L-shape found.
2.  **Determine Fill Color:** Examine the identified L-shapes. Find the *single* L-shape whose color is *not* azure (color 8). The color of this L-shape is the "Fill Color". If no L-shapes are found, or if only azure L-shapes are found, return the original input grid unchanged.
3.  **Define Fill Region:** Collect the coordinates of all pixels belonging to *any* identified L-shape (both the non-azure one and all azure ones). Calculate the minimum bounding box (minimum row, maximum row, minimum column, maximum column) that encloses all these collected L-shape coordinates. This is the "L-shape Bounding Box". If no L-shapes were found (and thus no coordinates), the process stops (as per step 2).
4.  **Generate Output Grid:**
    a.  Create a copy of the input grid. This will be the output grid.
    b.  Iterate through every cell (row `r`, column `c`) located *within* the L-shape Bounding Box (inclusive).
    c.  For each cell `(r, c)` inside the box, check its color in the *original input grid*.
    d.  If the original color of cell `(r, c)` was white (0), change the color of this cell in the output grid to the determined Fill Color.
    e.  If the original color of cell `(r, c)` was *not* white (i.e., it was 1-9, whether part of an L-shape or not), leave its color unchanged in the output grid (it retains its original color).
    f.  All cells *outside* the L-shape Bounding Box remain unchanged from the input grid.
5.  Return the modified output grid.
"""

# ================= HELPER FUNCTIONS =================

def find_l_shapes(grid):
    """
    Finds all distinct L-shaped objects in the grid.

    An L-shape is defined as 3 pixels of the same non-white color
    occupying 3 cells of a 2x2 square.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple is (color, frozenset_of_coordinates).
              frozenset_of_coordinates contains (row, col) tuples for the 3 pixels
              of the L-shape. Returns an empty list if no L-shapes are found.
              Using frozenset allows adding to a set to find unique L-shapes.
    """
    potential_l_shapes = []
    rows, cols = grid.shape
    if rows < 2 or cols < 2:
        return [] # Cannot form 2x2 squares

    for r in range(rows - 1):
        for c in range(cols - 1):
            # Extract the 2x2 subgrid
            subgrid = grid[r:r+2, c:c+2]

            # Count colors in the 2x2 subgrid, excluding white (0)
            colors = defaultdict(list)
            white_count = 0
            for i in range(2):
                for j in range(2):
                    color = subgrid[i, j]
                    coord = (r + i, c + j)
                    if color == 0:
                        white_count += 1
                    else:
                        colors[color].append(coord)

            # Check for the L-shape condition: 1 white pixel and 3 pixels of the same non-white color
            if white_count == 1:
                for color, coords in colors.items():
                    if len(coords) == 3:
                        # Use frozenset for hashability needed for set operations
                        potential_l_shapes.append((int(color), frozenset(coords)))
                        break # Only one L-shape per 2x2 possible

    # Remove duplicate L-shapes (same color and same set of coordinates)
    unique_l_shapes = list(set(potential_l_shapes))
    # Convert frozenset back to set for consistency if needed later, though not strictly necessary
    # result = [(color, set(coords)) for color, coords in unique_l_shapes]
    return unique_l_shapes # Return with frozensets

def find_coords_bounding_box(coords_set):
    """
    Finds the minimum bounding box enclosing a set of coordinates.

    Args:
        coords_set (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_r, max_r, min_c, max_c) defining the box,
               or None if the set is empty. Returns ints.
    """
    if not coords_set:
        return None
    min_r = min(r for r, c in coords_set)
    max_r = max(r for r, c in coords_set)
    min_c = min(c for r, c in coords_set)
    max_c = max(c for r, c in coords_set)
    return int(min_r), int(max_r), int(min_c), int(max_c)

# ================= MAIN TRANSFORM FUNCTION =================

def transform(input_grid):
    """
    Applies the L-shape based filling transformation within the bounding box
    defined by all L-shapes, preserving original non-white pixels.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    # Convert input to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy() # Start with a copy

    # 1. Identify all L-shapes
    all_l_shapes = find_l_shapes(grid_np)

    # If no L-shapes found, return original grid
    if not all_l_shapes:
        return input_grid

    # 2. Determine Fill Color
    fill_color = -1 # Default invalid color
    non_azure_l_shape_found = False
    for color, coords in all_l_shapes:
        if color != 8: # Not azure
            fill_color = color
            non_azure_l_shape_found = True
            break # Assuming only one non-azure L-shape exists

    # If no non-azure L-shape was found, return original grid
    if not non_azure_l_shape_found:
        return input_grid

    # 3. Define Fill Region (bounding box of *all* L-shape pixels)
    all_l_shape_pixels = set().union(*(coords for _, coords in all_l_shapes))
    l_shape_bounding_box = find_coords_bounding_box(all_l_shape_pixels)

    # This check should be redundant because we know L-shapes exist if we got here
    # but good practice to include it.
    if l_shape_bounding_box is None:
         return input_grid # Should not happen if all_l_shapes is not empty

    min_r, max_r, min_c, max_c = l_shape_bounding_box

    # 4. Generate the Output Grid
    # Iterate through each cell within the L-shape bounding box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # Check the color in the *original* input grid
            if grid_np[r, c] == 0:
                # If it was white, change it to the fill color in the output
                output_grid[r, c] = fill_color
            # Else (if original was non-white), leave it as is (already copied)

    # Convert back to list of lists for the required output format
    return output_grid.tolist()