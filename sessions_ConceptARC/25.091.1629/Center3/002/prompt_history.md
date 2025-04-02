
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

Okay, let's analyze the task examples.

**Perception of Elements:**

1.  **Input Structure:** Each input is a grid containing multiple distinct regions (objects) of different colors. There's usually a background color (white, 0) and often a frame or border object surrounding other objects.
2.  **Objects:** The core elements are contiguous blocks of single colors. Some of these objects form simple geometric shapes, particularly solid rectangles. Other objects might have holes or irregular shapes (like the borders).
3.  **Output Structure:** Each output is a smaller grid representing a solid rectangle.
4.  **Transformation:** The transformation involves selecting one specific object from the input grid and presenting it as the output. The selection criteria seem based on the object's shape (being a solid rectangle) and its properties (area, color) relative to other objects and potentially the border color.

**YAML Facts:**


```yaml
Task: Extract a specific rectangular object from the input grid.

Input_Features:
  - Grid: 2D array of pixels (colors 0-9).
  - Objects: Contiguous areas of the same non-white color.
  - Properties:
    - Color: The integer value (1-9) of the pixels in an object.
    - Shape: Geometric form of the object (rectangle, irregular, etc.).
    - Solid_Rectangle: An object whose bounding box contains only pixels of its own color.
    - Area: Number of pixels in an object (or its bounding box).
    - Position: Coordinates (row, column) of the object or its bounding box.
    - Border_Color: The color of the largest non-white object adjacent to the grid edges.

Output_Features:
  - Grid: A 2D array representing the selected object.
  - Content: A single, solid, monochromatic rectangle extracted from the input.

Relationships_and_Rules:
  - Selection_Criteria: Identify all solid, monochromatic, non-white rectangles in the input.
  - Primary_Rule: Select the solid rectangle with the largest area.
  - Tie_Breaking_Rule_1: If multiple rectangles share the largest area, check if any have the same color as the identified Border_Color. If one does, select it.
  - Tie_Breaking_Rule_2: If multiple rectangles share the largest area and none match the Border_Color, find the median color index among the tied rectangles. Select the rectangle with that median color index.

Examples_Analysis:
  - train_1:
    - Border_Color: Blue(1).
    - Solid_Rectangles: Yellow(4) [Area 16].
    - Max_Area: 16. Only Yellow qualifies.
    - Output: Yellow(4) rectangle.
  - train_2:
    - Border_Color: Red(2).
    - Solid_Rectangles: Green(3)[4], Orange(7)[4], Magenta(6)[4], Maroon(9)[4], Blue(1)[4].
    - Max_Area: 4. All five tie.
    - Border_Match: None match Red(2).
    - Tied_Colors: [1, 3, 6, 7, 9]. Median is 6.
    - Output: Magenta(6) rectangle.
  - train_3:
    - Border_Color: Yellow(4).
    - Solid_Rectangles: Yellow(4)[Area 24], smaller green shapes (not solid rectangles or smaller area).
    - Max_Area: 24. Only Yellow qualifies.
    - Output: Yellow(4) rectangle.
```


**Natural Language Program:**

