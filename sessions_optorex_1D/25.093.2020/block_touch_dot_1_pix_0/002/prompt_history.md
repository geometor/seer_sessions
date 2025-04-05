
## train_1

**input:**
```
0 3 3 3 3 2 0 0 0 0 0 0
```


**output:**
```
0 3 3 3 3 2 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 2 0 0 0 0 1 0 0 0
```


**output:**
```
0 0 0 2 0 0 0 1 0 0 0 0
```


## train_3

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 2
```


**output:**
```
1 1 1 1 1 1 1 1 1 1 1 2
```


## train_4

**input:**
```
7 7 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
7 7 2 0 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
2 0 0 9 9 9 9 9 0 0 0 0
```


**output:**
```
2 0 9 9 9 9 9 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 2 0 0 8 8 8 8 8 8
```


**output:**
```
0 0 0 2 0 8 8 8 8 8 8 0
```


## train_7

**input:**
```
0 0 0 2 0 0 8 8 8 8 8 0
```


**output:**
```
0 0 0 2 0 8 8 8 8 8 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are sequences of single digits, likely represented as integers, separated by spaces. The length of the sequence appears fixed (12 digits in all examples).
    *   The core operation involves identifying specific patterns within the sequence.
    *   The pattern seems to be a contiguous block (run) of identical non-zero digits.
    *   The transformation rule depends on the element immediately preceding this block.
    *   The action involves shifting this block one position to the left if the preceding element is a zero, and appending a zero at the end to maintain the sequence length.
    *   Crucially, the transformation seems to apply only to the *last* such block found in the sequence when reading from left to right (or equivalently, the first found when reading right to left).
    *   If the condition (preceding element is zero) is not met for the last block, or if no such block exists, the sequence remains unchanged.

*   **YAML Fact Document:**
    
```yaml
    task_description: Identify the last contiguous block of identical non-zero digits and shift it left if preceded by zero.
    elements:
      - object: sequence
        description: A fixed-length list of single-digit integers.
        properties:
          - length: 12 (based on examples)
          - type: List[int]
      - object: block
        description: A contiguous subsequence of identical non-zero digits within the main sequence.
        properties:
          - identity: All digits within the block are the same.
          - value: The digit must be non-zero (1-9).
          - contiguity: Elements are adjacent in the sequence.
        relationship: The task focuses on the *last* such block occurring in the sequence.
      - object: trigger_element
        description: The element immediately preceding the start of the identified 'last block'.
        properties:
          - existence: Must exist (block cannot start at the very beginning of the sequence).
          - value: Must be 0 to trigger the transformation.
    action:
      - name: conditional_shift
        description: If the trigger_element is 0, the 'last block' is moved one position left, replacing the trigger_element, and a 0 is appended to the sequence end.
        condition: trigger_element exists and is 0.
        steps:
          - Identify the start and end indices of the last contiguous block of identical non-zero digits.
          - Check if the block starts after index 0 and if the element at `start_index - 1` is 0.
          - If true:
            - Construct the output sequence by taking elements before the trigger zero, followed by the block, followed by elements after the block in the original input, and finally appending a 0.
          - If false:
            - The output sequence is identical to the input sequence.
    examples_analysis:
      - train_1, train_3, train_4: No change, as the last non-zero block ('2', '2', '2' respectively) is not preceded by '0'.
      - train_2: Last block '1' is preceded by '0'. '1' shifts left, '0' appended.
      - train_5: Last block '99999' is preceded by '0'. Block shifts left, '0' appended.
      - train_6: Last block '888888' is preceded by '0'. Block shifts left, '0' appended.
      - train_7: Last block '88888' is preceded by '0'. Block shifts left, '0' appended.
    ```


*   **Natural Language Program:**

    1.  Convert the input string of space-separated digits into a list of integers.
    2.  Search the list from right to left to find the start index, end index, and value of the last contiguous block composed of identical non-zero digits.
    3.  If no such block is found (e.g., the list contains only zeros or no repeating non-zero digits), return the original input list formatted as a space-separated string.
    4.  If a block is found, check if its start index is greater than 0 (meaning it has a preceding element).
    5.  If the block has a preceding element, check if this preceding element (at `start_index - 1`) is equal to 0.
    6.  If both conditions (block exists, starts after index 0, and is preceded by 0) are true:
        a.  Create a new list by concatenating:
            i.  The elements of the original list from the beginning up to (but not including) the preceding 0 (index `start_index - 1`).
            ii. The identified block of non-zero digits.
            iii.The elements of the original list from the position immediately after the block (`end_index + 1`) to the end of the original list.
            iv. A single integer `0`.
        b.  Convert this new list back into a space-separated string and return it.
    7.  If the conditions in step 5 are not met (block starts at index 0, or the preceding element is not 0), return the original input list formatted as a space-separated string.
```python
import re # Although not strictly necessary for the final implementation, re might be useful for pattern matching in similar tasks
from typing import List, Tuple, Optional

# Helper function to find the last block
def find_last_contiguous_block(data_list: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the start index, end index, and value of the last contiguous block
    of identical non-zero digits in the list.

    Args:
        data_list: The list of integers to search within.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise None.
    """
    last_block_start = -1
    last_block_end = -1
    last_block_value = -1
    n = len(data_list)
    i = 0
    while i < n:
        current_val = data_list[i]
        # Check if the current element is non-zero
        if current_val != 0:
            # Potential start of a block
            start_index = i
            # Find where this block of identical digits ends
            j = i + 1
            while j < n and data_list[j] == current_val:
                j += 1
            end_index = j - 1 # The index of the last element in the block

            # Since we iterate left-to-right, this block is the latest one found so far.
            # Update the record of the last block found.
            last_block_start = start_index
            last_block_end = end_index
            last_block_value = current_val

            # Continue the search *after* this block
            i = j
        else:
            # Current element is zero, move to the next element
            i += 1

    # After checking the whole list, return the details of the last block found
    if last_block_start != -1:
        return last_block_start, last_block_end, last_block_value
    else:
        # No non-zero blocks were found
        return None


def transform(input_str: str) -> str:
    """
    Identifies the last contiguous block of identical non-zero digits in a space-separated string of digits.
    If this block starts after the first position (index > 0) and is immediately preceded by a '0',
    the block is shifted one position to the left (overwriting the preceding '0'), and a '0' is appended
    to the end of the sequence to maintain length. Otherwise, the sequence remains unchanged.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)

    # Find the start index, end index, and value of the last contiguous block
    block_info = find_last_contiguous_block(input_list)

    # Default output is the original list (in case no transformation occurs)
    output_list = list(input_list) # Create a copy

    # Check if a block was found
    if block_info:
        start_index, end_index, _ = block_info

        # Check the condition: block exists, starts after index 0, and is preceded by 0
        if start_index > 0 and input_list[start_index - 1] == 0:
            # Condition met: perform the shift

            # Extract elements before the preceding zero
            part1 = input_list[:start_index - 1]
            # Extract the block itself
            block = input_list[start_index : end_index + 1]
            # Extract elements after the block
            part3 = input_list[end_index + 1:]

            # Construct the new list: part1 + block + part3 + appended zero
            output_list = part1 + block + part3 + [0]

    # Format the potentially modified list back into a space-separated string
    output_str = " ".join(map(str, output_list))
    return output_str
```
