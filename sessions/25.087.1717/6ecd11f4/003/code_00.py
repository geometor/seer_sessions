import numpy as np
from collections import deque

"""
Transformation Rule:
1. Find the largest contiguous object composed of a single non-white color in the input grid. Let its color be `FilterColor`.
2. Identify all other non-white pixels in the input grid (pixels not belonging to the largest object). Let this set of coordinates be `SourceCoords`.
3. Find the smallest bounding box that encloses all pixels in `SourceCoords`. Let the top-left corner be (min_r, min_c) and the dimensions be (height, width).
4. Determine the set of `TargetColors` to be filtered out based on the `FilterColor`:
    - If `FilterColor` is green (3), the `TargetColors` are {blue (1), azure (8), maroon (9)}.
    - If `FilterColor` is blue (1), the `TargetColors` are {blue (1), red (2), yellow (4), maroon (9)}.
    - If `FilterColor` is azure (8), the `TargetColors` are {blue (1), green (3), gray (5), orange (7)}.
    - Otherwise, `TargetColors` is an empty set.
5. Create a new output grid with dimensions (height, width), initialized with white (0).
6. Iterate through each coordinate `(r, c)` in `SourceCoords`:
    - Get the color `CurrentColor` from the input grid at `(r, c)`.
    - Check if `CurrentColor` is present in the set of `TargetColors`.
    - If `CurrentColor` is *not* in `TargetColors`, calculate the position in the output grid: `out_r = r - min_r`, `out_c = c - min_c`. Set the output grid cell `output_grid[out_r, out_c]` to `CurrentColor`.
7. Return the generated output grid.
"""


def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid using Breadth-First Search.
    Args:
        grid (np.array): Input grid.
    Returns:
        list: A list of objects, where each object is a dictionary containing
              'color', 'coords' (set of (r, c) tuples), and 'size'.
              Excludes objects with color 0 (white). Objects are found using 4-connectivity.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If the cell hasn't been visited and is not white
            if (r, c) not in visited and grid[r, c] != 0:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                
                # Start BFS from this cell
                while q:
                    row, col = q.popleft()
                    
                    # Check if the current cell matches the starting color
                    # This check ensures we only grow the object with the same color
                    if grid[row, col] == color:
                        obj_coords.add((row, col))
                        
                        # Check neighbors (4-connectivity: up, down, left, right)
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = row + dr, col + dc
                            
                            # Check if the neighbor is within bounds, not visited, and has the same color
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               (nr, nc) not in visited and grid[nr, nc] == color:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                    # Mark as visited even if color doesn't match, to prevent reprocessing starting points
                    # that might be adjacent to different colored objects already visited.
                    # However, the primary mechanism to avoid re-processing is the initial check.
                    # Adding the starting point here ensures it's marked visited if it was a single pixel object.
                    visited.add((r,c))

                # Add the found object if it has any coordinates
                if obj_coords:
                     objects.append({
                         'color': color,
                         'coords': obj_coords,
                         'size': len(obj_coords)
                     })
                     # Ensure all coordinates of the found object are marked as visited
                     # This is slightly redundant as BFS should have marked them, but safe.
                     visited.update(obj_coords) 

    return objects

def get_bounding_box(coords):
    """
    Calculates the bounding box for a set of coordinates.
    Args:
        coords (set): A set of (row, col) tuples.
    Returns:
        tuple: (min_row, min_col, max_row, max_col), or None if coords is empty.
    """
    if not coords:
        return None
    
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Applies the color filtering transformation based on the largest object's color.
    Filters a specific set of colors from the remaining non-white pixels,
    cropping the result to the bounding box of those remaining pixels.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # 1. Find all non-white objects
    objects = find_objects(input_array)
    
    # Handle edge case: no non-white objects found
    if not objects:
        # Return an empty grid represented as a list of lists
        return [[]] 
        
    # Find the largest object based on the number of pixels
    largest_object = max(objects, key=lambda obj: obj['size'])
    filter_color = largest_object['color']
    large_object_coords = largest_object['coords']

    # 2. Identify coordinates of the source pixels (all non-white pixels NOT in the largest object)
    all_non_white_coords = set()
    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] != 0:
                all_non_white_coords.add((r, c))
                
    source_coords = all_non_white_coords - large_object_coords

    # Handle edge case: only the largest object exists, no other non-white pixels
    if not source_coords:
         # Return an empty grid represented as a list of lists
        return [[]] 

    # 3. Get the bounding box of the source coordinates
    min_r, min_c, max_r, max_c = get_bounding_box(source_coords)
    
    # Calculate output dimensions
    out_height = max_r - min_r + 1
    out_width = max_c - min_c + 1

    # 4. Determine TargetColors based on FilterColor
    target_color_map = {
        3: {1, 8, 9},      # Green -> Filter Blue, Azure, Maroon
        1: {1, 2, 4, 9},  # Blue -> Filter Blue, Red, Yellow, Maroon
        8: {1, 3, 5, 7}   # Azure -> Filter Blue, Green, Gray, Orange
    }
    # Get the set of colors to filter, or an empty set if the filter_color is not a key
    target_colors = target_color_map.get(filter_color, set()) 

    # 5. Create the output grid, initialized with white (0)
    output_grid = np.zeros((out_height, out_width), dtype=int)
    
    # 6. Populate the output grid by copying non-filtered source pixels
    for r, c in source_coords:
        current_color = input_array[r, c]
        # Check if the color should be kept (i.e., not in target_colors)
        if current_color not in target_colors:
            # Calculate the position in the output grid relative to the bounding box origin
            out_r = r - min_r
            out_c = c - min_c
            # Place the color in the output grid
            output_grid[out_r, out_c] = current_color

    # 7. Return the result as a list of lists
    return output_grid.tolist()