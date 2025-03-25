"""
1. **Identify Lines:** Scan the input grid to identify all "lines". A line is a sequence of one or more contiguous pixels of the same non-zero color, aligned either horizontally or vertically.
2. **Filter Lines:**  Ignore any "lines" that consist of only a single pixel (length = 1).
3. **Fill Between:** For each identified line with a length greater than 1:
    - Determine the start and end points of the line.
    - Iterate through the pixels *between* the start and end points (exclusive of the endpoints themselves).
    - Change the color of these intermediate pixels to red (value 2).
4. **Output:**  The modified grid, with the spaces between qualifying lines filled with red, is the output.
"""

import numpy as np

def _find_lines(grid):
    lines = []
    rows, cols = grid.shape

    # Horizontal lines
    for r in range(rows):
        start = None
        for c in range(cols):
            if grid[r, c] != 0:
                if start is None:
                    start = (r, c)
            elif start is not None:
                lines.append({
                    "color": grid[r, start[1]],
                    "start_point": start,
                    "end_point": (r, c - 1),
                    "length": c - start[1],
                    "orientation": "horizontal"
                })
                start = None
        if start is not None:
            lines.append({
                "color": grid[r, start[1]],
                "start_point": start,
                "end_point": (r, cols - 1),
                "length": cols - start[1],
                "orientation": "horizontal"
            })

    # Vertical lines
    for c in range(cols):
        start = None
        for r in range(rows):
            if grid[r, c] != 0:
                if start is None:
                    start = (r, c)
            elif start is not None:
                lines.append({
                    "color": grid[start[0], c],
                    "start_point": start,
                    "end_point": (r - 1, c),
                    "length": r - start[0],
                    "orientation": "vertical"
                })
                start = None
        if start is not None:
            lines.append({
                "color": grid[start[0], c],
                "start_point": start,
                "end_point": (rows - 1, c),
                "length": rows - start[0],
                "orientation": "vertical"
            })

    return lines

def _fill_between(grid, line):
    if line["length"] > 1:
        if line["orientation"] == "horizontal":
            for c in range(line["start_point"][1] + 1, line["end_point"][1]):
                grid[line["start_point"][0], c] = 2
        elif line["orientation"] == "vertical":
            for r in range(line["start_point"][0] + 1, line["end_point"][0]):
                grid[r, line["start_point"][1]] = 2
    return grid

def transform(input_grid):
    """Transforms the input grid by filling the space between lines of the same color with red (2)."""
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find all lines
    lines = _find_lines(output_grid)

   # fill output pixels
    for line in lines:
      output_grid = _fill_between(output_grid,line)

    return output_grid