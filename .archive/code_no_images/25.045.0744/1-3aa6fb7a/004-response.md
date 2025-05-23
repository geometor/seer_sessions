# 25.045.0744 • 1-3aa6fb7a • 004 Response

---

*text:*

```python
"""
For the first connected component of color 8 (ordered by topmost cell position), change the cell below its topmost cell to color 1. For the second component, change the cell to the right of its topmost cell to color 1. For the third component, change the cell to the left of its topmost cell to color 1.
"""

import copy

def find_connected_regions(grid, color):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    regions = []

    def get_neighbors(r, c):
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        return neighbors

    def bfs(r, c, current_region):
        q = [(r, c)]
        visited[r][c] = True
        current_region.append((r, c))
        while q:
            row, col = q.pop(0)
            for nr, nc in get_neighbors(row, col):
                if grid[nr][nc] == color and not visited[nr][nc]:
                    visited[nr][nc] = True
                    current_region.append((nr, nc))
                    q.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == color and not visited[r][c]:
                current_region = []
                bfs(r, c, current_region)
                regions.append(current_region)
    return regions

def find_topmost_cell(region):
    topmost_cell = region[0]
    for r, c in region:
        if r < topmost_cell[0] or (r == topmost_cell[0] and c < topmost_cell[1]):
            topmost_cell = (r, c)
    return topmost_cell

def transform(input_grid):
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0
    output_grid = copy.deepcopy(input_grid)

    regions = find_connected_regions(input_grid, 8)
    if not regions:
        return output_grid

    regions_with_topmost = []
    for region in regions:
        topmost_cell = find_topmost_cell(region)
        regions_with_topmost.append((topmost_cell, region))

    regions_with_topmost.sort(key=lambda item: (item[0][0], item[0][1]))

    for i in range(min(len(regions_with_topmost), 3)):
        topmost_cell, _ = regions_with_topmost[i]
        r, c = topmost_cell
        if i == 0: # First block: change cell below
            if r + 1 < rows:
                output_grid[r+1][c] = 1
        elif i == 1: # Second block: change cell to the right
            if c + 1 < cols:
                output_grid[r][c+1] = 1
        elif i == 2: # Third block: change cell to the left
            if c - 1 >= 0:
                output_grid[r][c-1] = 1
    return output_grid


if __name__ == '__main__':

    input = [
        [0, 0, 0, 0, 8, 8, 0],
        [0, 0, 0, 0, 0, 8, 0],
        [0, 0, 8, 0, 0, 0, 0],
        [0, 0, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 8, 8, 0, 0]
    ]

    expected_output = [
        [0, 0, 0, 0, 8, 8, 0],
        [0, 0, 0, 0, 1, 8, 0],
        [0, 0, 8, 1, 0, 0, 0],
        [0, 0, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 8, 0, 0],
        [0, 0, 0, 8, 8, 0, 0]
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
```
