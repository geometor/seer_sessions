import numpy as np
from collections import deque
import math

"""
Identifies distinct rectangular objects composed solely of azure (8) and green (3) pixels against a white (0) background in the input grid.
Counts the number of such valid objects found (n).

If n = 4:
  Selects the object with the highest ratio of green pixels to total pixels (green + azure).

If n = 3:
  Calculates the ratio of green pixels to azure pixels for each object (handling division by zero).
  Selects the object whose ratio is closest to 0.5 (minimizes abs(Ratio - 0.5)).
  (Note: Examples do not show ties for the minimum difference.)

The output grid is an exact copy of the selected object's pixels.
"""


def find_valid_objects(grid):
    """
    Finds all distinct, rectangular objects composed only of azure (8) and green (3) pixels.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a valid object
              and contains keys like 'grid', 'area', 'green_count', 'azure_count',
              'bbox' (min_r, min_c, max_r, max_c). Returns empty list if no valid objects found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    valid_objects = []
    valid_colors = {3, 8} # Green and Azure

    for r in range(rows):
        for c in range(cols):
            # If pixel is not background, not visited, and is a potentially valid color
            if grid[r, c] in valid_colors and not visited[r, c]:
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                is_potentially_valid = True # Assume valid colors until proven otherwise
                
                # Use BFS to find connected component of non-background pixels
                bfs_q = deque([(r,c)])
                current_component_visited_in_bfs = set([(r,c)]) # Track pixels visited in *this specific* BFS

                while bfs_q:
                    curr_r, curr_c = bfs_q.popleft()
                    component_coords.add((curr_r, curr_c))
                    
                    # Check if the pixel color is valid *for the object*
                    if grid[curr_r, curr_c] not in valid_colors:
                        is_potentially_valid = False # Mark component as having invalid colors

                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and \
                           (nr, nc) not in current_component_visited_in_bfs:
                            visited[nr, nc] = True # Mark globally visited
                            current_component_visited_in_bfs.add((nr,nc))
                            bfs_q.append((nr, nc))

                # After BFS, check if the identified component meets all criteria
                if is_potentially_valid:
                    height = max_r - min_r + 1
                    width = max_c - min_c + 1
                    expected_area = height * width
                    
                    # Check 1: Is the component perfectly rectangular (fills its bounding box)?
                    # Check 2: Does it contain only valid colors (already checked by is_potentially_valid)?
                    is_solid_rectangle = True
                    if len(component_coords) != expected_area:
                        is_solid_rectangle = False
                    else:
                        # Double check all pixels within the bbox are part of the component
                        # (Handles cases where BFS might not have reached a background pixel inside)
                        for br in range(min_r, max_r + 1):
                           for bc in range(min_c, max_c + 1):
                               if (br, bc) not in component_coords:
                                    # This indicates a hole or non-rectangular shape within the bbox
                                    is_solid_rectangle = False
                                    break
                               if grid[br, bc] == 0: # Should not happen if component_coords is correct, but safety check
                                   is_solid_rectangle = False
                                   break
                           if not is_solid_rectangle:
                               break
                    
                    if is_solid_rectangle:
                         # Extract the object grid and calculate properties
                        object_grid_data = grid[min_r:max_r+1, min_c:max_c+1]
                        green_count = np.sum(object_grid_data == 3)
                        azure_count = np.sum(object_grid_data == 8)

                        # Final verification: all extracted pixels must be green or azure
                        if green_count + azure_count == expected_area:
                            valid_objects.append({
                                'grid': object_grid_data.copy(),
                                'area': expected_area,
                                'green_count': green_count,
                                'azure_count': azure_count,
                                'bbox': (min_r, min_c, max_r, max_c),
                                'height': height,
                                'width': width
                            })
    return valid_objects


def select_object_rule_4(objects):
    """Selects object based on rule for n=4: max (green / total area)."""
    best_object = None
    max_ratio = -1.0

    for obj in objects:
        if obj['area'] == 0: 
             continue
        ratio = obj['green_count'] / obj['area']
        if ratio > max_ratio:
            max_ratio = ratio
            best_object = obj
        # Tie-breaking not explicitly defined; first object with max ratio is selected.

    return best_object

def select_object_rule_3(objects):
    """Selects object based on rule for n=3: min abs( (green/azure) - 0.5 )."""
    best_object = None
    min_diff = float('inf')
    target_ratio = 0.5

    for obj in objects:
        green_count = obj['green_count']
        azure_count = obj['azure_count']
        
        # Calculate ratio Green/Azure, handling division by zero
        if azure_count == 0:
            # If azure is 0, ratio is effectively infinite if green > 0, or 0 if green is also 0.
            # Infinite ratio is infinitely far from 0.5, unless green is also 0 (ratio=0).
            ratio = float('inf') if green_count > 0 else 0.0
        else:
            ratio = green_count / azure_count

        # Calculate difference from the target ratio 0.5
        diff = abs(ratio - target_ratio)

        # Update best object if this one is closer
        if diff < min_diff:
            min_diff = diff
            best_object = obj
        # Tie-breaking: Examples don't show ties. If diff == min_diff, the first object
        # encountered with that minimum difference remains selected.
            
    return best_object


def transform(input_grid_list):
    """
    Transforms the input grid based on identifying and selecting specific rectangular objects.

    Args:
        input_grid_list (list): The input grid as a list of lists.

    Returns:
        list: The output grid (pixels of the selected object) as a list of lists.
              Returns [[0]] if no object is selected or an error occurs.
    """
    input_grid = np.array(input_grid_list, dtype=int)

    # 1. Find all valid rectangular objects made of green (3) and azure (8)
    valid_objects = find_valid_objects(input_grid)
    num_objects = len(valid_objects)

    selected_object = None

    # 2. Apply selection logic based on the number of objects
    if num_objects == 4:
        selected_object = select_object_rule_4(valid_objects)
    elif num_objects == 3:
        selected_object = select_object_rule_3(valid_objects)
    # else: No rule defined for other counts based on examples

    # 3. Generate output grid from the selected object
    if selected_object:
        output_grid = selected_object['grid']
    else:
        # Handle case where no object was selected (e.g., unexpected object count)
        # Return a minimal 1x1 black grid as an indicator of failure/no selection.
        # print(f"Warning/Error: Found {num_objects} objects, expected 3 or 4, or no object met selection criteria.")
        output_grid = np.array([[0]], dtype=int) 

    return output_grid.tolist() # Convert back to list of lists