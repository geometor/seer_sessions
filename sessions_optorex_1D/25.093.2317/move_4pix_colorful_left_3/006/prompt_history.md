
## train_1

**input:**
```
0 0 0 0 9 0 0 0 0 0 0 0
```


**output:**
```
9 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 2 1 0 0 0 0
```


**output:**
```
0 0 2 1 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 7 9 1 0 0 0 0
```


**output:**
```
0 7 9 1 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 9 8 4 5 1 9
```


**output:**
```
0 0 9 8 4 5 1 9 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 5 3 7
```


**output:**
```
0 0 0 0 0 5 3 7 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 0 5 1 5 4 4
```


**output:**
```
0 0 0 5 1 5 4 4 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 4 3 2 8 1 3
```


**output:**
```
0 0 4 3 2 8 1 3 0 0 0 0
```

*   **Perception of task elements:**
    *   The input and output are sequences of single digits, always 12 digits long.
    *   The sequences contain both zero and non-zero digits.
    *   The core transformation involves relocating a segment of the input sequence.
    *   Specifically, the contiguous block of digits starting from the first non-zero digit and ending with the last non-zero digit in the input sequence is identified.
    *   This identified block is then shifted 4 positions to the left to form the output sequence.
    *   Positions in the output sequence not filled by the shifted block are occupied by zeros.
    *   The relative order of the digits within the shifted block remains unchanged.
    *   If the calculated starting position after the shift is negative (i.e., index < 0), the block starts at index 0.

*   **Facts:**
    
```yaml
    Task: Shift a segment of a digit sequence.
    Objects:
      - InputSequence:
          Type: List of integers (digits 0-9)
          Properties:
            - Length: 12
            - Contains: Zeros and non-zero digits
      - OutputSequence:
          Type: List of integers (digits 0-9)
          Properties:
            - Length: 12 (same as input)
            - DerivedFrom: InputSequence
      - NonZeroSegment:
          Type: Sub-sequence of InputSequence
          Properties:
            - Starts: At the index of the first non-zero digit in InputSequence.
            - Ends: At the index of the last non-zero digit in InputSequence.
            - Content: All digits (including any zeros) between the start and end indices.
            - RelativeOrder: Preserved from InputSequence.
    Actions:
      - Identify: Locate the first and last non-zero digits in InputSequence to define NonZeroSegment.
      - CalculateShift: Determine the target start index for NonZeroSegment in OutputSequence.
          - Formula: `max(0, StartIndex_of_NonZeroSegment - 4)`
      - Construct: Create OutputSequence.
          - Initialize: Fill OutputSequence with zeros.
          - PlaceSegment: Copy NonZeroSegment into OutputSequence starting at the calculated target index.
    Relationships:
      - OutputSequence is a transformation of InputSequence.
      - NonZeroSegment is extracted from InputSequence.
      - The position of NonZeroSegment in OutputSequence depends on its original position in InputSequence and a fixed shift value (4).
    Constants:
      - SequenceLength: 12
      - ShiftAmount: 4 (positions to the left)
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of 12 digits.
    2.  Find the index of the first non-zero digit in the input sequence. If no non-zero digits exist, the output is the same as the input (all zeros).
    3.  Find the index of the last non-zero digit in the input sequence.
    4.  Extract the sub-sequence (the "segment") from the input sequence starting at the first non-zero index and ending at the last non-zero index (inclusive).
    5.  Calculate the target starting index for this segment in the output sequence by subtracting 4 from the original starting index (the first non-zero index). Ensure the target index is not less than 0; if it is, use 0 as the target index.
    6.  Create a new output sequence of 12 zeros.
    7.  Place the extracted segment into the output sequence, starting at the calculated target starting index. The digits following the segment in the output sequence remain zeros.
    8.  Return the constructed output sequence.
```python
import re
from typing import List, Optional, Tuple

"""
Transforms a sequence of 12 digits by identifying the contiguous segment between the first and last non-zero digits, 
shifting this segment 4 positions to the left (or to the beginning if the shift results in a negative index), 
and placing it into an output sequence of 12 zeros.
"""

