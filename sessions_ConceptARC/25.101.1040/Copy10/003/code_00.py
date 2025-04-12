import numpy as np
from collections import deque

"""
Identifies a unique composite object within the input grid, consisting of a 'container' object fully enclosing one or more 'contained' objects of different colors. Uses 8-way connectivity to define objects. Creates an output grid containing only this composite object and potentially a single translated copy. The copy is placed either to the right (with a gap of 2 pixels) or downwards (with a gap of 1 pixel), prioritizing the rightward placement if space allows within the grid boundaries. All other objects from the input are discarded.

Workflow:
1.  Find all distinct objects (contiguous regions of the same non-white color) using 8-way connectivity.
2.  Identify the unique 'container' object that fully encloses one or more 'contained' objects of different colors.
    - Enclosure check: A contained object is fully enclosed if it doesn't touch the grid boundary, has a different color than the container, and all its 8-way adjacent neighbors belong either to itself or the container.
3.  Determine the set of all pixels belonging to the container and all objects it encloses ('composite object'). Calculate its combined bounding box.
4.  Initialize an output grid of the same size as the input, filled with the background color (0).
5.  Draw the composite object onto the output grid at its original location.
6.  Determine the placement for a copy:
    - Calculate the composite object's bounding box dimensions (height H, width W).
    - Check if a copy fits right: `copy_start_col (min_c + W + 2) + W <= grid_width`.
    - Check if a copy fits down: `copy_start_row (min_r + H + 1) + H <= grid_height`.
    - If fits right, set translation `dx = W + 2`, `dy = 0`.
    - Else if fits down, set translation `dx = 0`, `dy = H + 1`.
    - Otherwise, no copy (`dx=0, dy=0`).
7.  If a valid translation `(dx, dy)` was determined, draw a copy of the composite object at the translated position.
8.  Return the resulting output grid.
"""


def find_objects_8_way(grid: np.ndarray) -> list[dict]:
    """
    Finds all connected components of non-background pixels using 8-way connectivity.
    Each object stores its color, pixel coordinates (set), and bounding box.
    """
    objects = []
    visited = set()
    height, width = grid.shape
    # Define 8-way neighbors (including diagonals)
    neighbors = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]

    for r in range(height):
        for c in range(width):
            # Check if pixel is non-background and not yet visited
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                obj_pixels = set()
                # Use BFS (deque) for finding connected components
                q = deque([(r, c)])
                visited.add((r, c))
                # Initialize bounding box coordinates
                min_r, min_c, max_r, max_c = r, c, r, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    # Update bounding box
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore 8 neighbors
                    for dr, dc in neighbors:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within bounds, has the same color, and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                # Store the found object's properties
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c), # min_row, min_col, max_row, max_col
                    'size': len(obj_pixels)
                })
    return objects

def is_fully_enclosed_8_way(container_obj: dict, contained_obj: dict, grid: np.ndarray) -> bool:
    """
    Checks if contained_obj is fully enclosed by container_obj using 8-way adjacency.
    Returns False if contained_obj touches the grid boundary, has the same color as container,
    or touches any pixel not belonging to the container or itself.
    """
    # Basic checks
    if container_obj is contained_obj or container_obj['color'] == contained_obj['color']:
        return False

    container_pixels = container_obj['pixels']
    contained_pixels = contained_obj['pixels']
    height, width = grid.shape

    if not contained_pixels:
        return False # Cannot enclose an empty object

    # Define 8-way neighbors
    neighbors = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]

    for r, c in contained_pixels:
        # Check if any pixel of the contained object is on the grid boundary
        if r == 0 or r == height - 1 or c == 0 or c == width - 1:
             return False # Cannot be fully enclosed if touching boundary

        # Check all 8 neighbors
        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc
            neighbor_pos = (nr, nc)

            # Neighbor must be within bounds (implicitly true due to boundary check above)
            # Check if neighbor belongs EITHER to the contained object OR the container object
            if neighbor_pos not in contained_pixels and neighbor_pos not in container_pixels:
                # Found a neighbor that is not part of the container or contained object
                # This means it touches background or another object -> not fully enclosed.
                return False

    # If all checks passed for all pixels, the object is fully enclosed.
    return True


