```python
import numpy as np
from collections import deque

"""
Transformation Rule Description:
1. Identify the border color (Yellow/4) and the background color (White/0).
2. Find all connected components (objects) within the input grid that consist of colors other than the border color.
3. Determine which of these objects are fully enclosed by the border color. An object is enclosed if none of its pixels touch the grid boundary, and all pixels immediately adjacent (up, down, left, right) to the object's pixels are either part of the object itself or are the border color.
4. Collect the color, coordinates, and bounding box (min/max row/col) of each enclosed object.
5. Examine the colors of all the identified enclosed objects.
6. Selection Rule:
    a. If the color Blue (1) is *not* present among the colors of the enclosed objects, select the enclosed object whose color is Azure (8).
    b. If the color Blue (1) *is* present among the colors of the enclosed objects, select the object whose bounding box top-left corner (min_row, min_col) has the minimum row index, and then the minimum column index in case of a tie in row index.
7. Take the selected object's color and coordinates.
8. Create the output grid: its dimensions should match the dimensions of the selected object's bounding box. Initialize this grid with the background color (White/0).
9. Map the pixels from the selected object's coordinates onto the output grid, preserving their color and relative positions within the bounding box. The pixel at `(r, c)` in the input grid (which belongs to the selected object) should be placed at `(r - min_row, c - min_col)` in the output grid, where `min_row` and `min_col` are from the object's bounding box.
"""

BORDER_COLOR = 4
BACKGROUND_COLOR = 0
BLUE = 1
AZURE = 8

def find_objects(grid):
    """
    Finds all connected components (objects) of non-border colors.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'color': The color of the object.
              'coords': A set of (row, col) tuples for the object's pixels.
              'bbox': A tuple (min_r, min_c, max_r, max_c) for the bounding box.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # Start BFS only if it's a non-border pixel and not visited yet
            if grid[r, c] != BORDER_COLOR and not visited[r, c]:
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                object_color = grid[r, c]
                min_r, min_c, max_r, max_c = r, c, r, c

                # Perform BFS to find all connected pixels of the same color
                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.add((curr_r, curr_c))

                    # Update bounding box dynamically
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check neighbor validity: within bounds, same color, not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == object_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                        # Also mark border neighbors as visited in the context of finding non-border objects
                        # This prevents starting a new BFS from a border pixel later
                        # if 0 <= nr < height and 0 <= nc < width and grid[nr, nc] == BORDER_COLOR:
                        #     visited[nr, nc] = True # Let's rethink this, it might mask valid objects starting near borders

                objects.append({
                    'color': object_color,
                    'coords': component_coords,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
                
    # After finding all potential objects, need to correct potential BFS overlaps if objects touch border
    # Revisit visited logic if issues arise
    return objects


def is_enclosed(grid, component_coords):
    """
    Checks if a component is fully enclosed by the border color.

    Args:
        grid (np.ndarray): The input grid.
        component_coords (set): A set of (row, col) tuples representing the component.

    Returns:
        bool: True if the component is enclosed, False otherwise.
    """
    height, width = grid.shape
    if not component_coords:
        return False # Cannot be enclosed if empty

    for r, c in component_coords:
        # Check all 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # If the neighbor is not part of the component itself...
                if (nr, nc) not in component_coords:
                    # ...it MUST be the border color for the component to be enclosed
                    if grid[nr, nc] != BORDER_COLOR:
                        return False
            else:
                # If a neighbor is outside the grid bounds, the component touches the edge
                # and is therefore not enclosed.
                return False

    # If all boundary checks passed for all coordinates in the component
    return True

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the output grid.
        Raises ValueError if the required object cannot be found based on the rules.
    """
    height, width = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool)
    enclosed_objects_data = []

    # 1 & 2: Find all connected components (objects) of non-border colors.
    # Using BFS approach similar to previous code, but ensuring correct grouping.
    for r in range(height):
        for c in range(width):
            if grid[r, c] != BORDER_COLOR and not visited[r, c]:
                object_color = input_grid[r, c]
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c, max_r, max_c = r, c, r, c
                is_monochromatic = True # Assume initially

                # Perform BFS
                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.add((curr_r, curr_c))
                    
                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        if 0 <= nr < height and 0 <= nc < width and not visited[nr, nc]:
                           # Only add neighbors of the *same* color to this component's queue
                           if input_grid[nr,nc] == object_color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                           # Note: We are *not* checking for non-border here, just same color as start
                           # This ensures monochromatic objects are found correctly.

                # 3 & 4: Check if the found object is enclosed and store its data.
                # Note: The task implies enclosed objects are monochromatic.
                if is_enclosed(input_grid, component_coords):
                     enclosed_objects_data.append({
                        'color': object_color,
                        'coords': component_coords,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'top_left': (min_r, min_c) # Store for easier sorting later
                    })

    # Check if any enclosed objects were found
    if not enclosed_objects_data:
        raise ValueError("No objects enclosed by the border color were found.")

    # 5: Examine the colors of all enclosed objects.
    enclosed_colors = {obj['color'] for obj in enclosed_objects_data}

    # 6: Apply the selection rule.
    selected_object = None
    if BLUE not in enclosed_colors:
        # Rule 6a: Blue is absent, select Azure.
        for obj in enclosed_objects_data:
            if obj['color'] == AZURE:
                selected_object = obj
                break
        if selected_object is None:
             raise ValueError(f"Rule conflict: Blue ({BLUE}) is absent, but Azure ({AZURE}) object not found among enclosed objects.")
    else:
        # Rule 6b: Blue is present, select the top-leftmost object.
        # Sort by top_left: first by row (index 0), then by column (index 1)
        enclosed_objects_data.sort(key=lambda x: x['top_left'])
        if enclosed_objects_data: # Should always be true if Blue is present
             selected_object = enclosed_objects_data[0]
        # No explicit error needed here as sort handles empty list okay,
        # but we should have found Blue earlier if the list was empty.

    if selected_object is None:
         # This should ideally not be reached if the logic for rules 6a/6b covers all cases
         raise ValueError("Could not select an object based on the rules.")

    # 7, 8, 9: Create the output grid from the selected object.
    sel_color = selected_object['color']
    sel_coords = selected_object['coords']
    min_r, min_c, max_r, max_c = selected_object['bbox']

    output_h = max_r - min_r + 1
    output_w = max_c - min_c + 1
    output_grid = np.full((output_h, output_w), BACKGROUND_COLOR, dtype=int)

    for r, c in sel_coords:
        output_r = r - min_r
        output_c = c - min_c
        if 0 <= output_r < output_h and 0 <= output_c < output_w:
             output_grid[output_r, output_c] = sel_color
        else:
             # This indicates an issue with coordinate mapping or bounding box calculation
             print(f"Warning: Coordinate ({r},{c}) mapped outside output grid bounds ({output_h}x{output_w})")


    return output_grid
```