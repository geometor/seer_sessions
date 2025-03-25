```python
"""
The transformation extracts a sub-grid from the input based on repeating patterns found in the top rows and creates a new output grid.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions of the same color (objects) in a grid.
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
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def get_object_bounds(obj):
    """
    get the bounding box of the object
    return (min_row, min_col, max_row, max_col)
    """
    min_row = min(p[0] for p in obj)
    min_col = min(p[1] for p in obj)
    max_row = max(p[0] for p in obj)
    max_col = max(p[1] for p in obj)
    return min_row, min_col, max_row, max_col
    

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Repeating Objects in the top few rows (e.g., top 3 rows).
    objects = find_objects(input_grid[:3,:])
    
    # Filter out objects that are just the background color filling entire rows

    filtered_objects = []
    for obj in objects:
      min_row, min_col, max_row, max_col = get_object_bounds(obj)
      if (max_col - min_col + 1) != cols:
        filtered_objects.append(obj)

    objects = filtered_objects

    # extract sections by tiling
    
    sections = []

    # use the first object as a starting point.
    if len(objects) > 0:

      obj = objects[0]
      min_row, min_col, max_row, max_col = get_object_bounds(obj)
      object_width = max_col - min_col + 1

      num_repeats = cols // object_width  # Use integer division
      section_height = max_row - min_row + 1
      
      
      for i in range (num_repeats):
          start_col = i * object_width
          end_col   = start_col + object_width
          
          section = input_grid[min_row: max_row+1, start_col: end_col]
          
          # append sections to output
          sections.append(section)


    # 3. Locate Matching Sections
    
    # get a reference section from joining all the objects
    reference_section = None
    
    if len(objects) > 0:
      reference_row = []
      
      for i in range(cols):
        
        found = False
        
        # check each object
        for obj in objects:
          min_row, min_col, max_row, max_col = get_object_bounds(obj)
          # check each object column for a match
          for c in range(min_col, max_col+1):
            if c == i:
              reference_row.append(input_grid[min_row,c])
              found = True
        
        if not found:
          # background
          reference_row.append(-1) # fill value

      
      reference_section = []
      for obj in objects:
        min_row, min_col, max_row, max_col = get_object_bounds(obj)
        reference_section.append(input_grid[min_row:max_row+1, min_col:max_col+1])
      reference_section = np.hstack(reference_section)
      section_height, section_width = reference_section.shape

      # Find matching sections
      for row_start in range(0,rows - section_height + 1):
          row_end = row_start + section_height

          section = input_grid[row_start:row_end, 0:cols]

          if cols % section_width == 0: # only works if evenly tiled
            num_tiles = cols // section_width
            tiled_section = np.tile(reference_section,num_tiles)

            if np.array_equal(section, tiled_section):
              sections.append(section)


    
    
    # 4. Stack Sections vertically

    if len(sections) > 0:
        output_grid = np.vstack(sections)
    else:
        output_grid = np.array([]) # empty output


    return output_grid.tolist()
```