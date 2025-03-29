```python
import numpy as np
from skimage import measure

"""
Transformation Rule Description:

1.  Identify all red (2) and blue (1) objects in the input grid.
2.  Determine which red objects are "isolated," meaning they are not adjacent (including diagonally) to any blue pixels from the *original* input grid.
3.  Copy the input grid to the output grid.
4.  Process the isolated red objects based on specific pairing configurations or as individuals:
    a.  **Vertical 1x1 Pair:** If two isolated 1x1 red pixels are found at `(r, c)` and `(r+3, c)`, draw a blue 'T' shape below each. The 'T' consists of a horizontal bar at row `y+1`, columns `c-1` to `c+1`, and a vertical stem at row `y+2`, column `c` (where `y` is the row of the red pixel). Mark these red objects as processed.
    b.  **Horizontal 2x2 Pair:** If two isolated 2x2 red squares are found starting at `(r, c)` and `(r, c')` (where `c' > c+1`), draw several blue shapes:
        i.  A connector rectangle from `(r, c+2)` to `(r+1, c'-1)`.
        ii. A 2x2 blue square centered horizontally below the connector, starting at row `r+2`. Let the connector span columns `col_start = c+2` to `col_end = c'-1`. The center column index needs calculation. If width `w = col_end - col_start + 1`, the center start col is `floor(col_start + w/2 - 1)`. The square is at `(r+2, center_start_col)` to `(r+3, center_start_col+1)`. Let's re-examine example 2: Connector cols 5-8 (width 4). Square cols 6-7. `5 + 4/2 - 1 = 6`. Correct.
        iii. A rectangle below the square, from `(r+4, c+2)` to `(r+5, c')`. Mark these red objects as processed.
    c.  **Single Isolated Object:** If an isolated red object was not part of a pair, find its bounding box `(r1, c1, r2, c2)` (inclusive rows/cols). Draw a blue rectangle from `(r1, 0)` to `(r2, c1-1)`. Mark this object as processed.
5.  Return the modified output grid. All original objects (red and blue) remain in the output.
"""

def find_objects(grid, color):
    """Finds all connected objects of a specific color."""
    objects = []
    mask = (grid == color)
    labeled_grid, num_labels = measure.label(mask, connectivity=2, background=0, return_num=True) # connectivity=2 means 8-way connection
    for i in range(1, num_labels + 1):
        coords = np.argwhere(labeled_grid == i)
        # Convert to set of tuples for easier handling
        objects.append(set(tuple(coord) for coord in coords))
    return objects

def get_bounding_box(obj_coords):
    """Calculates the inclusive bounding box of an object."""
    if not obj_coords:
        return None
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    return min(rows), min(cols), max(rows), max(cols)

def get_shape_size(obj_coords):
    """Gets the size (height, width) from the bounding box."""
    bbox = get_bounding_box(obj_coords)
    if not bbox:
        return 0, 0
    r1, c1, r2, c2 = bbox
    return r2 - r1 + 1, c2 - c1 + 1

def is_isolated(grid, red_obj_coords, blue_objects_coords_flat):
    """Checks if a red object is isolated from all blue objects."""
    height, width = grid.shape
    for r, c in red_obj_coords:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < height and 0 <= nc < width:
                    if (nr, nc) in blue_objects_coords_flat:
                        return False # Found adjacent blue pixel
    return True # No adjacent blue pixels found

def draw_pixels(grid, coords_to_draw, color):
    """Draws pixels on the grid, respecting boundaries."""
    height, width = grid.shape
    for r, c in coords_to_draw:
        if 0 <= r < height and 0 <= c < width:
            grid[r, c] = color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Find all red and blue objects
    red_objects = find_objects(input_grid, 2)
    blue_objects = find_objects(input_grid, 1)

    # Create a flat set of all blue coordinates for efficient adjacency checking
    blue_coords_flat = set()
    for b_obj in blue_objects:
        blue_coords_flat.update(b_obj)

    # 2. Identify isolated red objects
    isolated_red_objects = []
    for r_obj_coords in red_objects:
        if is_isolated(input_grid, r_obj_coords, blue_coords_flat):
            isolated_red_objects.append({
                "coords": r_obj_coords,
                "bbox": get_bounding_box(r_obj_coords),
                "shape_size": get_shape_size(r_obj_coords)
            })

    # Sort isolated objects by top-left corner (row, then column) for consistent pairing
    isolated_red_objects.sort(key=lambda x: (x["bbox"][0], x["bbox"][1]))

    processed_indices = set()
    num_isolated = len(isolated_red_objects)
    blue_color = 1

    # 4a. Process Vertical 1x1 Pairs
    for i in range(num_isolated):
        if i in processed_indices:
            continue
        obj1 = isolated_red_objects[i]
        # Check if it's a 1x1 pixel
        if obj1["shape_size"] == (1, 1):
            r1, c1, _, _ = obj1["bbox"]
            for j in range(i + 1, num_isolated):
                if j in processed_indices:
                    continue
                obj2 = isolated_red_objects[j]
                if obj2["shape_size"] == (1, 1):
                    r2, c2, _, _ = obj2["bbox"]
                    # Check for vertical alignment (same column, 3 rows apart)
                    if c1 == c2 and r2 == r1 + 3:
                        # Found a pair
                        processed_indices.add(i)
                        processed_indices.add(j)

                        # Draw T-shape below obj1
                        t1_coords = set()
                        t1_coords.add((r1 + 1, c1 - 1))
                        t1_coords.add((r1 + 1, c1))
                        t1_coords.add((r1 + 1, c1 + 1))
                        t1_coords.add((r1 + 2, c1))
                        draw_pixels(output_grid, t1_coords, blue_color)

                        # Draw T-shape below obj2
                        t2_coords = set()
                        t2_coords.add((r2 + 1, c2 - 1))
                        t2_coords.add((r2 + 1, c2))
                        t2_coords.add((r2 + 1, c2 + 1))
                        t2_coords.add((r2 + 2, c2))
                        draw_pixels(output_grid, t2_coords, blue_color)
                        break # obj1 is paired, move to the next i

    # 4b. Process Horizontal 2x2 Pairs
    for i in range(num_isolated):
        if i in processed_indices:
            continue
        obj1 = isolated_red_objects[i]
        # Check if it's a 2x2 square
        if obj1["shape_size"] == (2, 2):
            r1_start, c1_start, r1_end, c1_end = obj1["bbox"]
            for j in range(i + 1, num_isolated):
                if j in processed_indices:
                    continue
                obj2 = isolated_red_objects[j]
                if obj2["shape_size"] == (2, 2):
                    r2_start, c2_start, r2_end, c2_end = obj2["bbox"]
                    # Check for horizontal alignment (same rows, obj2 is to the right)
                    if r1_start == r2_start and r1_end == r2_end and c2_start > c1_end:
                         # Found a pair
                        processed_indices.add(i)
                        processed_indices.add(j)

                        # i. Draw connector rectangle
                        connector_coords = set()
                        for r in range(r1_start, r1_end + 1):
                            for c in range(c1_end + 1, c2_start):
                                connector_coords.add((r, c))
                        draw_pixels(output_grid, connector_coords, blue_color)

                        # ii. Draw 2x2 square below connector
                        conn_col_start = c1_end + 1
                        conn_col_end = c2_start - 1
                        conn_width = conn_col_end - conn_col_start + 1
                        # Ensure width > 0 before centering
                        if conn_width > 0:
                            square_start_col = conn_col_start + conn_width // 2 -1 # Center calculation
                            square_coords = set()
                            for r in range(r1_start + 2, r1_start + 4):
                                for c in range(square_start_col, square_start_col + 2):
                                     square_coords.add((r,c))
                            draw_pixels(output_grid, square_coords, blue_color)

                        # iii. Draw rectangle below square (Matches example 2 output)
                        # Width seems to span from connector start col to obj2 end col
                        # Example 2: Conn cols 5-8. Obj2 cols 9-10. Bottom Rect cols 5-10.
                        # So cols c1_end + 1 to c2_end.
                        bottom_rect_coords = set()
                        for r in range(r1_start + 4, r1_start + 6):
                             for c in range(c1_end + 1, c2_end + 1):
                                bottom_rect_coords.add((r,c))
                        draw_pixels(output_grid, bottom_rect_coords, blue_color)

                        break # obj1 is paired, move to the next i

    # 4c. Process Single Isolated Objects
    for i in range(num_isolated):
        if i in processed_indices:
            continue
        obj = isolated_red_objects[i]
        r1, c1, r2, c2 = obj["bbox"]

        # Draw rectangle to the left
        left_rect_coords = set()
        if c1 > 0: # Only draw if there's space to the left
            for r in range(r1, r2 + 1):
                for c in range(0, c1):
                    left_rect_coords.add((r, c))
            draw_pixels(output_grid, left_rect_coords, blue_color)

        # Mark as processed (though not strictly necessary in this final loop)
        processed_indices.add(i)

    return output_grid
```