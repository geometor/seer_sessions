"""
1.  **Identify Color Blocks:** Find all contiguous regions of the same color in the input grid. These are our "color blocks".
2.  **Locate Last object:** Find the last object on the grid which is defined by pixels from right to left, bottom to top, not equal to zero. Split the object into two at the halfway horizontal point.
3.  **Rearrange:** Shift all blocks of values horizontally.
4. **Combine**: The top half of the object from step 2 moves to combine with the preceding object, from right to left.
5. **Adjust Grid:** It is important to eliminate complete rows of zeros from top to bottom.
"""

import numpy as np

def find_objects(grid):
    """Find contiguous regions of the same color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                objects.append(object_pixels)
    return objects

def find_last_object(objects):
    """Find the last object based on right-to-left, bottom-to-top priority."""
    if not objects:
        return None

    # Sort objects based on the bottom-rightmost pixel
    sorted_objects = sorted(objects, key=lambda obj: (max(row for row, _ in obj), max(col for _, col in obj)), reverse=True)
    return sorted_objects[0]

def split_object(object_pixels):
    """Split an object horizontally into two halves."""
    if not object_pixels:
        return [], []

    # Find the horizontal midpoint
    cols = [col for _, col in object_pixels]
    mid_col = (min(cols) + max(cols)) // 2

    top_half = [(row, col) for row, col in object_pixels if col > mid_col]
    bottom_half = [(row, col) for row, col in object_pixels if col <= mid_col]
    return top_half, bottom_half

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Convert input_grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)

    # 1. Find all objects in the grid.
    objects = find_objects(input_grid)

    # 2. Find the last object.
    last_object = find_last_object(objects)

    # 3. Split the last object into two halves.
    top_half, bottom_half = split_object(last_object)
    
    #Remove last_object
    if last_object:
        for r, c in last_object:
            output_grid[r,c] = 0
    
    #Shift object based on last object split
    shift = 0
    if last_object:
        cols = [c for _, c in last_object]
        shift = max(cols) - (min(cols) + max(cols))//2
    
    objects = find_objects(input_grid)
    
    #Reorder objects based on position
    sorted_objects = sorted(objects, key=lambda obj: (max(row for row, _ in obj), max(col for _, col in obj)), reverse=False)

    #Add top_half of last object to the preceding one
    for obj in reversed(sorted_objects):
        if top_half:
            for r,c in obj:
                output_grid[r,c+shift] = input_grid[r,c]
        
        else:
            for r,c in obj:
                output_grid[r,c] = input_grid[r,c]
        
        shift = 0
        top_half = obj

    #Add split pieces to the grid
    if last_object:
        for r,c in top_half:
            output_grid[r,c]= input_grid[r,c]
        for r, c in bottom_half:
            output_grid[r,c + (len(top_half) > 0)] = input_grid[r,c]

    #Remove any rows that contain zeros
    rows_to_keep = ~np.all(output_grid == 0, axis = 1)
    output_grid = output_grid[rows_to_keep]
    
    
    return output_grid