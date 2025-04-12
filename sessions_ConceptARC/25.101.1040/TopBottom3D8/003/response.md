```python
"""
Transformation Rule:
1. Identify "horizontal bars": Rows where a single non-white color appears in more than half the cells. Record the row index and the dominant color (H_color).
2. Identify "vertical bars": Columns where a single non-white color appears in more than half the cells. Record the column index and the dominant color (V_color).
3. For each intersection point (r, c) where a horizontal bar in row 'r' meets a vertical bar in column 'c':
    a. Get the original color at (r, c) from the input grid (Original_color).
    b. Get the H_color for row r and V_color for column c.
    c. If Original_color equals H_color, change the color at (r, c) in the output grid to V_color.
    d. Else if Original_color equals V_color, change the color at (r, c) in the output grid to H_color.
    e. Otherwise (if Original_color is neither H_color nor V_color, including background), change the color at (r, c) in the output grid to V_color.
4. Pixels not at such intersection points remain unchanged from the input grid.
"""

import numpy as np
from collections import Counter

def _find_bars(grid_np: np.ndarray) -> tuple[dict[int, int], dict[int, int]]:
    """
    Identifies horizontal and vertical bars in the grid.

    A bar is defined as a row or column where a single non-white color
    occupies more than half of the cells in that row/column.

    Args:
        grid_np: The input grid as a NumPy array.

    Returns:
        A tuple containing two dictionaries:
        - h_bars: {row_index: dominant_color} for horizontal bars.
        - v_bars: {col_index: dominant_color} for vertical bars.
    """
    height, width = grid_np.shape
    h_bars = {} # {row_index: dominant_color}
    v_bars = {} # {col_index: dominant_color}
    
    # Find horizontal bars
    for r in range(height):
        line = grid_np[r, :]
        # Count non-white pixels
        counts = Counter(pixel for pixel in line if pixel != 0)
        if not counts:
            continue # Skip rows with only white pixels

        # Find the most frequent non-white color and its count
        # most_common(1) returns list like [(color, count)]
        dominant_color, max_count = counts.most_common(1)[0]

        # Check if the dominant color occurs in more than half the width
        if max_count > width / 2:
            # Ensure it's a single dominant color meeting the criteria
            # (Check if a second color has the same max_count)
            if len(counts) == 1 or counts.most_common(2)[1][1] < max_count:
                 h_bars[r] = dominant_color

    # Find vertical bars
    for c in range(width):
        line = grid_np[:, c]
        # Count non-white pixels
        counts = Counter(pixel for pixel in line if pixel != 0)
        if not counts:
             continue # Skip columns with only white pixels

        # Find the most frequent non-white color and its count
        dominant_color, max_count = counts.most_common(1)[0]

        # Check if the dominant color occurs in more than half the height
        if max_count > height / 2:
             # Ensure it's a single dominant color meeting the criteria
             if len(counts) == 1 or counts.most_common(2)[1][1] < max_count:
                 v_bars[c] = dominant_color

    return h_bars, v_bars


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the intersection color swap transformation based on dominant
    colors in identified horizontal and vertical bars.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_np = input_np.copy()

    # Identify horizontal and vertical bars and their dominant colors
    h_bars, v_bars = _find_bars(input_np)

    # Iterate through the identified intersections
    for r, h_color in h_bars.items():
        for c, v_color in v_bars.items():
            # This is an intersection point (r, c)
            original_color = input_np[r, c]

            # Apply the transformation rule at the intersection
            if original_color == h_color:
                output_np[r, c] = v_color
            elif original_color == v_color:
                output_np[r, c] = h_color
            else:
                # Default case (including background or other colors)
                # Based on analysis, V_color seems to take precedence
                output_np[r, c] = v_color

    # Convert the result back to a list of lists
    return output_np.tolist()
```