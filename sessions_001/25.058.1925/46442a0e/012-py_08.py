"""
1.  **Duplicate:** For every pixel in the input grid, create a 2x2 block of the same color in the output grid.
2.  **Mirror Horizontally:**  Create a horizontal mirror image of the expanded grid from step 1.
3.  **Concatenate Horizontally:** Combine the expanded grid (step 1) with its horizontal mirror (step 2), placing the mirrored image to the *right* of the original.
4.  **Mirror Vertically:** Create a vertical mirror image of the horizontally concatenated grid from step 3.
5. **Concatenate Vertically**: Combine the horizontally concatenated grid (step 3) with its vertical mirror (step 4), placing the mirrored version *below* the horizontally combined grid. The final output size will *always* be twice the width and twice the height of the input.
"""

import numpy as np

def transform(input_grid):
    # Create a numpy array from the input grid
    input_array = np.array(input_grid)

    # Get the dimensions of the input grid
    rows, cols = input_array.shape

    # 1. Duplicate each cell to create a 2x2 block.
    duplicated_array = np.repeat(np.repeat(input_array, 2, axis=0), 2, axis=1)
    
    # 2. Mirror horizontally.
    mirrored_horizontal = np.fliplr(duplicated_array)
    
    # 3. Concatenate the original duplicated array with its horizontal mirror.
    intermediate_result = np.hstack((duplicated_array, mirrored_horizontal))

    # 4. Mirror vertically.
    mirrored_vertical = np.flipud(intermediate_result)

    # 5. Concatenate the intermediate result with its vertical mirror.
    output_array = np.vstack((intermediate_result, mirrored_vertical))

    return output_array.tolist()