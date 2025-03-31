```python
import numpy as np
from collections import deque

"""
Identify all distinct contiguous objects composed of non-white pixels (colors 1-9) in the input grid, considering orthogonal adjacency.
Filter these objects to keep only those containing at least one blue (1) pixel.
For each filtered object, calculate:
1. Count of magenta (6) pixels.
2. Count of yellow (4) pixels.
3. Area (total count of non-white pixels in the object).
4. Topmost row index.
Select the object based on the following criteria, applied sequentially:
1. Maximum magenta count.
2. Minimum yellow count (among ties for max magenta).
3. Maximum area (among ties for yellow count).
4. Maximum topmost row index (lowest object visually, among ties for area).
Extract the selected object based on its bounding box.
Create an output grid matching the bounding box size.
Copy the pixels of the selected object into the output grid.
Replace any yellow (4) pixels in the output grid with blue (1) pixels.
Return the final output grid.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-white pixels in the grid using orthogonal adjacency.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of objects, where each object is represented as a list of 
              tuples (row, col, color).
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                # Start BFS to find a new object
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    color = grid[row, col]
                    obj_pixels.append((row, col, color))

                    # Check orthogonal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Check if the object contains at least one blue pixel
                has_blue = any(p[2] == 1 for p in obj_pixels)
                if has_blue:
                    objects.append(obj_pixels)
                    
    return objects

def analyze_object(obj_pixels):
    """
    Analyzes an object to calculate its properties for selection.

    Args:
        obj_pixels (list): List of (row, col, color) tuples for the object.

    Returns:
        dict: A dictionary containing 'magenta_count', 'yellow_count', 
              'area', 'top_row_index', and 'pixels'.
    """
    magenta_count = 0
    yellow_count = 0
    min_r = float('inf')
    
    for r, c, color in obj_pixels:
        if color == 6:
            magenta_count += 1
        elif color == 4:
            yellow_count += 1
        min_r = min(min_r, r)
        
    area = len(obj_pixels)
    
    return {
        'magenta_count': magenta_count,
        'yellow_count': yellow_count,
        'area': area,
        'top_row_index': min_r,
        'pixels': obj_pixels
    }

def get_bounding_box(obj_pixels):
    """Calculates the bounding box of an object."""
    if not obj_pixels:
        return 0, 0, 0, 0
    rows = [p[0] for p in obj_pixels]
    cols = [p[1] for p in obj_pixels]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    """
    Transforms the input grid based on the described object selection and modification rules.
    """
    # 1. Find all potential objects (non-white, containing blue)
    objects_pixels = find_objects(np.array(input_grid))

    if not objects_pixels:
        # Handle cases where no valid objects are found (return empty or original?)
        # Based on examples, there's always a valid object. If not, maybe return an empty grid?
        # Let's assume valid object exists.
        return np.array([[]]) # Or raise an error

    # 2. Analyze each object
    analyzed_objects = [analyze_object(obj) for obj in objects_pixels]

    # 3. Select the target object based on criteria
    # Sort using a stable sort is implicitly handled by applying criteria sequentially
    # Sort by magenta_count (descending)
    analyzed_objects.sort(key=lambda x: x['magenta_count'], reverse=True)
    max_magenta = analyzed_objects[0]['magenta_count']
    tied_magenta = [obj for obj in analyzed_objects if obj['magenta_count'] == max_magenta]

    # Sort by yellow_count (ascending)
    tied_magenta.sort(key=lambda x: x['yellow_count'])
    min_yellow = tied_magenta[0]['yellow_count']
    tied_yellow = [obj for obj in tied_magenta if obj['yellow_count'] == min_yellow]
    
    # Sort by area (descending)
    tied_yellow.sort(key=lambda x: x['area'], reverse=True)
    max_area = tied_yellow[0]['area']
    tied_area = [obj for obj in tied_yellow if obj['area'] == max_area]

    # Sort by top_row_index (descending - meaning lowest object)
    tied_area.sort(key=lambda x: x['top_row_index'], reverse=True)
    
    selected_object = tied_area[0]
    selected_pixels = selected_object['pixels']

    # 4. Determine bounding box
    min_r, min_c, max_r, max_c = get_bounding_box(selected_pixels)
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # 5. Create the output grid
    output_grid = np.zeros((height, width), dtype=int) # Initialize with background (0), though object pixels will overwrite

    # 6. Copy pixels, adjusting coordinates
    for r, c, color in selected_pixels:
        out_r, out_c = r - min_r, c - min_c
        # 7. Modify color if yellow
        output_grid[out_r, out_c] = 1 if color == 4 else color 

    return output_grid.tolist() # Convert back to list of lists for standard ARC format

```