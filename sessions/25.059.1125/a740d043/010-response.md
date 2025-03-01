# a740d043 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate all distinct colored regions within the input grid, ignoring the most frequent color (blue/1 in this case)
2.  **Extract Colors:**  Extract the colors of these regions, including what remains of the most frequent color (white/0)
3.  **Arrange Horizontally:** Create a new horizontal sequence of the unique colors, in order Green, White and Red
4.  **Duplicate row:** Repeat this sequence to add another identical row below the first. The new dimensions are number of unique colors x 2 rows.
5. **Output:** Output the new grid.
"""

import numpy as np

def get_objects(grid):
    """Find distinct colored regions, excluding the most frequent color."""
    unique_colors = np.unique(grid)
    counts = [np.sum(grid == color) for color in unique_colors]
    most_frequent_color = unique_colors[np.argmax(counts)]
    
    objects = []
    for color in unique_colors:
        if color != most_frequent_color:
            objects.append(color)
    return objects, most_frequent_color

def transform(input_grid):
    # Find distinct objects and the most frequent (background) color
    objects, background_color = get_objects(input_grid)

    #insert background color as white
    objects.insert(1,0)

    # Create the output grid:  Duplicate Row
    output_grid = np.array([objects, objects])

    return output_grid
```
