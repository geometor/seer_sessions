"""
1.  **Identify Objects:** Divide the input grid into distinct rectangular objects based on contiguous regions of the same color, excluding white (0).
2.  **Categorize by Initial Position:** Divide these objects into four positional groups: Top-Left (azure, grey, green), Top-Right (red, blue, maroon), Middle-Left (magenta, yellow), and other groups as applicable
3.  **Apply Transformations:**
    *   Objects starting in the "Top-Left" move to "Middle-Left" keeping the original size and the same nesting with the relative nesting.
    *    Objects starting in the "Top-Right" move to the "Middle-Right", keeping the original size and the same nesting with the relative nesting.
    *   Objects starting in "Middle-Left" move to "Bottom-Middle", keeping the original size and the same nesting with the relative nesting.
4. **Reconstruct Grid:** Combine the transformed objects, filling any remaining space with white (0), to create the output grid.
"""

import numpy as np

def find_objects(grid):
    """
    Finds distinct objects in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, object_pixels):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        object_pixels.append((r, c))
        dfs(r + 1, c, color, object_pixels)
        dfs(r - 1, c, color, object_pixels)
        dfs(r, c + 1, color, object_pixels)
        dfs(r, c - 1, color, object_pixels)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                object_pixels = []
                dfs(r, c, grid[r, c], object_pixels)
                if object_pixels:
                    objects.append({
                        'color': grid[r, c],
                        'pixels': object_pixels
                    })
    return objects

def categorize_objects(objects, grid_shape):
    """
    Categorizes objects based on their initial position.
    """
    top_left = []
    top_right = []
    middle_left = []
    other = []

    for obj in objects:
        min_r, min_c = float('inf'), float('inf')
        for r, c in obj['pixels']:
            min_r = min(min_r, r)
            min_c = min(min_c, c)

        if min_r < grid_shape[0] // 3 and min_c < grid_shape[1] // 2:
            top_left.append(obj)
        elif min_r < grid_shape[0] / 3 and min_c >= grid_shape[1] // 2:
            top_right.append(obj)
        elif min_r < grid_shape[0] * (2/3) and min_c < grid_shape[1] /2 and min_r >= grid_shape[0] / 3:
            middle_left.append(obj)
        
        else:
            other.append(obj) #Consider other cases for generalization.
    return top_left, top_right, middle_left, other

def move_objects(objects, grid_shape, category):
   
    moved_objects = []

    for obj in objects:
        new_pixels = []
        if category == "top_left":  # move_down_left
              # Calculate the offset needed to shift the object
            min_row = min([r for r, c in obj['pixels']])
            min_col = min([c for r, c in obj['pixels']])
            max_row = max([r for r,c in obj['pixels']])

            row_offset =  (grid_shape[0] // 3) - min_row
            
            #Calculate new pixel coordinates.            
            for r, c in obj['pixels']:                
                new_pixels.append((r + row_offset , c))

        elif category == "top_right": #move down right
              # Calculate the offset needed to shift the object
            min_row = min([r for r, c in obj['pixels']])
            min_col = min([c for r, c in obj['pixels']])
            max_row = max([r for r,c in obj['pixels']])
            max_col = max([c for r, c in obj['pixels']])

            row_offset = (grid_shape[0]//3) - min_row
            col_offset = 0
            
            #Calculate new pixel coordinates.            
            for r, c in obj['pixels']:                
                new_pixels.append((r + row_offset, c))
        elif category == "middle_left": #bottom middle
            min_row = min([r for r, c in obj['pixels']])
            min_col = min([c for r, c in obj['pixels']])
            row_offset =  grid_shape[0] * (2/3) - min_row
            for r, c in obj['pixels']:
                new_pixels.append((r + row_offset,c ))
        else:
             new_pixels = obj['pixels']

        moved_objects.append({
            'color': obj['color'],
            'pixels': new_pixels
        })
    return moved_objects

def reconstruct_grid(moved_objects, original_grid_shape):
    """Reconstructs the grid from the transformed objects."""
    new_grid = np.zeros(original_grid_shape, dtype=int)
    for obj in moved_objects:
        for r, c in obj['pixels']:
            if 0 <= r < original_grid_shape[0] and 0 <= c < original_grid_shape[1]: #Boundary check
                new_grid[r, c] = obj['color']
    return new_grid
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    original_grid_shape = input_grid.shape

    # Find objects
    objects = find_objects(input_grid)

    # catagorize objects
    top_left, top_right, middle_left, other = categorize_objects(objects, original_grid_shape)

     # Move objects based on category.
    moved_top_left = move_objects(top_left, original_grid_shape, "top_left")
    moved_top_right = move_objects(top_right, original_grid_shape, "top_right")
    moved_middle_left = move_objects(middle_left, original_grid_shape, "middle_left")
    moved_other = move_objects(other, original_grid_shape, "other")

    # Combine moved objects
    all_moved_objects = moved_top_left + moved_top_right + moved_middle_left + moved_other

     # Reconstruct the grid
    output_grid = reconstruct_grid(all_moved_objects, original_grid_shape)

    return output_grid