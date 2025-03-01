# e50d258f • 018 • refine_coder

---
```python
"""
1. Identify Target Objects: Find all rectangles of the same color in the input grid. It appears from example 2 that we are interested in the smallest object, if there is one.
2. Select Specific Rectangle(s): Choose the top-left-most rectangle of the smallest size.
3. Crop: Extract the selected rectangle from the grid.
"""

import numpy as np

def find_rectangles(grid):
    # Find all rectangles of same color
    rectangles = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, top_left):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return []

        visited[r, c] = True
        region = [(r, c)]

        # Explore adjacent cells
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            region.extend(dfs(r + dr, c + dc, color, top_left))
        
        return region

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r,c]!=0:
                color = grid[r, c]
                top_left = (r, c)
                region = dfs(r, c, color, top_left)

                if region:
                    min_row = min(p[0] for p in region)
                    max_row = max(p[0] for p in region)
                    min_col = min(p[1] for p in region)
                    max_col = max(p[1] for p in region)

                    rectangles.append({
                        'color': color,
                        'top_left': (min_row, min_col),
                        'bottom_right': (max_row, max_col),
                        'width': max_col - min_col + 1,
                        'height': max_row - min_row + 1
                    })

    return rectangles

def select_rectangle(rectangles):
    # select the top-left-most of the smallest rectangles

    if not rectangles:
        return None

    # Find the minimum area
    min_area = float('inf')
    for rect in rectangles:
      area = rect['width'] * rect['height']
      if area < min_area:
        min_area = area

    smallest_rectangles = [rect for rect in rectangles if rect['width'] * rect['height'] == min_area]

    if not smallest_rectangles:
      return None
    
    #sort by top left row, then top left col
    smallest_rectangles.sort(key=lambda rect: (rect['top_left'][0], rect['top_left'][1]))

    return smallest_rectangles[0]

def crop_rectangle(grid, top_left, bottom_right):
    # crop the grid based on top_left, bottom_right
    return grid[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find all rectangles
    rectangles = find_rectangles(input_grid)

    #select rectangle
    selected_rect = select_rectangle(rectangles)

    if selected_rect:
      #crop the selected rectangle
      cropped_grid = crop_rectangle(input_grid, selected_rect['top_left'], selected_rect['bottom_right'])
    else:
      cropped_grid = np.array([]) #return empty if nothing found

    return cropped_grid.tolist()
```
