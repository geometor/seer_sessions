```python
import numpy as np
from collections import defaultdict

"""
Transformation Rule:

1.  **Identify all L-shapes:** Scan the input grid for any L-shapes. An L-shape consists of exactly three pixels of the same non-white color (colors 1 through 9) that occupy three out of four cells in any 2x2 square. Record the color and the set of coordinates for each L-shape found.
2.  **Determine the Fill Color:** Examine the identified L-shapes. Find the L-shape(s) whose color is *not* azure (color 8). The color of this non-azure L-shape is the "Fill Color". (Based on the examples, there appears to be only one such non-azure color present per grid). If no non-azure L-shapes are found, return the original grid.
3.  **Collect all L-shape Pixel Coordinates:** Create a single set containing the coordinates of all pixels that are part of *any* identified L-shape (both azure and non-azure). These pixels will be preserved.
4.  **Calculate the Global Bounding Box:** Find the minimum and maximum row and column indices occupied by *any* non-white pixel (colors 1 through 9) in the input grid. This defines the rectangular region for the filling operation. If no non-white pixels exist, return the original grid.
5.  **Generate the Output Grid:**
    a.  Start with a copy of the input grid.
    b.  Iterate through every cell (row `r`, column `c`) within the Global Bounding Box (from `min_row` to `max_row`, and `min_col` to `max_col`, inclusive).
    c.  For each cell `(r, c)`, check if its coordinates are present in the set of collected L-shape pixel coordinates.
    d.  If the coordinates `(r, c)` are *not* in the L-shape coordinates set, change the color of this cell in the output grid to the determined Fill Color.
    e.  If the coordinates `(r, c)` *are* in the L-shape coordinates set, leave the cell's color unchanged (it keeps its original L-shape color).
    f.  All cells outside the Global Bounding Box remain unchanged from the input grid.
6.  Return the modified grid.
"""

def find_l_shapes(grid):
    """
    Finds all L-shaped objects in the grid.

    An L-shape is defined as 3 pixels of the same non-white color
    occupying 3 cells of a 2x2 square.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple is (color, set_of_coordinates).
              set_of_coordinates contains (row, col) tuples for the 3 pixels
              of the L-shape. Returns an empty list if no L-shapes are found.
    """
    l_shapes = []
    rows, cols = grid.shape
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
                        l_shapes.append((int(color), set(coords))) # Ensure color is python int
                        # Assuming a 2x2 can only contain one L-shape, break inner loop
                        break

    return l_shapes

def find_non_white_bounding_box(grid):
    """
    Finds the minimum bounding box enclosing all non-white pixels.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (min_r, max_r, min_c, max_c) defining the box,
               or None if no non-white pixels are found.
    """
    non_white_coords = np.argwhere(grid != 0)
    if non_white_coords.size == 0:
        return None # No non-white pixels
    min_r = int(np.min(non_white_coords[:, 0]))
    max_r = int(np.max(non_white_coords[:, 0]))
    min_c = int(np.min(non_white_coords[:, 1]))
    max_c = int(np.max(non_white_coords[:, 1]))
    return min_r, max_r, min_c, max_c


def transform(input_grid):
    """
    Applies the L-shape based filling transformation within the global bounds of non-white pixels.

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

    # If no L-shapes, the transformation might not be defined?
    # For now, let's return the original grid if no L-shapes are found.
    # Or maybe only proceed if a non-azure L-shape is found. Let's check that first.

    # 2. Determine Fill Color and collect non-azure shapes
    non_azure_l_shapes = []
    fill_color = -1 # Default invalid color
    l_shape_pixels = set() # Collect coordinates of all pixels part of *any* L-shape

    for color, coords in all_l_shapes:
        l_shape_pixels.update(coords) # Add coordinates to the master set
        if color != 8: # Not azure
            non_azure_l_shapes.append((color, coords))

    # Determine fill color from the first non-azure L-shape found
    if non_azure_l_shapes:
        fill_color = non_azure_l_shapes[0][0]
    else:
        # No non-azure L-shape found to determine fill color.
        # According to the rule, we should return the original grid.
        return input_grid

    # 3. L-shape pixel coordinates already collected in l_shape_pixels

    # 4. Calculate the Global Bounding Box of non-white pixels
    bounding_box = find_non_white_bounding_box(grid_np)

    # If no non-white pixels exist, return the original grid
    if bounding_box is None:
        return input_grid

    min_r, max_r, min_c, max_c = bounding_box

    # 5. Generate the Output Grid by filling within the bounding box
    # Iterate through each cell within the global bounding box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # Check if the current pixel is NOT part of any L-shape
            if (r, c) not in l_shape_pixels:
                # If not part of an L-shape, fill it with the fill color
                output_grid[r, c] = fill_color
            # Else: Pixel is part of an L-shape, leave its original color (already copied)

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```