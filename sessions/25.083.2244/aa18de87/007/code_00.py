"""
1.  **Identify Lines:** Find all horizontal and vertical lines in the input grid. A line is a contiguous sequence of pixels of the *same non-zero color* with a length greater than 1.
2.  **Group Lines:** Group the lines by their color and orientation (horizontal or vertical).
3.  **Fill Regions within Each Group:** For each group of lines (same color and orientation):
    *   **Horizontal Lines:**
        *   Find the bounding box:
          - get all starting row,col pairs and ending row,col pairs.
          - find the min row, min col, max row, and max col.
        * fill a region between rows min_row + 1 and max_row-1 with red(2) in the original grid.
        * fill a region between columns min_col + 1 and max_col -1.
    *   **Vertical Lines:**
        *   Find the bounding box:
          - get all starting row,col pairs and ending row,col pairs.
          - find the min row, min col, max row, and max col.
        * fill a region between rows min_row + 1 and max_row-1 with red(2) in the original grid.
        * fill a region between columns min_col + 1 and max_col -1.
4. **Output:** Return the modified grid with the filled regions. The output grid contains the original lines and the filled regions.
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
                if c - start[1] > 1:
                    lines.append({
                        "color": grid[r, start[1]],
                        "start_point": start,
                        "end_point": (r, c - 1),
                        "length": c - start[1],
                        "orientation": "horizontal"
                    })
                start = None
        if start is not None and cols - start[1] > 1:
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
                if r - start[0] > 1:
                    lines.append({
                        "color": grid[start[0], c],
                        "start_point": start,
                        "end_point": (r - 1, c),
                        "length": r - start[0],
                        "orientation": "vertical"
                    })
                start = None
        if start is not None and rows - start[0] > 1:
            lines.append({
                "color": grid[start[0], c],
                "start_point": start,
                "end_point": (rows - 1, c),
                "length": rows - start[0],
                "orientation": "vertical"
            })

    return lines

def _group_lines(lines):
    groups = {}
    for line in lines:
        color = line["color"]
        orientation = line["orientation"]
        key = (color, orientation)
        if key not in groups:
            groups[key] = []
        groups[key].append(line)
    return groups

def _fill_region(grid, grouped_lines):
    output_grid = np.copy(grid)
    for (color, orientation), lines in grouped_lines.items():
        if not lines:
            continue

        if orientation == "horizontal":
            rows = [line["start_point"][0] for line in lines]
            min_row = min(rows)
            max_row = max(rows)
            cols_start = [line["start_point"][1] for line in lines]
            cols_end = [line["end_point"][1] for line in lines]
            min_col = min(cols_start + cols_end)
            max_col = max(cols_start + cols_end)

            for r in range(min_row + 1, max_row):
              for c in range(output_grid.shape[1]):
                output_grid[r,c] = 2

        elif orientation == "vertical":
            cols = [line["start_point"][1] for line in lines]
            min_col = min(cols)
            max_col = max(cols)
            rows_start = [line["start_point"][0] for line in lines]
            rows_end = [line["end_point"][0] for line in lines]

            min_row = min(rows_start + rows_end)
            max_row = max(rows_start + rows_end)
            for c in range(min_col + 1, max_col ):
              for r in range(output_grid.shape[0]):
                output_grid[r,c] = 2
    return output_grid


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find all lines and filter lines of length 1
    lines = _find_lines(output_grid)

    # group by color and orientation
    grouped_lines = _group_lines(lines)

    # fill regions
    output_grid = _fill_region(output_grid, grouped_lines)

    return output_grid