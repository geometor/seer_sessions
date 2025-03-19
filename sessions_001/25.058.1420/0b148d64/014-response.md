# 0b148d64 • 014 • refine_coder

---
```python
"""
1.  **Identify Green Regions:** Locate all contiguous regions of green (3) pixels in the input grid.
2.  **Check for Context:** For each green region:
    *   Check if it's surrounded by a contiguous region of white (0) pixels.
    *   If white surrounds the green, check if the white region is surrounded by a contiguous region of red (2) pixels.
3. **Conditional Extraction**
    *   If the green is surrounded by white, and the white is surrounded by red, extract the *entire* region (green, white, and red).
    *    If green is surrounded by only white, extract green and surrounding white.
    *   Otherwise, extract only the green region.
4.  **Create Square:** If extracted object is not square, pad with the background color of the extracted region to make a square. If the extracted region includes the red and white context, the output is already the correctly cropped portion of the input.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds all contiguous regions of a given color."""
    visited = set()
    regions = []

    def dfs(row, col):
        """Depth-first search to find contiguous pixels."""
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return []
        
        visited.add((row, col))
        region = [(row, col)]
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            region.extend(dfs(row + dr, col + dc))
        
        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited and grid[row, col] == color:
                regions.append(dfs(row, col))

    return regions

def find_object_with_context(grid, color):
    """Finds objects and some context"""
    regions = find_contiguous_regions(grid, color)
    objects = []
    for region in regions:
        min_row = min(r[0] for r in region)
        max_row = max(r[0] for r in region)
        min_col = min(r[1] for r in region)
        max_col = max(r[1] for r in region)

        objects.append( {
            "coords": region,
            "bounding_box": (min_row, max_row, min_col, max_col)
            } )
    return objects

def get_surrounding_context(grid, obj, color):
    """Gets the contiguous region of a given color surrounding the object."""
    min_row, max_row, min_col, max_col = obj['bounding_box']
    context = []
    visited = set(obj['coords'])

    def dfs(row, col):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return []

        visited.add((row,col))
        current_context = [(row,col)]

        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
          current_context.extend(dfs(row+dr, col+dc))
        return current_context
      
    # Check the boundary around the object's bounding box
    for r in range(min_row - 1, max_row + 2):
        for c in range(min_col - 1, max_col + 2):
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:  # Within grid bounds
                if (r, c) not in obj['coords'] and grid[r,c] == color: #not part of obj, and correct color
                  context.extend(dfs(r,c))
    return list(set(context))

def extract_region_with_context(grid, green_obj):
    """Extracts region including context"""
    min_row, max_row, min_col, max_col = green_obj['bounding_box']

    white_context = get_surrounding_context(grid, green_obj, 0)
    if not white_context:
        # No white context, return only the green region, expanded to include.
      
        coords = green_obj['coords']
        rows, cols = zip(*coords)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
      
        return grid[min_row:max_row+1, min_col:max_col+1], 3 #green background

    red_context = get_surrounding_context(grid, {'coords': white_context, 'bounding_box': bounding_box(white_context)}, 2)

    if not red_context: #white but no red
        #expand to white
        all_coords = green_obj['coords'] + white_context
        rows, cols = zip(*all_coords)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        return grid[min_row:max_row+1, min_col:max_col+1], 0 #white background
    else: #white and red context
        all_coords = green_obj['coords'] + white_context + red_context
        rows, cols = zip(*all_coords)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        return grid[min_row:max_row + 1, min_col:max_col+1], 2 #red background

def bounding_box(coords):
    """calculate bounding box from coords"""
    rows, cols = zip(*coords)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return (min_row, max_row, min_col, max_col)

def pad_to_square(grid, fill_color):
    """Pads a region to a square, filling with the background"""
    height, width = grid.shape
    side = max(height, width)
    padded_grid = np.full((side, side), fill_color, dtype=grid.dtype)
    row_offset = (side - height) // 2
    col_offset = (side - width) // 2
    padded_grid[row_offset:row_offset + height, col_offset:col_offset + width] = grid
    return padded_grid

def transform(input_grid):
    # Convert to numpy array
    input_grid = np.array(input_grid)

    # Find green objects.
    green_objects = find_object_with_context(input_grid, 3)

    # Handle no green objects
    if not green_objects:
        return [[]]
        
    # Extract and process.
    extracted_grids = []
    backgrounds = []
    for obj in green_objects:
        extracted_region, background = extract_region_with_context(input_grid, obj)
        extracted_grids.append(extracted_region)
        backgrounds.append(background)


    if len(extracted_grids) > 0:
        output_grid = pad_to_square(extracted_grids[0], backgrounds[0])
    else:
        return [[]] #nothing green
    
    return output_grid.tolist()
```
