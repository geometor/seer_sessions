```python
import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    1. Count the occurrences of each color in the input grid, excluding azure (8) and white (0).
    2. Identify the color that appears most frequently ('preserved_color').
    3. Create an output grid where pixels matching the 'preserved_color' retain their color, 
       and all other pixels are changed to gray (5).
    If no colors other than azure(8) or white(0) are present, all pixels become gray(5).
    """

    # Convert input list of lists to a numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Initialize the output grid as a copy of the input initially
    # or create a new one filled with a default value
    output_array = np.full_like(input_array, 5) # Default to gray (5)

    # --- Step 1: Count color frequencies (excluding 8 and 0) ---
    color_counts = Counter()
    for r in range(rows):
        for c in range(cols):
            color = input_array[r, c]
            if color != 8 and color != 0:
                color_counts[color] += 1

    # --- Step 2: Identify the preserved color ---
    preserved_color = -1 # Initialize with an invalid color
    if color_counts: # Check if there are any non-8/0 colors
        # Find the color with the maximum count
        # If there's a tie, max() typically returns the first one encountered, 
        # or based on key order if using dict directly. Counter might be arbitrary.
        # Let's stick to the description "the most frequent". Examples don't show ties.
        preserved_color = max(color_counts, key=color_counts.get)

    # --- Step 3 & 4: Create output grid based on the preserved color ---
    # Iterate through the input grid and set output pixels
    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] == preserved_color:
                # Keep the pixel if it matches the preserved color
                output_array[r, c] = preserved_color
            else:
                # Otherwise, change it to gray (5)
                output_array[r, c] = 5

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```