def get_composite_object_pixels(objects: list[dict], grid: np.ndarray) -> tuple[set | None, tuple | None]:
    """
    Identifies the unique container object and collects all pixels from it
    and all objects it fully encloses (using 8-way check). Calculates the combined bounding box.
    Assumes at most one such top-level container object exists per grid.
    """
    the_container = None
    all_contained_objects = []

    # Find the container object
    for i, potential_container in enumerate(objects):
        currently_contained = []
        for j, potential_contained in enumerate(objects):
            # Use the 8-way enclosure check
            if is_fully_enclosed_8_way(potential_container, potential_contained, grid):
                 currently_contained.append(potential_contained)

        # If this object contains other objects, consider it the container
        if currently_contained:
            if the_container is not None:
                 # Handle multiple containers if needed, but assume uniqueness for now
                 # print("Warning: Multiple container objects found, using the first one.")
                 pass # Stick with the first one found
            else:
                the_container = potential_container
                all_contained_objects = currently_contained
                # break # Assume uniqueness, stop searching

    # If no container was found, return None
    if not the_container:
        return None, None

    # Collect all pixels from the container and all objects it encloses
    composite_pixels = set(the_container['pixels'])
    for contained_obj in all_contained_objects:
        composite_pixels.update(contained_obj['pixels'])

    # Calculate the combined bounding box of the composite object
    if not composite_pixels:
         return None, None # Should not happen if container was found

    min_r = min(r for r, c in composite_pixels)
    min_c = min(c for r, c in composite_pixels)
    max_r = max(r for r, c in composite_pixels)
    max_c = max(c for r, c in composite_pixels)
    bbox = (min_r, min_c, max_r, max_c)

    return composite_pixels, bbox


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying a composite object (container + contained using 8-way),
    keeping only that object, and adding a translated copy (right W+2 or down H+1).
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Step 1: Find all distinct objects in the grid using 8-way connectivity
    objects = find_objects_8_way(grid)
    if not objects:
        # If there are no objects, return an empty grid of the same size
        return np.zeros_like(grid).tolist()

    # Step 2: Identify the composite object (container + all enclosed) and its bounding box
    composite_pixels, composite_bbox = get_composite_object_pixels(objects, grid)

    # If no composite object (container enclosing others) is found, return empty grid
    if not composite_pixels:
         # print("Debug: No composite object found.") # Debugging line
         return np.zeros_like(grid).tolist()

    # Extract bounding box info
    min_r, min_c, max_r, max_c = composite_bbox
    comp_h = max_r - min_r + 1
    comp_w = max_c - min_c + 1

    # Step 3: Initialize an output grid filled with the background color (0)
    output_grid = np.zeros_like(grid)

    # Step 4: Draw the original composite object onto the output grid
    for r, c in composite_pixels:
        output_grid[r, c] = grid[r, c]

    # Step 5: Determine placement for the copy (prefer right W+2, then down H+1)
    dx, dy = 0, 0 # Initialize translation delta

    # Define gaps
    gap_h = 2 # Horizontal gap
    gap_v = 1 # Vertical gap

    # Calculate potential top-left positions and dimensions for the copy
    copy_start_col_right = min_c + comp_w + gap_h
    copy_end_col_right = copy_start_col_right + comp_w -1

    copy_start_row_down = min_r + comp_h + gap_v
    copy_end_row_down = copy_start_row_down + comp_h -1

    # Check if the entire copy fits within grid bounds if placed to the right
    # Need to check both max_r and copy_end_col_right
    fits_right = (max_r < height and copy_end_col_right < width)

    # Check if the entire copy fits within grid bounds if placed downwards
    # Need to check both copy_end_row_down and max_c
    fits_down = (copy_end_row_down < height and max_c < width)

    # Apply placement logic: prioritize right, then down
    if fits_right:
        # Set translation for rightward placement
        dx = comp_w + gap_h
        dy = 0
        # print(f"Debug: Placing copy right. dx={dx}, dy={dy}") # Debugging line
    elif fits_down:
        # Set translation for downward placement
        dx = 0
        dy = comp_h + gap_v
        # print(f"Debug: Placing copy down. dx={dx}, dy={dy}") # Debugging line
    # else:
        # print("Debug: Copy does not fit right or down.") # Debugging line


    # Step 6: Draw the copy if a valid placement was determined (dx > 0 or dy > 0)
    if dx > 0 or dy > 0:
        # Iterate through the original composite object's pixels
        for r, c in composite_pixels:
            # Calculate the corresponding coordinates for the copy
            nr, nc = r + dy, c + dx
            # Ensure the copy's pixel coordinates are within the grid bounds
            # (This check might be redundant given the fits_right/fits_down checks, but safe)
            if 0 <= nr < height and 0 <= nc < width:
                # Copy the color from the original position in the input grid
                output_grid[nr, nc] = grid[r, c]
            # else: # Debugging line
                 # print(f"Debug: Copy pixel ({nr},{nc}) out of bounds for original ({r},{c})")

    # Step 7: Convert the final numpy grid back to a list of lists and return
    return output_grid.tolist()