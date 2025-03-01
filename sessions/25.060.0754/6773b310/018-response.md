# 6773b310 • 018 • refine_coder

---
```python
"""
1.  **Identify Azure Lines:** Find all horizontal lines in the input grid that are completely filled with azure (8) pixels.
2.  **Define Sections:**
    *   If there are two azure lines:
        *   The *top* section consists of all rows above the first azure line.
        *   The *middle* section consists of all rows between the two azure lines (excluding the azure lines themselves).
        *   The *bottom* section consists of all rows below the second azure line.
    *   If there is only one azure line:
        *   The *top* section consists of all rows above the azure line.
        *   The *middle* section is empty, and it will have zero magenta pixels.
        *   The *bottom* section consists of all rows below the azure line.
    *   If no azure lines are present: The output is all white `[[0,0,0]]`

3.  **Count Magenta Pixels:** For each of the three sections (top, middle, bottom), count the number of magenta (6) pixels.

4.  **Generate Output:** Create a 1x3 output grid.
    *   For the *top* section: If the magenta pixel count is greater than 0, set the first element of the output grid to 1 (blue); otherwise, set it to 0 (white).
    *   For the *middle* section: If the magenta pixel count is greater than 0, set the second element of the output grid to 1 (blue); otherwise, set it to 0 (white).
    *   For the *bottom* section: If the magenta pixel count is greater than 0, set the third element of the output grid to 1 (blue); otherwise, set it to 0 (white).

5. **Return 1x3 Grid:** The output is always this 1x3 grid.
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
        return output_grid.tolist() # all white if no lines

    # Count magenta pixels and set output values
    for i, (start, end) in enumerate(sections):
        magenta_count = count_pixels_in_section(input_grid, start, end, 6)
        output_grid[0, i] = 1 if magenta_count > 0 else 0

    return output_grid.tolist()
```
