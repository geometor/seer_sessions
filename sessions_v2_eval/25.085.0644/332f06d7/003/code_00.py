import numpy as np
from collections import deque

"""
Transformation Rule Natural Language Description:

1. Identify the background color (typically green, 3).
2. Locate the single, contiguous red object (color 2, 'Agent').
3. Locate all distinct, contiguous white objects (color 0, 'Targets'). Count the total number of white objects.
4. Identify all blue pixels (color 1, 'Path').
5. Perform a Breadth-First Search (BFS) starting from blue pixels adjacent (including diagonally) to the red object. The search moves through adjacent blue pixels.
6. Identify the 'reachable' white object: This is the first white object encountered during the BFS (i.e., a blue pixel in the path is adjacent to a pixel belonging to a white object). If no white object is reachable, proceed without changing any white objects.
7. Create the output grid, initially as a copy of the input grid.
8. Transformation Rules:
   a. If a white object was reachable via the BFS path:
      i. Change all pixels of the reachable white object to blue (color 1).
      ii. If the total number of white objects found in step 3 was exactly one, change all pixels of the original red object to white (color 0).
      iii. If the total number of white objects found in step 3 was greater than one, leave the original red object unchanged (keep it red, color 2).
   b. If no white object was reachable via the BFS path, make no changes to the grid (return the copy).
   c. All other pixels (background, other path pixels, unreachable white objects) remain unchanged from the input grid.
"""

def find_objects(grid, color):
    """Finds all contiguous objects of a given color using 8-way connectivity."""
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
    """Gets valid neighbor coordinates for a given coordinate."""
    r, c = coord
    rows, cols = grid_shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center pixel itself
            if dr == 0 and dc == 0:
                continue
            # Skip diagonal neighbors if not included
            if not include_diagonal and abs(dr) + abs(dc) != 1:
                continue
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    """
    Applies the revised transformation rule based on white object count and reachability.
    Finds a red object, finds all white objects, finds the one reachable via a blue path,
    and transforms the red and reachable white objects based on the total count of white objects.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy() # Start with a copy
    rows, cols = grid.shape

    # Define colors used in the transformation
    agent_color = 2             # Red
    path_color = 1              # Blue
    target_color = 0            # White
    result_color_target = 1     # Blue (color to change reachable white object to)
    result_color_agent_single = 0 # White (color to change red agent to if only 1 white obj)
    # background_color = 3      # Green (not explicitly needed for modification rule)

    # --- 1. Find Objects and Path Pixels ---

    # Find the red agent object (assuming exactly one)
    red_objects = find_objects(grid, agent_color)
    if not red_objects:
        # If no red agent is found, return the original grid
        return input_grid
    # We assume based on examples there's only one red object
    red_object_coords = red_objects[0]

    # Find all white target objects
    white_objects = find_objects(grid, target_color)
    num_white_objects = len(white_objects)
    if num_white_objects == 0:
        # If no white targets are found, return the original grid
        return input_grid

    # Create a quick lookup map from a coordinate to the index of the white object it belongs to
    white_coord_to_object_index = {}
    for idx, obj in enumerate(white_objects):
        for coord in obj:
            white_coord_to_object_index[coord] = idx

    # Get coordinates of all blue path pixels
    blue_path_coords = set(zip(*np.where(grid == path_color)))
    # If there's no path, BFS will naturally find no reachable object

    # --- 2. Find Reachable White Object via BFS ---

    # Initialize BFS queue with blue pixels directly adjacent (including diagonally) to the red object
    queue = deque()
    visited_path = set() # Keep track of visited blue path pixels
    start_nodes = set()  # Blue pixels adjacent to the red object

    for r_coord in red_object_coords:
        for neighbor in get_neighbors(r_coord, grid.shape, include_diagonal=True):
            # Check if neighbor is a blue path pixel
            if neighbor in blue_path_coords:
                start_nodes.add(neighbor)

    # Add starting blue nodes to the queue and mark as visited
    for node in start_nodes:
         if node not in visited_path:
             queue.append(node)
             visited_path.add(node)

    reachable_white_object_index = -1 # Index of the reachable white object
    reachable_white_object_coords = None # Coordinates of the reachable white object

    # Perform BFS through the blue path
    while queue:
        current_coord = queue.popleft()

        # Check if current blue pixel is adjacent (including diagonally) to any white pixel
        found_target = False
        for neighbor in get_neighbors(current_coord, grid.shape, include_diagonal=True):
            if neighbor in white_coord_to_object_index:
                # Found a connection to a white object
                target_object_index = white_coord_to_object_index[neighbor]
                # Record the first reachable white object found
                reachable_white_object_index = target_object_index
                reachable_white_object_coords = white_objects[target_object_index]
                found_target = True
                break # Stop searching once the first reachable object is identified

        if found_target:
            break # Exit BFS

        # Add unvisited blue neighbors to the queue for further exploration
        for neighbor in get_neighbors(current_coord, grid.shape, include_diagonal=True):
            # Check if neighbor is a blue path pixel and hasn't been visited yet
            if neighbor in blue_path_coords and neighbor not in visited_path:
                visited_path.add(neighbor)
                queue.append(neighbor)

    # --- 3. Modify the Output Grid based on findings ---

    # Only proceed with modifications if a white object was reachable
    if reachable_white_object_coords is not None:
        # Rule a.i: Change reachable white object pixels to blue
        for r, c in reachable_white_object_coords:
            output_grid[r, c] = result_color_target

        # Determine the transformation of the red object based on the total count of white objects
        if num_white_objects == 1:
            # Rule a.ii: If only one white object total, change red object to white
            for r, c in red_object_coords:
                output_grid[r, c] = result_color_agent_single
        elif num_white_objects > 1:
            # Rule a.iii: If multiple white objects, red object remains red
            # No action needed as output_grid started as a copy
            pass
        # Note: The case num_white_objects == 0 was handled earlier

    # else: Rule b: If no white object was reachable, no changes are made to output_grid.

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()