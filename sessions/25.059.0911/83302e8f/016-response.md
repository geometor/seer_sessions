# 83302e8f • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Maroon Lines:** Locate all horizontal and vertical lines formed by maroon (9) pixels in the input grid.
2.  **Define Enclosed Areas:**  These lines create a set of rectangular enclosed areas.
3.  **Alternating Fill:** Starting from the top-left enclosed area, fill it with yellow (4).
4. **Propogate Filling:**
    -   Fill the area to the right with green (3).
    - Fill the area to the bottom with green(3).
5.  **Continue Alternation:** For each subsequent enclosed area:
    *   If the area to the left has been filled, fill this area with the other color among green and yellow.
    *   If an area has neighboring filled areas to both the left and above, fill this area with the other color among green and yellow.
    *   If there is no adjacent filled area, fill this area with yellow (4, as in the top-left).

In Summary the program fills the areas formed by the maroon pixels, alternatingly assigning green and yellow colors to the enclosed areas.
"""

import numpy as np

def get_enclosed_areas(grid):
    rows, cols = grid.shape
    enclosed_areas = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_maroon(r, c):
        return 0 <= r < rows and 0 <= c < cols and grid[r, c] == 9

    def dfs(r, c, current_area):
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or visited[r, c]
            or is_maroon(r, c)
        ):
            return
        visited[r, c] = True
        current_area.append((r, c))
        dfs(r + 1, c, current_area)
        dfs(r - 1, c, current_area)
        dfs(r, c + 1, current_area)
        dfs(r, c - 1, current_area)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and not is_maroon(r, c):
                current_area = []
                dfs(r, c, current_area)
                if current_area:
                    enclosed_areas.append(current_area)
    return enclosed_areas

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # get enclosed areas
    enclosed_areas = get_enclosed_areas(input_grid)

    # fill the areas
    filled = set()
    for area in enclosed_areas:
        area.sort() #sort the area so filling starts in top left.
        start_r, start_c = area[0]

        #determine fill color
        fill_color = 4
        for r, c in [(start_r,start_c-1),(start_r-1,start_c)]: #check left and above
            if (r,c) in filled:
                if output_grid[r,c] == 3:
                    fill_color = 4
                else:
                    fill_color = 3
                break

        for r, c in area:
            output_grid[r, c] = fill_color
            filled.add((r,c))
    return output_grid
```
