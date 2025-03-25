"""
1. **Identify Objects:** Scan the input grid and identify all contiguous blocks of non-zero pixels. Each block is an object.

2.  **Find Separator Columns**: There are columns of "1" (blue) pixels in the input

3.  **Object Extraction to the Right of the Separator**: For each row, select all contiguous non-zero pixel regions to the *right* of the separator.

4. **Create box**: Create a bounding box with the objects to the right of the separator.

5. **Remove Separator Column**: Discard the Separator column

6. **Create Output**: Create the output box by stacking, in alternating rows, two rows composed of alternating values in the input box.

    - For example, in Train_1, the selected objects in the box are [[4,4], [4,0]], [[3,0], [3,0]], [[2,2], [2,2] , [2,2] , [2,2]], and [[9,9], [9,9] , [9,9]].

    - In Train_1, the output has alternating rows of values, taken from the box: [[2,2], [2,9], [9,9], [2,2], [2,9]].
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
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
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r][c] != 0:
                obj_coords = []
                dfs(r, c, grid[r][c], obj_coords)
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def find_separator_columns(grid):
    """Finds columns containing only '1' (blue) pixels."""
    separator_cols = []
    for j in range(len(grid[0])):
        is_separator = True
        for i in range(len(grid)):
            if grid[i][j] != 1:
                is_separator = False
                break
        if is_separator:
            separator_cols.append(j)
    return separator_cols

def extract_objects_right_of_separator(grid, separator_cols):
    """Extracts objects to the right of the separator."""
    if not separator_cols:
        return []
    
    rightmost_separator = max(separator_cols)
    
    relevant_part = []
    for row in grid:
      relevant_part.append(row[rightmost_separator+1:])

    return relevant_part

def create_box(subgrid):
    """ create numpy array from subgrid """
    return np.array(subgrid)

def create_output(boxed_objects):
    """Creates the output grid based on alternating rows and values."""
    if boxed_objects.size == 0:  # Check if the array is empty
       return np.array([])
    rows, cols = boxed_objects.shape
    output_rows = []
    
    
    # use unique, preserve order
    unique_vals = []
    for val in boxed_objects.flatten():
      if val not in unique_vals:
        unique_vals.append(val)

    for i in range(0, rows,1):
        output_row1 = []

        for j in range(0, len(unique_vals),2):
          if j < len(unique_vals):
            output_row1.append(unique_vals[j])
            if j+1 < len(unique_vals):
                output_row1.append(unique_vals[j])
          
        if len(output_row1)>0:
            output_rows.append(output_row1[:cols])

        output_row2 = []
        for j in range(1, len(unique_vals),2):
          if j < len(unique_vals):
              output_row2.append(unique_vals[j])
              if j+1 < len(unique_vals):
                output_row2.append(unique_vals[j])


        if len(output_row2)> 0:
            output_rows.append(output_row2[:cols])


    return np.array(output_rows)


def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    # Convert input_grid to numpy array
    grid = np.array(input_grid)

    # 1. Identify Objects (not directly used in the final logic, but good for debugging)
    # objects = find_objects(grid)

    # 2. Find Separator Columns
    separator_cols = find_separator_columns(grid)

    # 3. Object Extraction to the Right of the Separator
    extracted_objects = extract_objects_right_of_separator(grid, separator_cols)
    
    # 4. create box
    boxed_objects = create_box(extracted_objects)

    # 5. Remove Separator Columns (implicitly done in step 3)

    # 6. Create Output
    output_grid = create_output(boxed_objects)
    
    return output_grid.tolist()