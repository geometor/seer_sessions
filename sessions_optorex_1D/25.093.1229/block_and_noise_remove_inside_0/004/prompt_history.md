
## train_1

**input:**
```
0 0 0 0 7 9 9 8 9 9 0 0
```


**output:**
```
0 0 0 0 9 9 9 9 9 9 0 0
```


## train_2

**input:**
```
6 8 8 8 8 8 5 0 0 0 0 0
```


**output:**
```
8 8 8 8 8 8 8 0 0 0 0 0
```


## train_3

**input:**
```
0 9 9 9 9 9 4 9 6 9 6 9
```


**output:**
```
0 9 9 9 9 9 9 9 9 9 9 9
```


## train_4

**input:**
```
0 0 0 0 4 2 2 4 4 4 4 0
```


**output:**
```
0 0 0 0 4 4 4 4 4 4 4 0
```


## train_5

**input:**
```
0 8 8 8 8 8 5 8 8 8 8 0
```


**output:**
```
0 8 8 8 8 8 8 8 8 8 8 0
```


## train_6

**input:**
```
0 0 6 6 2 6 6 6 6 6 0 0
```


**output:**
```
0 0 6 6 6 6 6 6 6 6 0 0
```


## train_7

**input:**
```
0 9 8 1 1 1 1 1 1 1 1 0
```


**output:**
```
0 1 1 1 1 1 1 1 1 1 1 0
```

**Perception:**

The task involves transforming a sequence of single digits. The transformation specifically targets a contiguous subsequence of non-zero digits within the input sequence. The leading and trailing zero digits act as delimiters for this subsequence and remain unchanged in the output. Within the identified non-zero subsequence, the core operation is to find the digit that appears most frequently (the mode). Subsequently, every digit within this non-zero subsequence is replaced by this most frequent digit. The length of the sequence remains the same.

**Facts:**


```yaml
objects:
  - name: input_sequence
    type: list of digits
    description: The initial sequence of numbers provided.
  - name: output_sequence
    type: list of digits
    description: The transformed sequence of numbers.
  - name: non_zero_subsequence
    type: list of digits
    description: A contiguous part of the input_sequence containing only non-zero digits, bounded by zeros or the sequence ends.
  - name: boundary_zeros
    type: list of digits
    description: The zero digits at the beginning and end of the input_sequence that delimit the non_zero_subsequence.
  - name: most_frequent_digit
    type: digit
    description: The non-zero digit that occurs most often within the non_zero_subsequence.

properties:
  - object: digit
    name: value
    description: The numerical value of the digit (0-9).
  - object: digit
    name: frequency
    description: The count of occurrences of a digit within a sequence or subsequence.
  - object: non_zero_subsequence
    name: length
    description: The number of digits in the subsequence.

actions:
  - name: identify_boundaries
    description: Find the start and end indices of the contiguous non_zero_subsequence within the input_sequence. Preserve the leading and trailing zeros.
  - name: extract_subsequence
    description: Isolate the non_zero_subsequence based on the identified boundaries.
  - name: calculate_mode
    description: Determine the most_frequent_digit within the extracted non_zero_subsequence.
  - name: replace_subsequence
    description: Create a new subsequence of the same length as the original non_zero_subsequence, filled entirely with the most_frequent_digit.
  - name: reconstruct_sequence
    description: Combine the leading boundary_zeros, the replaced subsequence, and the trailing boundary_zeros to form the output_sequence.

relationships:
  - type: containment
    subject: non_zero_subsequence
    object: input_sequence
    description: The non_zero_subsequence is a part of the input_sequence.
  - type: transformation
    subject: input_sequence
    object: output_sequence
    description: The output_sequence is derived from the input_sequence by modifying the non_zero_subsequence.
  - type: determination
    subject: most_frequent_digit
    object: non_zero_subsequence
    description: The most_frequent_digit is determined by analyzing the frequencies of digits within the non_zero_subsequence.
```


**Natural Language Program:**

