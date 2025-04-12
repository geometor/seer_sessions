```python
"""
Finds the non-white color (1-9) that appears the least number of times in the input grid.
If there is a tie for the least frequent color, selects the color with the smallest numerical value among the tied colors.
The output is the selected color value itself.
"""

from collections import Counter
import math

def transform(input_grid: list[list[int]]) -> int:
    """
    Transforms the input grid based on the frequency of non-white colors.

    Args:
        input_grid: A list of lists representing the input grid of colors (0-9).

    Returns:
        An integer representing the least frequent non-white color, with ties broken by choosing the smallest color value.
        Returns -1 if no non-white colors are found (edge case).
    """

    # 1. Create a frequency map for non-white colors
    color_counts = Counter()

    # 2. Iterate through the grid and count non-white pixels
    for r in range(len(input_grid)):
        for c in range(len(input_grid[0])):
            color = input_grid[r][c]
            # 3. Ignore white color (0)
            if color != 0:
                color_counts[color] += 1

    # Handle edge case: grid contains only white or is empty
    if not color_counts:
        # Or perhaps return 0? Based on examples, non-white always exists.
        # Returning an indicator like -1 might be clearer if this can happen.
        # For ARC, assuming valid inputs means non-white colors exist.
        # Let's proceed assuming color_counts is not empty.
        # If it could be empty, error handling or a default return (like 0) would be needed.
         return 0 # Or raise an error, or return a specific value like -1


    # 4. Find the minimum frequency count among non-white colors
    min_frequency = min(color_counts.values())

    # 5. Identify all colors that have this minimum frequency
    candidate_colors = [color for color, count in color_counts.items() if count == min_frequency]

    # 6. Select the output color:
    # If only one, it's the result.
    # If multiple (tie), choose the smallest numerical color value among them.
    output_color = min(candidate_colors)

    # The task output is a single number, not a grid.
    return output_color
```