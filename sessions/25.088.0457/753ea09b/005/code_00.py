import numpy as np
from collections import deque

"""
Transformation Rule: Conditional Flood Fill based on Color Counts and Adjacency

1.  **Analyze Colors**: Examine the input grid. Count the occurrences of each color.
2.  **Check Color Count**: If there are fewer than three distinct colors in the grid, return the original grid without changes.
3.  **Identify Key Colors**:
    *   Find the `background_color`, which is the color that appears most frequently.
    *   Identify the two remaining colors. If there are not exactly two other colors, return the original grid.
    *   Compare the counts of these two remaining colors. The one with the *smaller* count is the `fill_color`. If they have the same count, the one with the numerically lower color value is the `fill_color`.
    *   The color that is neither the `background_color` nor the `fill_color` is the `barrier_color`.
4.  **Check Initial Adjacency**: Determine if any pixel with the `fill_color` is directly next to (up, down, left, or right, not diagonally) any pixel with the `background_color` in the original input grid.
5.  **Apply Transformation**:
    *   **If** no `fill_color` pixel is adjacent to a `background_color` pixel, return the original grid unchanged.
    *   **If** at least one `fill_color` pixel *is* adjacent to a `background_color` pixel:
        *   Create a copy of the input grid to modify.
        *   Perform a "flood fill" operation: Imagine the `fill_color` spreading. Starting from all the original positions of the `fill_color`, change the color of any adjacent `background_color` pixel to the `fill_color`.
        *   Continue this process iteratively: any newly colored pixel also spreads the `fill_color` to its adjacent `background_color` neighbors.
        *   The spread stops at the grid boundaries and cannot change the color of `barrier_color` pixels or pixels that were already the `fill_color`.
        *   Return the modified grid after the spread is complete.
"""


def _is_adjacent(grid: np.ndarray, color1: int, color2: int) -> bool:
    """
    Checks if any pixel of color1 is cardinally adjacent to a pixel of color2.
    Optimized by only checking neighbors of color1 pixels.
    """
    rows, cols = grid.shape
    color1_coords = np.argwhere(grid == color1) # Find all coordinates of color1

    for r, c in color1_coords:
        # Check cardinal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within bounds and has color2
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color2:
                return True # Found an adjacency
    return False # No adjacency found after checking all color1 neighbors

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a conditional flood fill based on color frequencies and adjacency.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Analyze Input Colors
    colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(colors, counts))

    # 2. Check Color Count: Need at least 3 colors for the pattern
    if len(colors) < 3:
        return input_grid # Return original if less than 3 colors

    # 3. Identify Key Colors
    # Find background color (most frequent)
    # If there's a tie for most frequent, the logic might need refinement,
    # but np.argmax picks the first occurrence which is deterministic.
    background_color = colors[np.argmax(counts)]

    # Identify the other two colors and their counts
    non_background_colors = []
    non_background_counts = []
    for color, count in color_counts.items():
        if color != background_color:
            non_background_colors.append(color)
            non_background_counts.append(count)

    # Ensure exactly two other colors exist
    if len(non_background_colors) != 2:
        return input_grid # Return original if not exactly 2 other colors

    # Determine fill and barrier colors based on counts (fill = min count)
    color1, color2 = non_background_colors[0], non_background_colors[1]
    count1, count2 = non_background_counts[0], non_background_counts[1]

    if count1 < count2:
        fill_color = color1
        barrier_color = color2
    elif count2 < count1:
        fill_color = color2
        barrier_color = color1
    else: # Tie in counts, use lower color value as fill color
        fill_color = min(color1, color2)
        barrier_color = max(color1, color2)

    # 4. Check Initial Adjacency: Is fill_color adjacent to background_color?
    # Use the optimized helper function
    is_fill_adjacent = _is_adjacent(grid, fill_color, background_color)

    # 5. Perform Transformation
    if not is_fill_adjacent:
        # If fill color doesn't touch background initially, no fill occurs
        return input_grid
    else:
        # Perform flood fill
        output_grid = grid.copy() # Work on a copy
        queue = deque()
        visited = set()

        # Initialize queue and visited set with all initial fill_color pixels
        initial_fill_coords = np.argwhere(grid == fill_color)
        for r, c in initial_fill_coords:
            coord = (r, c)
            queue.append(coord)
            visited.add(coord)

        # BFS Flood Fill
        while queue:
            r, c = queue.popleft()

            # Check 4 cardinal neighbors
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                neighbor_coord = (nr, nc)

                # Check if neighbor is within bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if neighbor is background color (in original grid)
                    # AND has not been visited yet
                    # Note: We check the *original* grid (`grid`) for the background color
                    # but modify the `output_grid`.
                    if grid[nr, nc] == background_color and neighbor_coord not in visited:
                        # Change color in the output grid
                        output_grid[nr, nc] = fill_color
                        # Mark as visited
                        visited.add(neighbor_coord)
                        # Add to queue for further propagation
                        queue.append(neighbor_coord)

        # Convert back to list of lists for the expected output format
        return output_grid.tolist()