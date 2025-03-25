```python
"""
1. **Identify Frame:** Find the values and locations of the border of the input image.
2. **Identify inside Clusters:** Find all clusters/objects inside the frame
3.  **Invert location**: transpose frame and inside clusters - if input frame is along the x and y axis, it is only along the x axis in the output, with the contents displayed to it's side, preserving order of the rows, and the contents of each cluster rotated -90 degrees, and their order preserved and presented based on the order on the input grid
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects (regions of the same color) in a grid.
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
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(row + dr, col + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def get_frame(grid):
    """Extracts the frame (outermost rows and columns) of the grid."""
    rows, cols = grid.shape
    frame = []
    for r in range(rows):
        if r == 0 or r == rows -1:
            for c in range(cols):
                frame.append((r,c))
        else:
            frame.append((r, 0))
            frame.append((r, cols-1))
            
    return frame

def get_inside_clusters_location(input_grid, frame_coords):
    """
    Identifies objects located inside the area of the frame.

    Args:
        input_grid: The input grid as a NumPy array.
        frame: list of frame locations

    Returns:
        A list of objects inside frame.
    """
    
    inside_objects_coords = []
    input_rows, input_cols = input_grid.shape

    all_coords = set()
    for r in range(input_rows):
        for c in range(input_cols):
            all_coords.add((r,c))
    
    inside_coords = all_coords - set(frame_coords)
    inside_objects = []
    
    
    inside_grid = np.full(input_grid.shape, -1)
    for r,c in inside_coords:
        inside_grid[r,c] = input_grid[r,c]

    return inside_grid, inside_coords

def transform(input_grid):
    # Convert input grid to numpy array
    input_grid = np.array(input_grid)
    
    
    # 1. Identify Frame:
    frame_coords = get_frame(input_grid)
    frame_grid = np.full(input_grid.shape, -1)
    for r,c in frame_coords:
      frame_grid[r,c] = input_grid[r,c]
    
    # 2. Identify inside Clusters:
    inside_grid, inside_coords = get_inside_clusters_location(input_grid, frame_coords)
    
    # 3. Invert location:
    output_height = max(input_grid.shape[0], len(find_objects(inside_grid))) #find number of objects as proxy for height
    output_width = max(input_grid.shape[1], len(find_objects(frame_grid))) # find number of objects as proxy for width
    output_grid = np.full((output_height, output_width), -1)  # Initialize with -1 (empty)

    # Place frame elements along the x and y axis
    frame_objects = find_objects(frame_grid)

    # frame elements will make up x and y axis
    frame_row_index = 0
    for obj in frame_objects:
        for r, c in obj:
          if frame_row_index < output_grid.shape[0]:
              output_grid[frame_row_index,0] = input_grid[r,c]
              frame_row_index+=1

    # Place inside cluster elements to side of frame
    inside_objects = find_objects(inside_grid)
    inside_object_col = 1 # start one to side of frame
    for obj in inside_objects:
        for r, c in obj:
            if inside_object_col < output_grid.shape[1]:
              output_grid[r, inside_object_col] = input_grid[r,c]
        inside_object_col += 1
        
    output_grid = np.where(output_grid == -1, 9, output_grid)

    return output_grid.tolist()
```