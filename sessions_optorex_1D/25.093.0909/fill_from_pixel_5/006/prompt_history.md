
## train_1

**input:**
```
2 9 9 9 9 9 0 0 0 0 0 0
```


**output:**
```
2 9 9 9 9 9 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 4 1 1 1 1 1 1 0 0 0
```


**output:**
```
4 4 4 1 1 1 1 1 1 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 3 3 3 3 1 0
```


**output:**
```
0 0 0 0 0 0 3 3 3 3 1 1
```


## train_4

**input:**
```
0 0 0 0 0 0 0 6 6 6 3 0
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 3 3
```


## train_5

**input:**
```
0 5 5 5 2 0 0 0 0 0 0 0
```


**output:**
```
0 5 5 5 2 2 2 2 2 2 2 2
```


## train_6

**input:**
```
0 1 8 8 8 8 8 8 0 0 0 0
```


**output:**
```
1 1 8 8 8 8 8 8 0 0 0 0
```


## train_7

**input:**
```
0 0 2 8 8 8 8 0 0 0 0 0
```


**output:**
```
2 2 2 8 8 8 8 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The task operates on sequences of 12 digits.
    *   The core elements are digits, specifically distinguishing between zero (`0`) and non-zero digits (1-9).
    *   The transformation involves changing some zero digits to non-zero values based on their neighbors.
    *   Positional adjacency is crucial.
    *   Contiguous blocks of identical digits (both zeros and non-zeros) play a role. Specifically, whether a non-zero digit is part of a repeating block or stands alone seems important.

*   **YAML Facts:**
    ```
yaml
    elements:
      - type: sequence
        description: A fixed-length sequence of 12 digits (0-9).
        length: 12
      - type: digit
        value_range: 0-9
        properties:
          - is_zero: boolean (true if value is 0)
          - is_non_zero: boolean (true if value is 1-9)

    objects:
      - name: input_sequence
        type: sequence
      - name: output_sequence
        type: sequence
      - name: non_zero_digit
        type: digit
        properties:
          - is_non_zero: true
      - name: single_non_zero_digit
        type: non_zero_digit
        description: A non-zero digit whose immediate left and right neighbors (if they exist within the sequence boundaries) have different values from it.
      - name: zero_digit
        type: digit
        properties:
          - is_zero: true
      - name: contiguous_zero_block
        type: sequence
        description: A subsequence consisting only of one or more adjacent zero digits.

    relationships:
      - type: adjacency
        description: The property of digits being immediately next to each other (left or right) in the sequence.
      - type: context
        description: The value of neighboring digits determines if a non-zero digit is "single".
      - type: propagation
        description: The value of a "single" non-zero digit propagates into adjacent blocks of zeros.

    actions:
      - name: identify_singles
        description: Iterate through the input sequence to find non-zero digits that are not identical to their immediate left or right neighbors.
        input: input_sequence
        output: list of indices and values of single non-zero digits
      - name: fill_adjacent_zeros
        description: For each single non-zero digit, find contiguous blocks of zeros immediately to its left and right, and replace those zeros with the single digit's value.
        input: index and value of a single non-zero digit, sequence (initially input, progressively modified)
        output: modified sequence
    
