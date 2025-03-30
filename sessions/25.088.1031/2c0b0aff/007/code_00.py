import numpy as np
from collections import deque
import math

"""
Identifies distinct, solid, rectangular objects composed solely of azure (8) and green (3) pixels against a white (0) background in the input grid.
From these valid objects, selects the one with the highest ratio of green pixels to the total number of pixels (green + azure) within the object's bounding box.
The output grid is an exact copy of the selected object's pixels.
If multiple objects share the maximum ratio, the first one encountered during the scan (typically top-to-bottom, left-to-right) is selected.
If no such valid objects are found, returns a 1x1 white (0) grid.

Note: This rule correctly predicts the output for 3 out of 4 provided training examples. It fails on Example 4, where the object with the *minimum* green ratio is the expected output. Further refinement of the selection criteria might be needed if this discrepancy represents a consistent pattern rather than an anomaly.
"""

def find_valid_objects(grid):
    """
    Finds all distinct, solid, rectangular objects composed only of azure (8) and green (3) pixels.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a valid object
              and contains keys: 'grid', 'area', 'green_count', 'azure_count',
              'green_ratio', 'bbox' (min_r, min_c, max_r, max_c), 'height', 'width'.
              Returns empty list if no valid objects found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    valid_objects = []
    valid_colors = {3, 8} # Green and Azure

    for r in range(rows):
        for c in range(cols):
            # Start BFS if we find a potential object pixel that hasn't been visited
            if grid[r, c] in valid_colors and not visited[r, c]:
                component_coords = set()
                q = deque([(r, c)])
                # Use a set for visited nodes *within this specific BFS*
                current_component_visited = set([(r,c)])
                visited[r,c] = True # Mark globally visited

                min_r, min_c = r, c
                max_r, max_c = r, c
                # Assume component is valid color-wise until a non-valid color is found
                is_valid_colors_only = True

                # Perform BFS to find all connected non-background pixels
                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.add((curr_r, curr_c))

                    # Check if the current pixel's color is valid (3 or 8)
                    if grid[curr_r, curr_c] not in valid_colors:
                        is_valid_colors_only = False
                        # Continue BFS to mark the entire connected component as visited,
                        # but know it's not a candidate object due to invalid color.

                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds, if it's not background (0), and not visited in this BFS
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and \
                           (nr, nc) not in current_component_visited:

                            # Mark globally visited and locally for this component
                            visited[nr, nc] = True
                            current_component_visited.add((nr, nc))
                            q.append((nr, nc))

                # After BFS, validate the found component
                if is_valid_colors_only:
                    height = max_r - min_r + 1
                    width = max_c - min_c + 1
                    expected_area = height * width

                    # Check 1: Is the component perfectly rectangular?
                    # Does the number of pixels found match the bounding box area?
                    is_solid_rectangle = (len(component_coords) == expected_area)

                    # Check 2: (Double-check) Ensure all pixels *within* the bounding box
                    # belong to the component (ruling out holes or background pixels inside).
                    if is_solid_rectangle:
                         for br in range(min_r, max_r + 1):
                            for bc in range(min_c, max_c + 1):
                                if (br, bc) not in component_coords:
                                    # Found a pixel within bbox not in component
                                    is_solid_rectangle = False
                                    break
                                # Redundant check as is_valid_colors_only already checked this
                                # if grid[br, bc] not in valid_colors:
                                #    is_solid_rectangle = False
                                #    break
                            if not is_solid_rectangle:
                                break

                    # If it's a solid rectangle of only valid colors, add it
                    if is_solid_rectangle:
                        object_grid_data = grid[min_r:max_r+1, min_c:max_c+1]
                        green_count = np.sum(object_grid_data == 3)
                        azure_count = np.sum(object_grid_data == 8)

                        # Final verification: counts must match area
                        if green_count + azure_count == expected_area:
                             green_ratio = green_count / expected_area if expected_area > 0 else 0.0
                             valid_objects.append({
                                'grid': object_grid_data.copy(),
                                'area': expected_area,
                                'green_count': green_count,
                                'azure_count': azure_count,
                                'green_ratio': green_ratio,
                                'bbox': (min_r, min_c, max_r, max_c),
                                'height': height,
                                'width': width
                             })

    return valid_objects


def select_object(objects):
    """
    Selects the object with the highest ratio of green pixels to total area (G/T).
    Handles tie-breaking by selecting the first object encountered with the max ratio.

    Args:
        objects (list): A list of valid object dictionaries from find_valid_objects.

    Returns:
        dict: The dictionary of the selected object, or None if the list is empty.
    """
    if not objects:
        return None

    best_object = None
    # Initialize max_ratio to a value lower than any possible ratio (0.0)
    max_ratio = -1.0

    # Iterate through found objects
    for obj in objects:
        # If this object's ratio is higher than the current max, update
        if obj['green_ratio'] > max_ratio:
            max_ratio = obj['green_ratio']
            best_object = obj
        # If ratio is equal, the first object encountered (implicit from list order) remains best_object

    return best_object


def transform(input_grid_list):
    """
    Transforms the input grid based on the identified rule.

    Args:
        input_grid_list (list): The input grid as a list of lists.

    Returns:
        list: The output grid (pixels of the selected object) as a list of lists.
              Returns [[0]] if no valid object is found or selected.
    """
    # Convert list of lists to numpy array for easier processing
    input_grid = np.array(input_grid_list, dtype=int)

    # 1. Find all valid rectangular objects made of green (3) and azure (8)
    valid_objects = find_valid_objects(input_grid)

    # 2. Select the object based on the maximum green density rule
    selected_object = select_object(valid_objects)

    # 3. Generate output grid from the selected object
    if selected_object:
        # Get the grid data from the selected object dictionary
        output_grid = selected_object['grid']
    else:
        # Handle case where no valid object was found or selected
        # Return a default 1x1 white grid as specified
        output_grid = np.array([[0]], dtype=int)

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()