```python
import math

def transform(input_list):
    """
    Transforms the input list based on the following rule:
    1. Iterate through the input list to identify consecutive runs (blocks) of the digit 2.
    2. For each identified run of 2s:
        a. Calculate the length of the run (L).
        b. Calculate the number of elements to change to 8: floor(L / 2).
        c. Change the last floor(L / 2) elements of the run in the output list to 8.
    3. Elements that are 0, and the initial ceil(L / 2) elements of each run of 2s, remain unchanged.
    """
    
    # Initialize output_list as a copy of the input_list
    output_list = list(input_list)
    n = len(input_list)
    i = 0

    # Iterate through the list to find runs of '2's
    while i < n:
        # Check if the current element is '2'
        if input_list[i] == 2:
            # Found the start of a potential run of '2's
            start_index = i
            j = i + 1
            # Find the end of the run
            while j < n and input_list[j] == 2:
                j += 1
            end_index = j - 1 # Inclusive end index of the run

            # Calculate the length of the run
            run_length = end_index - start_index + 1

            # Calculate the number of '2's to change to '8'
            num_to_change = math.floor(run_length / 2)

            # If there are elements to change
            if num_to_change > 0:
                # Calculate the starting index for the change
                change_start_index = end_index - num_to_change + 1
                # Update the output list by changing '2's to '8's
                for k in range(change_start_index, end_index + 1):
                    output_list[k] = 8
            
            # Move the main iterator past the processed run
            i = j 
        else:
            # If the element is not '2', just move to the next element
            i += 1

    return output_list
```