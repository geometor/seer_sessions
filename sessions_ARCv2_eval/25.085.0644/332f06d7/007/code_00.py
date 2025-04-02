"""
Transformation Rule Natural Language Program:

1.  **Identify Objects and Features:**
    *   Locate the unique red object (color 2), referred to as the 'agent'. If no agent exists, return the input grid unchanged.
    *   Locate all distinct white objects (color 0), referred to as 'targets'. Count the total number of these target objects (`total_target_count`). If no targets exist, return the input grid unchanged.
    *   Identify all blue pixels (color 1), forming the 'path'.
    *   Note the background color (typically green, 3), which remains unchanged.

2.  **Determine Reachability:**
    *   Find all blue path pixels that are adjacent (including diagonally) to any pixel of the red agent. These are the starting points for the path search.
    *   Perform a Breadth-First Search (BFS) starting simultaneously from all these initial blue path pixels.
    *   The BFS explores the path by moving between adjacent (including diagonally) blue pixels.
    *   The search stops when the BFS encounters the *first* blue pixel that is adjacent (including diagonally) to *any* pixel belonging to *any* white target object.
    *   Identify the specific white target object that was reached ('reachable target'). If the BFS completes without finding such a connection, no target is reachable.

3.  **Apply Transformations:**
    *   Create the output grid as a copy of the input grid.
    *   **If a white target object was reachable:**
        *   Change the color of all pixels belonging to the 'reachable target' object to blue (color 1) in the output grid.
        *   Check the `total_target_count` determined in step 1:
            *   If `total_target_count` is exactly 1, change the color of all pixels belonging to the original red agent object to white (color 0) in the output grid.
            *   If `total_target_count` is greater than 1, the red agent object remains unchanged (stays red, color 2) in the output grid.
    *   **If no white target object was reachable:**
        *   Make no changes to the output grid (it remains identical to the input grid).

4.  **Return:** Output the modified grid.
"""

import numpy as np
from collections import deque

# --- Helper Functions ---

