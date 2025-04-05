```python
import math

"""
Transforms a space-separated sequence of digits ('0', '2') based on contiguous subsequences.
Preprocessing: Splits the input string by spaces into a list of digit strings.
Action: Identifies all maximal contiguous subsequences composed solely of "2"s within the list.
For_Each_Sequence:
  - Input: Sequence of "2"s of length L.
  - Calculate: Number of changes N = (L + (1 if L is even else 0)) // 2. (Integer division).
  - Modify: In the output list, changes the last N elements corresponding to this sequence from "2" to "8".
Other_Digits: Elements "0" and any "2"s not part of the last N elements of a sequence remain unchanged.
Postprocessing: Joins the elements of the modified list back into a single string separated by spaces.
"""

def _find_end_of_sequence(data_list, start_index, target_char):
    """Finds the index after the end of a contiguous sequence of target_char in a list."""
    i = start_index
    while i < len(data_list) and data_list[i] == target_char:
        i += 1
    return i

def _calculate_num_changes(seq_length):
    """Calculates the number of trailing '2's to change to '8' based on sequence length L."""
    # (seq_length % 2 == 0) evaluates to 1 if L is even, 0 if L is odd
    is_even = 1 if seq_length % 2 == 0 else 0
    # Formula: N = (L + is_even) // 2
    return (seq_length + is_even) // 2

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the space-separated input string.

    Args:
        input_str: The input string containing '0' and '2' separated by spaces.

    Returns:
        The transformed string containing '0', '2', and '8' separated by spaces.
    """
    # Preprocessing: Split the input string by spaces into a list of digit strings.
    input_list = input_str.split(' ')
    
    # Initialize output_list as a copy of the input list.
    output_list = list(input_list)
    n = len(output_list)
    i = 0 # Initialize index for iterating through the list

    # Iterate through the list
    while i < n:
        # If the current element is '0', skip it
        if output_list[i] == '0':
            i += 1
            continue

        # If the current element is '2', find the sequence
        if output_list[i] == '2':
            # Identify the start index of the contiguous sequence of '2's
            seq_start_index = i
            # Find the end index (exclusive) of the contiguous sequence of '2's
            seq_end_index = _find_end_of_sequence(output_list, seq_start_index, '2')

            # Calculate the length (L) of the sequence
            seq_length = seq_end_index - seq_start_index

            # Only proceed if a valid sequence was found
            if seq_length > 0:
                # Calculate the number of '2's to change to '8' at the end
                num_changes = _calculate_num_changes(seq_length)

                # Determine the starting index for the changes within the sequence
                change_start_index = seq_end_index - num_changes

                # Modify the output list: Change the last 'num_changes' elements of the sequence to '8'
                for j in range(change_start_index, seq_end_index):
                    if j < n: # Ensure index is within bounds (should always be true here)
                        output_list[j] = '8'

            # Advance the main index past the processed sequence
            i = seq_end_index
        else:
             # Handle unexpected characters defensively (though not expected per task)
             i += 1

    # Postprocessing: Join the elements of the modified list back into a space-separated string.
    return " ".join(output_list)

```