```python
import numpy as np
from collections import Counter

"""
Analyze the input grid to identify all unique non-white pixel colors (values 1-9).
Count the frequency of each unique non-white color.
Determine the output grid dimensions:
- Width (W_out) is the number of unique non-white colors found.
- Height (H_out) is calculated as: MaxCount + max(0, H_in - W_out + 1), 
  where MaxCount is the highest frequency of any non-white color, and H_in is the input grid height.
Create an output grid of H_out x W_out, initialized with white (0).
Sort the unique non-white colors based on their frequency counts in descending order.
Iterate through the sorted colors. For each color, assign it to a column in the output grid, 
starting from column 0 for the most frequent color. Fill the column from the top (row 0) downwards 
up to a height equal to the color's frequency count.
The resulting grid, representing a histogram of color frequencies, is the output.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms an input grid into an output grid representing a histogram
    of non-white color frequencies.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output histogram grid.
    """

    # 1. Scan the input grid to identify all unique non-white pixel colors and count frequencies
    h_in, w_in = input_grid.shape
    pixels = input_grid.flatten()
    color_counts = Counter(p for p in pixels if p != 0)

    # 2. Handle the edge case of no non-white colors
    if not color_counts:
        # Output width is 0, height is H_in + 1 according to formula
        # MaxCount = 0, W_out = 0
        # H_out = 0 + max(0, h_in - 0 + 1) = h_in + 1
        h_out = h_in + 1
        w_out = 0
        return np.zeros((h_out, w_out), dtype=int)

    # 3. Determine the number of unique non-white colors (output width)
    w_out = len(color_counts)

    # 4. Find the maximum count among all the unique non-white colors
    max_count = 0
    if color_counts:
      max_count = max(color_counts.values())

    # 5. Input height H_in is already known

    # 6. Calculate the height (H_out) of the output grid
    h_out = max_count + max(0, h_in - w_out + 1)

    # 7. Create a new grid with dimensions H_out x W_out, filled with white (0)
    output_grid = np.zeros((h_out, w_out), dtype=int)

    # 8. Sort the unique non-white colors based on their counts (descending)
    # Sorting by count descending. No explicit tie-breaker needed from examples.
    sorted_colors = sorted(color_counts.items(), key=lambda item: item[1], reverse=True)

    # 9. Iterate through the sorted colors and populate the output grid
    for col_idx, (color, count) in enumerate(sorted_colors):
        # Fill the column from row 0 down to row count - 1 with the color
        if count > 0: # Ensure count is positive before slicing
             # Make sure not to write past the calculated height h_out
             fill_height = min(count, h_out) 
             output_grid[0:fill_height, col_idx] = color

    # 10. The resulting grid is the final output
    return output_grid
```