1.  Identify the 'border color' by finding the color (excluding white/0) of the largest object that touches the edges of the input grid.
2.  Scan the input grid to find all distinct contiguous objects made of a single color (excluding white/0).
3.  For each object found, determine its bounding box.
4.  Check if the object is a 'solid rectangle' by verifying that all pixels within its bounding box have the same color as the object itself.
5.  Calculate the area (width * height) of each solid rectangle.
6.  Identify the maximum area found among all solid rectangles.
7.  Filter the list of solid rectangles to keep only those with the maximum area.
8.  If only one solid rectangle has the maximum area, select this rectangle as the target.
9.  If multiple solid rectangles share the maximum area (a tie):
    a.  Check if any of the tied rectangles have the same color as the 'border color' identified in step 1.
    b.  If exactly one tied rectangle matches the border color, select that rectangle as the target.
    c.  If none of the tied rectangles match the border color, collect the color indices of all the tied rectangles. Find the median value among these indices. Select the rectangle whose color index is this median value as the target. (Assumption: If there's an even number of tied colors, a consistent rule like choosing the lower median might be needed, but current examples suggest an odd number).
10. Create the output grid containing only the pixels of the selected target rectangle.
```python
"""
1. Identify the 'border color' by finding the color (excluding white/0) of the largest object that touches the edges of the input grid.
2. Scan the input grid to find all distinct contiguous objects made of a single color (excluding white/0).
3. For each object found, determine its bounding box.
4. Check if the object is a 'solid rectangle' by verifying that the number of pixels in the object equals the area of its bounding box.
5. Calculate the area (width * height) of the bounding box for each solid rectangle.
6. Identify the maximum area found among all solid rectangles.
7. Filter the list of solid rectangles to keep only those with the maximum area.
8. If only one solid rectangle has the maximum area, select this rectangle.
9. If multiple solid rectangles share the maximum area (a tie):
    a. Check if any of the tied rectangles have the same color as the 'border color'.
    b. If exactly one tied rectangle matches the border color, select that rectangle.
    c. If none of the tied rectangles match the border color (or more than one matches), collect the color indices of all the tied rectangles. Find the median value among these indices. Select the rectangle whose color index is this median value. If there's an even number of tied colors, use the lower of the two middle values after sorting.
10. Create the output grid containing only the pixels of the selected target rectangle, defined by its bounding box.
"""

import numpy as np
from collections import deque, defaultdict, Counter
import statistics

def find_objects(grid, colors_to_find=None, connectivity=4):
    """
    Finds all connected components (objects) of specified colors in the grid.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set, optional): A set of color values to search for.
                                         If None, searches for all non-background (0) colors.
        connectivity (int): 4 for cardinal directions, 8 for cardinal and diagonal.

    Returns:
        dict: A dictionary where keys are colors and values are lists of objects.
              Each object is represented as a set of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = defaultdict(list)

    if colors_to_find is None:
        colors_to_find = set(np.unique(grid)) - {0}

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color in colors_to_find and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()

                    # Define neighbors based on connectivity
                    if connectivity == 4:
                        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                    else: # connectivity == 8
                         neighbors = [
                            (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1),
                            (row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)
                         ]

                    for nr, nc in neighbors:
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            obj_coords.add((nr, nc))

                if obj_coords:
                    objects[color].append(obj_coords)
    return objects

def get_bounding_box(obj_coords):
    """Calculates the bounding box of an object."""
    if not obj_coords:
        return None
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    return (min_r, min_c, max_r, max_c)

def get_border_color(grid):
    """Finds the color of the largest object touching the grid borders."""
    rows, cols = grid.shape
    border_pixels = set()
    for r in range(rows):
        border_pixels.add((r, 0))
        border_pixels.add((r, cols - 1))
    for c in range(cols):
        border_pixels.add((0, c))
        border_pixels.add((rows - 1, c))

    border_object_sizes = Counter()
    visited = np.zeros_like(grid, dtype=bool)
    max_size = -1
    border_color = 0 # Default to background if no border objects

    for r_start, c_start in border_pixels:
        color = grid[r_start, c_start]
        if color != 0 and not visited[r_start, c_start]:
            current_object_coords = set()
            q = deque([(r_start, c_start)])
            visited[r_start, c_start] = True
            current_object_coords.add((r_start, c_start))
            is_border_object = False

            while q:
                r, c = q.popleft()
                if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1):
                     is_border_object = True

                # 4-connectivity for neighbors
                neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
                for nr, nc in neighbors:
                    if 0 <= nr < rows and 0 <= nc < cols and \
                       not visited[nr, nc] and grid[nr, nc] == color:
                        visited[nr, nc] = True
                        q.append((nr, nc))
                        current_object_coords.add((nr, nc))

            if is_border_object:
                 obj_size = len(current_object_coords)
                 # Accumulate size for the color (in case a border object is found multiple times)
                 # This part is tricky, maybe just finding the single largest connected border object is better.
                 # Let's reset the visited check and find all objects first, then check border touch & size.

    # Alternative approach: Find all non-background objects first
    all_objects = find_objects(grid)
    largest_border_object_size = -1
    determined_border_color = 0

    for color, objects_list in all_objects.items():
        for obj_coords in objects_list:
            touches_border = False
            for r, c in obj_coords:
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    touches_border = True
                    break
            if touches_border:
                obj_size = len(obj_coords)
                if obj_size > largest_border_object_size:
                    largest_border_object_size = obj_size
                    determined_border_color = color
                # Handle tie in size? Specification says "largest", implying unique. Assume unique for now.

    return determined_border_color


def transform(input_grid):
    """
    Transforms the input grid by extracting a specific solid rectangle based on area and border color rules.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Identify the border color
    border_color = get_border_color(grid)
    # print(f"Identified Border Color: {border_color}") # Debug

    # 2. Find all non-white objects
    all_objects = find_objects(grid)

    solid_rectangles = []

    # 3-5. Find solid rectangles and calculate area
    for color, objects_list in all_objects.items():
        for obj_coords in objects_list:
            bbox = get_bounding_box(obj_coords)
            if bbox:
                min_r, min_c, max_r, max_c = bbox
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                bbox_area = height * width
                obj_size = len(obj_coords)

                # Check if it's a solid rectangle (object size matches bounding box area)
                if obj_size == bbox_area:
                    solid_rectangles.append({
                        'color': color,
                        'bbox': bbox,
                        'area': bbox_area
                    })
                    # print(f"Found Solid Rectangle: Color={color}, Area={bbox_area}, BBox={bbox}") # Debug


    if not solid_rectangles:
        # Handle cases where no solid rectangles are found (return empty or original?)
        # Based on examples, there's always at least one. Assume this won't happen.
         # Or maybe return a 1x1 grid of black? Let's stick to finding one.
         # If this fails, need to re-evaluate. For now, assume it finds some.
         print("Warning: No solid rectangles found.") # Should not happen based on examples
         return [[0]] # Placeholder for error or unexpected case


    # 6. Find the maximum area
    max_area = 0
    if solid_rectangles:
       max_area = max(rect['area'] for rect in solid_rectangles)
    # print(f"Max Area: {max_area}") # Debug


    # 7. Filter rectangles with maximum area
    max_area_rectangles = [rect for rect in solid_rectangles if rect['area'] == max_area]
    # print(f"Max Area Rectangles ({len(max_area_rectangles)}): {max_area_rectangles}") # Debug


    selected_rectangle = None

    # 8. Select if only one
    if len(max_area_rectangles) == 1:
        selected_rectangle = max_area_rectangles[0]
        # print("Selected: Single max area") # Debug

    # 9. Handle ties
    elif len(max_area_rectangles) > 1:
        # 9a. Check for border color match
        border_color_matches = [rect for rect in max_area_rectangles if rect['color'] == border_color]
        # print(f"Border Color Matches ({len(border_color_matches)}): {border_color_matches}") # Debug


        # 9b. Select if exactly one matches border color
        if len(border_color_matches) == 1:
            selected_rectangle = border_color_matches[0]
            # print("Selected: Single border color match") # Debug

        # 9c. Use median color if no match or multiple matches
        else:
            tied_colors = sorted([rect['color'] for rect in max_area_rectangles])
            # print(f"Tied Colors for Median Calc: {tied_colors}") # Debug

            num_tied = len(tied_colors)
            if num_tied % 2 == 1:
                median_color = statistics.median(tied_colors)
            else:
                # Choose the lower of the two middle values for even counts
                median_color = tied_colors[num_tied // 2 - 1]

            # print(f"Median Color: {median_color}") # Debug


            # Find the rectangle with the median color
            # (Assumption: there will be exactly one rectangle with the median color among the tied ones)
            for rect in max_area_rectangles:
                if rect['color'] == median_color:
                    selected_rectangle = rect
                    # print(f"Selected: Median color ({median_color})") # Debug
                    break


    # 10. Create output grid
    if selected_rectangle:
        min_r, min_c, max_r, max_c = selected_rectangle['bbox']
        # Extract the subgrid corresponding to the bounding box
        output_grid_np = grid[min_r : max_r + 1, min_c : max_c + 1]
        return output_grid_np.tolist()
    else:
        # Should not happen given the logic and examples, but as a fallback:
        print("Error: Could not select a rectangle.")
        return [[0]] # Return minimal grid indicating failure
```
