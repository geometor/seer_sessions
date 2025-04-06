```python
import numpy as np

"""
Transform a 7x7 grid of digits by identifying 3x3 subgrids centered on the digit '7'. 
For each such identified subgrid:
1. Swap the corner elements: top-left (0,0) with bottom-right (2,2) relative to the block.
2. Swap the other corner elements: top-right (0,2) with bottom-left (2,0) relative to the block.
3. Rotate the resulting block 90 degrees clockwise.
Place the transformed block back into the output grid. Cells not part of these 
transformations remain unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the swap-corners-then-rotate transformation to 3x3 subgrids
    centered on the digit 7 within the input grid.
    """
    # Convert input list of lists to a NumPy array for efficient slicing and operations
    input_array = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input. Non-transformed cells will retain their original values.
    output_array = input_array.copy()
    
    rows, cols = input_array.shape

    # Iterate through all possible top-left corners (r, c) of a 3x3 block
    # The loops ensure the 3x3 block fits entirely within the grid dimensions.
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Check if the center cell of the potential 3x3 block is 7
            # Center coordinates relative to the grid are (r+1, c+1)
            if input_array[r + 1, c + 1] == 7:
                # Extract the 3x3 block from the input grid
                block = input_array[r:r + 3, c:c + 3]
                
                # Create a mutable copy of the block to perform swaps
                current_block = block.copy()

                # --- Perform transformations on the copied block ---
                # 1. Swap top-left (0,0) with bottom-right (2,2)
                current_block[0, 0], current_block[2, 2] = current_block[2, 2], current_block[0, 0]
                
                # 2. Swap top-right (0,2) with bottom-left (2,0)
                current_block[0, 2], current_block[2, 0] = current_block[2, 0], current_block[0, 2]

                # 3. Rotate the modified block 90 degrees clockwise (k=-1)
                rotated_block = np.rot90(current_block, k=-1)

                # --- Update the output grid ---
                # Place the finally transformed block into the corresponding position in the output array
                output_array[r:r + 3, c:c + 3] = rotated_block

    # Convert the final NumPy array back to a list of lists format
    output_grid = output_array.tolist()
    return output_grid

```