# 8a004b2b • 006 • refine_coder

---
```python
"""
1.  **Identify Lines:** Examine the input grid. Identify any horizontal or vertical lines that extend from one edge to another. A line consists of a series of adjacent pixels of the same color. The line can begin at any position along an edge.
2.  **Fill Inside of Lines:** Examine the pixels inside (not a part of) the lines.
3.  **Color Selection:** Replace the color of any pixels inside of lines with the color of the line.
"""

import numpy as np

def find_lines(grid):
    """Finds lines that extend from one edge to another."""
    height, width = grid.shape
    lines = []

    # Check for horizontal lines
    for r in range(height):
        first_pixel = grid[r, 0]
        if all(grid[r, c] == first_pixel for c in range(width)):
            lines.append({'orientation': 'horizontal', 'row': r, 'color': first_pixel})
        
        last_pixel = grid[r, width - 1]
        if all(grid[r, c] == last_pixel for c in range(width)):
             lines.append({'orientation': 'horizontal', 'row': r, 'color': last_pixel})

    # Check for vertical lines
    for c in range(width):
        first_pixel = grid[0, c]
        if all(grid[r, c] == first_pixel for r in range(height)):
             lines.append({'orientation': 'vertical', 'col': c, 'color': first_pixel})
        
        last_pixel = grid[height-1, c]
        if all(grid[r,c] == last_pixel for r in range(height)):
            lines.append({'orientation': 'vertical', 'col':c, 'color': last_pixel})
            
    return lines

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find lines
    lines = find_lines(input_grid)

    # Create a set of all line pixel coordinates for quick lookup
    line_pixels = set()
    for line in lines:
        if line['orientation'] == 'horizontal':
            for c in range(width):
                line_pixels.add((line['row'], c))
        else:  # vertical
            for r in range(height):
                line_pixels.add((r, line['col']))

    # Fill inside of lines
    for r in range(height):
        for c in range(width):
            if (r, c) not in line_pixels:  # Check if it IS NOT part of lines
                for line in lines:
                    # Determine color
                    output_grid[r, c] = line['color']
                    break # apply only one color

    return output_grid
```
