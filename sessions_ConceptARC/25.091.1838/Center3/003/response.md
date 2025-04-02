```python
import numpy as np
from collections import deque
import math

"""
Transforms an input grid by identifying all 'perfect rectangle' objects (both solid and hollow), 
then selecting one based on specific criteria, and finally cropping the grid to the bounding box 
of the selected rectangle.

Selection Logic:
1. Find all perfect rectangles (solid or hollow).
2. If exactly one hollow perfect rectangle exists, select it.
3. Otherwise (zero or multiple hollow rectangles):
    a. Calculate the bounding box area of all perfect rectangles.
    b. Find the median area.
    c. Filter for rectangles with the median area.
    d. If only one remains, select it.
    e. If multiple remain, find the median color among them.
    f. Select the rectangle with the median color (using the lower index for ties).
"""

def find_objects(grid, ignore_color=0):
    """
    Finds contiguous objects of colors other than ignore_color.

    Args:
        grid (np.array): The input grid.
        ignore_color (int): The color to ignore (usually background).

    Returns:
        list: A list of dictionaries, each representing an object with
              'color', 'coords' (set of (r, c) tuples), and 'bbox'
              (min_r, min_c, max_r, max_c). Returns empty list if grid is empty.
    """
    if grid.size == 0:
        return []
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != ignore_color:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and grid[nr, nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                if obj_coords: # Only add if pixels were found
                    objects.append({
                        'color': color,
                        'coords': obj_coords,
                        'bbox': (min_r, min_c, max_r, max_c)
                    })
    return objects

def is_perfect_rectangle_refined(obj, grid, background_color=0):
    """
    Checks if an object forms a perfect solid or hollow rectangle.

    Args:
        obj (dict): The object dictionary from find_objects.
        grid (np.array): The input grid.
        background_color (int): The background color.

    Returns:
        tuple: (bool, str or None) indicating (is_perfect, type), where type
               is 'solid', 'hollow', or None.
    """
    color = obj['color']
    coords = obj['coords']
    min_r, min_c, max_r, max_c = obj['bbox']
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # --- Solid Check ---
    is_solid = True
    if len(coords) != height * width: # Quick check: pixel count must match area
        is_solid = False
    else:
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if grid[r, c] != color:
                    is_solid = False
                    break
            if not is_solid:
                break
                
    if is_solid:
        return (True, 'solid')

    # --- Hollow Check (only if not solid) ---
    # Basic requirement: must have space for an interior
    if width <= 2 or height <= 2:
        return (False, None)

    is_hollow = True
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            is_border = (r == min_r or r == max_r or c == min_c or c == max_c)
            
            if is_border:
                # Border pixels must have the object's color
                if grid[r, c] != color:
                    is_hollow = False
                    break
                # Border pixels must be part of the found object's coordinates
                # This helps distinguish from adjacent noise.
                if (r,c) not in coords:
                     is_hollow = False
                     break
            else: # Interior pixels
                # Interior pixels must have the background color
                if grid[r, c] != background_color:
                    is_hollow = False
                    break
                # Interior pixels must NOT be part of the found object's coordinates
                # (Reinforces the background color check)
                if (r,c) in coords:
                    is_hollow = False
                    break
        if not is_hollow:
            break # Break outer loop if inner check failed

    if is_hollow:
        # Final check: ensure all original coords were on the border
        all_coords_on_border = True
        for r_obj, c_obj in coords:
             if not (r_obj == min_r or r_obj == max_r or c_obj == min_c or c_obj == max_c):
                 all_coords_on_border = False
                 break
        if all_coords_on_border:
             return (True, 'hollow')
        else:
             # If some object pixels were found inside, it's not a perfect hollow rect
             return (False, None)


    # If neither solid nor hollow criteria met
    return (False, None)


def get_bounding_box_area(bbox):
    """Calculates the area of a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height * width

def crop_grid(grid, bbox):
    """Extracts a subgrid defined by a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    return grid[min_r:max_r+1, min_c:max_c+1]

def calculate_median_value(values):
    """Calculates the median value, returns lower middle for even counts."""
    if not values: # Handle empty list
        return None
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 1:
        # Odd number of elements: return the middle one
        return sorted_values[n // 2]
    else:
        # Even number of elements: return the lower of the two middle elements
        return sorted_values[n // 2 - 1]

def transform(input_grid):
    """
    Transforms the input grid based on identifying and selecting a specific
    perfect rectangle object using the refined logic.
    """
    grid = np.array(input_grid)
    if grid.size == 0:
        return [] # Handle empty input
        
    background_color = 0 # Assume background is 0

    # 1. Find all non-background objects
    all_objects = find_objects(grid, ignore_color=background_color)
    
    # 2. Filter for perfect rectangles and classify them
    perfect_rectangles = []
    hollow_rectangles = []
    for obj in all_objects:
        is_perfect, rect_type = is_perfect_rectangle_refined(obj, grid, background_color)
        if is_perfect:
            obj['type'] = rect_type
            obj['area'] = get_bounding_box_area(obj['bbox'])
            perfect_rectangles.append(obj)
            if rect_type == 'hollow':
                hollow_rectangles.append(obj)
            
    # Handle case where no perfect rectangles are found
    if not perfect_rectangles:
        # Based on examples, this shouldn't happen for valid inputs.
        # Return empty list of lists as per ARC format for empty grid.
        return [[]] if grid.ndim > 1 else [] 

    selected_rectangle = None

    # 3. Selection Logic
    # Rule 1: Prioritize unique hollow rectangle
    if len(hollow_rectangles) == 1:
        selected_rectangle = hollow_rectangles[0]
    else:
        # Rule 2: Apply median logic (area, then color) to *all* perfect rectangles
        
        # a. Calculate median area using all perfect rectangles
        areas = [rect['area'] for rect in perfect_rectangles]
        median_area = calculate_median_value(areas) 
        
        # b. Filter by median area
        median_area_rectangles = [rect for rect in perfect_rectangles if rect['area'] == median_area]
        
        # c. If only one matches median area, select it
        if len(median_area_rectangles) == 1:
             selected_rectangle = median_area_rectangles[0]
        elif len(median_area_rectangles) > 1:
             # d. Multiple match median area: Find median color among them
             colors = [rect['color'] for rect in median_area_rectangles]
             median_color = calculate_median_value(colors)
             
             # e. Select the first rectangle matching median area AND median color
             for rect in median_area_rectangles:
                 if rect['color'] == median_color:
                     selected_rectangle = rect
                     break 
        # If median_area_rectangles is empty somehow (shouldn't happen if median calculated correctly)
        # or if no rectangle matches the median color (also shouldn't happen), 
        # selected_rectangle remains None initially. If perfect_rectangles was not empty,
        # this implies an issue, but let's select the first perfect rectangle as a fallback.
        if selected_rectangle is None and perfect_rectangles:
             selected_rectangle = perfect_rectangles[0]


    # 4. Crop the grid to the selected rectangle's bounding box
    if selected_rectangle:
        output_grid = crop_grid(grid, selected_rectangle['bbox'])
    else:
        # Fallback if no rectangle could be selected (e.g., only non-rect objects found)
         return [[]] if grid.ndim > 1 else []

    return output_grid.tolist() # Return as list of lists
```