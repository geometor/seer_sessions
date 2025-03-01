"""
1.  **Find Azure Lines:** Identify all horizontal lines in the input grid that are completely filled with azure (8) pixels. Record their row indices.

2.  **Define Sections:** Divide the input grid into three sections (top, middle, bottom) based on the azure lines:
    *   **Two Azure Lines:**
        *   *Top*: Rows above the first azure line.
        *   *Middle*: Rows between the two azure lines (excluding the lines).
        *   *Bottom*: Rows below the second azure line.
    *   **One Azure Line:**
        *   *Top*: Rows above the azure line.
        *   *Middle*: An empty section (conceptually exists, but has zero height, therefore zero magenta pixels).
        *   *Bottom*: Rows below the azure line.
    *   **No Azure Lines:**
        *   *Top*: An empty section (zero height).
        *   *Middle*: An empty section (zero height).
        *   *Bottom*: All rows of the input grid.

3.  **Count Magenta Pixels:** For each section (top, middle, bottom), count the number of magenta (6) pixels within that section's row boundaries.

4.  **Generate Output:** Create a 1x3 output grid.
    *   *Top*: If the top section's magenta pixel count is greater than 0, set the first element of the output grid to 1 (blue); otherwise, set it to 0 (white).
    *   *Middle*: If the middle section's magenta pixel count is greater than 0, set the second element to 1 (blue); otherwise, set it to 0 (white).
    *   *Bottom*: If the bottom section's magenta pixel count is greater than 0, set the third element to 1 (blue); otherwise, set it to 0 (white).

5.  **Return 1x3 Grid:** Return the resulting 1x3 grid.
"""

import numpy as np

def find_horizontal_lines(grid, color):
    line_rows = []
    for i, row in enumerate(grid):
        if all(pixel == color for pixel in row):
            line_rows.append(i)
    return line_rows

def count_pixels_in_section(grid, start_row, end_row, color):
    count = 0
    for row in grid[start_row:end_row]:
        for pixel in row:
            if pixel == color:
                count += 1
    return count

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Find the rows of the azure (8) lines
    azure_lines = find_horizontal_lines(input_grid, 8)

    # Initialize the output grid as a 1x3 array
    output_grid = np.zeros((1, 3), dtype=int)

    # Define the sections based on the number of azure lines
    if len(azure_lines) == 2:
        sections = [
            (0, azure_lines[0]),  # Top section
            (azure_lines[0] + 1, azure_lines[1]),  # Middle section
            (azure_lines[1] + 1, len(input_grid))  # Bottom section
        ]
    elif len(azure_lines) == 1:
        sections = [
            (0, azure_lines[0]),  # Top section
            (azure_lines[0], azure_lines[0]), # Middle section (empty)
            (azure_lines[0] + 1, len(input_grid))  # Bottom section
        ]
    else:
        sections = [
            (0, 0), # Top Section (empty)
            (0, 0), # Middle Section (empty)
            (0, len(input_grid))  # Bottom section: all rows
        ]


    # Count magenta pixels and set output values
    for i, (start, end) in enumerate(sections):
        magenta_count = count_pixels_in_section(input_grid, start, end, 6)
        output_grid[0, i] = 1 if magenta_count > 0 else 0

    return output_grid.tolist()