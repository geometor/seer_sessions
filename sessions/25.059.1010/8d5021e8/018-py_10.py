"""
1.  **Reflect Horizontally:** The input grid is reflected horizontally. Imagine a vertical mirror placed to the right of the input grid; the reflection appears next to the original.
2.  **Reflect Vertically:** The combined grid (original and horizontal reflection) is then reflected vertically. Imagine a horizontal mirror placed below the combined grid; the reflection appears below.
3. **Expansion**: The output grid size is double the size of the input grid in both dimensions.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # 1. Reflect Horizontally:
    # Use np.fliplr() to flip the input array along the horizontal axis (left-to-right).
    horizontal_reflection = np.fliplr(input_array)

    # Concatenate the original array and its horizontal reflection side-by-side.
    combined_horizontal = np.concatenate((input_array, horizontal_reflection), axis=1)

    # 2. Reflect Vertically:
    # Flip the combined array (original + horizontal reflection) along the vertical axis (up-to-down).
    vertical_reflection = np.flipud(combined_horizontal)

    # 3. Combine for Final Output:
    # Concatenate the combined_horizontal array and its vertical reflection.
    output_array = np.concatenate((combined_horizontal, vertical_reflection), axis=0)

    # Convert the NumPy array back to a list of lists for the final output.
    return output_array.tolist()