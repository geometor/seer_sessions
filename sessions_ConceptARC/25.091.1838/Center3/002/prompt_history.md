
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 1 0 3 3 3 3 0 0 2 2 2 0 0 0 0 1 0
0 1 0 3 0 0 3 0 0 2 0 2 0 0 0 0 1 0
0 1 0 3 0 0 3 0 0 2 2 2 0 0 0 0 1 0
0 1 0 3 3 3 3 0 0 0 0 0 0 0 0 0 1 0
0 1 0 0 0 0 0 4 4 4 4 0 0 0 0 0 1 0
0 1 0 0 0 0 0 4 0 0 4 0 0 0 0 0 1 0
0 1 0 0 0 0 0 4 0 0 4 0 0 0 0 0 1 0
0 1 0 0 0 0 0 4 4 4 4 7 7 7 7 7 1 0
0 1 0 0 0 0 0 0 0 0 0 7 0 0 0 7 1 0
0 1 0 0 0 0 0 8 8 8 8 7 0 0 0 7 1 0
0 1 0 0 0 0 0 8 0 0 8 7 0 0 0 7 1 0
0 1 0 0 0 0 0 8 0 0 8 7 7 7 7 7 1 0
0 1 0 0 0 0 0 8 8 8 8 0 0 0 0 0 1 0
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 4
4 0 0 4
4 0 0 4
4 4 4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 0 0
2 0 0 0 0 0 0 0 0 2 0 0
2 3 3 0 0 0 7 7 0 2 0 0
2 3 3 0 0 0 7 7 0 2 0 0
2 0 0 0 6 6 0 0 0 2 0 0
2 0 0 0 6 6 0 0 0 2 0 0
2 0 9 9 0 0 0 0 0 2 0 0
2 0 9 9 0 1 1 0 0 2 0 0
2 0 0 0 0 1 1 0 0 2 0 0
2 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6
6 6
```


## train_3

**input:**
```
0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 4 0 0 0 0 0 3 3 3 3 3 3 0 4
0 0 4 0 0 0 0 0 3 0 0 0 0 3 0 4
0 0 4 0 0 0 0 0 3 0 0 0 0 3 0 4
0 0 4 0 0 0 0 0 3 0 0 0 0 3 0 4
0 0 4 0 0 0 4 4 4 4 4 4 0 3 0 4
0 0 4 0 0 0 4 0 3 3 3 4 3 3 0 4
0 0 4 0 0 0 4 0 0 0 0 4 0 0 0 4
0 0 4 0 0 0 4 4 4 4 4 4 0 0 0 4
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 4 4 4
4 0 0 0 0 4
4 0 0 0 0 4
4 4 4 4 4 4
```

Okay, let's break down this task.

**Perception of Elements:**

1.  **Input Structure:** The input grids consist of a background (white, 0), an outer frame of a single color, and multiple distinct colored objects enclosed within the frame.
2.  **Object Types:** The objects within the frame appear to be geometric shapes, primarily rectangles. These rectangles can be solid (filled with a single color) or hollow (an outline of a single color with a background-colored interior). Some shapes might be more complex or irregular (like the green shape in example 3).
3.  **Output Structure:** The output is always a smaller grid representing one of the rectangular objects from the input grid, cropped to its bounding box.
4.  **Transformation Goal:** The core task is to identify *which* specific rectangular object from the input should be extracted to form the output.

**YAML Fact Document:**


```yaml
task_description: Extract a specific rectangular object from within a framed area in the input grid.

elements:
  - element: grid
    description: A 2D array of pixels with color values 0-9.
  - element: background
    property: color
    value: white (0)
    description: The typically most frequent color, surrounding other elements.
  - element: frame
    property: shape
    value: rectangle (usually 1 pixel thick)
    property: location
    value: outermost non-background border
    property: color
    value: variable (blue, red, yellow in examples)
    description: Encloses other objects. Not present in the output.
  - element: object
    property: location
    value: enclosed within the frame
    property: color
    value: variable (non-background)
    property: shape
    value: variable (contiguous pixels of the same color)
    description: Distinct items inside the frame.
  - element: perfect_rectangle_object
    description: An object forming a solid or hollow rectangle.
    property: type
    value: solid or hollow
    property: color
    value: single color
    property: area
    value: calculated from bounding box (width * height)
    relationship: subset of 'object'

transformation:
  input: grid
  output: subgrid (cropped perfect_rectangle_object)
  steps:
    - identify: background color (usually white=0).
    - identify: frame (outermost non-background border).
    - find: all contiguous non-background, non-frame objects inside the frame.
    - filter: keep only objects that are 'perfect rectangles' (solid or hollow with background-colored interior).
    - selection_logic:
        condition: if only one perfect rectangle exists
        action: select that rectangle.
        condition: if multiple perfect rectangles exist
        action:
          - calculate: bounding box area for each perfect rectangle.
          - determine: median area among them.
          - filter: keep only rectangles with the median area.
          - determine: median color index among the remaining rectangles.
          - select: the rectangle with the median color index.
    - final_step: extract the selected perfect rectangle object and crop it to its bounding box to create the output grid.

