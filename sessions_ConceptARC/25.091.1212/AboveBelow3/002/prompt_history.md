
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0
0 4 4 4 0 0 0 0
0 4 4 4 0 0 0 0
0 0 0 0 0 3 3 3
0 0 3 3 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0
0 4 4 4 0 0 0 0
0 4 4 4 0 0 0 0
0 4 4 4 0 0 0 0
0 0 0 0 0 3 3 3
0 0 3 3 3 0 0 0
```


## train_2

**input:**
```
0 0 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 0 0 0 0
0 0 6 6 6 6 0 0 0 0
0 0 6 6 6 6 0 0 0 0
0 0 6 6 6 6 0 0 0 0
2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 0 6 6 6 6 0 0 0 0
0 0 6 6 6 6 0 0 0 0
0 0 6 6 6 6 0 0 0 0
0 0 6 6 6 6 0 0 0 0
2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0
```


## train_3

**input:**
```
0 0 4 4 0 0 0
0 0 0 0 0 0 0
0 0 1 1 0 0 0
0 0 1 1 0 0 0
0 4 4 4 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 0 4 4 0 0 0
0 0 1 1 0 0 0
0 0 1 1 0 0 0
0 4 4 4 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output grids have the same dimensions.
    *   The background color is white (0).
    *   Each input grid contains multiple distinct objects composed of non-white pixels.
    *   The transformation focuses on a single object within the input grid: the "topmost" object. The topmost object is the one containing pixels with the smallest row index. If multiple objects share the same minimum row index, they are collectively treated as the topmost object component (though in the examples, the topmost object is always a single contiguous block).
    *   All objects other than the topmost object remain unchanged in their position and color from input to output.
    *   The topmost object is moved vertically downwards. Its horizontal position and shape remain the same.
    *   The distance the topmost object moves downwards depends on the number of completely white rows situated immediately below it in the input grid.
    *   Specifically, the downward shift distance is equal to the count of consecutive, entirely white rows starting from the row directly below the lowest row occupied by the topmost object.

*   **YAML Facts:**
    
```yaml
    task_context:
      grid_properties:
        - dimensions: Consistent between input and output.
        - background_color: white (0).
      object_properties:
        - type: Discrete, contiguous blocks of non-white pixels.
        - count: Multiple objects per grid.
    transformation:
      target_object:
        - identification: The object(s) containing the minimum row index with non-white pixels (topmost object).
      action:
        - name: Vertical shift downwards.
        - target: Only the identified topmost object.
        - other_objects: Remain static.
      shift_determination:
        - basis: Rows immediately below the target object in the input.
        - condition: Rows must be entirely composed of the background color (white).
        - calculation: Count the number of consecutive, entirely white rows starting from the row directly beneath the lowest extent of the topmost object. This count equals the downward shift distance.
      process:
        - Step 1: Identify the topmost object and its vertical extent (min_row, max_row).
        - Step 2: Count consecutive all-white rows starting from row `max_row + 1`. Let the count be `shift`.
        - Step 3: Create the output grid, initially identical to the input.
        - Step 4: Erase the original topmost object from the output grid (set its pixels to white).
        - Step 5: Redraw the topmost object in the output grid, shifted down by `shift` rows.
    ```


*   **Natural Language Program:**
    1.  Identify the set of pixels belonging to the topmost non-white object(s) in the input grid (those pixels with the minimum row index). Determine the maximum row index (`max_row`) occupied by any pixel of this topmost object.
    2.  Initialize a counter `shift` to 0.
    3.  Iterate through the rows of the input grid starting from the row immediately below the topmost object (`row_index = max_row + 1`).
    4.  For each `row_index`, check if all pixels in that row are the background color (white, 0).
    5.  If the row is entirely white, increment the `shift` counter and proceed to the next row (`row_index + 1`).
    6.  If the row is not entirely white, or if the bottom of the grid is reached, stop counting. The final value of `shift` is the required vertical displacement.
    7.  Create the output grid as a copy of the input grid.
    8.  Set all pixels corresponding to the original position of the topmost object in the output grid to the background color (white, 0).
    9.  For each pixel `(r, c)` that was part of the original topmost object, set the pixel at `(r + shift, c)` in the output grid to the original color of the pixel at `(r, c)`.
```python
import numpy as np
import collections

def transform_grid(input_grid):
    """
    Identifies the topmost non-white object(s) in the input grid, calculates 
    a vertical downward shift distance based on the number of consecutive 
    all-white rows immediately below the object, and moves only the topmost 
    object(s) down by that distance. Other objects remain stationary.

    1. Find all non-white pixels. If none, return the input grid.
    2. Determine the minimum row index (`min_r`) containing non-white pixels.
    3. Identify all connected non-white pixels starting from those at `min_r`. 
       This constitutes the "topmost object".
    4. Find the maximum row index (`max_r`) occupied by the topmost object.
    5. Count the number of consecutive rows composed entirely of the background 
       color (0) starting from the row immediately below the object (`max_r + 1`). 
       This count is the `shift` distance.
    6. Create an output grid, initially a copy of the input.
    7. Erase the topmost object from its original position in the output grid 
       by setting its pixels to the background color (0).
    8. Redraw the topmost object in the output grid at its new position, 
       shifted down by `shift` rows.
    """
    
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    background_color = 0

    # 1. Find all non-white pixels.
    non_white_coords = list(zip(*np.where(grid != background_color)))

    # If the grid is empty or all background, return it as is.
    if not non_white_coords:
        return input_grid

    # 2. Determine the minimum row index (`min_r`)
    min_r = min(r for r, c in non_white_coords)

    # 3. Identify all connected non-white pixels forming the topmost object(s).
    # Start BFS from all non-white pixels located at min_r.
    q = collections.deque([(r, c) for r, c in non_white_coords if r == min_r])
    visited = set(q)
    topmost_object_pixels = {} # Store {(r, c): color}

    while q:
        r, c = q.popleft()
        # Check if coord is valid before accessing grid (should be, but safe)
        if 0 <= r < height and 0 <= c < width:
             # Make sure we don't accidentally add background pixels if the initial
             # pixel was isolated and somehow the neighbors search reached a background pixel (unlikely with check below)
             color = grid[r, c]
             if color != background_color:
                 topmost_object_pixels[(r, c)] = color
             else:
                 continue # Should not happen if starting points are non-white
        else:
            continue # Should not happen with boundary checks below
       
        # Explore neighbors (4-connectivity)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check boundaries and if the neighbor is non-white and not visited
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] != background_color and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append((nr, nc))

    if not topmost_object_pixels:
         # This case should ideally not be reached if non_white_coords is not empty,
         # but provides safety. It means the identified min_r pixels were isolated bg pixels?
         return input_grid # Or handle error as appropriate

    # 4. Find the maximum row index (`max_r`) occupied by the topmost object.
    max_r = max(r for r, c in topmost_object_pixels.keys())

    # 5. Count consecutive all-white rows below the object.
    shift = 0
    for r_check in range(max_r + 1, height):
        if np.all(grid[r_check, :] == background_color):
            shift += 1
        else:
            break # Stop counting at the first non-white row

    # 6. Create the output grid as a copy.
    output_grid = grid.copy()

    # 7. Erase the original topmost object.
    for r, c in topmost_object_pixels.keys():
        output_grid[r, c] = background_color

    # 8. Draw the shifted topmost object.
    for (r, c), color in topmost_object_pixels.items():
        new_r = r + shift
        # Ensure the new position is within grid bounds
        if 0 <= new_r < height:
            output_grid[new_r, c] = color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()

```
