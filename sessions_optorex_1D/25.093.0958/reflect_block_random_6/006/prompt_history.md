
## train_1

**input:**
```
0 0 0 0 0 0 0 4 7 9 1 0
```


**output:**
```
0 0 0 0 0 0 0 1 9 7 4 0
```


## train_2

**input:**
```
4 7 9 2 4 6 2 3 4 3 1 5
```


**output:**
```
5 1 3 4 3 2 6 4 2 9 7 4
```


## train_3

**input:**
```
0 0 0 8 6 6 6 6 1 8 1 3
```


**output:**
```
0 0 0 3 1 8 1 6 6 6 6 8
```


## train_4

**input:**
```
3 7 4 7 7 1 3 6 8 6 4 9
```


**output:**
```
9 4 6 8 6 3 1 7 7 4 7 3
```


## train_5

**input:**
```
0 9 6 7 5 8 9 2 2 3 1 0
```


**output:**
```
0 1 3 2 2 9 8 5 7 6 9 0
```


## train_6

**input:**
```
8 3 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 8 0 0 0 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 3 6 8 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 6 3 0 0 0 0 0 0 0
```

*   **Perception**: The input and output are sequences of single digits separated by spaces. The transformation appears to involve reversing a portion of the sequence. Specifically, the contiguous subsequence containing all the non-zero digits is identified and reversed in place. The surrounding zero digits, both leading and trailing, remain in their original positions.

*   **Facts**:
    
```yaml
    task_type: sequence_transformation
    input_elements: sequence of single digits (represented as strings, separated by spaces)
    output_elements: sequence of single digits (represented as strings, separated by spaces)
    objects:
      - sequence: the input list of digits
      - subsequence: the contiguous part of the sequence starting from the first non-zero digit and ending at the last non-zero digit
      - leading_zeros: the sequence of zeros before the first non-zero digit
      - trailing_zeros: the sequence of zeros after the last non-zero digit
    properties:
      - digits: can be zero or non-zero
      - position: index within the sequence
    actions:
      - identify: find the start and end indices of the non-zero subsequence
      - extract: isolate the leading zeros, the non-zero subsequence, and the trailing zeros
      - reverse: reverse the order of the elements within the non-zero subsequence
      - concatenate: combine the leading zeros, the reversed subsequence, and the trailing zeros to form the output sequence
    relationships:
      - The output sequence maintains the same leading and trailing zeros as the input sequence.
      - The core part of the output sequence is the reverse of the core non-zero part of the input sequence.
      - If the input contains no non-zero digits, the output is identical to the input (inferred, not explicitly shown in examples).
      - If the input contains only non-zero digits, the entire output sequence is the reverse of the input sequence.
    ```


*   **Natural Language Program**:
    1.  Receive the input sequence of digits.
    2.  Find the index of the first non-zero digit in the sequence. If no non-zero digit exists, return the original sequence.
    3.  Find the index of the last non-zero digit in the sequence.
    4.  Extract the subsequence starting from the first non-zero digit's index up to and including the last non-zero digit's index.
    5.  Reverse the order of the digits within this extracted subsequence.
    6.  Construct the output sequence by concatenating:
        a.  The digits from the start of the original sequence up to (but not including) the first non-zero digit's index (the leading zeros).
        b.  The reversed subsequence.
        c.  The digits from the position immediately after the last non-zero digit's index to the end of the original sequence (the trailing zeros).
    7.  Return the constructed output sequence.