```


**Natural Language Program:**

1.  Identify the background color (typically white, color 0).
2.  Identify all contiguous groups of non-background pixels within the input grid.
3.  From these groups, identify the objects that form "perfect rectangles". A perfect rectangle can be either:
    *   A solid rectangle (a rectangular block of a single color).
    *   A hollow rectangle (a rectangular outline of a single color, at least one pixel thick, surrounding a rectangular area filled with the background color).
4.  Ignore any object that constitutes the outermost frame of the grid (if one exists). Focus only on objects fully contained within any such frame.
5.  Count the number of perfect rectangle objects identified in step 4.
6.  **If** exactly one perfect rectangle object was found, this object is the target.
7.  **Else (if multiple perfect rectangle objects were found):**
    a.  Calculate the bounding box area (width * height) for each perfect rectangle object.
    b.  Find the median value among these calculated areas.
    c.  Filter the list of perfect rectangles, keeping only those whose area matches the median area.
    d.  From this filtered list (of median-area rectangles), get the color index of each rectangle.
    e.  Find the median value among these color indices.
    f.  The target object is the perfect rectangle whose color index matches this median color index. (If there's an even number of items when finding the median color index, clarification might be needed - standard median definition usually averages the middle two, but ARC colors are discrete. Assume it takes the lower of the two middle indices if necessary, although examples suggest an odd number).
8.  Create the output grid by taking the selected target object and cropping the input grid to the exact bounding box of this object.
```python
import numpy as np
from collections import deque
import math

"""
Identify all contiguous non-background objects within the input grid.
Filter these objects to find only those that form 'perfect rectangles' (either solid rectangles or hollow rectangles with a background-colored interior).
If only one perfect rectangle is found, select it.
If multiple perfect rectangles are found:
1. Calculate the bounding box area for each perfect rectangle.
2. Find the median area among these rectangles.
3. Filter the rectangles to keep only those with the median area.
4. Get the color index of each remaining rectangle.
5. Find the median color index among these.
6. Select the rectangle with the median color index (if count is even, use the lower of the two middle indices).
Finally, crop the input grid to the bounding box of the selected perfect rectangle to produce the output grid.
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
              (min_r, min_c, max_r, max_c).
    """
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
                            
                objects.append({
                    'color': color,
                    'coords': obj_coords,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def is_perfect_rectangle(obj, grid, background_color=0):
    """
    Checks if an object forms a perfect solid or hollow rectangle.

    Args:
        obj (dict): The object dictionary from find_objects.
        grid (np.array): The input grid.
        background_color (int): The background color.

    Returns:
        bool: True if it's a perfect rectangle, False otherwise.
    """
    color = obj['color']
    coords = obj['coords']
    min_r, min_c, max_r, max_c = obj['bbox']
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    is_solid = True
    is_hollow = True

    # Check all cells within the bounding box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # Solid check
            if grid[r, c] != color:
                is_solid = False
            
            # Hollow check
            is_border = (r == min_r or r == max_r or c == min_c or c == max_c)
            if is_border:
                if (r, c) not in coords or grid[r, c] != color:
                    is_hollow = False
            else: # Interior
                if grid[r, c] != background_color:
                     is_hollow = False
                     
    # A hollow rectangle must have an interior (width/height > 2)
    if width <= 2 or height <= 2:
        is_hollow = False
        
    # An object made of only the pixels in coords could be hollow *only if*
    # the number of pixels matches the perimeter calculation.
    # Perimeter = 2 * (width + height) - 4 (for corners counted once)
    # But this doesn't account for thickness > 1.
    # Let's rely on the pixel checks within the bounding box.
    
    # Ensure all coords are within the bbox (should be by definition)
    # And ensure the checks covered all object pixels.
    
    # Must match either solid or hollow criteria
    return is_solid or is_hollow


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

def calculate_median_index(values):
    """Calculates the median value, returns lower middle for even counts."""
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n == 0:
        return None
    if n % 2 == 1:
        return sorted_values[n // 2]
    else:
        # For even count, choose the lower of the two middle elements
        return sorted_values[n // 2 - 1]

def transform(input_grid):
    """
    Transforms the input grid based on identifying and selecting a specific
    perfect rectangle object.
    """
    grid = np.array(input_grid)
    background_color = 0 # Assuming background is 0

    # 1. Find all non-background objects
    all_objects = find_objects(grid, ignore_color=background_color)
    
    # 2. Filter for perfect rectangles
    perfect_rectangles = []
    for obj in all_objects:
        if is_perfect_rectangle(obj, grid, background_color):
            perfect_rectangles.append(obj)
            
    # Handle case where no perfect rectangles are found
    if not perfect_rectangles:
        # Default or error behavior - returning empty for now
        # Based on examples, this shouldn't happen for valid inputs.
        return np.array([[]]) 

    selected_rectangle = None

    # 3. Select the target rectangle
    if len(perfect_rectangles) == 1:
        # If only one, select it
        selected_rectangle = perfect_rectangles[0]
    else:
        # If multiple, apply median logic
        
        # a. Calculate areas
        for rect in perfect_rectangles:
            rect['area'] = get_bounding_box_area(rect['bbox'])
        
        # b. Find median area
        areas = [rect['area'] for rect in perfect_rectangles]
        median_area = calculate_median_index(areas) 
        
        # c. Filter by median area
        median_area_rectangles = [rect for rect in perfect_rectangles if rect['area'] == median_area]
        
        # If filtering by area narrows it down to one, select it
        if len(median_area_rectangles) == 1:
             selected_rectangle = median_area_rectangles[0]
        else:
             # d. Get colors of remaining rectangles
             colors = [rect['color'] for rect in median_area_rectangles]
             
             # e. Find median color index
             median_color = calculate_median_index(colors)
             
             # f. Select the rectangle with the median color
             # If multiple rectangles have the median color and median area, 
             # the problem description doesn't specify tie-breaking.
             # We'll pick the first one found.
             for rect in median_area_rectangles:
                 if rect['color'] == median_color:
                     selected_rectangle = rect
                     break 

    # 4. Crop the grid to the selected rectangle's bounding box
    if selected_rectangle:
        output_grid = crop_grid(grid, selected_rectangle['bbox'])
    else:
        # Should not happen if logic is correct and input matches pattern
        output_grid = np.array([[]]) 

    return output_grid.tolist() # Return as list of lists

```
