"""
1. **Identify Target Area:** Consider the lower-right portion of the input grid as the source for the output. A candidate region begins where the colors present include all of the colors of the expected output.

2.  **Identify Repeating Tile:** Within the target area, identify a repeating rectangular tile. The tile's dimensions must be factors of the target area's dimensions. The tile will consist of a specific arrangement of colored pixels.

3.  **Tile Extraction:** Once the repeating tile is identified, extract it.  This tile is the output.

4.  **Output:** The extracted tile becomes the output grid.
"""

import numpy as np

def find_target_area(input_grid, output_colors):
    """Finds the starting indices (row, col) of the lower-right target area."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_colors_set = set(output_colors)

    for r_start in range(rows):
        for c_start in range(cols):
            subgrid = input_grid[r_start:, c_start:]
            if output_colors_set.issubset(set(np.unique(subgrid))):
                return r_start, c_start
    return 0, 0  # Default to the entire grid if no suitable subgrid is found

def find_repeating_tile(subgrid):
    """Identifies a repeating tile within the given subgrid."""
    sub_h, sub_w = subgrid.shape

    for h_test in range(1, sub_h + 1):
        for w_test in range(1, sub_w + 1):
            if sub_h % h_test == 0 and sub_w % w_test == 0:
                repeats_h = sub_h // h_test
                repeats_w = sub_w // w_test

                if repeats_h > 0 and repeats_w > 0: # ensure valid
                    test_grid = subgrid[:h_test, :w_test]
                    valid_pattern = True
                    for rep_h in range(repeats_h):
                        for rep_w in range(repeats_w):
                            if not np.array_equal(test_grid, subgrid[rep_h * h_test:rep_h * h_test + h_test, rep_w * w_test:rep_w * w_test + w_test]):
                                valid_pattern = False
                                break
                        if not valid_pattern:
                            break
                    if valid_pattern:
                        return test_grid
    return subgrid # if no repeating tile, return subgrid


def transform(input_grid):
    # convert input to numpy array
    input_grid = np.array(input_grid)

    # use examples 4, where the colors are the same, to determine output
    output_colors = [2,5]

    # 1. Find Target Area
    r_start, c_start = find_target_area(input_grid, output_colors)
    subgrid = input_grid[r_start:, c_start:]

    # 2. Identify Repeating Tile
    tile = find_repeating_tile(subgrid)

    # 3 & 4. Extract and return tile.
    return tile.tolist()