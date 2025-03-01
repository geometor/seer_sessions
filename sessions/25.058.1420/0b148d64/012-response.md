# 0b148d64 • 012 • refine_coder

---
```python
"""
1.  **Identify the green region:** Locate all green (3) pixels within the input grid.
2.  **Determine the shape:** Analyze the shape formed by the green pixels. The shape may be a rectangle or a single pixel.
3.  **Extract the green region:** Extract the green region. If the green region is surrounded by white, which is surrounded by red, extract the green pixels and the surrounding white pixels.
4.  **Construct output:** Create the output grid. The output grid contains only the extracted green pixels. If the extracted shape has any missing cells to create a perfect rectangle or square, fill in those cells with the same green color.
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

def extract_region(grid, region_coords):
    """Extracts a region from the grid given its coordinates."""
    rows, cols = zip(*region_coords)  # Unzip coordinates
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return grid[min_row:max_row + 1, min_col:max_col + 1]

def pad_to_square(grid, color):
    """Pads a rectangular region to a square."""
    height, width = grid.shape
    side = max(height, width)
    padded_grid = np.full((side, side), color, dtype=grid.dtype)
    row_offset = (side - height) // 2
    col_offset = (side - width) // 2
    padded_grid[row_offset:row_offset + height, col_offset:col_offset + width] = grid
    return padded_grid

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    # Convert to numpy array
    input_grid = np.array(input_grid)

    # Find green objects.
    green_objects = find_object_with_context(input_grid, 3)

    # Handle no green objects
    if not green_objects:
        return [[]]
        
    # Extract and process.
    extracted_grids = []
    for obj in green_objects:
        extracted_region = extract_region(input_grid, obj['coords'])
        extracted_grids.append(extracted_region)

    # Determine largest extracted shape and pad all to match.
    if len(extracted_grids) > 0:
        max_height = max(grid.shape[0] for grid in extracted_grids)
        max_width = max(grid.shape[1] for grid in extracted_grids)
        
        if max_height != max_width:
            #make square
            target_size = max(max_height, max_width)
            output_grid = np.full((target_size,target_size), 3, dtype=int) #fill square with green

            #copy object to output_grid
            obj_height = extracted_grids[0].shape[0]
            obj_width = extracted_grids[0].shape[1]
            row_start = (target_size - obj_height) // 2
            col_start = (target_size - obj_width) // 2
            output_grid[row_start:row_start+obj_height, col_start:col_start+obj_width] = extracted_grids[0]

        else: #already square
            output_grid = extracted_grids[0]
    else:
        return [[]] #nothing green
    
    return output_grid.tolist()
```