```python
import math
import numpy as np # Although not strictly needed for list manipulation, good practice to import common libraries

"""
Identifies "single" non-zero digits in a sequence and propagates their value into adjacent blocks of zeros.
A non-zero digit is considered "single" if its immediate left and right neighbors (if they exist within the sequence bounds) have different values from it. In other words, it's a non-zero digit that is not part of a contiguous block of the same non-zero digit.
The value of each identified single digit replaces the zeros in the contiguous block(s) of zeros immediately to its left and/or right. Propagation stops when a non-zero digit or the boundary of the sequence is encountered.
"""

def is_single(input_list, index):
    """
    Checks if the digit at the given index in the input list is a 'single' non-zero digit.

    A digit is 'single' if it's non-zero and its immediate neighbors (if they exist)
    have different values.

    Args:
        input_list: The list of integers representing the sequence.
        index: The index of the digit to check.

    Returns:
        True if the digit at the index is single, False otherwise.
    """
    n = len(input_list)
    value = input_list[index]

    # Rule 1: Must be non-zero
    if value == 0:
        return False

    # Rule 2: Check left neighbor (if it exists) must be different
    left_different = (index == 0) or (input_list[index - 1] != value)

    # Rule 3: Check right neighbor (if it exists) must be different
    right_different = (index == n - 1) or (input_list[index + 1] != value)

    # Satisfies all rules if non-zero and different from existing neighbors
    return left_different and right_different

def transform(input_str: str) -> str:
    """
    Transforms an input sequence string based on the single digit propagation rule.

    It finds non-zero digits not part of a block of identical digits and propagates
    their value into adjacent zero blocks.

    Args:
        input_str: A string of space-separated digits (e.g., "0 0 4 1 1 0").

    Returns:
        A string of space-separated digits representing the transformed sequence.
    """
    # Parse input string into a list of integers
    input_list = [int(d) for d in input_str.split()]
    n = len(input_list)

    # Initialize output_list as a copy of the input list.
    # Modifications will be made to this list.
    output_list = list(input_list)

    # --- Identify single non-zero digits ---
    # Iterate through the original input list to find digits that meet the 'single' criteria.
    singles = []
    for i in range(n):
        if is_single(input_list, i):
            # Store the index and value of each single digit found.
            singles.append({"index": i, "value": input_list[i]})

    # --- Propagate values into adjacent zeros ---
    # Iterate through the identified single digits.
    for single in singles:
        idx = single["index"]
        val = single["value"]

        # Propagate to the left:
        # Start from the position immediately left of the single digit.
        j = idx - 1
        # Move leftwards as long as we are within bounds and encounter zeros in the *original* input.
        # Checking the original input prevents propagation into areas filled by other singles in this step.
        while j >= 0 and input_list[j] == 0:
            # Update the corresponding position in the output list with the single digit's value.
            output_list[j] = val
            j -= 1 # Move one step further left.

        # Propagate to the right:
        # Start from the position immediately right of the single digit.
        j = idx + 1
        # Move rightwards as long as we are within bounds and encounter zeros in the *original* input.
        while j < n and input_list[j] == 0:
            # Update the corresponding position in the output list with the single digit's value.
            output_list[j] = val
            j += 1 # Move one step further right.

    # Format the final output list back into a space-separated string.
    output_str = " ".join(map(str, output_list))
    return output_str
```
```python
import math
import numpy as np # Common library, though not strictly needed for this logic

"""
Identifies "single" non-zero digits in an input sequence (list or NumPy array of 12 integers) and propagates their value into adjacent blocks of zeros.
A non-zero digit is considered "single" if its immediate left and right neighbors (if they exist within the sequence bounds) have different values from it.
The value of each identified single digit (based on the original input) replaces the zeros in the contiguous block(s) of zeros immediately to its left and/or right in an output sequence. Propagation stops when a non-zero digit (in the original input) or the boundary of the sequence is encountered.
"""

def is_single(sequence, index):
    """
    Checks if the digit at the given index in the sequence is a 'single' non-zero digit.

    A digit is 'single' if it's non-zero and its immediate neighbors (if they exist)
    have different values.

    Args:
        sequence: The list or array of integers representing the sequence.
        index: The index of the digit to check.

    Returns:
        True if the digit at the index is single, False otherwise.
    """
    n = len(sequence)
    value = sequence[index]

    # Rule 1: Must be non-zero
    if value == 0:
        return False

    # Rule 2: Check left neighbor (if it exists) must be different
    # True if it's the first element OR the element to the left is different
    left_different = (index == 0) or (sequence[index - 1] != value)

    # Rule 3: Check right neighbor (if it exists) must be different
    # True if it's the last element OR the element to the right is different
    right_different = (index == n - 1) or (sequence[index + 1] != value)

    # Satisfies all rules if non-zero and different from existing neighbors
    return left_different and right_different

def transform(input_sequence):
    """
    Transforms an input sequence based on the single digit propagation rule.

    Args:
        input_sequence: A list or NumPy array of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    n = len(input_sequence)
    # Initialize output_sequence as a mutable copy (list) of the input sequence.
    # We will modify this copy.
    output_sequence = list(input_sequence)

    # --- Step 1: Identify all single non-zero digits in the ORIGINAL input sequence ---
    singles = []
    for i in range(n):
        # Use the helper function to check if the element at index 'i' is single
        if is_single(input_sequence, i):
            # Store the index and value of each single digit found.
            singles.append({"index": i, "value": input_sequence[i]})

    # --- Step 2: Propagate values from identified singles into adjacent zeros ---
    # Iterate through the list of single digits identified in Step 1.
    for single in singles:
        idx = single["index"] # Original index of the single digit
        val = single["value"] # Value of the single digit

        # --- Propagate to the left ---
        # Start checking from the position immediately left of the single digit.
        j = idx - 1
        # Keep moving left as long as we are within the sequence bounds (j >= 0)
        # AND the element at position 'j' in the ORIGINAL input_sequence is 0.
        while j >= 0 and input_sequence[j] == 0:
            # Update the corresponding position in the output_sequence with the single digit's value.
            output_sequence[j] = val
            j -= 1 # Move one step further left.

        # --- Propagate to the right ---
        # Start checking from the position immediately right of the single digit.
        j = idx + 1
        # Keep moving right as long as we are within the sequence bounds (j < n)
        # AND the element at position 'j' in the ORIGINAL input_sequence is 0.
        while j < n and input_sequence[j] == 0:
            # Update the corresponding position in the output_sequence with the single digit's value.
            output_sequence[j] = val
            j += 1 # Move one step further right.

    # Return the modified output sequence.
    return output_sequence
```
```python
import math
# It's good practice to import numpy if dealing with array-like structures, 
# even if the core logic uses lists, as the testing harness might use numpy.
import numpy as np 

"""
Identifies "single" non-zero digits in an input sequence (list or array of 12 integers) 
and propagates their value into adjacent blocks of zeros based on the original input state.

A non-zero digit is considered "single" if its immediate left and right neighbors 
(if they exist within the sequence bounds) have different values from it in the 
original input sequence. It's essentially a non-zero digit not part of a 
contiguous block of the same non-zero digit.

The value of each identified single digit (based on the original input) replaces 
the zeros in the contiguous block(s) of zeros immediately to its left and/or 
right in an output sequence. Propagation stops when a non-zero digit (in the 
original input) or the boundary of the sequence is encountered.
"""

def is_single(sequence, index):
    """
    Checks if the digit at the given index in the sequence is a 'single' non-zero digit.

    A digit is 'single' if it's non-zero and its immediate neighbors (if they exist)
    have different values.

    Args:
        sequence: The list of integers representing the sequence.
        index: The index of the digit to check.

    Returns:
        True if the digit at the index is single, False otherwise.
    """
    n = len(sequence)
    value = sequence[index]

    # Rule 1: Must be non-zero
    if value == 0:
        return False

    # Rule 2: Check left neighbor (if it exists) must be different
    # True if it's the first element OR the element to the left is different
    left_different = (index == 0) or (sequence[index - 1] != value)

    # Rule 3: Check right neighbor (if it exists) must be different
    # True if it's the last element OR the element to the right is different
    right_different = (index == n - 1) or (sequence[index + 1] != value)

    # Satisfies all rules if non-zero and different from existing neighbors
    return left_different and right_different

def transform(input_sequence):
    """
    Applies the single digit propagation rule to the input sequence.

    Args:
        input_sequence: A list, NumPy array, or similar iterable of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    
    # --- Input Handling & Initialization ---
    # Ensure input is a standard Python list of integers for consistent processing
    # This handles potential variations like NumPy arrays from the test harness.
    if isinstance(input_sequence, str): # Handle potential string input if needed based on earlier examples
         input_list = [int(d) for d in input_sequence.split()]
    elif isinstance(input_sequence, np.ndarray):
         input_list = input_sequence.astype(int).tolist() # Convert numpy array to list
    else:
         input_list = list(map(int, input_sequence)) # Assume iterable, convert elements to int

    n = len(input_list)
    if n != 12:
        # Optional: Add error handling or logging if length is not 12
        print(f"Warning: Input sequence length is {n}, expected 12.")

    # Initialize output_sequence as a mutable copy of the processed input list.
    # Modifications will be made to this list.
    output_sequence = list(input_list)

    # --- Step 1: Identify all single non-zero digits in the ORIGINAL input list ---
    singles = []
    for i in range(n):
        # Use the helper function to check if the element at index 'i' is single
        if is_single(input_list, i):
            # Store the index and value of each single digit found.
            singles.append({"index": i, "value": input_list[i]})

    # --- Step 2: Propagate values from identified singles into adjacent zeros ---
    # Iterate through the list of single digits identified in Step 1.
    for single in singles:
        idx = single["index"] # Original index of the single digit
        val = single["value"] # Value of the single digit

        # --- Propagate to the left ---
        # Start checking from the position immediately left of the single digit.
        j = idx - 1
        # Keep moving left as long as we are within the sequence bounds (j >= 0)
        # AND the element at position 'j' in the ORIGINAL input_list is 0.
        # This prevents propagation over non-zeros or into areas filled by other singles.
        while j >= 0 and input_list[j] == 0:
            # Update the corresponding position in the output_sequence with the single digit's value.
            output_sequence[j] = val
            j -= 1 # Move one step further left.

        # --- Propagate to the right ---
        # Start checking from the position immediately right of the single digit.
        j = idx + 1
        # Keep moving right as long as we are within the sequence bounds (j < n)
        # AND the element at position 'j' in the ORIGINAL input_list is 0.
        while j < n and input_list[j] == 0:
            # Update the corresponding position in the output_sequence with the single digit's value.
            output_sequence[j] = val
            j += 1 # Move one step further right.

    # Return the modified output sequence as a list.
    return output_sequence
```
