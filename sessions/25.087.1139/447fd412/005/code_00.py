import numpy as np
import math

try:
    # skimage is used for finding connected components (objects)
    from skimage import measure
    SKIMAGE_AVAILABLE = True
except ImportError:
    # Fallback if skimage is not available
    SKIMAGE_AVAILABLE = False
    # Basic BFS implementation for connected components as a fallback
    def bfs_find_objects(grid, color, connectivity=8):
        """
        Finds connected objects of a specific color using Breadth-First Search.
        connectivity=8 means 8-way connection (includes diagonals).
        Returns a list of sets, where each set contains the (row, col) coordinates of an object.
        """
        objects = []
        height, width = grid.shape
        visited = np.zeros((height, width), dtype=bool)
        
        for r in range(height):
            for c in range(width):
                if grid[r, c] == color and not visited[r, c]:
                    obj_coords = set()
                    q = [(r, c)]
                    visited[r, c] = True
                    obj_coords.add((r, c))
                    
                    while q:
                        row, col = q.pop(0)
                        
                        # Define neighbors based on connectivity
                        if connectivity == 8:
                            neighbor_deltas = [(-1, -1), (-1, 0), (-1, 1),
                                               (0, -1),          (0, 1),
                                               (1, -1), (1, 0), (1, 1)]
                        else: # connectivity = 4 (default)
                             neighbor_deltas = [(-1, 0), (0, -1), (0, 1), (1, 0)]

                        for dr, dc in neighbor_deltas:
                            nr, nc = row + dr, col + dc
                            
                            # Check bounds, color, and visited status
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                obj_coords.add((nr, nc))
                                
                    if obj_coords:
                        objects.append(obj_coords)
        return objects
    
