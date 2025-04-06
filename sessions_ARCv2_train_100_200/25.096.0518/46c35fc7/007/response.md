```python
import numpy as np

"""
Transforms a 7x7 grid of digits by identifying specific 3x3 subgrids and applying a transformation. 
A 3x3 subgrid is transformed if and only if its center element is 7 AND all 8 surrounding elements within the block are not 7.
The transformation consists of two steps applied to the identified block:
1. Swap corner elements: top-left (0,0) with bottom-right (2,2), and top-right (0,2) with bottom-left (2,0).
2. Rotate the resulting block 90 degrees clockwise.
The transformed block replaces the original block in the output grid. All other cells remain unchanged.
"""

def apply_transformation(block: np.ndarray) -> np.ndarray:
    """Applies the corner-swap and rotation to a 3x3 block."""
    # Create a mutable copy to perform swaps on
    swapped_block = block.copy()

    # Swap top-left (0,0) with bottom-right (2,2)
    swapped_block[0, 0], swapped_block[2, 2] = swapped_block[2, 2], swapped_block[0, 0]
    
    # Swap top-right (0,2) with bottom-left (2,0)
    swapped_block[0, 2], swapped_block[2, 0] = swapped_block[2, 0], swapped_block[0, 2]

    # Rotate the swapped block 90 degrees clockwise
    rotated_block = np.rot90(swapped_block, k=-1) # k=-1 for clockwise

    return rotated_block

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    Identifies 3x3 blocks (center=7, neighbors!=7), transforms them, and updates the grid.
    """
    # Convert input list of lists to a NumPy array for efficient slicing and operations
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input. 
    # Cells not part of any transformation will retain their original values.
    output_array = input_array.copy()
    
    rows, cols = input_array.shape

    # Ensure grid is large enough for 3x3 blocks
    if rows < 3 or cols < 3:
        return input_grid # Or handle error appropriately

    # Iterate through all possible top-left corners (r, c) of a 3x3 block
    # The loops range ensures the 3x3 block fits entirely within the grid dimensions.
    for r in range(rows - 2):
        for c in range(cols - 2):
            
            # Extract the 3x3 block from the input grid
            block = input_array[r:r + 3, c:c + 3]
            
            # Check the criteria for transformation:
            # 1. Center element (1, 1) must be 7
            # 2. The total count of 7s in the block must be exactly 1 (meaning only the center is 7)
            is_center_7 = (block[1, 1] == 7)
            num_sevens_in_block = np.sum(block == 7)
            
            if is_center_7 and num_sevens_in_block == 1:
                # If criteria are met, apply the transformation to the block
                transformed_subgrid = apply_transformation(block)
                
                # Place the transformed block into the corresponding position in the output array
                output_array[r:r + 3, c:c + 3] = transformed_subgrid

    # Convert the final NumPy array back to a list of lists format for the output
    output_grid = output_array.tolist()
    
    return output_grid
```