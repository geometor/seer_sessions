```python
import numpy as np

"""
Transforms an input sequence (1D NumPy array of integers) by identifying patterns 
where a non-zero digit 'X' is surrounded by zeros ('[0, X, 0]') in the original 
input and replacing the adjacent zeros with 'X' in the output array to form 
'[X, X, X]'. Elements not part of such a pattern are copied unchanged from input 
to output.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the '[0, X, 0]' to '[X, X, X]' transformation rule to a 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers representing the input sequence.

    Returns:
        A 1D NumPy array of integers representing the transformed sequence.
    """
    # 1. Get the length of the input array.
    n = len(input_grid)

    # 2. Create a copy of the input array to serve as the basis for the output array.
    #    This ensures modifications don't affect the checking conditions based on the original input.
    output_grid = np.copy(input_grid)

    # 3. Handle edge case: If the grid has fewer than 3 elements, the pattern cannot exist.
    if n < 3:
        return output_grid

    # 4. Iterate through the input array from the second element (index 1)
    #    up to the second-to-last element (index n - 2), as we need to check neighbors.
    #    Crucially, use the original 'input_grid' for checks to avoid cascading effects
    #    from modifications made to the 'output_grid' within the same loop pass.
    for i in range(1, n - 1):
        # 5. Check for the '0 X 0' pattern in the input_grid:
        #    a. Element at i-1 is 0?
        #    b. Element at i is non-zero (X)?
        #    c. Element at i+1 is 0?
        if input_grid[i-1] == 0 and input_grid[i] != 0 and input_grid[i+1] == 0:
            # 6. If the pattern is found:
            #    a. Get the non-zero value (X) from the center of the pattern in the input.
            non_zero_val = input_grid[i]
            #    b. Update the corresponding elements (the flanking zeros) in the output_grid.
            output_grid[i-1] = non_zero_val
            #    c. output_grid[i] is already correct (equal to X) because it was copied initially.
            output_grid[i+1] = non_zero_val

    # 7. Return the modified output array.
    return output_grid
```