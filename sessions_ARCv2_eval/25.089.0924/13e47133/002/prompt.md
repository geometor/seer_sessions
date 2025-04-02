
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1.  Identify the boundary color (Red=2) and the background color (the most frequent color in the input excluding Red=2).
2.  Create the output grid as a copy of the input grid.
3.  Find distinct connected regions of non-boundary pixels in the input grid using BFS, treating boundary pixels as walls.
4.  For each region:
    a.  Identify all "source pixels" within the region in the *input* grid. A source pixel is neither the background color nor the boundary color.
    b.  If the region contains source pixels:
        i.  For each pixel within the region's coordinates in the *output* grid:
            - Calculate the Manhattan distance to all source pixels belonging to this region.
            - Find the minimum distance.
            - Identify all source pixels at this minimum distance.
            - Apply tie-breaking: select the source pixel with the minimum row index, then the minimum column index among those tied for minimum distance.
            - Set the output grid pixel's color to the color of the selected source pixel.
    c.  If the region contains no source pixels, its pixels in the output grid remain unchanged from the initial copy.
5.  Return the modified output grid.
"""

def get_background_color(grid, boundary_color=2):
    """Finds the most frequent color in the grid, excluding the boundary color."""
    colors, counts = np.unique(grid, return_counts=True)
    max_count = 0
    background = 0 # Default background
    # Find the most frequent non-boundary color
    found_non_boundary = False
    sorted_indices = np.argsort(-counts) # Sort counts descending

    for idx in sorted_indices:
        color = colors[idx]
        if color != boundary_color:
             background = color
             found_non_boundary = True
             break
             
    # If only boundary color exists, pick 0 as default, although this case might not matter
    # based on the logic as no regions would be processed. If other colors exist but only
    # boundary and sources, pick the most frequent source as background? No, the prompt
    # implied a dominant background. Let's stick to the most frequent non-boundary.
    # If no non-boundary color exists, the concept of background might be irrelevant.
    # Let's assume a background always exists if there are non-boundary pixels.
    # If the grid contains only boundary cells, this function might return 0 or the boundary color itself.
    # Check the first non-boundary color found.
    if not found_non_boundary and len(colors) > 0:
         # Handle cases where only boundary color exists or something unexpected
         # Pick the smallest color value as a fallback if needed, or 0.
         non_boundary_colors = colors[colors != boundary_color]
         if len(non_boundary_colors) > 0:
             background = np.min(non_boundary_colors) # Fallback strategy
         else:
             background = 0 # Default if truly only boundary color

    return background

def manhattan_distance(p1, p2):
    """Calculates Manhattan distance between two points (r1, c1) and (r2, c2)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    """
    Applies the described region-filling transformation based on closest source pixels.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape
    boundary_color = 2
    background_color = get_background_color(input_np, boundary_color)
    visited = np.zeros_like(input_np, dtype=bool)

    # Iterate through each cell to find the start of a new region
    for r in range(rows):
        for c in range(cols):
            # If the cell is not a boundary and hasn't been visited yet, start BFS
            if input_np[r, c] != boundary_color and not visited[r, c]:
                region_coords = []
                region_sources = []
                q = deque([(r, c)])
                visited[r, c] = True

                # Perform BFS to find all cells in the current connected region
                while q:
                    curr_r, curr_c = q.popleft()
                    region_coords.append((curr_r, curr_c))

                    # Check if the current cell is a source pixel
                    pixel_color = input_np[curr_r, curr_c]
                    if pixel_color != background_color and pixel_color != boundary_color:
                        region_sources.append((curr_r, curr_c, pixel_color))

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds and if neighbor is valid (not boundary, not visited)
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           input_np[nr, nc] != boundary_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # After finding all cells and sources for the region, fill it if sources exist
                if region_sources:
                    for reg_r, reg_c in region_coords:
                        min_dist = float('inf')
                        closest_sources = []

                        # Calculate distance to all sources in this region
                        for src_r, src_c, src_color in region_sources:
                            dist = manhattan_distance((reg_r, reg_c), (src_r, src_c))
                            if dist < min_dist:
                                min_dist = dist
                                closest_sources = [(src_r, src_c, src_color)]
                            elif dist == min_dist:
                                closest_sources.append((src_r, src_c, src_color))

                        # Apply tie-breaking rule (min row, then min col)
                        if closest_sources:
                            closest_sources.sort(key=lambda x: (x[0], x[1])) # Sort by row, then col
                            winning_source_color = closest_sources[0][2]
                            output_grid[reg_r, reg_c] = winning_source_color
                # If region_sources is empty, the output_grid pixels retain their original input value (copied initially)

    return output_grid.tolist() # Return as list of lists
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
7 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 8
1 8 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 4 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 3 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 4 1 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 2 1 1 1
1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
7 7 7 7 7 7 7 7 2 8 8 8 8 8 8 8 8 8 8 8
7 8 8 8 8 8 8 7 2 8 4 4 4 4 4 4 4 4 4 8
7 8 7 7 7 7 8 7 2 8 4 8 8 8 8 8 8 8 4 8
7 8 7 8 8 7 8 7 2 8 4 8 4 4 4 4 4 8 4 8
7 8 7 8 8 7 8 7 2 8 4 8 4 8 8 8 4 8 4 8
7 8 7 8 8 7 8 7 2 8 4 8 4 4 4 4 4 8 4 8
7 8 7 8 8 7 8 7 2 8 4 8 8 8 8 8 8 8 4 8
7 8 7 8 8 7 8 7 2 8 4 4 4 4 4 4 4 4 4 8
7 8 7 8 8 7 8 7 2 8 8 8 8 8 8 8 8 8 4 8
7 8 7 8 8 7 8 7 2 2 2 2 2 2 2 2 2 8 4 8
7 8 7 8 8 7 8 7 2 3 3 3 3 3 3 3 2 8 4 8
7 8 7 8 8 7 8 7 2 3 4 4 4 4 4 3 2 8 4 8
7 8 7 8 8 7 8 7 2 3 4 3 3 3 4 3 2 8 4 8
7 8 7 8 8 7 8 7 2 3 4 4 4 4 4 3 2 8 4 8
7 8 7 8 8 7 8 7 2 3 3 3 3 3 3 3 2 8 4 8
7 8 7 8 8 7 8 7 2 2 2 2 2 2 2 2 2 8 4 8
7 8 7 8 8 7 8 7 2 8 8 8 8 8 8 8 8 8 4 8
7 8 7 7 7 7 8 7 2 8 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 7 2 8 4 4 4 4 4 4 4 4 4 8
7 7 7 7 7 7 7 7 2 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
7 7 7 7 7 7 7 7 2 8 8 8 8 8 8 8 8 8 8 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 4 4 8
7 8 8 8 8 8 8 8 2 3 3 3 3 3 3 3 2 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 3 2 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 3 2 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 3 2 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 3 2 4 4 8
7 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 8 2 4 4 4 4 4 4 4 4 4 4 8
```
Match: False
Pixels Off: 140
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 70.0

## Example 2:
Input:
```
4 4 4 4 4 4 4 4 4 4 2 8 4 4 4 4 4 4 4 4
4 3 4 4 4 4 4 4 4 4 2 4 1 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 2 5 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 0 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4 4 4 4 4 4 4 4 2 8 8 8 8 8 8 8 8 8
4 3 3 3 3 3 3 3 3 4 2 8 1 1 1 1 1 1 1 8
4 3 4 4 4 4 4 4 3 4 2 8 1 8 8 8 8 8 1 8
4 3 4 3 3 3 3 4 3 4 2 8 1 8 1 1 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 8 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 8 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 8 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 8 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 1 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 8 8 8 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 1 1 1 1 1 1 8
4 3 4 3 4 4 3 4 3 4 2 8 8 8 8 8 8 8 8 8
4 3 4 3 4 4 3 4 3 4 2 2 2 2 2 2 2 2 2 2
4 3 4 3 4 4 3 4 3 4 2 5 5 5 5 5 5 5 5 5
4 3 4 3 4 4 3 4 3 4 2 5 0 0 0 0 0 0 0 5
4 3 4 3 4 4 3 4 3 4 2 5 0 1 1 1 1 1 0 5
4 3 4 3 3 3 3 4 3 4 2 5 0 1 5 5 5 1 0 5
4 3 4 4 4 4 4 4 3 4 2 5 0 1 1 1 1 1 0 5
4 3 3 3 3 3 3 3 3 4 2 5 0 0 0 0 0 0 0 5
4 4 4 4 4 4 4 4 4 4 2 5 5 5 5 5 5 5 5 5
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3 2 8 8 8 8 8 8 8 8 8
3 3 3 3 3 3 3 3 3 3 2 8 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 8 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 8 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 8 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 8 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 8 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 8 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 8 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 8 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 8 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 8 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 2
3 3 3 3 3 3 3 3 3 3 2 5 5 5 5 5 5 5 5 5
3 3 3 3 3 3 3 3 3 3 2 5 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 2 5 0 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 5 0 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 5 0 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 5 0 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 5 0 1 1 1 1 1 1 1
```
Match: False
Pixels Off: 189
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 94.5