def _find_nonzero_indices(digits: List[int]) -> Optional[Tuple[int, int]]:
    """Finds the indices of the first and last non-zero digits."""
    first_nonzero = -1
    last_nonzero = -1
    for i, digit in enumerate(digits):
        if digit != 0:
            if first_nonzero == -1:
                first_nonzero = i
            last_nonzero = i
    
    if first_nonzero == -1: # No non-zero digits found
        return None
    else:
        return (first_nonzero, last_nonzero)

def transform(input_str: str) -> str:
    """
    Applies the segment shifting transformation to the input digit string.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing the transformed 12 space-separated digits.
    """
    # 1. Receive the input sequence and convert to list of integers.
    input_digits = [int(d) for d in input_str.split()]
    n = len(input_digits) # Should be 12 based on examples

    # 2 & 3. Find the indices of the first and last non-zero digits.
    indices = _find_nonzero_indices(input_digits)

    # Handle the case where no non-zero digits exist.
    if indices is None:
        return input_str # Output is the same as input (all zeros)

    start_index, end_index = indices

    # 4. Extract the sub-sequence (the "segment").
    segment = input_digits[start_index : end_index + 1]

    # 5. Calculate the target starting index for the segment.
    # Shift amount is 4 to the left.
    shift_amount = 4
    target_start_index = max(0, start_index - shift_amount)

    # 6. Create a new output sequence of n zeros.
    output_digits = [0] * n

    # 7. Place the extracted segment into the output sequence.
    segment_len = len(segment)
    # Ensure placement doesn't go out of bounds (although problem description implies it fits)
    end_placement_index = min(n, target_start_index + segment_len)
    
    # Adjust segment if placement exceeds bounds (slice the segment)
    segment_to_place = segment[:end_placement_index - target_start_index] 
    
    output_digits[target_start_index : end_placement_index] = segment_to_place
    
    # 8. Return the constructed output sequence as a space-separated string.
    return " ".join(map(str, output_digits))

# Example usage based on provided train cases:
# print(f"train_1: {transform('0 0 0 0 9 0 0 0 0 0 0 0')}")
# print(f"train_2: {transform('0 0 0 0 0 0 2 1 0 0 0 0')}")
# print(f"train_3: {transform('0 0 0 0 0 7 9 1 0 0 0 0')}")
# print(f"train_4: {transform('0 0 0 0 0 0 9 8 4 5 1 9')}")
# print(f"train_5: {transform('0 0 0 0 0 0 0 0 0 5 3 7')}")
# print(f"train_6: {transform('0 0 0 0 0 0 0 5 1 5 4 4')}")
# print(f"train_7: {transform('0 0 0 0 0 0 4 3 2 8 1 3')}")
```
```python
"""
Transforms a 1D NumPy array of 12 digits by identifying the contiguous segment between the first and last non-zero digits, 
shifting this segment 4 positions to the left (clamping the start index at 0), 
and placing it into an output array initialized with 12 zeros.
"""

import numpy as np
from typing import Tuple, Optional

