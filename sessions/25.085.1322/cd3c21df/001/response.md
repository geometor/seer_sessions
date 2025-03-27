```python
import numpy as np

"""
Identifies all solid rectangular objects in the input grid. 
If multiple exist, selects the one with the aspect ratio closest to 1 (squareness).
Ties are broken by selecting the object whose top-left corner has the highest row index, 
and then the highest column index.
The output is the selected rectangular object, cropped to its bounding box.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-background pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of objects. Each object is represented as a dictionary 
              containing 'pixels' (list of (r, c) tuples), 'min_row', 'min_col', 
              'max_row', 'max_col', and 'size'.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({
                    'pixels': obj_pixels,
                    'min_row': min_r,
                    'min_col': min_c,
                    'max_row': max_r,
                    'max_col': max_c,
                    'size': len(obj_pixels)
                })
    return objects

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    input_grid = np.array(input_grid)
    
    # 1. Identify all distinct contiguous objects
    all_objects = find_objects(input_grid)
    
    if not all_objects:
        # Handle case with no objects found (though not in examples)
        return np.array([[]]) # Or some other representation for empty output

    # 2. & 3. Filter for solid rectangles and calculate properties
    rectangular_objects = []
    for obj in all_objects:
        height = obj['max_row'] - obj['min_row'] + 1
        width = obj['max_col'] - obj['min_col'] + 1
        bbox_area = height * width
        
        # Check if the object size equals the bounding box area
        if obj['size'] == bbox_area:
            # Calculate aspect ratio (squareness)
            aspect_ratio = min(height, width) / max(height, width) if max(height, width) > 0 else 1.0
            obj['height'] = height
            obj['width'] = width
            obj['aspect_ratio'] = aspect_ratio
            rectangular_objects.append(obj)

    # 4. Handle case where no rectangular objects are found
    if not rectangular_objects:
        # Handle case (though not in examples)
         return np.array([[]]) # Or appropriate empty output

    # 5. & 6. Select the target object based on criteria
    selected_object = None
    if len(rectangular_objects) == 1:
        selected_object = rectangular_objects[0]
    else:
        # Sort by aspect ratio (descending), then row index (descending), then col index (descending)
        rectangular_objects.sort(key=lambda o: (o['aspect_ratio'], o['min_row'], o['min_col']), reverse=True)
        selected_object = rectangular_objects[0] # The first one after sorting is the desired one

    # 7. Extract the subgrid corresponding to the selected object's bounding box
    min_r = selected_object['min_row']
    min_c = selected_object['min_col']
    max_r = selected_object['max_row']
    max_c = selected_object['max_col']
    
    output_grid = input_grid[min_r : max_r + 1, min_c : max_c + 1]
    
    return output_grid.tolist() # Convert back to list of lists for consistency
```