def find_objects(grid, color):
    """
    Finds all contiguous objects of a given color using 8-way connectivity (including diagonals).

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of a distinct object. Returns empty list if no objects found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS from an unvisited pixel of the target color
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 8 neighbors (orthogonal and diagonal)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            # Check bounds and if neighbor is same color and unvisited
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                obj_coords.add((nr, nc))
                # Add the found object's coordinates to the list of objects
                objects.append(obj_coords)
    return objects

def get_neighbors(coord, grid_shape, include_diagonal=True):
    """
    Gets valid neighbor coordinates for a given coordinate within the grid boundaries.

    Args:
        coord (tuple): The (row, col) coordinate.
        grid_shape (tuple): The (rows, cols) shape of the grid.
        include_diagonal (bool): Whether to include diagonal neighbors.

    Returns:
        list[tuple]: A list of valid neighbor (row, col) coordinates.
    """
    r, c = coord
    rows, cols = grid_shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center pixel itself
            if dr == 0 and dc == 0:
                continue
            # Skip diagonal neighbors if not included (though default is True)
            if not include_diagonal and abs(dr) + abs(dc) > 1:
                 continue
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule based on agent, targets, and path reachability.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify, ensuring the original input is unchanged
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Define colors used in the transformation logic
    agent_color = 2             # Red
    path_color = 1              # Blue
    target_color = 0            # White
    result_color_target = 1     # Blue (color to change reachable white object to)
    result_color_agent_single = 0 # White (color to change red agent to if only 1 white obj)
    # agent_color_multi = 2     # Red (agent color if multiple white objs - no change needed)

    # --- Step 1: Identify Objects and Features ---

    # Locate the red agent object
    red_objects = find_objects(grid, agent_color)
    # If no red agent is found, return the original grid unchanged
    if not red_objects:
        return input_grid # Return original list[list]
    # Assumption based on examples: there is only one red object
    red_object_coords = red_objects[0]

    # Locate all white target objects and count them
    white_objects = find_objects(grid, target_color)
    num_white_objects = len(white_objects)
    # If no white targets are found, return the original grid unchanged
    if num_white_objects == 0:
        return input_grid # Return original list[list]

    # Create a lookup map for quick identification of which white object a coordinate belongs to
    white_coord_to_object_index = {}
    for idx, obj in enumerate(white_objects):
        for coord in obj:
            white_coord_to_object_index[coord] = idx

    # Identify all blue path pixels
    blue_path_coords = set(zip(*np.where(grid == path_color)))
    if not blue_path_coords: # If there's no path, nothing can be reached
        return input_grid

    # --- Step 2: Determine Reachability ---

    # Initialize BFS structures
    queue = deque()
    visited_path = set() # Keep track of visited blue path pixels during BFS
    start_nodes = set()  # Collect unique blue pixels adjacent to the red object

    # Find blue pixels adjacent (including diagonally) to any part of the red object
    for r_coord in red_object_coords:
        for neighbor in get_neighbors(r_coord, grid.shape, include_diagonal=True):
            # Check if the neighbor is a blue path pixel and hasn't been visited yet (as a starting node)
            if neighbor in blue_path_coords and neighbor not in start_nodes:
                 start_nodes.add(neighbor)
                 queue.append(neighbor) # Add valid starting nodes to the queue
                 visited_path.add(neighbor) # Mark starting nodes as visited

    reachable_white_object_index = -1 # Index of the first reachable white object found
    reachable_white_object_coords = None # Coordinates of that object

    # Perform BFS through the blue path
    while queue:
        current_coord = queue.popleft() # Get the next blue pixel from the path

        # Check if the current blue pixel is adjacent (including diagonally) to any white pixel
        found_target = False
        potential_targets = [] # Store potential targets reached from this node

        for neighbor in get_neighbors(current_coord, grid.shape, include_diagonal=True):
            if neighbor in white_coord_to_object_index:
                # A connection to a white object is found
                target_object_index = white_coord_to_object_index[neighbor]
                potential_targets.append(target_object_index)
                found_target = True
                # Don't break here, check all neighbors first to handle cases where
                # a path node touches multiple targets simultaneously. We need the "first"
                # reached overall, which BFS handles by level. If multiple are found
                # at the same BFS level, the specific one chosen might depend on queue order,
                # but the logic requires *any* first reachable one. We'll take the first one
                # identified in this neighbor loop if multiple are hit by the same path node.

        if found_target:
            # Record the first reachable white object encountered at this BFS level
            reachable_white_object_index = potential_targets[0] # Take the first one found
            reachable_white_object_coords = white_objects[reachable_white_object_index]
            break # Exit BFS entirely, as we only care about the first reachable object

        # If no target found yet, expand the BFS to adjacent unvisited blue path pixels
        if not found_target: # Only expand if we haven't found the target yet
            for neighbor in get_neighbors(current_coord, grid.shape, include_diagonal=True):
                # Check if the neighbor is part of the blue path and hasn't been visited in this BFS
                if neighbor in blue_path_coords and neighbor not in visited_path:
                    visited_path.add(neighbor)
                    queue.append(neighbor)

    # --- Step 3: Apply Transformations ---

    # Check if the BFS successfully found a reachable white object
    if reachable_white_object_coords is not None:
        # Rule 3.If_true.i: Change all pixels of the reachable white object to blue
        for r, c in reachable_white_object_coords:
            output_grid[r, c] = result_color_target

        # Rule 3.If_true.ii: Determine the transformation of the red object based on the *total* count of white objects
        if num_white_objects == 1:
            # If exactly one white object existed *in the input grid*, change the red object to white
            for r, c in red_object_coords:
                output_grid[r, c] = result_color_agent_single
        elif num_white_objects > 1:
            # If more than one white object existed *in the input grid*, the red object remains unchanged (red)
            # No action needed as output_grid started as a copy with the red object intact
            pass
        # Note: The case num_white_objects == 0 was handled earlier

    # Rule 3.If_false: If no white object was reachable (reachable_white_object_coords is None),
    # no changes are made beyond the initial copy, so the grid remains as is.

    # Convert the final NumPy array back to a standard list of lists before returning
    return output_grid.tolist()