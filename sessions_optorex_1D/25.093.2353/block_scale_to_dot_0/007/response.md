```python
import math
# No other specific libraries seem necessary based on the logic.

"""
Transforms a 1D sequence of single-digit integers based on the following rule:
1. Identify all non-zero digits and their positions (indices) in the sequence.
2. Examine each contiguous segment composed entirely of zeros that is located strictly *between* two non-zero digits found in step 1.
3. Let the non-zero digit to the left of such a zero segment be 'L' (at index 'i'), and the non-zero digit to the right be 'R' (at index 'j').
4. Apply the filling rule:
   - If 'L' is 2 AND 'R' is *not* 2, fill the zero segment (elements from index i+1 to j-1) with the value of 'R'.
   - If 'L' is *not* 2 AND 'R' *is* 2, fill the zero segment (elements from index i+1 to j-1) with the value of 'L'.
   - In all other cases for the boundaries (both are 2, or neither is 2), the zero segment remains unchanged.
5. Zero segments not strictly between two non-zero numbers (e.g., at the start/end of the sequence, or adjacent to only one non-zero number) are not modified.
6. The length of the sequence remains constant.
"""

def find_non_zero_indices(grid: list[int]) -> list[int]:
    """Finds the indices of all non-zero elements in the grid."""
    return [i for i, x in enumerate(grid) if x != 0]

def transform(input_grid) -> list[int]:
    """
    Applies the transformation rule to the input sequence.
    """
    # Ensure input is a list for easier manipulation and copying
    input_list = list(input_grid) 
    
    # Initialize output_grid as a mutable copy of the input
    # Changes will be made to this grid, preserving the original input_list for checks
    output_grid = list(input_list)
    n = len(input_list)

    # Step 1: Identify all non-zero elements and their indices (boundaries)
    non_zero_indices = find_non_zero_indices(input_list)

    # Step 2 & 3: Iterate through consecutive pairs of non-zero indices to find potential segments
    # We need at least two non-zero numbers to define a segment *between* them.
    for idx in range(len(non_zero_indices) - 1):
        i = non_zero_indices[idx]      # Index of the left boundary
        j = non_zero_indices[idx + 1]  # Index of the right boundary

        # Step 4a: Check if there is a gap (one or more elements) between the boundaries
        if j > i + 1:
            # Step 4b: Extract the segment between the boundaries from the *original* input
            segment = input_list[i + 1 : j]
            
            # Step 4c: Check if this segment consists *only* of zeros
            is_zero_segment = all(x == 0 for x in segment)

            if is_zero_segment:
                # Step 4d: Get the values of the boundary elements
                left_val = input_list[i]
                right_val = input_list[j]

                # Step 4e: Determine the fill value based on the specific conditional logic involving '2'
                fill_value = None # Use None to indicate no fill needed by default
                if left_val == 2 and right_val != 2:
                    # Fill with the right value if left is 2 and right is not 2
                    fill_value = right_val
                elif left_val != 2 and right_val == 2:
                    # Fill with the left value if left is not 2 and right is 2
                    fill_value = left_val
                
                # Step 4f: If a fill condition was met (fill_value is not None), update the output grid
                if fill_value is not None:
                    for k in range(i + 1, j):
                        output_grid[k] = fill_value
                # Otherwise (both 2, neither 2, or fill_value is None), the segment remains zeros 
                # as initialized in output_grid (copied from input_list)

    # Step 5: Return the modified grid
    return output_grid
```