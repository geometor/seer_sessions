
## train_1

**input:**
```
7 2 9 6 6 8 4 2 0 0 0 7
```


**output:**
```
0 0 0 7 7 2 9 6 6 8 4 2
```


## train_2

**input:**
```
2 4 8 6 2 9 3 4 0 6 7 3
```


**output:**
```
0 6 7 3 2 4 8 6 2 9 3 4
```


## train_3

**input:**
```
3 6 4 8 0 6 1 3 1 2 6 3
```


**output:**
```
1 2 6 3 3 6 4 8 0 6 1 3
```


## train_4

**input:**
```
0 0 0 0 0 0 0 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 2
```


## train_5

**input:**
```
5 0 0 0 0 0 0 0 0 0 0 9
```


**output:**
```
0 0 0 9 5 0 0 0 0 0 0 0
```


## train_6

**input:**
```
3 1 1 0 0 0 0 0 6 8 5 9
```


**output:**
```
6 8 5 9 3 1 1 0 0 0 0 0
```


## train_7

**input:**
```
0 0 6 7 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 6 7 0 0 0 0
```

*   **Perception of task elements:**
    *   The input and output are sequences of numerical digits, presented as space-separated strings.
    *   The length of the sequence is consistently 12 digits in all provided examples.
    *   The digits present in the input are the same as the digits in the output, indicating a rearrangement or permutation rather than addition, subtraction, or replacement of digits.
    *   Comparing input and output sequences, a specific pattern of rearrangement emerges: the last four digits of the input sequence are moved to the beginning of the output sequence, while the remaining preceding digits follow in their original relative order.

*   **YAML Facts:**
    
```yaml
    task_description: Rearrange a sequence of digits by moving the last segment to the front.
    input_data:
      type: string
      format: space-separated digits
      length: 12
      elements: digits (0-9)
    output_data:
      type: string
      format: space-separated digits
      length: 12
      elements: digits (0-9)
      relationship_to_input: rearrangement
    transformation:
      action: block_move
      source_block:
        location: end_of_sequence
        length: 4 elements
      destination_block_location: start_of_sequence
      preserved_properties:
        - element_identity
        - total_length
        - relative_order_within_moved_block
        - relative_order_within_remaining_block
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of 12 space-separated digits.
    2.  Split the input sequence into two parts: the first 8 digits (Part A) and the last 4 digits (Part B).
    3.  Construct the output sequence by placing Part B at the beginning, followed immediately by Part A.
    4.  Format the resulting sequence as a space-separated string.
```python
import re

"""
Rearrange a sequence of 12 space-separated digits by moving the last 4 digits to the beginning of the sequence, preserving the relative order within both the moved block and the remaining block.
"""

def parse_input(input_str: str) -> list[str]:
    """Parses the space-separated input string into a list of strings."""
    return input_str.split(' ')

def format_output(output_list: list[str]) -> str:
    """Formats a list of strings into a space-separated string."""
    return ' '.join(output_list)

def transform(input_str: str) -> str:
    """
    Transforms a space-separated string of 12 digits by moving the last 4 digits
    to the front.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string representing the transformed sequence of digits.
    """
    # 1. Receive the input sequence and parse it into elements
    elements = parse_input(input_str)
    
    # Assuming fixed length of 12 based on examples
    sequence_length = 12
    block_size_to_move = 4
    
    # Check if the input has the expected length (optional, based on problem constraints)
    # if len(elements) != sequence_length:
    #     raise ValueError(f"Input sequence must have exactly {sequence_length} elements.")

    # 2. Split the input sequence into two parts: 
    #    Part A: the first (sequence_length - block_size_to_move) digits
    #    Part B: the last block_size_to_move digits
    part_a_end_index = sequence_length - block_size_to_move
    part_a = elements[:part_a_end_index] # First 8 elements
    part_b = elements[part_a_end_index:] # Last 4 elements

    # 3. Construct the output sequence by placing Part B at the beginning, 
    #    followed immediately by Part A.
    output_elements = part_b + part_a

    # 4. Format the resulting sequence as a space-separated string.
    output_str = format_output(output_elements)

    return output_str
```