# --- Helper Functions ---

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color. Uses skimage if available,
    otherwise uses a basic BFS implementation.
    Connectivity is 8-way (including diagonals).
    Returns a list of sets, where each set contains the (row, col) coordinates of an object.
    """
    if SKIMAGE_AVAILABLE:
        objects = []
        mask = (grid == color)
        # connectivity=2 means 8-way connection (includes diagonals)
        labeled_grid, num_labels = measure.label(mask, connectivity=2, background=0, return_num=True)
        for i in range(1, num_labels + 1):
            coords = np.argwhere(labeled_grid == i)
            # Convert to set of tuples for easier handling and lookup
            objects.append(set(tuple(coord) for coord in coords))
        return objects
    else:
        # Use BFS fallback if skimage is not present
        # print("Warning: scikit-image not found. Using BFS for object detection.") # Optional warning
        return bfs_find_objects(grid, color, connectivity=8)


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

def get_neighbors(r, c, shape):
    """ Gets 8-way neighbors for a coordinate within grid shape. """
    neighbors = set()
    h, w = shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue # Skip self
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w: # Check bounds
                neighbors.add((nr, nc))
    return neighbors

def is_isolated(grid, red_obj_coords, blue_coords_flat):
    """
    Checks if a red object (given by its coordinates) is isolated, meaning
    none of its pixels are adjacent (8-way) to any blue pixel coordinates
    provided in blue_coords_flat.
    """
    grid_shape = grid.shape
    for r, c in red_obj_coords:
        # Check all 8 neighbors of the current red pixel
        pixel_neighbors = get_neighbors(r, c, grid_shape)
        # Check if any neighbor coordinate is in the set of blue coordinates
        if not pixel_neighbors.isdisjoint(blue_coords_flat):
            return False # Found adjacent blue pixel, so not isolated
    return True # No adjacent blue pixels found for any pixel in the red object

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
    Transformation Rule:
    1. Identify red (2) objects and blue (1) pixels in the input.
    2. Filter red objects to find 'isolated' ones (not 8-way adjacent to any input blue pixel).
    3. Sort isolated red objects by top-left corner (row, then column).
    4. Process specific pairs of isolated red objects first:
        a. Vertical Pair (1x1 pixels, same column 'c', rows 'r1' and 'r1+3'):
           Draw two blue T-shapes below each pixel.
        b. Horizontal Pair (2x2 squares, same rows 'r, r+1', columns 'c1' and 'c2' with c2 > c1+1):
           Draw a blue connector between them, a 2x2 square below the connector, and a wider rectangle below the square.
    5. Process any remaining (unpaired) isolated red objects:
        a. If the object's leftmost column 'c1' > 0, draw a blue rectangle from column 0 to c1-1 covering the object's rows.
    6. Return the modified grid.
    """
    # 1. Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    blue_color = 1 # Define color constants
    red_color = 2

    # 2. Identify all red and blue objects/pixels
    red_objects = find_objects(input_grid, red_color)
    blue_objects = find_objects(input_grid, blue_color) # Used to find coordinates

    # Create a flat set of all input blue coordinates for efficient adjacency checking
    blue_coords_flat = set()
    for b_obj in blue_objects:
        blue_coords_flat.update(b_obj)
    # Also add single blue pixels if find_objects missed them (e.g., if no blue objects found)
    if not blue_coords_flat:
         blue_coords_flat.update(tuple(coord) for coord in np.argwhere(input_grid == blue_color))


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
                        # Horizontal bar: (r2+1, c2-1), (r2+1, c2), (r2+1, c2+1)
                        # Vertical stem: (r2+2, c2)
                        t2_coords.add((r2 + 1, c1 - 1)) # use c1 since c1==c2
                        t2_coords.add((r2 + 1, c1))
                        t2_coords.add((r2 + 1, c1 + 1))
                        t2_coords.add((r2 + 2, c1))
                        draw_pixels(output_grid, t2_coords, blue_color)

                        # Break inner loop once obj1 is paired
                        break # Found pair for obj1, move to next i

    # 5b. Process Horizontal 2x2 Pairs
    for i in range(num_isolated):
        if i in processed_indices:
            continue
        obj1 = isolated_red_objects_data[i]
        # Check if it's a 2x2 square
        if obj1["shape_size"] == (2, 2) and len(obj1["coords"]) == 4: # Ensure it's exactly 2x2
            r1_start, c1_start, r1_end, c1_end = obj1["bbox"] # r1_end=r1_start+1, c1_end=c1_start+1
            # Search for a potential pair starting from the next object
            for j in range(i + 1, num_isolated):
                if j in processed_indices:
                    continue
                obj2 = isolated_red_objects_data[j]
                if obj2["shape_size"] == (2, 2) and len(obj2["coords"]) == 4: # Ensure it's exactly 2x2
                    r2_start, c2_start, r2_end, c2_end = obj2["bbox"] # r2_end=r2_start+1, c2_end=c2_start+1
                    # Check for horizontal alignment (same rows, obj2 is to the right with a gap)
                    # c2_start must be at least c1_start+3 (c1_end+2)
                    if r1_start == r2_start and c2_start > c1_end + 1:
                        # Found a horizontal 2x2 pair
                        processed_indices.add(i)
                        processed_indices.add(j)

                        # i. Draw connector rectangle (rows r1_start to r1_end, cols c1_end+1 to c2_start-1)
                        conn_col_start = c1_end + 1
                        conn_col_end = c2_start - 1
                        connector_coords = set()
                        for r in range(r1_start, r1_end + 1):
                            for c in range(conn_col_start, conn_col_end + 1):
                                connector_coords.add((r, c))
                        draw_pixels(output_grid, connector_coords, blue_color)

                        # ii. Draw 2x2 square below connector
                        conn_width = conn_col_end - conn_col_start + 1
                        if conn_width >= 0: # Should always be true if c2_start > c1_end+1
                            # Calculate top-left corner of the 2x2 square
                            # Centered below the connector
                            # square_start_col = conn_col_start + math.floor((conn_width - 2) / 2) This was causing issues, let's rethink
                            # Midpoint column index of connector (approx): conn_col_start + (conn_width-1)/2
                            # We want the 2x2 square's columns sc, sc+1 to be centered around this midpoint.
                            # Start col for 2x2: floor(Midpoint - 0.5) = floor(conn_col_start + (conn_width-1)/2 - 0.5)
                            # floor(conn_col_start + conn_width/2 - 1)
                            # Let's test example 2: c1_start=3, c1_end=4. c2_start=9, c2_end=10.
                            # conn_col_start = 5. conn_col_end = 8. conn_width = 4.
                            # Midpoint = 5 + (4-1)/2 = 6.5
                            # square_start_col = floor(6.5 - 0.5) = 6. Correct square cols: 6, 7.
                            square_start_col = conn_col_start + math.floor(conn_width / 2) -1 # Adjusted calculation seems correct

                            square_start_row = r1_start + 2
                            square_coords = set()
                            for r in range(square_start_row, square_start_row + 2):
                                for c in range(square_start_col, square_start_col + 2):
                                     square_coords.add((r,c))
                            draw_pixels(output_grid, square_coords, blue_color)

                        # iii. Draw bottom rectangle below square structure
                        # Rows r1_start+4 to r1_start+5 (height 2)
                        # Cols c1_end+1 to c2_end (conn_col_start to c2_end)
                        bottom_rect_start_row = r1_start + 4
                        bottom_rect_coords = set()
                        for r in range(bottom_rect_start_row, bottom_rect_start_row + 2):
                             for c in range(conn_col_start, c2_end + 1): # Columns span under connector AND obj2
                                bottom_rect_coords.add((r,c))
                        draw_pixels(output_grid, bottom_rect_coords, blue_color)

                        # Break inner loop once obj1 is paired
                        break # Found pair for obj1, move to next i

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

        # No need to mark as processed here, as we only iterate once more

    # 7. Return the final modified grid
    return output_grid