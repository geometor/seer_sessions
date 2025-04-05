```python
"""
Transforms an input sequence (list of integers) containing only 0s and 2s into an output sequence. The transformation rule is as follows:
1. Identify contiguous runs (blocks) consisting solely of the integer 2 within the input sequence.
2. For each identified run of 2s:
   a. Determine the length of the run (L).
   b. Calculate the number of elements at the end of this run that should be changed to 8. This number is floor(L / 2).
   c. If this number is greater than zero, modify the corresponding positions in the output sequence by changing the value from 2 to 8 for the last floor(L / 2) elements of the run. The first ceil(L / 2) elements of the run remain 2.
3. Elements that were originally 0 in the input sequence remain 0 in the output sequence.
The output sequence will contain integers 0, 2, and 8.
"""

import math
# No other specific libraries needed for this logic.

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (1D list).
    
    Args:
        input_grid: A list of integers (0s and 2s).
        
    Returns:
        A new list of integers (0s, 2s, and 8s) representing the transformed grid.
    """
    
    # initialize output_grid as a copy of the input to preserve 0s and original 2s
    output_grid = list(input_grid)
    n = len(input_grid)
    i = 0 # current index for scanning the input_grid

    # Iterate through the list to find runs of '2's
    while i < n:
        # Check if the current element is '2', indicating a potential start of a run
        if input_grid[i] == 2:
            # Found the start of a run
            start_index = i
            
            # Find the end of the run
            j = i + 1
            while j < n and input_grid[j] == 2:
                j += 1
            # The run ends at index j-1 (inclusive)
            end_index = j - 1 
            
            # Calculate the length of the identified run
            run_length = end_index - start_index + 1

            # Calculate the number of '2's to change to '8' at the end of the run
            num_to_change = math.floor(run_length / 2)

            # If there are elements to change (i.e., run length >= 2)
            if num_to_change > 0:
                # Calculate the starting index within the grid for the change
                # This is the index of the first element that needs to become '8'
                change_start_index = end_index - num_to_change + 1
                
                # Update the output_grid by changing the relevant '2's to '8's
                for k in range(change_start_index, end_index + 1):
                    output_grid[k] = 8
            
            # Move the main iterator 'i' past the processed run
            # 'j' is already at the position immediately after the run
            i = j 
        else:
            # If the element is not '2', just move to the next element
            i += 1

    # Return the modified grid
    return output_grid

```