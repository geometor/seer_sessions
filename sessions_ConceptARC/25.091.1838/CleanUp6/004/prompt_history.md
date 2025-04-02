
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 3
3 0 3 3 3 3 3 0 0 0
0 0 0 3 3 3 0 0 0 0
0 1 0 0 3 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 1 0 0 3 0 0 0 0 3
0 0 0 3 3 3 0 0 0 0
0 0 3 3 3 3 3 0 0 1
3 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 6 8 0 0 0 8 0 0 0 0 0 6 8 0 0
0 0 6 6 6 0 0 0 0 0 0 0 6 6 6 0 0
0 0 8 6 6 6 0 0 0 0 0 6 6 6 6 0 0
0 0 6 8 6 0 0 0 0 8 0 0 6 6 6 0 0
0 0 6 6 0 0 8 0 0 0 8 0 0 6 6 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 6 6 0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 6 6 6 0 0 0 0 0 0 0 6 6 6 0 0
0 0 6 6 6 6 0 0 0 0 0 6 6 6 6 0 0
0 0 6 6 6 0 0 0 0 0 0 0 6 6 6 0 0
0 0 6 6 0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

### Perception

1.  **Grid Structure:** Both inputs and outputs are grids of pixels represented by numbers (colors). The background color is consistently white (0).
2.  **Colors & Objects:** The inputs contain multiple non-background colors (Example 1: blue=1, green=3; Example 2: magenta=6, azure=8). These colors often form contiguous objects (shapes) of varying sizes, but can also appear as isolated pixels.
3.  **Transformation:** The transformation selectively removes some colored pixels, turning them white (0), while keeping others.
    *   In Example 1, all blue pixels are removed. Some green pixels (those not part of the main large green shape) are also removed. Only the pixels forming the largest connected green object remain.
    *   In Example 2, all azure pixels are removed. All magenta pixels remain. The magenta pixels form two large, separate objects of equal size.
4.  **Pattern Identification:** The key pattern seems to involve:
    *   Identifying the non-background colors present.
    *   Counting the frequency of each non-background color.
    *   Focusing on the color that appears most frequently.
    *   Identifying contiguous objects formed by this most frequent color.
    *   Selecting the largest object(s) of this color.
    *   The output grid retains *only* the pixels belonging to these largest object(s) of the most frequent color. All other pixels become white (background).

### Facts


```yaml
analysis:
  - task_type: object_filtering # Based on properties like color frequency and size/connectivity
  - background_color: 0 # white
  - non_background_colors_input_ex1: [1, 3] # blue, green
  - non_background_colors_input_ex2: [6, 8] # magenta, azure
  - processing_steps:
      - step: count_colors
        description: Count occurrences of each non-background color in the input grid.
        example_1: { color_1: 6, color_3: 21 }
        example_2: { color_6: 28, color_8: 10 }
      - step: identify_primary_color
        description: Determine the most frequent non-background color.
        example_1: color_3 # green (21 occurrences)
        example_2: color_6 # magenta (28 occurrences)
        tie_breaking: If multiple colors share the maximum frequency, all are considered primary (though not seen in examples).
      - step: find_objects
        description: Identify all contiguous objects (4-neighbor connectivity) for the primary color(s).
        example_1_color_3: [object_size_19, object_size_1, object_size_1]
        example_2_color_6: [object_size_15, object_size_15]
      - step: find_largest_objects
        description: Determine the maximum object size for the primary color(s).
        example_1_max_size: 19
        example_2_max_size: 15
      - step: filter_pixels
        description: Keep only the pixels belonging to the largest object(s) of the primary color(s). Set all other pixels to the background color (0).
        example_1_kept_pixels: Pixels belonging to the size 19 green object.
        example_2_kept_pixels: Pixels belonging to both size 15 magenta objects.
  - output_grid_content: Contains only the background color and the pixels from the largest object(s) of the most frequent input color.
```


### Natural Language Program