1.  Identify the start index of the first non-zero digit and the end index of the last non-zero digit in the input sequence.
2.  Extract the subsequence of digits between these start and end indices (inclusive). This is the `non_zero_subsequence`.
3.  Keep track of the leading zeros (before the start index) and trailing zeros (after the end index).
4.  Count the frequency of each unique non-zero digit within the `non_zero_subsequence`.
5.  Determine the digit with the highest frequency (the mode). This is the `most_frequent_digit`.
6.  Create a new subsequence of the same length as the original `non_zero_subsequence`, where every element is the `most_frequent_digit`.
7.  Construct the final output sequence by concatenating the leading zeros, the newly created subsequence, and the trailing zeros.
```python
import collections
import re

"""
Transforms a sequence of digits by identifying the contiguous subsequence of non-zero digits, 
finding the most frequent digit (mode) within that subsequence, and replacing all digits 
in that subsequence with the mode. Leading and trailing zeros are preserved.
"""

def find_non_zero_boundaries(sequence):
    """
    Finds the start and end indices of the first contiguous non-zero block.
    
    Args:
        sequence: A list of integers.
        
    Returns:
        A tuple (start_index, end_index) or (None, None) if no non-zeros found.
        Indices are inclusive.
    """
    start_index = -1
    end_index = -1
    for i, digit in enumerate(sequence):
        if digit != 0:
            if start_index == -1:
                start_index = i
            end_index = i # Keep updating end_index to the last non-zero found
            
    if start_index == -1: # No non-zero digits found
        return None, None
        
    return start_index, end_index

def calculate_mode(sequence):
    """
    Calculates the mode (most frequent element) of a sequence.
    If there are ties, it returns the element that appears first among the modes.
    If the sequence is empty, returns None.
    
    Args:
        sequence: A list of items.
        
    Returns:
        The most frequent item or None.
    """
    if not sequence:
        return None
    counts = collections.Counter(sequence)
    # most_common(1) returns a list of tuples [(element, count)]
    mode, _ = counts.most_common(1)[0] 
    # Handle potential ties: Check if other elements have the same max count.
    # The prompt examples don't seem to have ties requiring a specific tie-breaking rule beyond what Counter provides. 
    # Counter's behavior in ties isn't strictly defined but often relates to insertion order or value.
    # For this task, the examples suggest simple mode finding is sufficient.
    return mode

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to an input string of space-separated digits.
    
    1. Parses the input string into a list of integers.
    2. Finds the start and end indices of the contiguous non-zero subsequence.
    3. Extracts the leading zeros, the non-zero subsequence, and the trailing zeros.
    4. Calculates the most frequent digit (mode) in the non-zero subsequence.
    5. Creates a new subsequence of the same length, filled with the mode.
    6. Reconstructs the sequence by combining the leading zeros, the new subsequence, and the trailing zeros.
    7. Formats the result back into a space-separated string.
    """
    
    # 1. Parse the input string into a list of integers.
    input_list = [int(d) for d in input_str.split()]
    
    # 2. Find boundaries of the non-zero subsequence
    start_index, end_index = find_non_zero_boundaries(input_list)
    
    # Handle case where the input is all zeros or empty
    if start_index is None:
        return input_str # No transformation needed
        
    # 3. Extract subsequences
    leading_zeros = input_list[:start_index]
    non_zero_subsequence = input_list[start_index : end_index + 1]
    trailing_zeros = input_list[end_index + 1 :]
    
    # 4. Calculate the mode of the non-zero subsequence
    if not non_zero_subsequence: # Should not happen if start_index is not None, but good practice
         mode = 0 # Or handle as error, though logically this means only zeros were present.
    else:
        mode = calculate_mode(non_zero_subsequence)
        # If mode calculation somehow fails (e.g., empty list passed incorrectly), handle it.
        if mode is None: 
             # This case implies non_zero_subsequence was empty, contradictory to finding boundaries.
             # Revert to original if something went wrong. Consider error logging.
             return input_str 


    # 5. Create the new subsequence filled with the mode
    replaced_subsequence = [mode] * len(non_zero_subsequence)
    
    # 6. Reconstruct the full sequence
    output_list = leading_zeros + replaced_subsequence + trailing_zeros
    
    # 7. Format the output list back into a space-separated string
    output_str = " ".join(map(str, output_list))
    
    return output_str

```
```python
import numpy as np
import collections

"""
Transforms a 1D NumPy array of integers by identifying the contiguous subsequence 
of non-zero integers, finding the most frequent integer (mode) within that 
subsequence, and replacing all integers in that subsequence with the mode. 
Leading and trailing zeros are preserved.
"""

def _find_non_zero_boundaries(arr: np.ndarray) -> tuple[int | None, int | None]:
    """
    Finds the start and end indices of the contiguous non-zero block.

    Args:
        arr: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index) inclusive, or (None, None) if 
        no non-zero elements are found.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(arr != 0)[0]
    
    # Handle case where there are no non-zero elements
    if non_zero_indices.size == 0:
        return None, None
        
    # The start index is the minimum non-zero index
    start_index = np.min(non_zero_indices)
    # The end index is the maximum non-zero index
    end_index = np.max(non_zero_indices)
    
    return start_index, end_index

def _calculate_mode(arr_slice: np.ndarray) -> int | None:
    """
    Calculates the mode (most frequent element) of a NumPy array slice.
    If there are ties, returns the element that appears first among the modes 
    as per collections.Counter behavior.
    If the slice is empty, returns None.

    Args:
        arr_slice: A 1D NumPy array slice.

    Returns:
        The most frequent integer or None if the slice is empty.
    """
    # Handle empty slice case
    if arr_slice.size == 0:
        return None
        
    # Count occurrences of each element
    counts = collections.Counter(arr_slice)
    
    # Find the element with the highest count
    # most_common(1) returns a list like [(element, count)]
    mode, _ = counts.most_common(1)[0] 
    
    return mode

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with the transformation applied.
    """
    
    # Find the boundaries of the contiguous non-zero subsequence
    start_index, end_index = _find_non_zero_boundaries(input_grid)
    
    # If no non-zero elements exist, return a copy of the original grid
    if start_index is None:
        return input_grid.copy()
        
    # Extract the non-zero subsequence (inclusive slicing)
    non_zero_subsequence = input_grid[start_index : end_index + 1]
    
    # Calculate the mode of the non-zero subsequence
    # Note: _find_non_zero_boundaries ensures the subsequence is not empty if start_index is not None
    mode = _calculate_mode(non_zero_subsequence)
    
    # Create a copy of the input grid to modify
    output_grid = input_grid.copy()
    
    # Replace the elements within the non-zero subsequence boundaries with the mode
    output_grid[start_index : end_index + 1] = mode
    
    return output_grid
```
