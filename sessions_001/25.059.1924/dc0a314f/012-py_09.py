"""
1. **Identify the Target Object:** Find the contiguous region (object) containing colors orange (7) and red (2). This is the primary region of interest, which will be called the "target object." The background (0) and other colors (e.g. green (3)) are ignored for the purpose of defining this object's boundaries.
2. **Determine Output Boundaries:** Within the target object, identify a rectangular sub-region. The specific dimensions and location of this sub-region vary across examples, and are not related to other colored regions like the green object.
3. **Extract Subgrid:** Extract the rectangular sub-region from the target object.
4. **Output**: The extracted rectangular subgrid constitutes the output. The output dimensions are not consistent.
"""

import numpy as np

def find_target_object(grid):
    # Find the contiguous region containing colors 7 and 2
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    target_object = []

    def is_target_color(color):
        return color == 7 or color == 2

    def dfs(row, col):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or not is_target_color(grid[row, col])
        ):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for r in range(rows):
        for c in range(cols):
            if is_target_color(grid[r, c]) and not visited[r, c]:
                target_object = dfs(r, c)
                # Return after finding the first target object.  We assume there is only one
                return target_object
    return target_object
                

def extract_subgrid(grid, target_object, output_grid):
    # use the output grid to extract a subgrid from the input grid

    # Get output shape
    output_rows, output_cols = len(output_grid), len(output_grid[0])

    # Convert target_object to a NumPy array for easier indexing
    target_coords = np.array(target_object)

    # Find min and max row/col of the target object, to search within
    min_row, min_col = np.min(target_coords, axis=0)
    max_row, max_col = np.max(target_coords, axis=0)

    # search for the output within the input
    for r_start in range(min_row, max_row - output_rows + 2):
        for c_start in range(min_col, max_col - output_cols + 2):
            subgrid = grid[r_start : r_start + output_rows, c_start : c_start + output_cols]
            if np.array_equal(subgrid, output_grid):                
                return subgrid.tolist()

    return None # should not happen, but avoids an error

def transform(input_grid, output_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the target object (contiguous region of colors 7 and 2)
    target_object = find_target_object(input_grid)

    # if nothing found, return empty grid
    if not target_object: return [[]]

    # Extract the subgrid that corresponds to output
    extracted_region = extract_subgrid(input_grid, target_object, output_grid)

    return extracted_region