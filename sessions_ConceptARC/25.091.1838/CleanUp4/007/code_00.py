import numpy as np
from collections import deque

"""
Transforms an input grid based on a sequence of prioritized conditional rules:

1.  **Rule 1 (Azure/Green Adjacency):** If the grid contains both azure (8) and green (3) pixels, AND at least one azure (8) pixel is adjacent (using 8-connectivity: orthogonal or diagonal) to any green (3) pixel, then change *only those specific azure (8) pixels* that have a green(3) neighbor to white (0). Output the modified grid and stop.

2.  **Rule 2 (Keep Large Objects):** If Rule 1 condition is not met, identify all distinct contiguous non-white objects (using 4-connectivity: orthogonal neighbors only). Count how many of these objects have a size (pixel count) of 10 or more. If this count is 4 or greater, then create a new grid containing *only* the pixels belonging to these large objects (size >= 10). All other pixels become white (0). Output the new grid and stop.

3.  **Rule 3 (Yellow to Green):** If neither Rule 1 nor Rule 2 conditions are met, and the grid contains any yellow (4) pixels, change all yellow (4) pixels to green (3). Other pixels remain unchanged. Output the modified grid and stop.

4.  **Default:** If none of the above conditions are met, return the input grid unchanged.
"""

def get_neighbors(r, c, height, width, connectivity=8):
    """
    Gets valid neighbor coordinates for a given cell (r, c).

    Args:
        r: Row index of the cell.
        c: Column index of the cell.
        height: Grid height.
        width: Grid width.
        connectivity: 8 for orthogonal and diagonal, 4 for orthogonal only.

    Returns:
        A list of (row, col) tuples for valid neighbors.
    """
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            # Skip diagonals if 4-connectivity is specified
            if connectivity == 4 and abs(dr) + abs(dc) != 1:
                 continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_objects(grid, ignore_color=0, connectivity=4):
    """
    Finds all contiguous objects of colors other than ignore_color using BFS.

    Args:
        grid: The 2D numpy array representing the grid.
        ignore_color: The color to ignore (usually background color 0).
        connectivity: 4 or 8, for defining adjacency in object finding. Standard ARC uses 4.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys: 'color', 'size', 'pixels' (a set of (r, c) tuples).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # Check if pixel is not the ignored color and hasn't been visited
            if grid[r, c] != ignore_color and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_pixels.add((r, c))

                # Breadth-First Search to find all connected pixels of the same color
                while q:
                    curr_r, curr_c = q.popleft()
                    # Check neighbors based on specified connectivity
                    for nr, nc in get_neighbors(curr_r, curr_c, height, width, connectivity=connectivity):
                        if grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            obj_pixels.add((nr, nc))
                            q.append((nr, nc))
                
                # Store the found object if it has any pixels
                if obj_pixels:
                    objects.append({'color': color, 'size': len(obj_pixels), 'pixels': obj_pixels})
    return objects


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # --- Rule 1: Check Azure (8) / Green (3) Adjacency (8-connectivity) ---
    has_azure = np.any(grid == 8)
    has_green = np.any(grid == 3)
    azure_pixels_adjacent_to_green = set() # Store coordinates of azure pixels to remove
    adjacency_found_rule1 = False

    if has_azure and has_green:
        azure_pixels = np.argwhere(grid == 8)
        # Iterate through all azure pixels
        for r_az, c_az in azure_pixels:
            # Check 8-connectivity neighbors for green pixels
            is_adjacent = False
            for nr, nc in get_neighbors(r_az, c_az, height, width, connectivity=8):
                if grid[nr, nc] == 3:
                    is_adjacent = True
                    break # Found a green neighbor for this azure pixel
            if is_adjacent:
                adjacency_found_rule1 = True
                # Add this azure pixel's location to the set for removal
                azure_pixels_adjacent_to_green.add((r_az, c_az))
        # No need to check all azure pixels if we only cared *if* adjacency exists,
        # but Rule 1 action requires knowing *which* azure pixels are adjacent.

    # --- Apply Rule 1 if condition met ---
    if adjacency_found_rule1:
        output_grid = grid.copy()
        # Set *only* the identified adjacent azure pixels to white
        for r, c in azure_pixels_adjacent_to_green:
            output_grid[r, c] = 0
        return output_grid.tolist() # Rule 1 applied, return result

    # --- Rule 2: Check for >= 4 Large Objects (size >= 10) (if Rule 1 didn't apply) ---
    # Find objects using standard 4-connectivity for object definition
    all_objects = find_objects(grid, ignore_color=0, connectivity=4) 
    # Filter objects to find only those with size 10 or greater
    large_objects = [obj for obj in all_objects if obj['size'] >= 10]
    # Check if the condition (4 or more large objects) is met
    rule2_triggered = len(large_objects) >= 4

    # --- Apply Rule 2 if condition met ---
    if rule2_triggered:
        # Create a new grid initialized to white (0)
        output_grid = np.full_like(grid, 0) 
        # Iterate through only the large objects identified (size >= 10)
        for obj in large_objects:
            color = obj['color']
            # Draw the pixels of each large object onto the white grid
            for r, c in obj['pixels']:
                output_grid[r, c] = color
        return output_grid.tolist() # Rule 2 applied, return result

    # --- Rule 3: Check for Yellow (4) pixels (if Rules 1 and 2 didn't apply) ---
    has_yellow = np.any(grid == 4)

    # --- Apply Rule 3 if condition met ---
    if has_yellow:
        output_grid = grid.copy()
        # Find coordinates of all yellow pixels
        yellow_coords = np.where(grid == 4)
        # Change yellow pixels to green (3)
        output_grid[yellow_coords] = 3 
        return output_grid.tolist() # Rule 3 applied, return result

    # --- Default Case ---
    # If none of the rules were triggered, return the original grid unmodified
    return grid.tolist()