```python
"""
1.  **Object Identification:** Identify all red (2) and azure (8) objects within the input grid.
2.  **Red-Azure Connection:** For each red object, find the nearest azure object. The red object expands towards the azure object, creating a path. The expansion first completes the vertical movement, and *then* completes the horizontal movement towards the target.
3. **Yellow Intersection:** After the red object has finished expanding, a pixel is changed to yellow (4). This yellow pixel is the pixel in the expanded red object path closest to the *original* position of the azure object.
4.  **Azure Mirroring:** The azure object expands by mirroring the expansion of the red object. If the red expands two cells down and one to the left, the azure will expand the same. It appears that the *closest* azure expands, in the case that there are multiple.
"""

import numpy as np

def find_objects(grid, color):
    """Finds the coordinates of all pixels of a given color."""
    objects = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                objects.append((r, c))
    return objects

def closest_object(grid, coord, target_color):
    """Finds the closest object of a given color to a coordinate."""
    target_objects = find_objects(grid, target_color)
    if not target_objects:
        return None

    min_dist = float('inf')
    closest_coord = None

    for target_coord in target_objects:
        dist = abs(target_coord[0] - coord[0]) + abs(target_coord[1] - coord[1])
        if dist < min_dist:
            min_dist = dist
            closest_coord = target_coord
    return closest_coord

def expand_and_connect(grid, start_coord, end_coord):
    """Expands from start_coord towards end_coord, first vertically, then horizontally."""
    output_grid = np.copy(grid)
    r, c = start_coord
    tr, tc = end_coord
    path = []

    # Move vertically
    if r != tr:
        step = 1 if tr > r else -1
        for i in range(r + step, tr + step, step):
            output_grid[i, c] = output_grid[r,c]  # Use original color
            path.append((i, c))
        r = tr

    # Move horizontally
    if c != tc:
        step = 1 if tc > c else -1
        for i in range(c + step, tc + step, step):
            output_grid[r, i] = output_grid[r,c] #use original color
            path.append((r, i))
        c = tc

    return output_grid, path

def get_nearest_to_original(path, original_target_objects):
    """
    Of the points in the path, find the one nearest to the *original*
    target object.
    """
    if not path:
      return None

    min_dist = float('inf')
    nearest_coord = None
    
    for path_coord in path:
        for target_coord in original_target_objects:
            dist = abs(path_coord[0] - target_coord[0]) + abs(path_coord[1] - target_coord[1])
            if dist < min_dist:
                min_dist = dist
                nearest_coord = path_coord
    return nearest_coord
  
def calculate_movement(start, end):
    """ calculate vertical and horizontal movement vectors"""
    vr = end[0] - start[0]
    vc = end[1] - start[1]
    return vr, vc

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Object Identification
    red_objects = find_objects(input_grid, 2)
    azure_objects = find_objects(input_grid, 8)
    original_azure_objects = azure_objects.copy() #track for yellow placement

    # Red-Azure Connection and Yellow Intersection
    for red_coord in red_objects:
        closest_azure_coord = closest_object(input_grid, red_coord, 8)
        if closest_azure_coord:
            output_grid, path = expand_and_connect(output_grid, red_coord, closest_azure_coord)
            nearest_to_original = get_nearest_to_original(path, original_azure_objects)
            if nearest_to_original:
                output_grid[nearest_to_original] = 4  # Yellow Intersection

    # Azure Mirroring - *AFTER* red expansion and yellow placement
    # need to re-find objects since they have moved
    red_objects = find_objects(output_grid, 2)
    azure_objects = find_objects(output_grid, 8)

    for red_coord in red_objects:
      closest_azure = closest_object(output_grid, red_coord, 8)
      if closest_azure:
        vr, vc = calculate_movement(red_coord, closest_azure)
        for az_r, az_c in azure_objects:
          #check bounds
          if (az_r + vr) < output_grid.shape[0] and (az_r + vr) >= 0 \
            and (az_c+vc) < output_grid.shape[1] and (az_c + vc) >=0:
              if output_grid[az_r + vr, az_c + vc] != 2: #don't overwrite red
                output_grid[az_r+vr, az_c+vc] = 8
              
    return output_grid
```