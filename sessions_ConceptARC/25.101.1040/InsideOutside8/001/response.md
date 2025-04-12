```python
import numpy as np
from collections import Counter

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on color frequencies and neighbor rules.

    1.  Identify the background color (assumed to be 0).
    2.  Count the frequency of all non-background colors.
    3.  Identify the 'deleter' color (D) as the most frequent non-background color.
    4.  Identify the 'target' color (T) as the second most frequent non-background color.
    5.  Create an output grid of the same size, filled with the background color.
    6.  Iterate through each pixel of the input grid.
    7.  If a pixel has the 'target' color (T):
        a.  Check if it's on the border of the grid.
        b.  If it's *not* on the border, count its 8 neighbors (including diagonals) that have the 'deleter' color (D).
        c.  If the pixel is *not* on the border AND has 0 or 1 'deleter' neighbors, copy its color (T) to the corresponding position in the output grid.
    8.  Return the output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    background_color = 0

    # --- Step 1 & 2: Count non-background color frequencies ---
    colors, counts = np.unique(input_array, return_counts=True)
    color_counts = Counter(dict(zip(colors, counts)))

    # Remove background color from counts
    if background_color in color_counts:
        del color_counts[background_color]

    # --- Step 3 & 4: Identify deleter (D) and target (T) colors ---
    # Sort colors by frequency (descending)
    sorted_colors = color_counts.most_common()

    if len(sorted_colors) < 2:
        # Not enough non-background colors to define D and T
        # Return an empty grid (all background) as per the observed logic
        return np.full((height, width), background_color, dtype=int).tolist()

    deleter_color = sorted_colors[0][0]
    target_color = sorted_colors[1][0]

    # --- Step 5: Initialize output grid ---
    output_array = np.full_like(input_array, background_color)

    # --- Step 6-8: Iterate and apply rules ---
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is the target color
            if input_array[r, c] == target_color:

                # Check if the pixel is on the border
                is_border = (r == 0 or c == 0 or r == height - 1 or c == width - 1)

                # If not on the border, count deleter neighbors
                if not is_border:
                    deleter_neighbor_count = 0
                    # Iterate through 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip the center pixel itself

                            nr, nc = r + dr, c + dc

                            # Check if neighbor is within grid bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is the deleter color
                                if input_array[nr, nc] == deleter_color:
                                    deleter_neighbor_count += 1
                    
                    # Apply the keep condition
                    if deleter_neighbor_count <= 1:
                         output_array[r, c] = target_color

    # Convert back to list of lists for the required output format
    return output_array.tolist()

```