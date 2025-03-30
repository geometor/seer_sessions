
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies initial green (3) rectangular objects in the input grid.
Iteratively places copies of these objects diagonally downwards.
A copy of an object with top-left (r, c), height h, and width w is potentially placed at:
1. (r + 2, c - w) (Down 2, Left by width)
2. (r + 2, c + w) (Down 2, Right by width)
Placement only occurs if the new object fits entirely within the grid boundaries
AND the entire area where the object would be placed currently consists of background (0) pixels.
The process continues recursively from newly placed objects until no more valid placements can be made.
"""

def find_initial_objects(grid, color):
    """
    Finds all contiguous solid rectangular objects of a specific color in the grid using BFS.
    
    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list of tuples: Each tuple represents an object: (top_left_r, top_left_c, height, width).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(rows):
        for c in range(cols):
            # If this pixel is the target color and hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                # Use BFS to find all connected pixels of the same color
                q_bfs = deque([(r, c)])
                visited[r, c] = True
                object_pixels = set([(r, c)])
                min_r, max_r, min_c, max_c = r, r, c, c

                while q_bfs:
                    curr_r, curr_c = q_bfs.popleft()

                    # Update bounding box coordinates
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check if neighbor is within grid bounds, is the target color, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            object_pixels.add((nr, nc))
                            q_bfs.append((nr, nc))
                
                # Calculate height and width from bounding box
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                
                # Verify if the object perfectly fills its bounding box (is a solid rectangle)
                is_solid_rectangle = True
                if len(object_pixels) != height * width:
                    is_solid_rectangle = False
                else:
                    # Double check: ensure all pixels within the bounding box are the target color
                    # This handles cases where BFS might find a shape fitting the bbox size
                    # but isn't actually solid (e.g., hollow rectangle)
                    for check_r in range(min_r, max_r + 1):
                        for check_c in range(min_c, max_c + 1):
                            if grid[check_r, check_c] != color:
                                is_solid_rectangle = False
                                break
                        if not is_solid_rectangle:
                            break

                # Add the found object properties if it's a solid rectangle
                if is_solid_rectangle:
                    objects.append((min_r, min_c, height, width))
                    # Mark all pixels within the confirmed rectangle bounding box as visited 
                    # to avoid redundant checks by the outer loop. This is safe because
                    # we confirmed it's a solid rectangle of the target color.
                    visited[min_r:max_r+1, min_c:max_c+1] = True

                
    return objects

