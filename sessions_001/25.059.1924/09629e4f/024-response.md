# 09629e4f • 024 • refine_coder

---
```python
"""
The transformation rule is as follows:

1.  **Identify Horizontal Lines:** Find all horizontal lines composed entirely of grey (5) pixels. These lines are constant and remain unchanged in the output.

2.  **Define Regions:** Divide the input grid into regions. Regions are the areas between the constant grey lines. If no grey lines are present, the entire grid is considered a single region.

3.  **Process Each Region Independently:**
    *   Iterate through each row of the region.
    *   Within each row find contiguous blocks of pixels that are non-zero and not gray (5) and extract these pixels into 'color_groups'.
    *    For each 'color_group', create a corresponding 3x3 block in the output.
    *   Preserve the *relative horizontal positions* of colors within each group when placing them in the 3x3 block. The leftmost color in the group should be on the left side of the 3x3 block, etc. If multiple colors exist on one row, condense them in the output.
    *   If gray (5) valued pixels exist within a row, copy these to the output region.

4.  **Combine Regions:** Combine the processed regions, including the constant grey lines (if any), to create the final output grid. Ensure the regions are placed in the correct order, maintaining the original structure.
"""

import numpy as np

def find_horizontal_lines(grid, color=5):
    """Finds rows that are entirely composed of a specified color."""
    lines = []
    for i, row in enumerate(grid):
        if np.all(row == color):
            lines.append(i)
    return lines

def get_regions(grid, lines):
    """Divides the grid into regions based on the horizontal lines."""
    regions = []
    if not lines:
        regions.append(grid)  # Entire grid is one region
    else:
        # Region before the first line
        regions.append(grid[:lines[0]])
        # Regions between lines
        for i in range(len(lines) - 1):
            regions.append(grid[lines[i] + 1:lines[i+1]])
        # Region after the last line
        regions.append(grid[lines[-1] + 1:])
    return regions

def extract_color_groups(row):
    """Extracts contiguous color groups (non-zero, non-grey) from a row."""
    color_groups = []
    current_group = []
    for x, pixel in enumerate(row):
        if pixel != 0 and pixel != 5:
            current_group.append((x, pixel))
        elif current_group:
            color_groups.append(current_group)
            current_group = []
    if current_group:  # Add last group if any
        color_groups.append(current_group)
    return color_groups

def process_region(region, row_offset):
    """Processes a single region to create its corresponding output."""
    output_region = np.zeros_like(region)
    for y, row in enumerate(region):
        color_groups = extract_color_groups(row)
        for group in color_groups:
            # Determine the starting column for the 3x3 block.  Use the position of the FIRST element of the group
            start_col = group[0][0]

            # place colors within the 3x3 block
            for i, (x, color) in enumerate(group):
              if(start_col + i < region.shape[1]):
                output_region[y, start_col + i] = color

        #copy any gray columns, if any
        for col_index in range(region.shape[1]):
            if 5 in region[:, col_index]:
                output_region[:,col_index] = 5
    return output_region

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find horizontal grey lines
    lines = find_horizontal_lines(input_grid)

    # Divide into regions
    regions = get_regions(input_grid, lines)

    # Initialize output grid
    output_grid = np.zeros_like(input_grid)

    # Process each region
    row_offset = 0
    for i, region in enumerate(regions):
        processed_region = process_region(region, row_offset)

        # Determine where to place the processed region in the output
        if not lines:
            output_grid = processed_region #if no grey lines use whole grid
        else:
            if i == 0:
                output_grid[:lines[0]] = processed_region
            else:
                output_grid[lines[i-1] + 1:lines[i]] = processed_region

    # Copy the constant lines to output
    for line_row in lines:
        output_grid[line_row, :] = input_grid[line_row, :]

    return output_grid.tolist()
```
