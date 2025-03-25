```python
"""
1.  **Identify Inner Azure Region:** Locate the rectangular region of azure (8) pixels within the input grid. This region is enclosed by a border of gray (5) pixels, which is itself enclosed by a border of black (0) pixels.
2.  **Extract Top-Left Azure:** Get the azure pixels that form from left to right, from top to bottom.
3.  **Create Output Grid:** Create a 3x3 output grid.
4.  **Populate Output Grid:** Place the extracted azure pixels into the top-left of the output grid.
5.  **Fill Remaining:** Fill the remaining cells of the output grid with black (0) pixels.
"""

import numpy as np

def find_azure_region(grid):
    """Finds the bounding box of the azure (8) region."""
    rows, cols = np.where(grid == 8)
    if len(rows) == 0:
        return None  # No azure region found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def extract_top_left_azure(grid, top_left, bottom_right):
    """Extracts azure pixels, starting from top-left going right and down"""
    azure_pixels = []
    
    min_row, min_col = top_left
    max_row, max_col = bottom_right

    for r in range(min_row, max_row + 1):
      for c in range(min_col, max_col+ 1):
        if grid[r,c] == 8:
          azure_pixels.append(grid[r,c])
        else:
          azure_pixels.append(0)

    return azure_pixels

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)

    # 1. Identify Inner Azure Region
    azure_region = find_azure_region(input_grid)
    if azure_region is None:
        return np.zeros((3, 3), dtype=int)  # Return a 3x3 black grid if no azure region

    top_left, bottom_right = azure_region

    # 2. Extract Top-Left Azure
    azure_pixels = extract_top_left_azure(input_grid, top_left, bottom_right)

    # 3. Create Output Grid
    output_grid = np.zeros((3, 3), dtype=int)

    # 4. Populate Output Grid & 5. Fill Remaining
    for i in range(min(9, len(azure_pixels))):  # Iterate up to 9 (3x3 grid size) or fewer pixels
        row = i // 3
        col = i % 3
        output_grid[row, col] = azure_pixels[i]

    return output_grid
```