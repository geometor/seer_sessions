
## train_1

**input:**
```
0 9 9 9 7 9 8 0 0 0 0 0
```


**output:**
```
0 9 9 9 9 9 9 0 0 0 0 0
```


## train_2

**input:**
```
0 8 3 3 3 3 3 3 3 3 0 0
```


**output:**
```
0 3 3 3 3 3 3 3 3 3 0 0
```


## train_3

**input:**
```
6 3 6 6 6 6 0 0 0 0 0 0
```


**output:**
```
6 6 6 6 6 6 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 4 4 4 4 4 4 4 3 4 4
```


**output:**
```
0 0 4 4 4 4 4 4 4 4 4 4
```


## train_5

**input:**
```
0 4 4 6 9 4 4 4 4 4 4 0
```


**output:**
```
0 4 4 4 4 4 4 4 4 4 4 0
```


## train_6

**input:**
```
2 8 8 8 8 8 8 0 0 0 0 0
```


**output:**
```
8 8 8 8 8 8 8 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 2 7 7 7 1 7 7 7 0
```


**output:**
```
0 0 0 7 7 7 7 7 7 7 7 0
```

*   **Perception:**
    *   The input and output are sequences of digits, presented as space-separated strings.
    *   The transformation operates on contiguous blocks (islands) of non-zero digits.
    *   Zero digits ('0') act as separators for these islands and remain unchanged in the output.
    *   Within each island of non-zero digits, one digit appears to be "dominant".
    *   All non-zero digits within an island are replaced by the dominant digit for that island.
    *   The dominant digit within an island is the digit that occurs most frequently in that specific island in the input.

*   **Facts:**
    
```yaml
    objects:
      - sequence:
          type: list of digits
          description: Represents the input and output data.
      - digit:
          type: integer (0-9)
          properties:
            - value: the numerical value of the digit.
            - position: the index of the digit in the sequence.
            - is_zero: boolean indicating if the value is 0.
      - island:
          type: contiguous subsequence of non-zero digits
          properties:
            - digits: list of non-zero digits belonging to the island.
            - start_index: position of the first digit in the island.
            - end_index: position of the last digit in the island.
            - dominant_digit: the most frequent digit within the island.
    actions:
      - identify_islands:
          input: sequence
          output: list of islands
          description: Scan the sequence and group consecutive non-zero digits into islands, separated by zeros.
      - find_dominant_digit:
          input: island
          output: digit value
          description: Calculate the frequency of each digit within the island and return the digit with the highest frequency.
      - replace_digits:
          input: sequence, list of islands
          output: modified sequence
          description: Iterate through each island and replace all its constituent non-zero digits in the original sequence with the island's dominant digit.
    relationships:
      - contains: A sequence contains digits.
      - separates: Zero digits separate islands within the sequence.
      - belongs_to: Each non-zero digit belongs to exactly one island (or none if it's zero).
      - determines: The frequency of digits within an island determines the dominant_digit.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of digits.
    2.  Initialize an empty list for the output sequence, having the same length as the input.
    3.  Iterate through the input sequence to identify contiguous subsequences (islands) of non-zero digits. Keep track of the start and end indices and the digits within each island. Zeroes act as delimiters between islands.
    4.  For each identified island:
        a.  Count the occurrences of each distinct non-zero digit within that island.
        b.  Determine the digit that has the highest frequency (the dominant digit).
        c.  For all positions in the output sequence corresponding to the current island's indices in the input sequence, set the value to the dominant digit.
    5.  For all positions in the input sequence that contain a zero, set the corresponding position in the output sequence to zero.
    6.  Join the digits in the output sequence into a space-separated string.
```python
import collections
import math  # Available, but not used in this specific solution
import numpy as np # Available, but not used in this specific solution

"""
Transforms an input sequence of digits by identifying contiguous subsequences (islands) 
of non-zero digits. Within each island, it finds the most frequently occurring 
digit (the dominant digit). All digits within that island in the input sequence 
are then replaced by this dominant digit in the output sequence. Zero digits act 
as separators between islands and remain unchanged in the output.
"""

def find_dominant_digit(island_digits):
  """
  Finds the most frequent digit in a list of non-zero digits.
  If there's a tie, the behavior might depend on the underlying Counter implementation,
  but based on examples, a single dominant digit seems expected.
  
  Args:
    island_digits: A list of integers representing the digits in an island.

  Returns:
    The integer digit that appears most frequently in the list. Returns None if 
    the list is empty (though this shouldn't happen with valid islands).
  """
  if not island_digits:
    return None 
  # Count occurrences of each digit
  counts = collections.Counter(island_digits)
  # Find the digit with the highest count. most_common(1) returns a list like [ (digit, count) ]
  dominant_digit = counts.most_common(1)[0][0]
  return dominant_digit