1.  Identify all unique pixel colors present in the input grid, excluding the background color (white, 0).
2.  Calculate the frequency (count) of each identified non-background color.
3.  Determine the color(s) that has the highest frequency count. This is the "primary" color (or colors, if tied).
4.  Find all separate, contiguous objects (groups of connected pixels of the same color, using side-by-side adjacency) composed of the primary color(s).
5.  Calculate the size (number of pixels) of each of these objects.
6.  Identify the maximum size among these objects.
7.  Create a new output grid of the same dimensions as the input grid, filled entirely with the background color (white, 0).
8.  Iterate through all the identified objects of the primary color(s). If an object's size is equal to the maximum size found in step 6, copy all pixels belonging to that object from their original positions in the input grid to the corresponding positions in the new output grid.
9.  The resulting grid is the final output.
```python
import numpy as np
from collections import Counter, deque

def find_connected_objects(grid, target_color):
    """
    Finds all connected objects of a specific color in a grid using BFS.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is represented as a list
              of (row, col) coordinate tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited yet,
            # start a BFS to find its connected component (object).
            if grid[r, c] == target_color and not visited[r, c]:
                current_object_coords = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_object_coords.append((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check boundaries and if the neighbor is the target color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if current_object_coords:
                    objects.append(current_object_coords)
    
    return objects

def transform(input_grid):
    """
    Transforms the input grid by performing the following steps:
    1. Identify all unique non-background pixel colors (0 is background).
    2. Count the frequency of each non-background color.
    3. Determine the color(s) with the highest frequency ('primary' color(s)).
    4. Find all contiguous objects composed of the primary color(s).
    5. Identify the largest size among these primary color objects.
    6. Create an output grid containing only the pixels belonging to the largest object(s) 
       of the primary color(s), preserving their original color. All other pixels are 
       set to the background color (0).
    """
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    output_grid = np.zeros_like(input_grid_np) # Initialize output with background color

    # 1. & 2. Count frequencies of non-background colors
    pixels = input_grid_np.flatten()
    non_background_pixels = pixels[pixels != 0]
    
    if len(non_background_pixels) == 0:
        # If the input grid is empty or only background, return the empty grid
        return output_grid.tolist()
        
    color_counts = Counter(non_background_pixels)
    
    # 3. Determine the primary color(s) - highest frequency
    max_freq = 0
    primary_colors = []
    if color_counts: # Check if there are any non-background colors
        max_freq = max(color_counts.values())
        primary_colors = [color for color, count in color_counts.items() if count == max_freq]

    # If no primary color identified (e.g., only background color present), return zero grid
    if not primary_colors:
         return output_grid.tolist()

    # 4. Find all objects of the primary color(s)
    all_primary_objects = []
    for color in primary_colors:
        objects_of_color = find_connected_objects(input_grid_np, color)
        all_primary_objects.extend(objects_of_color) # Store objects as lists of coordinates

    # If no objects found for any primary color, return zero grid
    if not all_primary_objects:
        return output_grid.tolist()

    # 5. Identify the maximum object size
    max_object_size = 0
    for obj in all_primary_objects:
        max_object_size = max(max_object_size, len(obj))

    # 6. Filter and create the output grid
    for obj_coords in all_primary_objects:
        if len(obj_coords) == max_object_size:
            # Keep this object - copy its pixels to the output grid
            for r, c in obj_coords:
                # We already know the color from the primary_colors list, 
                # or we can just grab it from the input grid
                output_grid[r, c] = input_grid_np[r, c] 

    return output_grid.tolist()
```
```python
"""
Transforms an input grid by identifying the most frequent non-background color(s), finding all contiguous objects of that color(s), determining the maximum size among these objects, and returning a new grid containing only the pixels belonging to the object(s) that match this maximum size. All other pixels are set to the background color (0). Connectivity for objects is defined by 4-way adjacency (up, down, left, right).
"""

import numpy as np
from collections import Counter, deque

def find_connected_objects(grid, target_color):
    """
    Finds all connected objects of a specific color in a grid using BFS
    with 4-way adjacency.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is represented as a list
              of (row, col) coordinate tuples. Returns an empty list if no
              objects of the target_color are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if we find an unvisited pixel of the target color
            if grid[r, c] == target_color and not visited[r, c]:
                current_object_coords = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_object_coords.append((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check boundaries and if the neighbor is the target color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Add the found object (list of coordinates) to our list of objects
                if current_object_coords:
                    objects.append(current_object_coords)

    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    # Initialize output grid with background color 0
    output_grid = np.zeros_like(input_grid_np)

    # 1. & 2. Count frequencies of non-background colors
    pixels = input_grid_np.flatten()
    non_background_pixels = pixels[pixels != 0]

    # Handle edge case: grid is empty or only contains background color
    if len(non_background_pixels) == 0:
        return output_grid.tolist()

    color_counts = Counter(non_background_pixels)

    # 3. Determine the primary color(s) - highest frequency
    max_freq = 0
    primary_colors = []
    if color_counts: # Check if there are any non-background colors counted
        max_freq = max(color_counts.values())
        primary_colors = [color for color, count in color_counts.items() if count == max_freq]

    # This check is technically redundant due to the len(non_background_pixels) check above,
    # but kept for robustness.
    if not primary_colors:
         return output_grid.tolist()

    # 4. Find all objects of the primary color(s)
    all_primary_objects = []
    for color in primary_colors:
        # Find all objects for the current primary color
        objects_of_color = find_connected_objects(input_grid_np, color)
        # Add all found objects to the master list
        all_primary_objects.extend(objects_of_color) # Store objects as lists of coordinates

    # Handle edge case: No objects of the primary color(s) were found
    if not all_primary_objects:
        return output_grid.tolist()

    # 5. & 6. Identify the maximum object size among primary objects
    max_object_size = 0
    for obj in all_primary_objects:
        max_object_size = max(max_object_size, len(obj))

    # 7. & 8. Filter and create the output grid
    # Iterate through all found primary objects
    for obj_coords in all_primary_objects:
        # Check if the current object's size matches the maximum size
        if len(obj_coords) == max_object_size:
            # Keep this object: copy its pixels to the output grid
            for r, c in obj_coords:
                # Get the color from the input grid at this coordinate
                output_grid[r, c] = input_grid_np[r, c]

    # 9. Return the result as a list of lists
    return output_grid.tolist()
```
