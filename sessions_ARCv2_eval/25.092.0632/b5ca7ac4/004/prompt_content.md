
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies specific rectangular objects within the input grid and moves them horizontally.
Objects are defined as having a 1-pixel thick frame of either azure (8) or red (2),
enclosing a solid rectangular core of a different color (not the frame color and not the background color).
The size must be at least 3x3.

Transformation Steps:
1. Copy the input grid to create the output grid.
2. Identify the background color.
3. Find all qualifying framed rectangular objects.
4. For each found object:
    a. Erase the object from its original position in the output grid by filling its bounding box with the background color.
    b. Calculate the new horizontal position based on the frame color:
        - Azure (8) frames move to the left edge (column 0).
        - Red (2) frames move to the right edge (last column).
    c. Draw the object's original pixel data at its new position in the output grid.
5. Return the modified output grid.

Static elements (pixels not part of the identified movable objects) remain unchanged.
"""

def find_objects(grid, background_color):
    """
    Finds all framed rectangular objects in the grid matching the criteria.

    Args:
        grid (np.array): The input grid.
        background_color (int): The background color.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'bbox': (min_r, min_c, max_r, max_c) - Original bounding box
              'frame_color': The color of the frame (2 or 8)
              'subgrid': A numpy array containing the object's pixels.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # Look for potential frame pixels (red or azure) that haven't been visited
            # and are not the background color (handles cases where frame color might match background)
            if grid[r, c] in [2, 8] and grid[r, c] != background_color and not visited[r, c]:
                frame_color = grid[r, c]
                
                # Use BFS to find all connected pixels of the *same* frame color
                # This helps identify the extent of a potential frame
                q = deque([(r, c)])
                frame_pixels = set([(r,c)]) # Store pixels belonging to this potential frame component
                component_visited = set([(r, c)]) # Track visited during this specific BFS
                min_r_bfs, min_c_bfs, max_r_bfs, max_c_bfs = r, c, r, c

                while q:
                    curr_r, curr_c = q.popleft()
                    min_r_bfs = min(min_r_bfs, curr_r)
                    min_c_bfs = min(min_c_bfs, curr_c)
                    max_r_bfs = max(max_r_bfs, curr_r)
                    max_c_bfs = max(max_c_bfs, curr_c)

                    # Explore 8 neighbors for connectivity
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = curr_r + dr, curr_c + dc
                            
                            # Check bounds and if neighbor has the same frame color and wasn't visited in this BFS
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == frame_color and (nr, nc) not in component_visited:
                                component_visited.add((nr, nc))
                                frame_pixels.add((nr, nc))
                                q.append((nr, nc))

                # Define the bounding box based on the BFS extent
                min_r, min_c, max_r, max_c = min_r_bfs, min_c_bfs, max_r_bfs, max_c_bfs
                obj_h = max_r - min_r + 1
                obj_w = max_c - min_c + 1

                # Basic size check
                if obj_h < 3 or obj_w < 3:
                    # Mark only the BFS-found pixels as visited globally to avoid reprocessing this invalid component
                    for fr, fc in frame_pixels:
                        visited[fr, fc] = True
                    continue 

                # Verify the strict rectangular frame structure and solid core
                is_valid_object = True
                core_color = -1 # Sentinel value
                core_pixels = set() # Track core pixels for marking visited later

                for ir in range(min_r, max_r + 1):
                    for ic in range(min_c, max_c + 1):
                        pixel_val = grid[ir, ic]
                        # Check if it's on the border of the bounding box (potential frame)
                        is_border = (ir == min_r or ir == max_r or ic == min_c or ic == max_c)

                        if is_border:
                            if pixel_val != frame_color: # All border pixels MUST be the frame color
                                is_valid_object = False
                                break
                        else: # Inner pixel (potential core)
                            # Core cannot be frame or background color
                            if pixel_val == frame_color or pixel_val == background_color: 
                                is_valid_object = False
                                break
                            # Check for solid color core
                            if core_color == -1: # First core pixel found
                                core_color = pixel_val
                            elif pixel_val != core_color: # Core must be solid (same color)
                                is_valid_object = False
                                break
                            core_pixels.add((ir,ic)) # Add to core set if valid so far
                    if not is_valid_object:
                        break # Exit inner loop if invalid
                
                # Final check: ensure a core color was actually found (handles hollow shapes)
                if core_color == -1:
                     is_valid_object = False

                # If all checks pass, it's a valid object
                if is_valid_object:
                    # Extract the object's pixel data
                    subgrid = grid[min_r:max_r+1, min_c:max_c+1]
                    objects.append({
                        'bbox': (min_r, min_c, max_r, max_c),
                        'frame_color': frame_color,
                        'subgrid': subgrid
                    })
                    # Mark all pixels within the valid object's bounding box as visited globally
                    for ir in range(min_r, max_r + 1):
                        for ic in range(min_c, max_c + 1):
                            visited[ir, ic] = True
                else:
                     # Mark only the BFS-found pixels as visited globally if it wasn't a valid object
                    for fr, fc in frame_pixels:
                       visited[fr, fc] = True

    return objects


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_np)

    # Determine background color (assume top-left is representative)
    background_color = input_np[0, 0]

    # Find all qualifying framed objects
    objects_to_move = find_objects(input_np, background_color)

    # Process each identified object
    for obj in objects_to_move:
        min_r, min_c, max_r, max_c = obj['bbox']
        frame_color = obj['frame_color']
        subgrid = obj['subgrid']
        obj_h, obj_w = subgrid.shape

        # Erase the object from its original position in the output grid
        output_grid[min_r:max_r+1, min_c:max_c+1] = background_color

        # Calculate new horizontal position
        new_c = 0 # Default for azure
        if frame_color == 2: # Red frame moves right
            new_c = width - obj_w
        
        # Vertical position remains the same
        new_r = min_r

        # Draw the object at its new position
        # Ensure slicing bounds are within the grid dimensions (should be fine if width calculation is correct)
        end_r = new_r + obj_h
        end_c = new_c + obj_w
        
        # Check bounds before drawing (safety measure)
        if 0 <= new_r < height and end_r <= height and 0 <= new_c < width and end_c <= width:
             output_grid[new_r:end_r, new_c:end_c] = subgrid

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 5 5 5 8 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 8 5 5 5 8 0 0 0 2 1 1 1 2 0 8 8 8 8 8 0 0
0 8 5 5 5 8 0 0 0 2 1 1 1 2 0 8 3 3 3 8 0 0
0 8 8 8 8 8 0 0 0 2 1 1 1 2 0 8 3 3 3 8 0 0
0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 8 3 3 3 8 0 0
0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 2 9 9 9 2 0 0 0 0
0 0 0 0 2 2 2 2 2 0 0 0 0 2 9 9 9 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 2 0 0 0 0
2 2 2 2 2 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0
2 6 6 6 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 6 6 6 2 0 0 0 0 0 0 0 8 8 8 8 8 0 0 0 0 0
2 6 6 6 2 2 2 2 2 2 0 0 8 4 4 4 8 0 0 0 0 0
2 2 2 2 2 2 4 4 4 2 0 0 8 4 4 4 8 0 0 0 0 0
0 0 0 0 0 2 4 4 4 2 0 0 8 4 4 4 8 0 0 0 0 0
0 0 0 0 0 2 4 4 4 2 0 0 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 5 5 5 8 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
8 5 5 5 8 8 8 8 8 8 0 0 0 0 0 0 0 2 1 1 1 2
8 5 5 5 8 8 3 3 3 8 0 0 0 0 0 0 0 2 1 1 1 2
8 8 8 8 8 8 3 3 3 8 0 0 0 0 0 0 0 2 1 1 1 2
0 0 0 0 0 8 3 3 3 8 0 0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 8 8 8 8 8 0 0 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 2 6 6 6 2 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0 2 6 6 6 2 0 0 0 0 0
8 4 4 4 8 0 0 0 0 0 0 0 2 6 6 6 2 2 2 2 2 2
8 4 4 4 8 0 0 0 0 0 0 0 2 2 2 2 2 2 4 4 4 2
8 4 4 4 8 0 0 0 0 0 0 0 0 0 0 0 0 2 4 4 4 2
8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 2 4 4 4 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 5 5 5 8 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 2 1 1 1 2 0 0 0 0 0 0 0 0
8 3 3 3 8 0 0 0 0 2 1 1 1 2 0 0 0 0 0 0 0 0
8 3 3 3 8 0 0 0 0 2 1 1 1 2 0 0 0 0 0 0 0 0
8 3 3 3 8 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
8 8 8 8 8 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 2 3 3 3 2 0 0 0 0 0 0 0 0 2 9 9 9 2
0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 2
2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
2 6 6 6 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 4 4 4 8 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
8 4 4 4 8 2 4 4 4 2 0 0 0 0 0 0 0 0 0 0 0 0
8 4 4 4 8 2 4 4 4 2 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 2 4 4 4 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 220
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 90.90909090909092

