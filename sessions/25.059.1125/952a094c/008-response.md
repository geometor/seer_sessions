# 952a094c • 008 • refine_coder

---
```python
"""
1.  **Identify Azure Regions:** Find all connected regions of azure (color 8) pixels.

2.  **Identify Target Pixels:** Find single, non-black, non-azure pixels directly adjacent (up, down, left, or right, but *not* diagonally) to the azure region(s).

3. **Conditional Reposition target pixels:**
   * If it is above the azure region, move it to the top row (index 1), preserving the original column.
   * If the target pixel is *to the left* of the azure region, move it to the second-to-last row (index -2) of the grid, preserving the original column.
    *  If the target pixel is *below* or *to the right* of the azure region, leave it at original location.

4. **Clear original:** Set the original position to black (color 0) *only* if the pixel was moved.
"""

import numpy as np

def find_azure_regions(grid):
    # Find all connected regions of azure (8) pixels.
    azure_pixels = np.where(grid == 8)
    azure_coords = list(zip(azure_pixels[0], azure_pixels[1]))
    if not azure_coords:
        return []

    regions = []
    visited = set()

    def _explore_region(row, col, current_region):
      # recursively explore connected azure pixels
        if (row, col) in visited or (row, col) not in azure_coords:
            return
        visited.add((row, col))
        current_region.append((row, col))

        # Check adjacent pixels (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < grid.shape[0] and 0 <= new_col < grid.shape[1]:
                _explore_region(new_row, new_col, current_region)

    for row, col in azure_coords:
        if (row, col) not in visited:
            current_region = []
            _explore_region(row, col, current_region)
            regions.append(current_region)
    return regions

def find_target_pixels(grid, azure_regions):
    # Find single, non-black, non-azure pixels adjacent to azure regions.
    target_pixels = []
    for region in azure_regions:
        for row, col in region:
            # Check adjacent cells (up, down, left, right)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < grid.shape[0] and 0 <= new_col < grid.shape[1]:
                    if grid[new_row, new_col] != 0 and grid[new_row, new_col] != 8:
                        # Check if it's a single pixel (not part of a larger object)
                        is_single = True
                        for dr2, dc2 in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            check_row, check_col = new_row + dr2, new_col + dc2
                            if (0 <= check_row < grid.shape[0] and 0 <= check_col < grid.shape[1] and
                                    (check_row, check_col) != (row, col) and
                                    grid[check_row, check_col] == grid[new_row, new_col]):
                                is_single = False
                                break  # It's connected to another pixel of same color
                        if is_single and ((new_row, new_col), grid[new_row,new_col]) not in target_pixels:
                            target_pixels.append( ((new_row, new_col), grid[new_row,new_col]))
    return target_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find azure regions
    azure_regions = find_azure_regions(input_grid)

    # find target pixels
    target_pixels = find_target_pixels(input_grid, azure_regions)

    # reposition target pixels
    for (row, col), color in target_pixels:
        is_above = False
        is_left = False
        for a_row, a_col in azure_regions[0]: # only check against the first region...
            if col == a_col and row < a_row:
                is_above = True
                break
            if row == a_row and col < a_col:
                is_left = True
                break

        if is_above or is_left:
            output_grid[row,col] = 0 # clear original only if moved

        if is_above:
            output_grid[1, col] = color
        elif is_left:
            output_grid[-2, col] = color

    return output_grid
```
