
## train_1

**input:**
```
0 0 0 1 1 0 0 0 1 1 1 0
```


**output:**
```
0 0 3 1 1 3 0 0 1 1 1 0
```


## train_2

**input:**
```
0 1 1 1 0 0 0 0 1 0 0 0
```


**output:**
```
0 1 1 1 0 0 0 0 1 0 0 0
```


## train_3

**input:**
```
1 0 0 0 0 1 1 1 0 0 0 0
```


**output:**
```
1 0 0 0 0 1 1 1 0 0 0 0
```


## train_4

**input:**
```
0 0 1 0 0 0 1 0 0 0 0 0
```


**output:**
```
0 0 1 0 0 0 1 0 0 0 0 0
```


## train_5

**input:**
```
0 1 1 0 0 0 1 1 0 0 0 0
```


**output:**
```
3 1 1 3 0 3 1 1 3 0 0 0
```


## train_6

**input:**
```
0 1 0 0 0 0 1 1 1 0 0 0
```


**output:**
```
0 1 0 0 0 0 1 1 1 0 0 0
```


## train_7

**input:**
```
0 1 0 0 0 1 1 1 0 0 0 0
```


**output:**
```
0 1 0 0 0 1 1 1 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are sequences (lists or arrays) of single-digit integers.
    *   Input sequences contain only 0s and 1s.
    *   Output sequences contain 0s, 1s, and 3s.
    *   The transformation modifies some of the 0s in the input sequence to 3s in the output sequence based on their proximity to specific patterns of 1s.
    *   The lengths of the input and output sequences are always identical.
    *   The positions of the 1s remain unchanged from input to output.
    *   The change from 0 to 3 seems conditional on the 0 being adjacent to a block of exactly two consecutive 1s.

*   **Facts:**
    
```yaml
    objects:
      - sequence:
          description: A list of integers.
          properties:
            - elements: Integers (0, 1 for input; 0, 1, 3 for output).
            - length: The number of elements in the sequence.
      - number:
          description: An integer element within the sequence.
          properties:
            - value: The integer itself (0, 1, or 3).
            - position: The index of the number within the sequence.
      - block:
          description: A contiguous sub-sequence of identical numbers.
          properties:
            - type: Consists of the number 1.
            - length: The count of consecutive 1s.
            - location: Starting and ending indices within the sequence.
    relationships:
      - adjacency:
          description: A number is directly next to a block (either immediately preceding its start index or immediately following its end index).
          applies_to: [number, block]
    actions:
      - identify_blocks:
          description: Find all contiguous blocks of the number 1 within the input sequence.
          constraints: The block must have a specific length (exactly 2).
      - check_adjacency:
          description: For each identified block of two 1s, check if the numbers at adjacent positions are 0.
      - modify_number:
          description: Change the value of an adjacent 0 to 3.
          condition: The 0 must be adjacent to a block of exactly two 1s.
          target: The output sequence at the corresponding position.
      - copy_number:
          description: If a number is not modified, copy its value from the input to the output at the same position.
          condition: Applies to all 1s and any 0s not meeting the modification condition.
          target: The output sequence.
    ```


*   **Natural Language Program:**
    1.  Iterate through the input sequence to identify all contiguous blocks consisting of exactly two 1s (i.e., sub-sequences `1 1`). Record the starting and ending indices of each such block.
    2.  Create a copy of the input sequence to serve as the initial output sequence.
    3.  For each identified block of two 1s found in step 1:
        a.  Check the element immediately *before* the block's starting index (if it exists within the sequence bounds). If this element is a 0, change its value to 3 in the output sequence.
        b.  Check the element immediately *after* the block's ending index (if it exists within the sequence bounds). If this element is a 0, change its value to 3 in the output sequence.
    4.  Return the modified sequence as the final output.
```python
import re

def parse_input(input_str):
  """Parses the space-separated string into a list of integers."""
  return [int(x) for x in input_str.strip().split()]

def format_output(output_list):
  """Formats the list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

def transform(input_str):
  """
  Transforms the input sequence by changing 0s adjacent to blocks of exactly two 1s to 3s.
  1. Iterate through the input sequence to find blocks of exactly two 1s ('1 1').
  2. For each '1 1' block found:
     a. Check the element immediately before the block. If it's a 0, change it to 3 in the output.
     b. Check the element immediately after the block. If it's a 0, change it to 3 in the output.
  3. Keep all other elements (1s and 0s not adjacent to '1 1' blocks) the same.
  """
  # Parse the input string into a list of integers
  input_list = parse_input(input_str)
  n = len(input_list)
  
  # Initialize output_list as a copy of input_list
  output_list = list(input_list)

  # Iterate through the list to find blocks of '1 1'
  # We only need to check up to n-2 because we need pairs input_list[i] and input_list[i+1]
  for i in range(n - 1):
      # Check if the current element and the next element form a '1 1' block
      if input_list[i] == 1 and input_list[i+1] == 1:
          # Ensure it's *exactly* two 1s. 
          # Check before the block
          is_start_of_block = (i == 0 or input_list[i-1] != 1)
          # Check after the block
          is_end_of_block = (i + 2 >= n or input_list[i+2] != 1)

          if is_start_of_block and is_end_of_block:
              # Modify the element *before* the block if it's a 0 and within bounds
              if i > 0 and input_list[i-1] == 0:
                  output_list[i-1] = 3
              
              # Modify the element *after* the block if it's a 0 and within bounds
              if i + 2 < n and input_list[i+2] == 0:
                  output_list[i+2] = 3

  # Format the output list back into a string
  return format_output(output_list)

```