def _find_nonzero_segment_indices(input_array: np.ndarray) -> Optional[Tuple[int, int]]:
    """
    Finds the indices of the first and last non-zero elements in a 1D array.

    Args:
        input_array: The 1D NumPy array to search within.

    Returns:
        A tuple containing the (start_index, end_index) of the non-zero segment,
        or None if no non-zero elements are found.
    """
    nonzero_indices = np.where(input_array != 0)[0]
    if len(nonzero_indices) == 0:
        return None # No non-zero elements found
    else:
        start_index = nonzero_indices[0]
        end_index = nonzero_indices[-1]
        return start_index, end_index

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Applies the segment shifting transformation to the input NumPy array.

    Args:
        input_array: A 1D NumPy array of 12 integers.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    n = len(input_array) # Get the length (should be 12)

    # 1. Find the indices of the first and last non-zero elements.
    indices = _find_nonzero_segment_indices(input_array)

    # 2. Handle the case where no non-zero digits exist (return zeros or original).
    if indices is None:
        # Returning zeros matches the apparent behavior for all-zero inputs,
        # though returning input_array would also work if it's guaranteed to be zeros.
        return np.zeros(n, dtype=input_array.dtype) 

    start_index, end_index = indices

    # 3. Extract the sub-array (the "segment").
    segment = input_array[start_index : end_index + 1]

    # 4. Calculate the target starting index for the segment in the output array.
    # Shift amount is 4 positions to the left.
    shift_amount = 4
    target_start_index = max(0, start_index - shift_amount)

    # 5. Create a new output array of n zeros with the same dtype.
    output_array = np.zeros(n, dtype=input_array.dtype)

    # 6. Calculate placement bounds and determine the segment portion to place.
    segment_len = len(segment)
    # Ensure placement doesn't go out of bounds of the output array.
    end_placement_index = min(n, target_start_index + segment_len)
    # Calculate how many elements from the segment will actually fit.
    length_to_place = end_placement_index - target_start_index
    
    # Slice the segment if its full length doesn't fit.
    segment_to_place = segment[:length_to_place] 

    # 7. Place the (potentially truncated) segment into the output array.
    # Check if there's actually anything to place (length_to_place > 0)
    if length_to_place > 0:
        output_array[target_start_index : end_placement_index] = segment_to_place
    
    # 8. Return the constructed output array.
    return output_array
```
```python
"""
Transforms a sequence of 12 digits by identifying the contiguous segment between the first and last non-zero digits, 
shifting this segment 4 positions to the left (clamping the start index at 0), 
and placing it into an output sequence initialized with 12 zeros. The input and output are space-separated strings.
"""

from typing import List, Optional, Tuple

# Helper function to parse the input string
def _parse_input(input_str: str) -> List[int]:
    """Converts a space-separated string of digits into a list of integers."""
    return [int(d) for d in input_str.split()]

# Helper function to find the indices of the non-zero segment
def _find_nonzero_segment_indices(digits: List[int]) -> Optional[Tuple[int, int]]:
    """
    Finds the indices of the first and last non-zero digits in a list.

    Returns:
        A tuple (start_index, end_index) or None if no non-zero digits are found.
    """
    first_nonzero = -1
    last_nonzero = -1
    for i, digit in enumerate(digits):
        if digit != 0:
            if first_nonzero == -1:
                first_nonzero = i
            last_nonzero = i
    
    if first_nonzero == -1: # No non-zero digits found
        return None
    else:
        return (first_nonzero, last_nonzero)

# Helper function to format the output list back to a string
def _format_output(digits: List[int]) -> str:
    """Converts a list of integers back into a space-separated string."""
    return " ".join(map(str, digits))

def transform(input_str: str) -> str:
    """
    Applies the segment shifting transformation to the input digit string.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing the transformed 12 space-separated digits.
    """
    
    # 1. & 2. Receive and parse the input string into a list of integers.
    input_digits = _parse_input(input_str)
    n = len(input_digits) # Should be 12 based on examples

    # 3. Locate the indices of the first and last non-zero digits.
    indices = _find_nonzero_segment_indices(input_digits)

    # 4. Check for Non-Zeros: If none found, create and return an all-zero string.
    if indices is None:
        output_digits = [0] * n
        return _format_output(output_digits)

    start_index, end_index = indices

    # 5. Extract the contiguous segment.
    segment = input_digits[start_index : end_index + 1]

    # 6. Calculate the target starting position for the segment in the output.
    shift_amount = 4
    target_start_index = max(0, start_index - shift_amount)

    # 7. Construct the output sequence:
    #    - Initialize a new sequence of n zeros.
    output_digits = [0] * n
    
    #    - Copy the extracted segment into the new sequence at the target position.
    segment_len = len(segment)
    #    - Determine the actual end position in the output array, preventing overflow.
    end_placement_index = min(n, target_start_index + segment_len)
    #    - Determine how much of the segment actually fits.
    length_to_place = end_placement_index - target_start_index
    
    #    - Place the segment (or the part that fits) into the output list.
    if length_to_place > 0:
         output_digits[target_start_index : end_placement_index] = segment[:length_to_place]

    # 8. Format the resulting sequence back into a space-separated string.
    output_str = _format_output(output_digits)

    # 9. Return the formatted output string.
    return output_str
```
