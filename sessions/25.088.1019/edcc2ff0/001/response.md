```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1.  **Identify Zones:** The grid is conceptually divided into a Top Section (rows 0-6) and a Bottom Section (rows 7 to end).
2.  **Identify Key Colors:**
    *   Indicator Colors: Non-white colors found in the first column (column 0) of the Top Section.
    *   Background Color: The color located at the top-left corner of the Bottom Section (row 7, column 0).
3.  **Filter Bottom Section:** Create the output Bottom Section by iterating through the input Bottom Section. Any pixel whose color is NOT the Background Color AND NOT one of the Indicator Colors is replaced with the Background Color. Pixels matching the Background Color or an Indicator Color remain unchanged.
4.  **Generate Top Section:** Create the output Top Section based on the Indicator Colors and object counts in the *input* Bottom Section.
    *   For each row `r` (0-6) in the Top Section:
        *   Get the color `C` at `input_grid[r, 0]`.
        *   If `C` is white (0), the entire output row `r` becomes white (0).
        *   If `C` is an Indicator Color:
            *   Count the number `N` of distinct, contiguous objects (connected horizontally/vertically) of color `C` present in the *input* Bottom Section.
            *   In the output grid, set the first `N` cells of row `r` (columns 0 to `N-1`) to color `C`.
            *   Set the remaining cells in row `r` (columns `N` to end) to white (0).
"""

def count_objects(grid_section, target_color):
    """
    Counts the number of distinct contiguous objects of a target_color
    within the given grid_section. Objects are connected horizontally
    and vertically.
    """
    if grid_section is None or grid_section.size == 0:
        return 0

    height, width = grid_section.shape
    visited = np.zeros_like(grid_section, dtype=bool)
    object_count = 0

    for r in range(height):
        for c in range(width):
            # If this cell is the target color and hasn't been visited yet
            # it means we found a new object.
            if grid_section[r, c] == target_color and not visited[r, c]:
                object_count += 1
                # Start a Breadth-First Search (BFS) to find all connected
                # parts of this object and mark them as visited.
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    curr_r, curr_c = q.popleft()
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor is target color and not visited
                            if grid_section[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
    return object_count


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    output_grid = input_grid_np.copy()

    # Define section boundaries
    top_section_rows = 7
    bottom_section_start_row = 7

    # 1. Identify Key Colors
    indicator_colors = set(c for c in input_grid_np[0:top_section_rows, 0] if c != 0)
    # Handle potential empty grid or section
    if height > bottom_section_start_row:
        background_color = input_grid_np[bottom_section_start_row, 0]
    else:
        background_color = 0 # Default or handle as error? Assume default for now.

    # 2. Filter Bottom Section
    if height > bottom_section_start_row:
        for r in range(bottom_section_start_row, height):
            for c in range(width):
                pixel_color = input_grid_np[r, c]
                is_background = (pixel_color == background_color)
                is_indicator = (pixel_color in indicator_colors)
                # If it's not background and not an indicator, replace with background
                if not is_background and not is_indicator:
                    output_grid[r, c] = background_color

    # 3. Generate Top Section
    input_bottom_section = None
    if height > bottom_section_start_row:
        input_bottom_section = input_grid_np[bottom_section_start_row:, :]

    for r in range(top_section_rows):
        indicator_color = input_grid_np[r, 0]

        if indicator_color == 0:
            # If indicator is white, make the whole output row white
            output_grid[r, :] = 0
        else:
            # Count objects of this indicator color in the input bottom section
            num_objects = 0
            if input_bottom_section is not None:
                 num_objects = count_objects(input_bottom_section, indicator_color)

            # Draw the line in the output grid
            if num_objects <= width:
                output_grid[r, 0:num_objects] = indicator_color
                output_grid[r, num_objects:] = 0
            else: # Should not happen with grid constraints, but handle defensively
                 output_grid[r, :] = indicator_color # Fill whole row if count exceeds width


    return output_grid.tolist()
```