```python
"""
1.  **Identify Objects:** Scan the input grid to find all distinct objects. An object is a contiguous block of pixels with the same non-zero color.
2.  **Object Selection with Background**: Identify all objects and check if they are part of a 3x3 block. Iterate through the object and consider the object and surrounding pixels. Check for a 3 x 3 shape using both the colored object, and the '0' valued pixels surrounding that shape. The color and relative shape and locations of non-zero pixels of the selected object is copied into the 3x3 output.
3.  **Construct 3x3 Output:** Create a 3x3 output grid. Copy the selected object (from step 2) and it's surrounding '0' pixels into the 3x3 output grid, maintaining the relative positions of the colored pixels and the '0' background pixels.
4. **Return Output:** Return the output grid.
"""

import numpy as np

def find_objects(grid):
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r][c] != 0:
                obj_coords = []
                dfs(r, c, grid[r][c], obj_coords)
                objects.append(obj_coords)
    return objects

def check_3x3_grid(grid, obj_coords):
    """Checks if the object and its neighboring 0s form a 3x3 grid."""
    rows, cols = len(grid), len(grid[0])
    
    obj_coords_array = np.array(obj_coords)
    min_r = np.min(obj_coords_array[:, 0])
    max_r = np.max(obj_coords_array[:, 0])
    min_c = np.min(obj_coords_array[:, 1])
    max_c = np.max(obj_coords_array[:, 1])

    if (max_r - min_r + 1) > 3 or (max_c - min_c + 1) > 3:
        return None, None  # Object itself is larger than 3x3

    
    for start_r in range(max(0, min_r - 2), min(rows - 2, max_r + 1)):
        for start_c in range(max(0, min_c - 2), min(cols-2, max_c+1)):
          
            is_3x3 = True
            for r in range(start_r, start_r + 3):
                for c in range(start_c, start_c + 3):
                  
                    found = False
                    for obj_r,obj_c in obj_coords:
                        if obj_r == r and obj_c == c:
                            found = True
                            break
                    if not found:
                        if grid[r][c] != 0:
                          is_3x3 = False
                          break
                if not is_3x3:
                    break
            if is_3x3:
                return start_r, start_c

    return None, None


def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    objects = find_objects(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)

    # select and construct 3x3
    for obj_coords in objects:
        start_r, start_c = check_3x3_grid(input_grid, obj_coords)
        if start_r is not None:
            
            color = input_grid[obj_coords[0][0]][obj_coords[0][1]]
            
            for r in range(3):
                for c in range(3):
                    input_r = start_r + r
                    input_c = start_c + c
                    
                    is_object = False
                    for obj_coord in obj_coords:
                        if obj_coord[0] == input_r and obj_coord[1] == input_c:
                            is_object = True
                            break

                    if is_object:
                        output_grid[r,c] = color
                    elif input_grid[input_r][input_c] == 0:
                        output_grid[r,c] = 0
            
            return output_grid
    
    return output_grid
```