```python
import math
import numpy as np
import re # Added for potential regex use, though list operations might be simpler here

"""
Reverses the contiguous subsequence containing all non-zero digits within a sequence of digits, 
leaving leading and trailing zeros in their original positions.

1.  Receive the input sequence of digits (as a string).
2.  Convert the input string into a list of digit strings.
3.  Find the index of the first non-zero digit in the sequence.
4.  Find the index of the last non-zero digit in the sequence.
5.  If no non-zero digits are found, return the original input string.
6.  Extract the leading zeros (elements before the first non-zero).
7.  Extract the subsequence containing digits from the first non-zero up to and including the last non-zero.
8.  Extract the trailing zeros (elements after the last non-zero).
9.  Reverse the extracted subsequence.
10. Concatenate the leading zeros, the reversed subsequence, and the trailing zeros.
11. Join the elements of the resulting list back into a space-separated string.
12. Return the constructed output string.
"""

def _find_first_nonzero_index(digit_list):
    """Finds the index of the first non-zero digit string."""
    for i, digit in enumerate(digit_list):
        if digit != '0':
            return i
    return -1 # Return -1 if no non-zero digit is found

def _find_last_nonzero_index(digit_list):
    """Finds the index of the last non-zero digit string."""
    for i in range(len(digit_list) - 1, -1, -1):
        if digit_list[i] != '0':
            return i
    return -1 # Return -1 if no non-zero digit is found

def transform(input_str: str) -> str:
    """
    Reverses the subsequence of non-zero digits within a space-separated string of digits.

    Args:
        input_str: A string containing space-separated single digits.

    Returns:
        A string with the non-zero subsequence reversed, preserving leading/trailing zeros.
    """
    
    # 1 & 2. Convert the input string into a list of digit strings.
    input_list = input_str.split(' ')
    
    # 3. Find the index of the first non-zero digit.
    start_index = _find_first_nonzero_index(input_list)
    
    # 5. If no non-zero digits are found, return the original input string.
    if start_index == -1:
        return input_str
        
    # 4. Find the index of the last non-zero digit.
    end_index = _find_last_nonzero_index(input_list) # We know at least one exists now
    
    # 6. Extract the leading zeros.
    leading_zeros = input_list[:start_index]
    
    # 7. Extract the subsequence.
    # Note: Python slicing is exclusive of the end index, so add 1 to end_index.
    subsequence = input_list[start_index : end_index + 1] 
    
    # 8. Extract the trailing zeros.
    trailing_zeros = input_list[end_index + 1 :]
    
    # 9. Reverse the extracted subsequence.
    reversed_subsequence = subsequence[::-1]
    
    # 10. Concatenate the parts.
    output_list = leading_zeros + reversed_subsequence + trailing_zeros
    
    # 11. Join the elements back into a space-separated string.
    output_str = ' '.join(output_list)
    
    # 12. Return the constructed output string.
    return output_str

```
```python
import numpy as np
import math

"""
Reverses the contiguous subsequence of a 1D NumPy array that starts at the first 
non-zero element and ends at the last non-zero element. Leading and trailing 
zeros outside this subsequence remain in their original positions.
"""

def _find_first_last_nonzero_indices(arr: np.ndarray):
    """
    Finds the indices of the first and last non-zero elements in a 1D array.

    Args:
        arr: The input 1D NumPy array.

    Returns:
        A tuple (start_index, end_index). Returns (None, None) if no non-zero
        elements are found.
    """
    non_zero_indices = np.nonzero(arr)[0] # Get indices of non-zero elements
    if len(non_zero_indices) == 0:
        return None, None # No non-zero elements found
    
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1]
    return start_index, end_index

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Reverses the subsequence of non-zero elements within a 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array with the non-zero subsequence reversed, 
        preserving leading/trailing zeros.
    """
    # 1. Receive the input 1D NumPy array (already done via input_grid).
    
    # 2 & 4. Find the index of the first and last non-zero elements.
    start_index, end_index = _find_first_last_nonzero_indices(input_grid)

    # 3. If there are no non-zero elements, return the original input array.
    if start_index is None:
        return input_grid.copy() # Return a copy to avoid modifying the original if passed by reference

    # 5. Extract three parts of the array:
    #    a. Leading zeros slice
    leading_zeros = input_grid[:start_index]
    
    #    b. Subsequence slice (inclusive of end_index)
    subsequence = input_grid[start_index : end_index + 1]
    
    #    c. Trailing zeros slice
    trailing_zeros = input_grid[end_index + 1 :]

    # 6. Reverse the subsequence slice.
    reversed_subsequence = subsequence[::-1]

    # 7. Construct the output array by concatenating the slices.
    # Use np.concatenate which handles empty arrays correctly.
    output_grid = np.concatenate((leading_zeros, reversed_subsequence, trailing_zeros))

    # 8. Return the constructed output array.
    return output_grid
```
```python
import numpy as np
import math

"""
Reverses the contiguous subsequence of a 1D NumPy array that starts at the first 
non-zero element and ends at the last non-zero element. Leading and trailing 
zeros outside this subsequence remain in their original positions.
"""

def _find_first_last_nonzero_indices(arr: np.ndarray):
    """
    Finds the indices of the first and last non-zero elements in a 1D array.

    Args:
        arr: The input 1D NumPy array.

    Returns:
        A tuple (start_index, end_index). Returns (None, None) if no non-zero
        elements are found.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.nonzero(arr)[0] 
    
    # Handle case where there are no non-zero elements
    if len(non_zero_indices) == 0:
        return None, None 
    
    # The first non-zero index is the minimum of the found indices
    start_index = non_zero_indices[0]
    # The last non-zero index is the maximum of the found indices
    end_index = non_zero_indices[-1]
    
    return start_index, end_index

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Reverses the subsequence of non-zero elements within a 1D NumPy array,
    preserving leading and trailing zeros.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array with the non-zero subsequence reversed.
    """

    # 1. Find the index of the first and last non-zero elements.
    start_index, end_index = _find_first_last_nonzero_indices(input_grid)

    # 2. If there are no non-zero elements, return the original input array.
    if start_index is None:
        # Return a copy to avoid modifying the original if it was passed by reference
        return input_grid.copy() 

    # 3. Extract three parts of the array:
    #    a. Leading zeros slice (elements before the first non-zero)
    leading_zeros = input_grid[:start_index]
    
    #    b. Subsequence slice (elements from first non-zero up to and including last non-zero)
    #       Note: Slicing up to end_index + 1 includes the element at end_index.
    subsequence = input_grid[start_index : end_index + 1]
    
    #    c. Trailing zeros slice (elements after the last non-zero)
    trailing_zeros = input_grid[end_index + 1 :]

    # 4. Reverse the subsequence slice.
    reversed_subsequence = subsequence[::-1] # Standard Python slicing for reversal

    # 5. Construct the output array by concatenating the slices.
    #    np.concatenate handles potentially empty leading/trailing zero arrays correctly.
    output_grid = np.concatenate((leading_zeros, reversed_subsequence, trailing_zeros))

    # 6. Return the constructed output array.
    return output_grid
```
