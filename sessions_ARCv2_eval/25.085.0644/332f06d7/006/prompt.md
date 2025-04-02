
Previous Code:
```python
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

import numpy as np
from collections import deque

def find_objects(grid, color):
    """
    Finds all contiguous objects of a given color using 8-way connectivity (including diagonals).

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of a distinct object.
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
    Applies the transformation rule: finds a red agent, identifies white targets,
    determines reachability via a blue path, and modifies the agent and the first
    reachable target based on the total count of targets.
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
    # background_color = 3      # Green (not explicitly needed for modification rule)

    # --- Step 2: Locate the red agent object ---
    red_objects = find_objects(grid, agent_color)
    # If no red agent is found, return the original grid unchanged
    if not red_objects:
        return input_grid # Return original list[list]
    # Assumption based on examples: there is only one red object
    red_object_coords = red_objects[0]

    # --- Step 3: Locate all white target objects and count them ---
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

    # --- Step 4: Identify all blue path pixels ---
    blue_path_coords = set(zip(*np.where(grid == path_color)))

    # --- Step 5 & 6: Find Reachable White Object via BFS starting from agent's adjacent path ---

    # Initialize BFS structures
    queue = deque()
    visited_path = set() # Keep track of visited blue path pixels during BFS
    start_nodes = set()  # Collect unique blue pixels adjacent to the red object

    # Find blue pixels adjacent (including diagonally) to any part of the red object
    for r_coord in red_object_coords:
        for neighbor in get_neighbors(r_coord, grid.shape, include_diagonal=True):
            # Check if the neighbor is a blue path pixel
            if neighbor in blue_path_coords:
                start_nodes.add(neighbor)

    # Add starting blue nodes to the queue and mark as visited
    for node in start_nodes:
         if node not in visited_path:
             queue.append(node)
             visited_path.add(node)

    reachable_white_object_index = -1 # Index of the first reachable white object found
    reachable_white_object_coords = None # Coordinates of that object

    # Perform BFS through the blue path
    while queue:
        current_coord = queue.popleft() # Get the next blue pixel from the path

        # Check if the current blue pixel is adjacent (including diagonally) to any white pixel
        found_target = False
        for neighbor in get_neighbors(current_coord, grid.shape, include_diagonal=True):
            if neighbor in white_coord_to_object_index:
                # A connection to a white object is found
                target_object_index = white_coord_to_object_index[neighbor]
                # Record the first reachable white object encountered
                reachable_white_object_index = target_object_index
                reachable_white_object_coords = white_objects[target_object_index]
                found_target = True
                break # Stop checking neighbors for this blue pixel

        if found_target:
            break # Exit BFS entirely, as we only care about the first reachable object

        # If no target found yet, expand the BFS to adjacent unvisited blue path pixels
        for neighbor in get_neighbors(current_coord, grid.shape, include_diagonal=True):
            # Check if the neighbor is part of the blue path and hasn't been visited in this BFS
            if neighbor in blue_path_coords and neighbor not in visited_path:
                visited_path.add(neighbor)
                queue.append(neighbor)

    # --- Step 8: Modify the Output Grid based on BFS findings ---

    # Check if the BFS successfully found a reachable white object
    if reachable_white_object_coords is not None:
        # Rule 8.a.i: Change all pixels of the reachable white object to blue
        for r, c in reachable_white_object_coords:
            output_grid[r, c] = result_color_target

        # Rules 8.a.ii & 8.a.iii: Determine the transformation of the red object based on the *total* count of white objects
        if num_white_objects == 1:
            # If exactly one white object existed in the input grid, change the red object to white
            for r, c in red_object_coords:
                output_grid[r, c] = result_color_agent_single
        elif num_white_objects > 1:
            # If more than one white object existed, the red object remains unchanged (red)
            # No action needed as output_grid started as a copy with the red object intact
            pass
        # Note: The case num_white_objects == 0 was handled earlier by returning the input grid

    # Rule 8.b: If no white object was reachable (reachable_white_object_coords is None),
    # no changes are made beyond the initial copy, so the grid remains as is.

    # Rule 8.c: All other pixels remain unchanged implicitly because we started with a copy.

    # Convert the final NumPy array back to a standard list of lists before returning
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
3 2 2 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3
3 1 1 3 3 3 3 3 3 3 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 3 1 1 3 3
3 1 1 1 3 3 3 3 0 0 3 3
3 3 3 3 3 3 3 3 0 0 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 0 0 3 3 3 3 3 3 3 3 3
3 0 0 3 3 3 3 3 3 3 3 3
3 1 1 3 3 3 3 3 3 3 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 3 1 1 3 3
3 1 1 1 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
3 0 0 3 3 3 3 3 3 3 3 3
3 0 0 3 3 3 3 3 3 3 3 3
3 1 1 3 3 3 3 3 3 3 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 3 1 1 3 3
3 1 1 1 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 0 0 3 3
3 3 3 3 3 1 1 1 1 1 0 0 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 3 3 3 3
3 3 3 3 3 1 1 1 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 1 1 3 3
3 3 3 3 3 1 1 1 1 1 1 1 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 0 0 3 3 3 3
3 3 3 3 3 1 1 1 0 0 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 1 1 3 3
3 3 3 3 3 1 1 1 1 1 1 1 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 3 3 3 3
3 3 3 3 3 1 1 1 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 0 0 3 3 3 3 3 3 3 3 3 3 3
3 0 0 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 8.163265306122469

## Example 3:
Input:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3
2 2 2 1 1 1 1 3 3 1 1 1 1 1 1 3
2 2 2 1 1 3 3 3 3 3 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 1 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 3 3 1 1 3 3 3 1 1 1 3
3 0 0 0 1 3 3 1 1 1 1 1 1 1 1 3
3 0 0 0 1 3 3 1 1 1 1 1 1 1 1 3
3 0 0 0 1 3 3 1 1 1 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3
2 2 2 1 1 1 1 3 3 1 1 1 1 1 1 3
2 2 2 1 1 3 3 3 3 3 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 0 0 0 3 3 3 1 1 3
3 3 3 1 1 1 1 0 0 0 3 3 3 1 1 3
3 3 1 1 1 1 3 0 0 0 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 3 3 1 1 3 3 3 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 3
0 0 0 1 1 1 1 3 3 1 1 1 1 1 1 3
0 0 0 1 1 3 3 3 3 3 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 1 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 3 3 1 1 3 3 3 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 18
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 14.0625

## Example 4:
Input:
```
3 3 3 3 3 3 3 3 3 3
3 0 1 1 3 3 3 3 3 3
3 3 3 1 3 1 1 1 3 3
3 3 3 1 3 1 3 1 3 3
3 3 3 1 1 1 3 1 3 3
3 3 3 3 3 3 3 1 3 3
3 3 3 3 1 1 1 1 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 2 3 3 3 3 3
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3
3 1 1 1 3 3 3 3 3 3
3 3 3 1 3 1 1 1 3 3
3 3 3 1 3 1 3 1 3 3
3 3 3 1 1 1 3 1 3 3
3 3 3 3 3 3 3 1 3 3
3 3 3 3 1 1 1 1 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 0 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3
3 1 1 1 3 3 3 3 3 3
3 3 3 1 3 1 1 1 3 3
3 3 3 1 3 1 3 1 3 3
3 3 3 1 1 1 3 1 3 3
3 3 3 3 3 3 3 1 3 3
3 3 3 3 1 1 1 1 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 0 3 3 3 3 3
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
