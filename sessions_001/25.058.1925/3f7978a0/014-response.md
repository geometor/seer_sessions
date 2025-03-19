# 3f7978a0 • 014 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous blocks of pixels of the same color (excluding white/0).
2.  **Identify Primary Diagonal:** Find the longest diagonal structure formed by connected azure (8) and gray (5) pixels running from top-right to bottom-left.  "Connected" means adjacent horizontally, vertically, or diagonally.
3.  **Object Filtering:** Select all objects that intersect with the primary diagonal. Intersection means that at least one pixel of the object shares either a row or a column with any pixel in the primary diagonal.
4.  **Construct Output Grid:** Create a new grid containing only the selected objects. The output grid's dimensions and empty spaces are determined by the positions of the selected object pixels. All pixels of a selected object that are present in the input should be preserved.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of non-zero color in the grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            dfs(row + dr, col + dc, color, current_object)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0 and (row, col) not in visited:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append(current_object)
    return objects

def find_primary_diagonal(grid, objects):
    """
    Finds the longest top-right to bottom-left diagonal formed by 8 and 5.
    """
    
    #Find the 8 and 5 objects
    candidate_objects = []
    for obj in objects:
      color = grid[obj[0]]
      if color == 8 or color == 5:
        candidate_objects.append(obj)
    
    if not candidate_objects:
        return []

    longest_diagonal = []
    
    for start_obj in candidate_objects:
      for start_row, start_col in start_obj:
          current_diagonal = [(start_row, start_col)]
          current_row, current_col = start_row, start_col
        
          while True:
            found_next = False
            for dr, dc in [(1, -1), (1,0), (1,1), (0,1), (0,-1), (-1,0), (-1,-1), (-1,1)]:  # Check all neighbors
                next_row, next_col = current_row + dr, current_col + dc
                if (next_row, next_col) not in current_diagonal: #check not in current diagonal
                    for obj in candidate_objects: #find next
                        if (next_row, next_col) in obj:
                            current_diagonal.append((next_row, next_col))
                            current_row, current_col = next_row, next_col
                            found_next = True
                            break
                    if found_next:
                      break
            if not found_next:
                break
          if len(current_diagonal) > len(longest_diagonal):
            longest_diagonal = current_diagonal

    return longest_diagonal

def check_object_intersection(obj, diagonal):
    """
    Checks if an object intersects with the diagonal (shares a row or column).
    """
    if not diagonal:
        return False
    diagonal_rows = {r for r, _ in diagonal}
    diagonal_cols = {c for _, c in diagonal}
    for row, col in obj:
        if row in diagonal_rows or col in diagonal_cols:
            return True
    return False

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Objects
    objects = find_objects(input_grid)

    # 2. Identify Primary Diagonal
    primary_diagonal = find_primary_diagonal(input_grid, objects)

    # 3. Object Filtering
    selected_objects = [obj for obj in objects if check_object_intersection(obj, primary_diagonal)]

   # 4. Construct Output Grid
    if not selected_objects:
        return []

    all_selected_pixels = []
    for obj in selected_objects:
        all_selected_pixels.extend(obj)

    if not all_selected_pixels:
        return []

    min_row = min(r for r, _ in all_selected_pixels)
    max_row = max(r for r, _ in all_selected_pixels)
    min_col = min(c for _, c in all_selected_pixels)
    max_col = max(c for _, c in all_selected_pixels)

    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    for obj in selected_objects:
        for r, c in obj:
            output_grid[r - min_row, c - min_col] = input_grid[r, c]

    return output_grid.tolist()
```