def transform(input_str: str) -> str:
    """
    Applies the island dominance transformation to the input string sequence.

    Args:
      input_str: A string of space-separated digits.

    Returns:
      A string of space-separated digits representing the transformed sequence.
    """
    # 1. Parse the input string into a list of integers.
    input_digits = [int(d) for d in input_str.split()]
    n = len(input_digits)
    # Initialize the output sequence as a copy of the input. 
    # This ensures zeros are preserved unless overwritten by an island rule.
    output_digits = list(input_digits) 

    # 2. Iterate through the input sequence to identify islands.
    i = 0
    while i < n:
      # Check if the current digit is non-zero, indicating a potential start of an island.
      if input_digits[i] != 0:
        start_index = i
        current_island_digits = []
        # 3. Find the extent of the current island (all consecutive non-zero digits).
        while i < n and input_digits[i] != 0:
          current_island_digits.append(input_digits[i])
          i += 1
        # The loop exits when a zero is found or the end of the sequence is reached.
        # The last non-zero digit was at index i-1.
        end_index = i - 1 

        # 4a. Determine the dominant digit for the identified island.
        dominant_digit = find_dominant_digit(current_island_digits)

        # 4c. Update the output sequence: Replace all digits in the island's range
        #     with the dominant digit.
        for j in range(start_index, end_index + 1):
          output_digits[j] = dominant_digit
      else:
        # 5. If the current digit is zero, it's a separator. 
        #    It's already correctly placed in output_digits (initialized as a copy).
        #    Simply move to the next position.
        i += 1

    # 6. Join the digits in the output sequence back into a space-separated string.
    output_str = " ".join(map(str, output_digits))
    return output_str

```
```python
import collections
import math # Available
import numpy as np # Available

"""
Transforms an input sequence of digits (provided as a list or NumPy array) by 
identifying contiguous subsequences (islands) of non-zero digits. Within each 
island, it finds the most frequently occurring digit (the dominant digit). All 
digits within that island in the input sequence are then replaced by this 
dominant digit in the output sequence. Zero digits act as separators between 
islands and remain unchanged in the output. The function returns the transformed 
sequence as a list of integers.
"""

def find_dominant_digit(island_digits):
  """
  Finds the most frequent digit in a list of non-zero digits.
  If there's a tie, the digit appearing first in the most_common list is chosen.
  
  Args:
    island_digits: A list of integers representing the digits in an island.

  Returns:
    The integer digit that appears most frequently in the list. Returns None if 
    the list is empty.
  """
  if not island_digits:
    return None 
  # Count occurrences of each digit
  counts = collections.Counter(island_digits)
  # Find the digit with the highest count. most_common(1) returns list like [(digit, count)]
  dominant_digit = counts.most_common(1)[0][0]
  return dominant_digit

def transform(input_sequence) -> list:
    """
    Applies the island dominance transformation to the input sequence.

    Args:
      input_sequence: A list or NumPy array of integers.

    Returns:
      A list of integers representing the transformed sequence.
    """
    # Convert input to list if it's a numpy array to ensure consistent processing
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    else:
        # Assume it's already list-like (e.g., list, tuple)
        input_list = list(input_sequence) 
        
    n = len(input_list)
    
    # Initialize the output sequence as a copy of the input list.
    # This preserves zeros unless overwritten by an island rule.
    output_sequence = list(input_list) 

    # Iterate through the input sequence to identify islands.
    i = 0
    while i < n:
        # Check if the current digit is non-zero, indicating a potential start of an island.
        if input_list[i] != 0:
            start_index = i
            current_island_digits = []
            
            # Find the extent of the current island (all consecutive non-zero digits).
            # Use input_list to read original values, iterate using i.
            while i < n and input_list[i] != 0:
                current_island_digits.append(input_list[i])
                i += 1
            # The loop exits when a zero is found or the end of the sequence is reached.
            # The last non-zero digit was at index i-1.
            end_index = i - 1 # Inclusive index of the last element in the island

            # Determine the dominant digit for the identified island.
            dominant_digit = find_dominant_digit(current_island_digits)

            # Update the output sequence: Replace all digits in the island's range
            # with the dominant digit, only if a dominant digit was found (island wasn't empty).
            if dominant_digit is not None:
                for j in range(start_index, end_index + 1):
                    output_sequence[j] = dominant_digit
            # The outer loop's index 'i' is already positioned at the element *after* the island
        else:
            # If the current digit is zero, it's a separator. 
            # It's already correctly placed in output_sequence (initialized as a copy).
            # Simply move to the next position.
            i += 1

    # Return the modified sequence as a list of integers.
    return output_sequence
```
