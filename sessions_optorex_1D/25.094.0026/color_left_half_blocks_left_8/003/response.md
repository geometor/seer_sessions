```python
import numpy as np
import math

"""
Transforms a 1D NumPy array of digits (0, 2) by modifying runs of consecutive '2's.
For each run of '2's of length L, the last floor(L/2) elements of that run 
are changed from 2 to 8. Zeros act as delimiters and remain unchanged.
"""

def find_runs_of_twos(arr):
    """
    Finds the start index and length of consecutive runs of the number 2.

    Args:
        arr: A 1D NumPy array of integers.

    Yields:
        Tuples of (start_index, length) for each run of 2s.
    """
    n = len(arr)
    i = 0
    while i < n:
        if arr[i] == 2:
            run_start_index = i
            run_length = 0
            # Count the length of the run
            while i < n and arr[i] == 2:
                run_length += 1
                i += 1
            # Yield the details of the found run
            yield (run_start_index, run_length)
            # i is already advanced past the run, continue loop
        else:
            # Move to the next element if not a 2
            i += 1

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array containing integers (0 or 2).

    Returns:
        A 1D NumPy array containing the transformed digits (0, 2, or 8).
    """
    # 1. Create a copy of the input array to store the output.
    output_grid = np.copy(input_grid)
    
    # 2. Find all runs of consecutive '2's using the helper function.
    runs = find_runs_of_twos(input_grid)

    # 3. Iterate through the identified runs.
    for run_start_index, run_length in runs:
        # 4. Calculate the number of elements to change.
        # Use integer division // for floor(L/2).
        num_to_change = run_length // 2
        
        # 5. Modify the latter part of the run if necessary.
        if num_to_change > 0:
            # Calculate the starting index within the array for modification.
            # modify_start_index = run start + (length of run - number to change)
            modify_start_index = run_start_index + (run_length - num_to_change)
            
            # Calculate the end index for modification (exclusive).
            modify_end_index = run_start_index + run_length
            
            # Change the required number of '2's to '8's at the end of the run
            # using array slicing for efficiency.
            output_grid[modify_start_index:modify_end_index] = 8
            
    # 6. Return the modified array.
    return output_grid
```