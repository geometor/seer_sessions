import numpy as np
try:
    # skimage is used for finding connected components (objects)
    # If running locally, ensure scikit-image is installed: pip install scikit-image
    from skimage import measure
    SKIMAGE_AVAILABLE = True
except ImportError:
    # Fallback if skimage is not available
    SKIMAGE_AVAILABLE = False
    print("Warning: scikit-image not found. Object detection will be limited.")
    # NOTE: A manual implementation of connected components (e.g., BFS/DFS)
    # would be needed here for a complete fallback. For now, we proceed
    # assuming skimage is available, as it's crucial for the logic.


"""
Transformation Rule Description:

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct red (2) objects and blue (1) objects in the input grid, considering pixels connected 8-directionally (including diagonals) as part of the same object. Store the coordinates of all pixels belonging to blue objects.
3.  Determine which red objects are "isolated". A red object is isolated if none of its pixels are adjacent (8-directionally) to any pixel belonging to any *original* blue object.
4.  Create a list of the isolated red objects and sort them based on their top-left corner coordinates (first by row, then by column). Keep track of which isolated objects have been processed.
5.  Iterate through the sorted list of isolated red objects to find and process specific pairs:
    *   **Vertical 1x1 Pair:** Search for two *unprocessed* isolated red objects where both are single pixels (1x1), have the same column index `c`, and their row indices `r1`, `r2` satisfy `r2 = r1 + 3`. If found:
        *   Draw a blue 'T' shape immediately below the first pixel: a horizontal 3-pixel bar at `r1+1` (cols `c-1` to `c+1`) and a vertical 1-pixel stem at `(r1+2, c)`.
        *   Draw an identical blue 'T' shape relative to the second pixel (rows `r2+1`, `r2+2`).
        *   Mark both red objects as processed.
    *   **Horizontal 2x2 Pair:** Search for two *unprocessed* isolated red objects where both are 2x2 squares, located on the same rows `r` and `r+1`, with the second square starting at a column `c2` that is at least 2 columns to the right of the first square's starting column `c1` (i.e., `c2 > c1+1`). Let the first square span columns `c1` to `c1+1` and the second span `c2` to `c2+1`. If found:
        *   Draw a blue connector rectangle of size 2xN between the squares: rows `r` to `r+1`, columns `c1+2` to `c2-1`.
        *   Draw a blue 2x2 square centered horizontally below the connector rectangle, starting at row `r+2`.
        *   Draw a blue bottom rectangle of size 2xM below the square structure: rows `r+4` to `r+5`, columns `c1+2` to `c2+1`.
        *   Mark both red objects as processed.
6.  Iterate through the list of isolated red objects again. For any isolated red object that is still *unprocessed*:
    *   Find its bounding box `(r1, c1, r2, c2)`.
    *   If its minimum column `c1` is greater than 0, draw a blue rectangle covering all cells from row `r1` to `r2` and column `0` to `c1-1`.
7.  Return the modified output grid.
"""

