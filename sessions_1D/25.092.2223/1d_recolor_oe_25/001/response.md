```python
"""
Recolors contiguous horizontal segments of gray (5) pixels based on their sequential order found by scanning top-to-bottom, left-to-right. The first segment becomes azure (8), the second maroon (9), the third azure (8), and so on, alternating between 8 and 9. White (0) pixels remain unchanged.
"""

import numpy as np

def find_gray_segments(grid):
    """
    Finds all contiguous horizontal segments of gray (5) pixels in the grid.

    Args:
        grid: A 2D numpy array representing the input grid.

    Returns:
        A list of tuples, where each tuple represents a segment
        and contains (row_index, start_column_index, end_column_index).
        The list is ordered by the scanning order (top-to-bottom, left-to-right).
    """
    segments = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool) # Keep track of visited gray pixels

    # Iterate through the grid, row by row, then column by column
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is gray and hasn't been visited as part of a segment yet
            if grid[r, c] == 5 and not visited[r, c]:
                start_col = c
                end_col = c
                visited[r, c] = True
                # Extend the segment to the right as long as we find gray pixels
                nc = c + 1
                while nc < width and grid[r, nc] == 5:
                    visited[r, nc] = True
                    end_col = nc
                    nc += 1
                # Record the found segment
                segments.append((r, start_col, end_col))
    return segments

def transform(input_grid):
    """
    Transforms the input grid by recoloring horizontal gray segments.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Find all horizontal gray segments in the specified order
    gray_segments = find_gray_segments(input_grid)

    # Iterate through the found segments and assign alternating colors
    for i, segment in enumerate(gray_segments):
        row, start_col, end_col = segment
        
        # Determine the target color based on the segment's index (order)
        # Even index (0, 2, 4, ...) -> azure (8)
        # Odd index (1, 3, 5, ...) -> maroon (9)
        target_color = 8 if i % 2 == 0 else 9
        
        # Recolor the pixels belonging to this segment in the output grid
        output_grid[row, start_col:end_col+1] = target_color

    return output_grid
```