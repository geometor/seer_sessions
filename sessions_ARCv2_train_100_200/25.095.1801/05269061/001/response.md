```python
import math

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input grid based on a repeating pattern derived from its non-zero elements.

    1. Determine the height (H) and width (W) of the input grid.
    2. Scan the input grid row by row, left to right, to find the unique non-zero 
       elements in their order of first appearance, forming a sequence S.
    3. Record the coordinates (r0, c0) of the very first non-zero element encountered.
    4. Calculate the length L of the sequence S.
    5. Calculate an offset k = (-(r0 + c0)) % L. Handle the case where L is 0 (no non-zeros found).
    6. Create a new output grid of dimensions H x W.
    7. Fill each cell (r, c) of the output grid with the value S[(r + c + k) % L].
    """

    # 1. Determine dimensions
    if not input_grid or not input_grid[0]:
        return [] # Handle empty grid case
    height = len(input_grid)
    width = len(input_grid[0])

    # 2. Scan input to find sequence S and first non-zero coordinates (r0, c0)
    non_zero_sequence = []
    found_non_zeros = set()
    first_non_zero_coord = None

    for r in range(height):
        for c in range(width):
            value = input_grid[r][c]
            if value != 0:
                # 3. Record coordinates of the first non-zero element
                if first_non_zero_coord is None:
                    first_non_zero_coord = (r, c)
                
                # Add to sequence if it's a new non-zero value
                if value not in found_non_zeros:
                    non_zero_sequence.append(value)
                    found_non_zeros.add(value)

    # Handle case where no non-zero elements are found
    if not non_zero_sequence:
        # Return a grid of zeros with the same dimensions
        return [[0 for _ in range(width)] for _ in range(height)]

    # 4. Calculate length L
    seq_len = len(non_zero_sequence)

    # 5. Calculate offset k
    r0, c0 = first_non_zero_coord
    # We use floor division for negative numbers to ensure correct modulo behavior consistent with examples
    offset_k = (-(r0 + c0)) % seq_len 

    # 6. Create a new output grid
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # 7. Fill the output grid based on the pattern
    for r in range(height):
        for c in range(width):
            # Calculate the index into the sequence
            index = (r + c + offset_k) % seq_len
            # Assign the value from the sequence
            output_grid[r][c] = non_zero_sequence[index]

    return output_grid
```