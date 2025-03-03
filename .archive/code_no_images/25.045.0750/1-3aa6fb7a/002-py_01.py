"""
Identifies connected regions of color 8 in the input grid.
For each region, finds the top-leftmost cell and changes the color of a neighboring white cell to blue (1),
prioritizing the right neighbor and then the bottom neighbor.
"""

import copy

def find_regions(grid, color_to_find):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    regions = []

    def explore_region(r, c, current_region):
        if r < 0 or r >= rows or c < 0 or c >= cols or visited[r][c] or grid[r][c] != color_to_find:
            return
        visited[r][c] = True
        current_region.append((r, c))
        explore_region(r + 1, c, current_region)
        explore_region(r - 1, c, current_region)
        explore_region(r, c + 1, current_region)
        explore_region(r, c - 1, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == color_to_find and not visited[r][c]:
                current_region = []
                explore_region(r, c, current_region)
                regions.append(current_region)
    return regions

def find_top_leftmost_cell(region):
    top_row = min(r for r, c in region)
    top_leftmost_col = min(c for r, c in region if r == top_row)
    return top_row, top_leftmost_col

def transform(input_grid):
    output_grid = copy.deepcopy(input_grid)
    regions = find_regions(input_grid, 8)

    for region in regions:
        if not region:
            continue

        top_left_row, top_left_col = find_top_leftmost_cell(region)

        # Check right neighbor
        right_col = top_left_col + 1
        if 0 <= right_col < len(input_grid[0]) and output_grid[top_left_row][right_col] == 0:
            output_grid[top_left_row][right_col] = 1
            continue # Move to the next region after changing color

        # Check bottom neighbor if right neighbor was not changed
        bottom_row = top_left_row + 1
        if 0 <= bottom_row < len(input_grid) and output_grid[bottom_row][top_left_col] == 0:
            output_grid[bottom_row][top_left_col] = 1
            continue # Move to the next region after changing color

    return output_grid


if __name__ == '__main__':

    input = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0],
        [0, 8, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 0],
        [0, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]

    expected_output = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 8, 1, 0, 0, 0, 0],
        [0, 8, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 0],
        [0, 0, 0, 0, 1, 8, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]

    output = transform(input)

    if output == expected_output:
        print("SUCCESS!\n")
    else:
        print("FAILED!\n")
        print("Expected Output:", expected_output)
        print("Transformed Output:", output)

    print()
    assert output == expected_output, "Transformed output does not match expected output."