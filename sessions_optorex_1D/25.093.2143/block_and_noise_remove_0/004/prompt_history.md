
## train_1

**input:**
```
8 0 0 8 8 8 0 0 8 0 0 8
```


**output:**
```
0 0 0 8 8 8 0 0 0 0 0 0
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 0 8 0 0
```


**output:**
```
8 8 8 8 8 8 8 8 0 0 0 0
```


## train_3

**input:**
```
0 6 6 6 0 0 6 0 0 6 0 6
```


**output:**
```
0 6 6 6 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 7 0 7 0 7 7 7 7 7 7
```


**output:**
```
0 0 0 0 0 0 7 7 7 7 7 7
```


## train_5

**input:**
```
8 0 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
0 0 8 8 8 8 8 8 8 8 8 8
```


## train_6

**input:**
```
0 0 6 6 6 6 6 0 6 0 6 0
```


**output:**
```
0 0 6 6 6 6 6 0 0 0 0 0
```


## train_7

**input:**
```
4 0 0 4 0 4 4 0 0 0 4 0
```


**output:**
```
0 0 0 0 0 4 4 0 0 0 0 0
```

**Perception of the Elements:**

The task operates on sequences of single-digit integers. Each input sequence appears to contain predominantly zeros and repetitions of a single non-zero digit (which I'll call the "dominant digit"). The transformation rule seems to filter the input sequence based on the contiguity of the dominant digit. Specifically, it retains blocks of the dominant digit that are of length two or more, while isolated instances (blocks of length one) of the dominant digit are replaced with zero. The original zero elements remain zero in the output. The length of the output sequence is identical to the length of the input sequence.

**YAML Facts:**


```yaml
objects:
  - sequence:
      description: An ordered list of single-digit integers.
      properties:
        - elements: The individual digits in the sequence.
        - length: The number of digits in the sequence.
        - dominant_digit: The single non-zero digit that appears in the input (if any).
  - digit:
      description: An integer from 0 to 9.
      properties:
        - value: The integer value (0-9).
        - position: The index of the digit within the sequence.
  - block:
      description: A contiguous subsequence of identical non-zero digits within the main sequence.
      properties:
        - digit_value: The value of the digits in the block (must be the dominant_digit).
        - start_index: The position of the first digit in the block.
        - end_index: The position of the last digit in the block.
        - length: The number of digits in the block (end_index - start_index + 1).
actions:
  - identify_dominant_digit: Find the single non-zero digit present in the input sequence.
  - identify_blocks: Scan the input sequence to find all contiguous blocks of the dominant digit.
  - filter_blocks: Select blocks based on a length criterion.
  - construct_output: Build the output sequence based on the filtered blocks and original zeros.
relationships:
  - contiguity: Digits are adjacent to each other in the sequence.
  - isolation: A dominant digit is not contiguous with another identical dominant digit (forms a block of length 1).
rules:
  - Zeros in the input remain zeros in the output.
  - Dominant digits forming a block of length >= 2 in the input are retained in the output at their original positions.
  - Dominant digits forming a block of length 1 (isolated) in the input are replaced by zero in the output.
```


**Natural Language Program:**

1.  Examine the input sequence to identify the single non-zero digit present (the "dominant digit"). If no non-zero digit exists, return the input sequence unchanged.
2.  Create a new output sequence of the same length as the input, initially filled with zeros.
3.  Iterate through the input sequence, identifying all contiguous blocks composed solely of the dominant digit. Record the start index, end index, and length of each block.
4.  For each identified block of the dominant digit:
    *   If the block's length is 2 or greater, copy the digits from this block in the input sequence to the corresponding positions in the output sequence.
5.  Return the constructed output sequence.
```python
import re
from collections import Counter

"""
Identify the single non-zero 'dominant' digit in the input sequence.
Iterate through the input sequence, identifying contiguous blocks of this dominant digit.
Create an output sequence initially filled with zeros, having the same length as the input.
For each block of the dominant digit found in the input:
  If the block's length is 2 or greater, copy the dominant digit into the corresponding positions in the output sequence.
Retain zeros from the input sequence in their original positions (this is handled by initializing the output with zeros).
Isolated dominant digits (blocks of length 1) are effectively replaced by zero in the output because they are not copied over.
Return the constructed output sequence.
"""

def find_dominant_digit(int_list):
    """
    Finds the single non-zero digit present in the list.
    Returns the dominant digit, or 0 if none exists or if only zeros are present.
    Handles the (unseen in examples) case of multiple distinct non-zero digits
    by returning the most frequent one, or the smallest if frequencies are equal.
    """
    non_zeros = [d for d in int_list if d != 0]
    if not non_zeros:
        return 0

    counts = Counter(non_zeros)
    # If only one type of non-zero digit exists
    if len(counts) == 1:
        return list(counts.keys())[0]

    # If multiple non-zero digits exist (not in examples, but robust handling)
    # Find the highest frequency
    max_freq = 0
    for digit in counts:
        if counts[digit] > max_freq:
            max_freq = counts[digit]

    # Get all digits with the highest frequency
    most_frequent_digits = [digit for digit in counts if counts[digit] == max_freq]

    # Return the smallest digit among the most frequent ones
    return min(most_frequent_digits)


def transform(input_str: str) -> str:
    """
    Transforms the input sequence string based on contiguous blocks of the dominant digit.

    Args:
        input_str: A string of space-separated single-digit integers.

    Returns:
        A string of space-separated single-digit integers representing the transformed sequence.
    """
    # Parse input string into a list of integers
    input_list = [int(d) for d in input_str.split()]
    n = len(input_list)

    # Identify the dominant digit
    # This helper function finds the single non-zero digit, or 0 if input is all zeros.
    dominant_digit = find_dominant_digit(input_list)

    # If there's no dominant digit (input is all zeros), return a string of zeros
    if dominant_digit == 0:
        return ' '.join(['0'] * n)

    # Initialize the output list with zeros, same length as input
    output_list = [0] * n

    # Iterate through the input list to find blocks of the dominant digit
    i = 0
    while i < n:
        # Check if the current element is the dominant digit
        if input_list[i] == dominant_digit:
            # Found the start of a potential block
            block_start = i
            j = i
            # Find the end of the contiguous block of the dominant digit
            while j < n and input_list[j] == dominant_digit:
                j += 1
            block_end = j - 1 # Inclusive end index of the block
            block_length = block_end - block_start + 1

            # Check if the block length meets the criterion (>= 2)
            if block_length >= 2:
                # If yes, copy the dominant digit to the corresponding positions in the output list
                for k in range(block_start, block_end + 1):
                    output_list[k] = dominant_digit

            # Move the main index 'i' past the processed block
            i = j
        else:
            # If the current element is not the dominant digit, just move to the next element
            i += 1

    # Format the output list back into a space-separated string
    output_str = ' '.join(map(str, output_list))
    return output_str

```
```python
import numpy as np
from collections import Counter

"""
Transforms an input 1D NumPy array of single-digit integers based on the 
contiguity of the dominant non-zero digit.

1. Identifies the single dominant non-zero digit in the input array. If 
   only zeros are present, returns an array of zeros.
2. Finds all contiguous blocks (runs) of this dominant digit within the input.
3. Creates an output array of the same shape as the input, initialized with zeros.
4. Copies the dominant digit into the output array only for those positions 
   that belong to an input block of length 2 or greater.
5. Isolated occurrences (blocks of length 1) of the dominant digit are 
   effectively replaced by zero in the output.
6. Zeros in the input are preserved as zeros in the output (due to 
   initialization and selective copying).
"""

def find_dominant_digit(arr):
    """
    Finds the single non-zero digit present in the array.
    Returns the dominant digit, or 0 if none exists or if only zeros are present.
    Handles the (unseen in examples) case of multiple distinct non-zero digits
    by returning the most frequent one, or the smallest if frequencies are equal.

    Args:
        arr (np.ndarray): The input 1D NumPy array of integers.

    Returns:
        int: The dominant non-zero digit, or 0.
    """
    # Filter out zeros
    non_zeros = arr[arr != 0]

    # Handle case where the array contains only zeros
    if non_zeros.size == 0:
        return 0

    # Count occurrences of each non-zero digit
    counts = Counter(non_zeros)

    # If only one type of non-zero digit exists
    if len(counts) == 1:
        return list(counts.keys())[0]

    # If multiple non-zero digits exist (handling robustness, though not seen in examples)
    # Find the highest frequency
    max_freq = 0
    for digit in counts:
        if counts[digit] > max_freq:
            max_freq = counts[digit]

    # Get all digits with the highest frequency
    most_frequent_digits = [digit for digit in counts if counts[digit] == max_freq]

    # Return the smallest digit among the most frequent ones
    return min(most_frequent_digits)


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid (np.ndarray): A 1D NumPy array of single-digit integers.

    Returns:
        np.ndarray: The transformed 1D NumPy array.
    """
    # Ensure input is a NumPy array (it should be based on the environment)
    # Handle potential non-1D arrays gracefully if necessary, though examples are 1D
    if input_grid.ndim != 1:
        # This case isn't expected based on examples, but provides robustness
        # For now, raise an error or return input, depending on desired behavior
        # Raising an error is safer if the assumption is strictly 1D input.
        raise ValueError("Input grid must be a 1D array")

    input_list = input_grid # Use the numpy array directly
    n = len(input_list)

    # Identify the dominant non-zero digit
    dominant_digit = find_dominant_digit(input_list)

    # If there's no dominant digit (input is all zeros), return an array of zeros
    if dominant_digit == 0:
        return np.zeros_like(input_list)

    # Initialize the output array with zeros, same shape as input
    output_grid = np.zeros_like(input_list)

    # Iterate through the input array to find blocks of the dominant digit
    i = 0
    while i < n:
        # Check if the current element is the dominant digit
        if input_list[i] == dominant_digit:
            # Found the start of a potential block
            block_start = i
            j = i
            # Find the end of the contiguous block of the dominant digit
            while j < n and input_list[j] == dominant_digit:
                j += 1
            block_end = j - 1 # Inclusive end index of the block
            block_length = block_end - block_start + 1

            # Check if the block length meets the criterion (>= 2)
            if block_length >= 2:
                # If yes, assign the dominant digit to the corresponding slice in the output array
                output_grid[block_start:block_end + 1] = dominant_digit

            # Move the main index 'i' past the processed block
            i = j
        else:
            # If the current element is not the dominant digit, just move to the next element
            i += 1

    return output_grid
```
