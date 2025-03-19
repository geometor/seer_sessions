# a87f7484 • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Select Region:** From the input grid, select a 3x3 sub-grid starting at row 0, column 3 (the first instance of color 4).
2.  **Identify Dominant Color:** Within this 3x3 sub-grid, count the occurrences of each non-zero color.
3.  **Construct Output:** Create the output grid which contains the selected 3x3 subgrid.
4.  **Replace non-dominant colors:** Within the sub-grid, replace all colors except the dominant one to 0.
"""

import numpy as np

def get_dominant_color(grid):
    # count occurences of each color, excluding 0 (white)
    counts = {}
    for row in grid:
        for pixel in row:
            if pixel != 0:
                if pixel not in counts:
                    counts[pixel] = 0
                counts[pixel] += 1
    # find color with max occurences
    dominant_color = 0
    max_count = 0
    for color, count in counts.items():
        if count > max_count:
            max_count = count
            dominant_color = color
    return dominant_color

def transform(input_grid):
    # 1. Select Region: 3x3 sub-grid starting at row 0, column 3.
    sub_grid = [row[3:6] for row in input_grid[0:3]]

    # 2. Identify Dominant Color
    dominant_color = get_dominant_color(sub_grid)
    
    # 3. & 4. Construct output and replace
    output_grid = []
    for row in sub_grid:
      new_row = []
      for pixel in row:
        if pixel == dominant_color:
          new_row.append(pixel)
        else:
          new_row.append(0)
      output_grid.append(new_row)
    
    return output_grid
```
