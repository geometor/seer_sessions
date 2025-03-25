```python
"""
1.  **Object Identification:** Identify all red (2) and azure (8) objects in the input grid. Record the original positions of the azure objects.
2.  **Iterative Red Expansion:** For each red object, find the nearest *original* azure object.
3.  **Single Step Expansion:** The red object expands *one step* towards the azure object. Prioritize vertical movement. If vertical movement is not possible or complete, take one step horizontally.
4.  **Yellow Placement:** After *each* step of the red object's expansion, place a yellow (4) pixel. The yellow pixel is the one in the red object's current path (including its starting point) that is closest to the *original* position of the targeted azure object.
5.  **Azure Mirroring:** After the red object has taken one step, *and* the yellow pixel is placed, the closest azure object mirrors this single step expansion. The expansion uses relative coordinates - e.g. if red moves up, azure moves up - if red moves right, azure moves right. If after a red move, there are multiple azure pixels that are the same distance, all of the tied azure pixels are moved.
6. **Repeat:** Repeat steps 3-5 until the red object reaches the *original* position of the azure object (connects with original bounds). Note that there is only *one* red object expansion per iteration, and only one azure expansion per iteration, but multiple azure expansions in total are possible if multiple objects tie.
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

def closest_object(grid, coord, target_objects):
    """Finds the closest object of a given color to a coordinate."""
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

def single_step_expansion(grid, start_coord, end_coord):
    """Expands one step from start_coord towards end_coord, prioritizing vertical."""
    r, c = start_coord
    tr, tc = end_coord

    # Move vertically
    if r != tr:
        step = 1 if tr > r else -1
        return (r + step, c)

    # Move horizontally
    elif c != tc:
        step = 1 if tc > c else -1
        return (r, c + step)

    return (r,c) #already at target

def mirror_step(grid, azure_coords, red_step):
  """Mirrors the red step for all closest azure coords"""
  new_grid = np.copy(grid)
  dr = red_step[0] - red_step[2]
  dc = red_step[1] - red_step[3]

  for az_r, az_c in azure_coords:
    nr = az_r + dr
    nc = az_c + dc
    if 0 <= nr < new_grid.shape[0] and 0<= nc < new_grid.shape[1]:
      if new_grid[nr, nc] != 2: #don't overwrite red
        new_grid[nr,nc] = 8
  return new_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Object Identification
    red_objects = find_objects(input_grid, 2)
    azure_objects = find_objects(input_grid, 8)
    original_azure_objects = azure_objects.copy() #track for yellow placement

    # Iterative Red Expansion
    for red_coord in red_objects:
        closest_azure_coord = closest_object(input_grid, red_coord, original_azure_objects)

        if closest_azure_coord:
          path = [red_coord]
          current_red = red_coord
          while current_red != closest_azure_coord:
            #single step expansion
            next_red = single_step_expansion(output_grid, current_red, closest_azure_coord)
            output_grid[next_red] = 2
            path.append(next_red)

            #yellow placement
            nearest_to_original = get_nearest_to_original(path, original_azure_objects)
            output_grid[nearest_to_original] = 4

            #azure mirroring
            #find all closest azure
            min_dist = float('inf')
            closest_azures = []
            for az_obj in azure_objects:
                dist = abs(az_obj[0] - next_red[0]) + abs(az_obj[1] - next_red[1])
                if dist < min_dist:
                    min_dist = dist
                    closest_azures = [az_obj]
                elif dist == min_dist:
                    closest_azures.append(az_obj)
            output_grid = mirror_step(output_grid, closest_azures, (next_red[0], next_red[1], current_red[0], current_red[1]))
            azure_objects = find_objects(output_grid, 8) #re-find since they can move

            current_red = next_red # update for next loop


    return output_grid
```