# --- Helper Functions ---

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color using skimage.measure.label.
    Connectivity is 8-way (including diagonals).
    Returns a list of sets, where each set contains the (row, col) coordinates of an object.
    Returns an empty list if skimage is not available or no objects are found.
    """
    if not SKIMAGE_AVAILABLE:
        # Cannot find objects without skimage or a manual implementation
        return []
    objects = []
    mask = (grid == color)
    # connectivity=2 means 8-way connection (includes diagonals)
    labeled_grid, num_labels = measure.label(mask, connectivity=2, background=0, return_num=True)
    for i in range(1, num_labels + 1):
        coords = np.argwhere(labeled_grid == i)
        # Convert to set of tuples for easier handling and lookup
        objects.append(set(tuple(coord) for coord in coords))
    return objects

def get_bounding_box(obj_coords):
    """
    Calculates the inclusive bounding box (min_row, min_col, max_row, max_col)
    for a set of object coordinates.
    Returns None if the object coordinates set is empty.
    """
    if not obj_coords:
        return None
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    return min(rows), min(cols), max(rows), max(cols)

def get_shape_size(obj_coords):
    """
    Gets the size (height, width) of an object based on its bounding box.
    Returns (0, 0) if the object coordinates set is empty.
    """
    bbox = get_bounding_box(obj_coords)
    if not bbox:
        return 0, 0
    r1, c1, r2, c2 = bbox
    return r2 - r1 + 1, c2 - c1 + 1

def is_isolated(grid, red_obj_coords, blue_coords_flat):
    """
    Checks if a red object (given by its coordinates) is isolated, meaning
    none of its pixels are adjacent (8-way) to any blue pixel coordinates
    provided in blue_coords_flat.
    """
    height, width = grid.shape
    for r, c in red_obj_coords:
        # Check all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip the pixel itself
                nr, nc = r + dr, c + dc
                # Check if neighbor is within grid bounds
                if 0 <= nr < height and 0 <= nc < width:
                    # Check if the neighbor is a blue pixel
                    if (nr, nc) in blue_coords_flat:
                        return False # Found adjacent blue pixel, so not isolated
    return True # No adjacent blue pixels found

def draw_pixels(grid, coords_to_draw, color):
    """
    Draws pixels onto the grid at the specified coordinates with the given color.
    Checks boundaries to avoid errors.
    """
    height, width = grid.shape
    for r, c in coords_to_draw:
        # Ensure coordinates are within the grid boundaries
        if 0 <= r < height and 0 <= c < width:
            grid[r, c] = color

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule to the input grid based on isolated red objects.
    """
    # 1. Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    blue_color = 1 # Define color constants
    red_color = 2

    # 2. Identify all red and blue objects
    red_objects = find_objects(input_grid, red_color)
    blue_objects = find_objects(input_grid, blue_color)

    # Create a flat set of all blue coordinates for efficient adjacency checking
    blue_coords_flat = set()
    for b_obj in blue_objects:
        blue_coords_flat.update(b_obj)

    # 3. Determine which red objects are isolated
    isolated_red_objects_data = []
    for r_obj_coords in red_objects:
        if is_isolated(input_grid, r_obj_coords, blue_coords_flat):
            bbox = get_bounding_box(r_obj_coords)
            if bbox: # Ensure object is valid
                 isolated_red_objects_data.append({
                    "coords": r_obj_coords,
                    "bbox": bbox,
                    "shape_size": get_shape_size(r_obj_coords)
                })

    # 4. Sort isolated red objects by top-left corner (row, then column)
    isolated_red_objects_data.sort(key=lambda x: (x["bbox"][0], x["bbox"][1]))

    # Keep track of processed objects (by index in the sorted list)
    processed_indices = set()
    num_isolated = len(isolated_red_objects_data)

    # 5. Process pairs first
    # 5a. Process Vertical 1x1 Pairs
    for i in range(num_isolated):
        if i in processed_indices:
            continue
        obj1 = isolated_red_objects_data[i]
        # Check if it's a 1x1 pixel
        if obj1["shape_size"] == (1, 1):
            r1, c1, _, _ = obj1["bbox"]
            # Search for a potential pair starting from the next object
            for j in range(i + 1, num_isolated):
                if j in processed_indices:
                    continue
                obj2 = isolated_red_objects_data[j]
                if obj2["shape_size"] == (1, 1):
                    r2, c2, _, _ = obj2["bbox"]
                    # Check for vertical alignment (same column, 3 rows apart)
                    if c1 == c2 and r2 == r1 + 3:
                        # Found a vertical 1x1 pair
                        processed_indices.add(i)
                        processed_indices.add(j)

                        # Draw T-shape below obj1
                        t1_coords = set()
                        # Horizontal bar: (r1+1, c1-1), (r1+1, c1), (r1+1, c1+1)
                        # Vertical stem: (r1+2, c1)
                        t1_coords.add((r1 + 1, c1 - 1))
                        t1_coords.add((r1 + 1, c1))
                        t1_coords.add((r1 + 1, c1 + 1))
                        t1_coords.add((r1 + 2, c1))
                        draw_pixels(output_grid, t1_coords, blue_color)

                        # Draw T-shape below obj2
                        t2_coords = set()
                        # Horizontal bar: (r2+1, c2-1), (r2+1, c2), (r2+1, c2+1) -> (r1+4, c1-1), (r1+4, c1), (r1+4, c1+1)
                        # Vertical stem: (r2+2, c2) -> (r1+5, c1)
                        t2_coords.add((r1 + 4, c1 - 1))
                        t2_coords.add((r1 + 4, c1))
                        t2_coords.add((r1 + 4, c1 + 1))
                        t2_coords.add((r1 + 5, c1))
                        draw_pixels(output_grid, t2_coords, blue_color)

                        # Break inner loop once obj1 is paired
                        break

    # 5b. Process Horizontal 2x2 Pairs
    for i in range(num_isolated):
        if i in processed_indices:
            continue
        obj1 = isolated_red_objects_data[i]
        # Check if it's a 2x2 square
        if obj1["shape_size"] == (2, 2):
            r1_start, c1_start, r1_end, c1_end = obj1["bbox"] # r1_end=r1_start+1, c1_end=c1_start+1
            # Search for a potential pair starting from the next object
            for j in range(i + 1, num_isolated):
                if j in processed_indices:
                    continue
                obj2 = isolated_red_objects_data[j]
                if obj2["shape_size"] == (2, 2):
                    r2_start, c2_start, r2_end, c2_end = obj2["bbox"] # r2_end=r2_start+1, c2_end=c2_start+1
                    # Check for horizontal alignment (same rows, obj2 is to the right with a gap)
                    if r1_start == r2_start and c2_start > c1_end + 1: # c2_start must be at least c1_start+2+1 = c1_end+2
                         # Found a horizontal 2x2 pair
                        processed_indices.add(i)
                        processed_indices.add(j)

                        # i. Draw connector rectangle (rows r1_start to r1_end, cols c1_end+1 to c2_start-1)
                        connector_coords = set()
                        for r in range(r1_start, r1_end + 1):
                            for c in range(c1_end + 1, c2_start):
                                connector_coords.add((r, c))
                        draw_pixels(output_grid, connector_coords, blue_color)

                        # ii. Draw 2x2 square below connector
                        conn_col_start = c1_end + 1
                        conn_col_end = c2_start - 1
                        conn_width = conn_col_end - conn_col_start + 1
                        # Ensure width > 0 before centering (should be guaranteed by c2_start > c1_end + 1)
                        if conn_width > 0:
                            # Calculate top-left corner of the 2x2 square
                            # Center col index within connector is roughly conn_col_start + conn_width / 2
                            # For a 2x2 square, we want its left column `square_start_col` such that
                            # `square_start_col` and `square_start_col+1` are centered.
                            # Midpoint of connector: conn_col_start + (conn_width - 1) / 2
                            # Start col for 2x2: floor(Midpoint - 0.5) = floor(conn_col_start + conn_width/2 - 1/2 - 0.5) = floor(conn_col_start + conn_width/2 - 1)
                            # Example: cols 5-8 (width 4). Mid = 5 + 1.5 = 6.5. square_start = floor(6.5 - 0.5) = 6. Correct.
                            # Example: cols 5-9 (width 5). Mid = 5 + 2 = 7. square_start = floor(7 - 0.5) = 6. Square at 6,7. Centered? Yes.
                            # simpler: conn_col_start + (conn_width // 2) - 1
                            square_start_col = conn_col_start + (conn_width // 2) -1
                            square_start_row = r1_start + 2
                            square_coords = set()
                            for r in range(square_start_row, square_start_row + 2):
                                for c in range(square_start_col, square_start_col + 2):
                                     square_coords.add((r,c))
                            draw_pixels(output_grid, square_coords, blue_color)

                        # iii. Draw bottom rectangle below square structure
                        # Rows r1_start+4 to r1_start+5 (height 2)
                        # Cols c1_end+1 to c2_end (c1_start+1+1 to c2_start+1 -> c1_start+2 to c2_start+1)
                        # Example 2: c1=3, c2=9. c1_end=4, c2_end=10. Cols 5 to 10. Correct.
                        bottom_rect_start_row = r1_start + 4
                        bottom_rect_coords = set()
                        for r in range(bottom_rect_start_row, bottom_rect_start_row + 2):
                             for c in range(c1_end + 1, c2_end + 1):
                                bottom_rect_coords.add((r,c))
                        draw_pixels(output_grid, bottom_rect_coords, blue_color)

                        # Break inner loop once obj1 is paired
                        break

    # 6. Process Single Isolated Objects (those not part of pairs)
    for i in range(num_isolated):
        if i in processed_indices:
            continue # Skip objects already processed as part of a pair

        obj = isolated_red_objects_data[i]
        r1, c1, r2, c2 = obj["bbox"]

        # Draw blue rectangle to the left of the object's bounding box
        left_rect_coords = set()
        if c1 > 0: # Only draw if there's space to the left (column index > 0)
            for r in range(r1, r2 + 1): # Iterate through rows of the bounding box
                for c in range(0, c1):   # Iterate through columns from 0 up to (but not including) c1
                    left_rect_coords.add((r, c))
            draw_pixels(output_grid, left_rect_coords, blue_color)

        # Mark as processed (technically redundant here, but good practice)
        processed_indices.add(i)

    # 7. Return the final modified grid
    return output_grid