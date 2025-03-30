import numpy as np
from collections import deque
import math

"""
Identifies distinct rectangular objects composed solely of azure (8) and green (3) pixels against a white (0) background in the input grid.
From these valid objects, selects the one with the highest ratio of green pixels to the total number of pixels (green + azure) in the object.
The output grid is an exact copy of the selected object's pixels.
If multiple objects share the maximum ratio, the behavior is currently undefined by the examples, but the implementation will select the first one encountered during the scan (typically top-to-bottom, left-to-right).
If no such valid objects are found, returns a 1x1 white (0) grid.
"""

def find_valid_objects(grid):
    """
    Finds all distinct, rectangular objects composed only of azure (8) and green (3) pixels.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a valid object
              and contains keys like 'grid', 'area', 'green_count', 'azure_count',
              'bbox' (min_r, min_c, max_r, max_c), 'height', 'width'. 
              Returns empty list if no valid objects found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    valid_objects = []
    valid_colors = {3, 8} # Green and Azure

    for r in range(rows):
        for c in range(cols):
            # If pixel is a potential object color and not visited yet
            if grid[r, c] in valid_colors and not visited[r, c]:
                component_coords = set()
                q = deque([(r, c)])
                # Need to track visited status *within this specific BFS* to correctly identify components
                # that might be adjacent but separated by background
                current_component_visited = set([(r,c)]) 
                visited[r,c] = True # Mark globally visited too
                
                min_r, min_c = r, c
                max_r, max_c = r, c
                is_potentially_valid_color_wise = True # Assume valid colors until proven otherwise

                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.add((curr_r, curr_c))

                    # Check if the pixel color is valid *for the object*
                    if grid[curr_r, curr_c] not in valid_colors:
                        is_potentially_valid_color_wise = False 
                        # We can potentially break early here if strict validity is needed during BFS,
                        # but it's safer to find the full component first, then validate.

                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors (4-directional) using the grid value check
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and \
                           (nr, nc) not in current_component_visited:
                            
                            # Check if the neighbor has a valid color *before* adding to queue
                            if grid[nr, nc] not in valid_colors:
                                is_potentially_valid_color_wise = False # Mark component as having invalid colors

                            visited[nr, nc] = True # Mark globally visited
                            current_component_visited.add((nr, nc))
                            q.append((nr, nc))

                # After BFS, check if the identified component meets all criteria
                if is_potentially_valid_color_wise:
                    height = max_r - min_r + 1
                    width = max_c - min_c + 1
                    expected_area = height * width

                    # Check 1: Is the component perfectly rectangular (fills its bounding box)?
                    # Check 2: Does it contain only valid colors (already checked by is_potentially_valid_color_wise)?
                    is_solid_rectangle = True
                    if len(component_coords) != expected_area:
                        is_solid_rectangle = False
                    else:
                        # Double check all pixels within the bbox are part of the component
                        # and have the correct color. This ensures no background pixels inside
                        # the bounding box and confirms the shape.
                        for br in range(min_r, max_r + 1):
                           for bc in range(min_c, max_c + 1):
                               if (br, bc) not in component_coords:
                                    is_solid_rectangle = False
                                    break
                               # This check should be redundant due to is_potentially_valid_color_wise
                               # and the BFS condition `grid[nr, nc] != 0`, but kept for safety.
                               if grid[br, bc] not in valid_colors: 
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
                        # and their sum must equal the area.
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
                        # else: # Debugging - print if counts don't match area
                        #     print(f"Warning: Object at {min_r},{min_c} failed final count check. G={green_count}, A={azure_count}, Area={expected_area}")

    return valid_objects


def select_object(objects):
    """
    Selects the object with the highest ratio of green pixels to total area (G/T).

    Args:
        objects (list): A list of valid object dictionaries found by find_valid_objects.

    Returns:
        dict: The dictionary of the selected object, or None if the input list is empty.
    """
    if not objects:
        return None

    best_object = None
    max_ratio = -1.0 # Initialize with a value lower than any possible ratio (0)

    for obj in objects:
        # Prevent division by zero if an object somehow has zero area (shouldn't happen with valid objects)
        if obj['area'] == 0: 
             continue 
        
        # Calculate the ratio of green pixels to total area
        ratio = obj['green_count'] / obj['area']

        # Update best object if this one has a higher ratio
        if ratio > max_ratio:
            max_ratio = ratio
            best_object = obj
        # Tie-breaking: If ratio == max_ratio, the first object encountered with 
        # that maximum ratio remains selected (based on scan order in find_valid_objects).

    return best_object


def transform(input_grid_list):
    """
    Transforms the input grid by finding rectangular green/azure objects 
    and selecting the one with the highest density of green pixels.

    Args:
        input_grid_list (list): The input grid as a list of lists.

    Returns:
        list: The output grid (pixels of the selected object) as a list of lists.
              Returns [[0]] if no valid object is found or selected.
    """
    input_grid = np.array(input_grid_list, dtype=int)

    # 1. Find all valid rectangular objects made of green (3) and azure (8)
    valid_objects = find_valid_objects(input_grid)
    
    # 2. Select the object based on the maximum green density rule
    selected_object = select_object(valid_objects)

    # 3. Generate output grid from the selected object
    if selected_object:
        output_grid = selected_object['grid']
    else:
        # Handle case where no valid object was found
        output_grid = np.array([[0]], dtype=int) # Return 1x1 white grid

    return output_grid.tolist() # Convert back to list of lists
