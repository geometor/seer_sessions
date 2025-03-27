```python
import numpy as np
from collections import Counter

"""
Identify the pixel with a unique color (occurs exactly once, excluding white) in the input grid.
Create an output grid of the same dimensions, initially all white (0).
Place the identified unique color pixel at its original location in the output grid.
Draw a 3x3 frame of red (2) pixels around this central pixel in the output grid, respecting grid boundaries.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the unique color pixel rule.

    Args:
        input_grid (list of lists): The input grid with color values 0-9.

    Returns:
        list of lists: The transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # --- Step 1 & 2: Count non-white color frequencies ---
    color_counts = Counter()
    for r in range(height):
        for c in range(width):
            color = input_array[r, c]
            if color != 0:  # Exclude white
                color_counts[color] += 1

    # --- Step 3: Identify the unique color ---
    unique_color = -1
    for color, count in color_counts.items():
        if count == 1:
            unique_color = color
            break
            
    # Handle case where no unique color is found (though not expected based on examples)
    if unique_color == -1:
        # Return an empty or all-white grid matching input size
        return np.zeros_like(input_array).tolist() 

    # --- Step 4: Find the location of the unique color pixel ---
    center_row, center_col = -1, -1
    for r in range(height):
        for c in range(width):
            if input_array[r, c] == unique_color:
                center_row, center_col = r, c
                break
        if center_row != -1: # Stop searching once found
             break

    # --- Step 5: Create and initialize the output grid ---
    output_array = np.zeros_like(input_array, dtype=int)

    # --- Step 6: Place the center pixel ---
    if 0 <= center_row < height and 0 <= center_col < width: # Ensure location is valid
        output_array[center_row, center_col] = unique_color

        # --- Step 7: Draw the red frame ---
        for r_offset in range(-1, 2):  # -1, 0, 1
            for c_offset in range(-1, 2): # -1, 0, 1
                # Skip the center pixel itself
                if r_offset == 0 and c_offset == 0:
                    continue

                # Calculate neighbor coordinates
                nr, nc = center_row + r_offset, center_col + c_offset

                # Check if the neighbor is within grid boundaries
                if 0 <= nr < height and 0 <= nc < width:
                    # Set the neighbor pixel to red (2)
                    output_array[nr, nc] = 2

    # --- Step 8: Return the completed output grid ---
    return output_array.tolist()
```