def transform(input_grid):
    """
    Applies the recursive diagonal object copying transformation with overlap prevention.
    
    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input state
    output_grid = np.copy(input_np)
    grid_height, grid_width = output_grid.shape
    green_color = 3 
    background_color = 0

    # Find all initial green solid rectangular objects
    initial_objects = find_initial_objects(input_np, green_color) # Find in original grid

    # Use a queue for BFS traversal of object placements
    placement_q = deque()
    # Use a set to track top-left locations (r, c) where an object *has been successfully placed*
    # by the generation rule. This prevents redundant checks if the same potential 
    # placement arises from different generation branches.
    placed_locations = set() 

    # Initialize the queue with the initial objects found
    for r, c, h, w in initial_objects:
        # Only add valid objects (positive height and width)
        if h > 0 and w > 0: 
            placement_q.append((r, c, h, w))
            # Note: Initial objects are *not* added to placed_locations, as they weren't
            # generated by the placement rule itself.

    # Process the placement queue iteratively using BFS
    while placement_q:
        # Get the properties of the object whose potential children we are generating
        current_r, current_c, h, w = placement_q.popleft()

        # Define the two potential next top-left positions based on the rule
        # (down 2 rows, left/right by the object's width)
        next_positions_candidates = [
            (current_r + 2, current_c - w), # Down 2, Left by width
            (current_r + 2, current_c + w)  # Down 2, Right by width
        ]

        # Evaluate each potential next position for placement
        for next_r, next_c in next_positions_candidates:
            
            # --- Validation Checks ---
            
            # 1. Check Grid Bounds (Top-Left): 
            #    Is the potential top-left corner within the grid?
            if not (0 <= next_r < grid_height and 0 <= next_c < grid_width):
                continue # Skip if top-left is out of bounds

            # 2. Check Grid Bounds (Bottom-Right / Fit):
            #    Does the *entire* object fit within the grid when placed here?
            #    Bottom-right corner: (next_r + h - 1, next_c + w - 1)
            if not (next_r + h <= grid_height and next_c + w <= grid_width):
                continue # Skip if the object doesn't fit

            # 3. Check Redundant Placement (Optimization):
            #    Have we already successfully placed an object starting at this exact location?
            if (next_r, next_c) in placed_locations:
                continue # Skip if this location has already resulted in a successful placement

            # 4. Check Overlap / Background Condition (Crucial Constraint):
            #    Is the entire area where the object would be placed currently background color?
            target_area = output_grid[next_r : next_r + h, next_c : next_c + w]
            if np.any(target_area != background_color):
                continue # Skip if the area is not entirely background (contains non-zero pixels)

            # --- Placement and Enqueue ---
            # If all checks passed, the placement is valid and hasn't been done before starting here.
            
            # Record that we are placing an object starting at this location.
            placed_locations.add((next_r, next_c))
            
            # Modify the output grid: Draw the solid green rectangle.
            output_grid[next_r : next_r + h, next_c : next_c + w] = green_color

            # Add the newly placed object's details (position, height, width) to the queue.
            # This allows its own potential children to be generated in subsequent iterations.
            placement_q.append((next_r, next_c, h, w))

    # Convert the final numpy grid back to a list of lists for the required output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0
3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0
0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0
0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0
0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0
```
Match: False
Pixels Off: 114
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 41.45454545454547

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 3 3 3 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 3 3 3 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 3 3 3 0 3 3 3 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 3 3 3 0 3 3 3 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 3 3 3 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
3 3 3 0 3 3 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
3 3 3 0 3 3 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 3 3 3 0 0 0 3 3 3 0 0
0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0
0 3 3 3 0 0 0 3 3 3 3 3 3 3 3 0 0 0 3 3 3 0 0 0 3 3 3 0 0
0 3 3 3 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 3 3 3 0 3 3 3 3 3 3 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 3 3 3 0 3 3 3 3 3 3 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0
0 3 3 3 0 0 3 3 3 3 3 3 3 3 3 3 0 0 3 3 3 0 0 0 3 3 3 0 0
0 3 3 3 0 0 3 3 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 3 3 3 3 3 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 3 3 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 3 3 3 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 3 3 0 0 3 3 0 0 3 3 0 0 3 3 0 0 3 3 0 0 3 3 0 0 0 0 0
0 0 3 3 0 0 3 3 0 0 3 3 0 0 3 3 0 0 3 3 0 0 3 3 0 0 0 0 0
```
Match: False
Pixels Off: 318
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 75.6242568370987

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 3 3 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 3 3 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 3 3 0 0 3 3 3 0 0 0 0
0 0 3 3 3 0 0 0 3 3 3 0 0 0 0 0 3 3 0 0 3 3 3 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 3 3 3 3 3 3 3 3 3 0 0 0 3 3 3 0
0 0 0 0 0 3 3 3 0 0 0 3 3 3 3 3 3 3 3 3 0 0 0 3 3 3 0
0 0 3 3 3 0 0 0 3 3 3 0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 0 0 0 3 3 3 0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 3 3 3 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 3 3 3 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 3 3 0 0 3 3 0 0 3 3 0 0 3 3 0 0 3 3 0 0 3 3 0
0 0 0 0 3 3 0 0 3 3 0 0 3 3 0 0 3 3 0 0 3 3 0 0 3 3 0
```
Match: False
Pixels Off: 240
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 61.30268199233717
