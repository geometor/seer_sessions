# 09629e4f • 020 • refine_coder

---
```python
"""
1.  **Identify Gray Lines:** Find all horizontal lines (rows) in the input grid that consist entirely of gray pixels (value 5).

2.  **Determine Regions and Boundaries:**
    *   If no gray lines are found, check colors adjacent to the bottom of the grid, return a solid color grid.
    *   If one gray line is found, it divides the grid into two regions: "above" and "below." The gray line is the "top boundary". The bottom edge of the grid is the "bottom boundary"
    *   If two or more gray lines are found, use the first two.  These lines define three regions: "above" (above the first line), "middle" (between the two lines), and "below" (below the second line). The first gray line is the "top boundary". The second gray line is the "middle boundary." The bottom edge of the grid is the "bottom boundary".

3.  **Determine Fill Color for Each Region:**
    *   **Above Region:** Find all pixels in the input grid that are *adjacent* (horizontally, vertically, or diagonally) to the *first* gray line.  Determine the most frequent color among these adjacent pixels. This is the fill color for the "above" region.
    *   **Middle Region (if it exists):** Find all pixels adjacent to the *second* gray line. Determine the most frequent color. This is the fill color for the "middle" region.
    *   **Below Region:**
        *    If there are two gray lines, consider colors adjacent to the second gray line
        *    If there is only one gray line, consider colors *adjacent to bottom edge of input grid*.
        *   Find all pixels adjacent to this bottom boundary, and use the most frequent color.

4.  **Handle Color Ties:** If there's a tie for the most frequent color:
    *   If the tie includes any color *other* than white (0), choose one of the non-white colors.
    *   Otherwise, if all tied colors are white, choose white (0)

5.  **Fill Regions:**
    *   Fill the "above" region with its determined color.
    *   Fill the "middle" region (if it exists) with its determined color.
    *   Fill the "below" region with its determined color.
    *   Preserve the gray lines in the output.

6. **Return:** The result is the transformed grid.
"""

import numpy as np
from collections import Counter

def get_adjacent_colors(grid, row_index, col_index):
    """Gets colors adjacent to a given cell, handling boundaries."""
    rows, cols = grid.shape
    adjacent_colors = []

    # Orthogonal
    if row_index > 0:
        adjacent_colors.append(grid[row_index - 1, col_index])  # Up
    if row_index < rows - 1:
        adjacent_colors.append(grid[row_index + 1, col_index])  # Down
    if col_index > 0:
        adjacent_colors.append(grid[row_index, col_index - 1])  # Left
    if col_index < cols - 1:
        adjacent_colors.append(grid[row_index, col_index + 1])  # Right

    # Diagonal
    if row_index > 0 and col_index > 0:
        adjacent_colors.append(grid[row_index - 1, col_index - 1])  # Up-Left
    if row_index > 0 and col_index < cols - 1:
        adjacent_colors.append(grid[row_index - 1, col_index + 1])  # Up-Right
    if row_index < rows - 1 and col_index > 0:
        adjacent_colors.append(grid[row_index + 1, col_index - 1])  # Down-Left
    if row_index < rows - 1 and col_index < cols - 1:
        adjacent_colors.append(grid[row_index + 1, col_index + 1])  # Down-Right

    return adjacent_colors

def most_frequent_color(colors):
    """Returns the most frequent color, with tie-breaking rules."""
    counts = Counter(colors)

    # Remove 0 from counts if other colors exist
    if 0 in counts and len(counts) > 1:
        del counts[0]

    if not counts:
        return 0

    max_count = max(counts.values())
    most_frequent = [color for color, count in counts.items() if count == max_count]

    return most_frequent[0] if most_frequent else 0

def get_adjacent_to_line(grid, line_row):
    """Gets colors adjacent to an entire gray line."""
    adjacent_colors = []
    for col in range(grid.shape[1]):
        if grid[line_row, col] == 5:
            adjacent_colors.extend(get_adjacent_colors(grid, line_row, col))
    return adjacent_colors

def get_adjacent_to_bottom(grid):
    """Gets colors adjacent to the bottom edge of the grid."""
    rows, cols = grid.shape
    adjacent_colors = []
    for col in range(cols):
        adjacent_colors.extend(get_adjacent_colors(grid, rows - 1, col))
    return adjacent_colors

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find gray lines
    gray_lines = [r for r in range(rows) if np.all(input_grid[r] == 5)]

    if not gray_lines:  # No gray lines
        adjacent_colors = get_adjacent_to_bottom(input_grid)
        fill_color = most_frequent_color(adjacent_colors)
        output_grid[:] = fill_color
        return output_grid.tolist()

    # Region 1 (Above first gray line)
    top_line = gray_lines[0]
    adjacent_colors_top = get_adjacent_to_line(input_grid, top_line)
    fill_color_top = most_frequent_color(adjacent_colors_top)
    output_grid[:top_line, :] = fill_color_top
    output_grid[top_line, :] = 5  # Preserve first gray line


    if len(gray_lines) >= 2: # Two or more gray lines

        middle_line = gray_lines[1]

        # Middle region
        adjacent_colors_middle = get_adjacent_to_line(input_grid, middle_line)
        fill_color_middle = most_frequent_color(adjacent_colors_middle)
        output_grid[top_line+1:middle_line, :] = fill_color_middle

        # Bottom Region
        adjacent_colors_bottom = get_adjacent_to_line(input_grid, middle_line)
        fill_color_bottom = most_frequent_color(adjacent_colors_bottom)
        output_grid[middle_line+1:,:] = fill_color_bottom

        # Preserve gray lines
        output_grid[middle_line, :] = 5 # Preserve gray line

    else: # Only one gray line
        # Bottom Region (adjacent to bottom of input grid)
        adjacent_colors_bottom = get_adjacent_to_bottom(input_grid)
        fill_color_bottom = most_frequent_color(adjacent_colors_bottom)
        output_grid[top_line + 1:, :] = fill_color_bottom


    return output_grid.tolist()
```
