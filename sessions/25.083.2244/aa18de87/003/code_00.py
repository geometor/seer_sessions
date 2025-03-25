"""
1.  **Identify Lines:** Scan the input grid to find all horizontal and vertical lines. A line is a contiguous sequence of pixels of the *same non-zero color*.
2.  **Filter:** Only consider lines with a length greater than 1.
3.  **Same Color Grouping**: Group lines by their color.
4. **Fill Between**: For each color group:
    *   If the group contains more than one line of a particular color and orientation, fill the spaces *between* consecutive lines (horizontal or vertical) of that color with red (2). "Between" is defined as all pixels located exclusively between the start and end coordinates of the lines.
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

def _group_lines_by_color(lines):
    groups = {}
    for line in lines:
        color = line["color"]
        if color not in groups:
            groups[color] = []
        groups[color].append(line)
    return groups

def _fill_between_lines(grid, lines):
    for i in range(len(lines) - 1):
        line1 = lines[i]
        line2 = lines[i+1]

        if line1["orientation"] == "horizontal" and line2["orientation"] == "horizontal" and line1["start_point"][0] == line2["start_point"][0]:
            for c in range(line1["end_point"][1] + 1, line2["start_point"][1]):
                grid[line1["start_point"][0], c] = 2
        elif line1["orientation"] == "vertical" and line2["orientation"] == "vertical" and line1["start_point"][1] == line2["start_point"][1]:
              for r in range(line1["end_point"][0] + 1, line2["start_point"][0]):
                  grid[r,line1["start_point"][1]] = 2
    return grid


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find all lines and filter lines of length 1
    lines = _find_lines(output_grid)

    # group by color
    grouped_lines = _group_lines_by_color(lines)

    # fill between lines in each group
    for color_group in grouped_lines.values():
        # Sort lines within each group by start_point to ensure correct "between" filling
        horizontal_lines = sorted([line for line in color_group if line["orientation"] == "horizontal"], key=lambda x: x["start_point"][1])
        output_grid = _fill_between_lines(output_grid, horizontal_lines)

        vertical_lines = sorted([line for line in color_group if line["orientation"] == "vertical"], key=lambda x: x["start_point"][0])
        output_grid = _fill_between_lines(output_grid, vertical_lines)

    return output_grid