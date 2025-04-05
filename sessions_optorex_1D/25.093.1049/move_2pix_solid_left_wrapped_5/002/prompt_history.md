
## train_1

**input:**
```
0 0 0 0 0 0 0 9 0 0 0 0
```


**output:**
```
0 0 0 0 0 9 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 5 5 0 0 0
```


**output:**
```
0 0 0 0 0 5 5 0 0 0 0 0
```


## train_3

**input:**
```
4 4 4 4 4 4 0 0 0 0 4 4
```


**output:**
```
4 4 4 4 0 0 0 0 4 4 4 4
```


## train_4

**input:**
```
0 5 5 5 5 5 5 5 5 5 5 5
```


**output:**
```
5 5 5 5 5 5 5 5 5 5 0 5
```


## train_5

**input:**
```
0 0 0 9 9 9 9 9 9 9 9 9
```


**output:**
```
0 9 9 9 9 9 9 9 9 9 0 0
```


## train_6

**input:**
```
8 8 8 8 0 0 0 0 0 0 0 8
```


**output:**
```
8 8 0 0 0 0 0 0 0 8 8 8
```


## train_7

**input:**
```
4 4 4 4 4 0 0 0 4 4 4 4
```


**output:**
```
4 4 4 0 0 0 4 4 4 4 4 4
```

Okay, let's break down the transformation logic based on the provided examples.

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are sequences (or lists) of 12 single digits.
2.  **Digits:** The digits involved are primarily 0, 4, 5, 8, 9. The digit '0' appears to play a special role, often acting as a background or placeholder.
3.  **Transformation Type:** The transformation involves rearranging the elements within the sequence. The relative order of the non-zero digits seems preserved, but their absolute positions change.
4.  **Core Mechanism:** Comparing inputs and outputs suggests a shift or rotation operation. Specifically, the non-zero elements appear to shift two positions to the left.
5.  **Boundary Handling:** The shift seems to be circular or wrap-around (modulo the sequence length). For example, an element at index 1 shifts to index 11, and an element at index 0 shifts to index 10.
6.  **Role of Zeros:** Zeros fill the positions that are not occupied by the shifted non-zero elements. They don't seem to shift themselves but rather occupy the "empty" slots created by the movement of non-zero elements.

**YAML Facts:**


```yaml
task_elements:
  - object: sequence
    properties:
      - type: list
      - content: digits (0-9)
      - length: 12
    roles:
      - input
      - output
  - object: digit
    properties:
      - value: integer (0-9)
    attributes:
      - is_zero: boolean
      - is_non_zero: boolean
  - object: position
    properties:
      - type: index
      - range: 0 to 11
action:
  - name: identify_non_zeros
    inputs: input_sequence
    outputs: list_of_non_zero_elements_with_indices
  - name: calculate_new_position
    inputs: original_index
    parameters:
      - shift_amount: -2
      - sequence_length: 12
    outputs: target_index
    logic: (original_index + shift_amount) mod sequence_length
  - name: place_elements
    inputs:
      - target_index
      - element_value
      - output_sequence (initially empty/placeholder)
    outputs: updated_output_sequence
  - name: fill_remaining
    inputs: output_sequence
    parameters:
      - fill_value: 0
    outputs: final_output_sequence
relationship:
  - type: positional_mapping
    from: input_sequence non-zero element at index `i`
    to: output_sequence element at index `(i - 2) mod 12`
  - type: default_value
    condition: position in output_sequence not filled by a mapped non-zero element
    action: set value to 0
```


**Natural Language Program:**

1.  Create a new output sequence of length 12, initially filled with a placeholder value (e.g., null or empty).
2.  Iterate through the input sequence from index 0 to 11.
3.  For each element in the input sequence:
    a.  Check if the element is non-zero.
    b.  If the element is non-zero, calculate its target index in the output sequence by subtracting 2 from its current index and taking the result modulo 12 (this handles the wrap-around).
    c.  Place the non-zero element at the calculated target index in the output sequence.
4.  After processing all elements from the input sequence, iterate through the output sequence.
5.  Replace any remaining placeholder values in the output sequence with the digit 0.
6.  The resulting sequence is the final output.
```python
import math

"""
Create a new output sequence of length 12, initially filled with zeros.
Iterate through the input sequence (represented as a list of digits).
If an element at index `i` in the input is non-zero, place that element 
at index `(i - 2) mod 12` in the output sequence.
Elements at positions in the output sequence that do not receive a non-zero
value from the input remain zero.
Return the final output sequence.
"""

def transform(input_str: str) -> str:
    """
    Shifts non-zero elements of a 12-digit sequence two positions to the left,
    wrapping around the ends, and fills remaining positions with zeros.

    Args:
        input_str: A string of 12 space-separated digits.

    Returns:
        A string of 12 space-separated digits representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_grid = [int(x) for x in input_str.split()]
    n = len(input_grid)

    # Initialize the output grid with zeros
    output_grid = [0] * n

    # Iterate through the input grid
    for i in range(n):
        # Check if the element is non-zero
        if input_grid[i] != 0:
            # Calculate the target index with wrap-around
            # (i - 2) % n handles the left shift and wrap-around correctly
            target_index = (i - 2) % n
            # Place the non-zero element in the output grid
            output_grid[target_index] = input_grid[i]

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_grid))
    return output_str

# Example usage (based on train_1)
# input_example = "0 0 0 0 0 0 0 9 0 0 0 0"
# output_example = transform(input_example)
# print(f"Input: {input_example}")
# print(f"Output: {output_example}")

# Example usage (based on train_3)
# input_example = "4 4 4 4 4 4 0 0 0 0 4 4"
# output_example = transform(input_example)
# print(f"Input: {input_example}")
# print(f"Output: {output_example}")

# Example usage (based on train_6)
# input_example = "8 8 8 8 0 0 0 0 0 0 0 8"
# output_example = transform(input_example)
# print(f"Input: {input_example}")
# print(f"Output: {output_example}")
```