## Example 2:
Input:
```
4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 2 5 5 5 2 4 4 4 4 4 4 4 4 4
4 4 8 8 8 8 8 4 2 5 5 5 2 4 2 2 2 2 2 4 4 4
4 4 8 9 9 9 8 4 2 5 5 5 2 4 2 3 3 3 2 4 4 4
4 4 8 9 9 9 8 4 2 2 2 2 2 4 2 3 3 3 2 4 4 4
4 4 8 9 9 9 8 4 4 4 4 4 4 4 2 3 3 3 2 4 4 4
4 4 8 8 8 8 8 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2 4
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2 4
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 8 8 8 8 8 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4
4 4 8 1 1 1 8 4 4 4 4 4 4 4 2 1 1 1 2 4 4 4
4 4 8 1 1 1 8 4 8 8 8 8 8 4 2 1 1 1 2 4 4 4
4 4 8 1 1 1 8 4 8 6 6 6 8 4 2 1 1 1 2 4 4 4
4 4 8 8 8 8 8 4 8 6 6 6 8 4 2 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 8 6 6 6 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 2 5 5 5 2 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 2 5 5 5 2 2 2 2 2 2
8 9 9 9 8 4 4 4 4 4 4 4 2 5 5 5 2 2 3 3 3 2
8 9 9 9 8 4 4 4 4 4 4 4 2 2 2 2 2 2 3 3 3 2
8 9 9 9 8 4 4 4 4 4 4 4 4 4 4 4 4 2 3 3 3 2
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 1 1 1 8 4 4 4 4 4 4 4 4 4 4 4 4 2 1 1 1 2
8 1 1 1 8 8 8 8 8 8 4 4 4 4 4 4 4 2 1 1 1 2
8 1 1 1 8 8 6 6 6 8 4 4 4 4 4 4 4 2 1 1 1 2
8 8 8 8 8 8 6 6 6 8 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 8 6 6 6 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Transformed Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2 5 5 5 2
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 9 9 9 8 4 4 4 4 4 4 4 4 4 4 4 4 2 3 3 3 2
8 9 9 9 8 4 4 4 4 4 4 4 4 4 4 4 4 2 3 3 3 2
8 9 9 9 8 4 4 4 4 4 4 4 4 4 4 4 4 2 3 3 3 2
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 1 1 1 8 4 4 4 4 4 4 4 4 4 4 4 4 2 1 1 1 2
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 1 1 1 2
8 6 6 6 8 4 4 4 4 4 4 4 4 4 4 4 4 2 1 1 1 2
8 6 6 6 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 6 6 6 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 79
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 32.64462809917353

## Example 3:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 1 1 1 1 1
1 1 1 8 8 8 8 8 1 1 1 1 2 3 3 3 2 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 2 3 3 3 2 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 2 3 3 3 2 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 2 2 2 2 2 1 1 1 1 1
1 1 1 8 8 8 8 8 1 1 1 1 8 8 8 8 8 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 2 2 2 2 2 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 2 5 5 5 2 1 1 1 1 1 8 8 8 8 8 1 1 1 1 1
1 1 2 5 5 5 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 2 5 5 5 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 2 2 2 2 2 1 1 1 1 1 1 1 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2 1 1 1
1 1 1 1 1 1 1 8 8 8 8 8 1 1 2 4 4 4 2 1 1 1
1 1 1 1 1 1 1 8 3 3 3 8 1 1 2 4 4 4 2 1 1 1
1 1 1 1 1 1 1 8 3 3 3 8 1 1 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 8 3 3 3 8 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 6 6 6 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 6 6 6 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 6 6 6 8 1 1 2 2 2 2 2 1 1 1 1 1
1 1 1 1 1 8 8 8 8 8 1 1 2 5 5 5 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Transformed Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
8 6 6 6 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
8 6 6 6 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
8 6 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 5 5 5 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 5 5 5 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 5 5 5 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Match: False
Pixels Off: 84
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 34.71074380165288
