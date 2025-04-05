
## train_1

**input:**
```
7 8 7 2 0 0 0 0 8 1 2 7
```


**output:**
```
0 0 0 0 8 1 2 7 7 8 7 2
```


## train_2

**input:**
```
0 0 0 0 0 3 8 8 1 6 0 0
```


**output:**
```
0 3 8 8 1 6 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 8 0 0 0 0 0 0
```


**output:**
```
0 8 0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
2 2 9 5 0 0 0 0 7 5 9 5
```


**output:**
```
0 0 0 0 7 5 9 5 2 2 9 5
```


## train_5

**input:**
```
3 3 1 7 1 6 5 8 5 0 0 1
```


**output:**
```
1 6 5 8 5 0 0 1 3 3 1 7
```


## train_6

**input:**
```
0 0 0 0 0 4 3 6 9 0 0 0
```


**output:**
```
0 4 3 6 9 0 0 0 0 0 0 0
```


## train_7

**input:**
```
1 0 0 0 5 1 9 3 9 3 1 1
```


**output:**
```
5 1 9 3 9 3 1 1 1 0 0 0
```

**Perception:**

The input is a sequence of 12 integers. The output is also a sequence of 12 integers, which appears to be a rearrangement of the input sequence. By comparing the input and output sequences across the examples, a consistent pattern emerges. The input sequence seems to be divided into two subsequences. The first subsequence consists of the first 4 integers, and the second subsequence consists of the remaining 8 integers. The output sequence is formed by placing the second subsequence first, followed by the first subsequence.

**Facts:**


```yaml
task_description: Rearrange a sequence of 12 integers by swapping two fixed-length blocks.
elements:
  - type: sequence
    role: input
    subtype: integer
    length: 12
    representation: space-separated string
  - type: sequence
    role: output
    subtype: integer
    length: 12
    representation: space-separated string
transformation:
  action: split
  input: input sequence
  parameters:
    split_index: 4 # Split after the 4th element (index 3)
  outputs:
    - name: part1
      elements: input[0:4]
    - name: part2
      elements: input[4:12]
  action: concatenate
  inputs:
    - part2
    - part1
  output: output sequence
relationship:
  output_sequence = concatenate(part2, part1) where part1 = input[0:4] and part2 = input[4:12]
```


**Natural Language Program:**

1.  Take the input sequence of 12 integers.
2.  Divide the input sequence into two parts:
    *   The first part consists of the first 4 integers.
    *   The second part consists of the remaining 8 integers (from the 5th to the 12th integer).
3.  Construct the output sequence by concatenating the second part followed by the first part.
```python
import re

"""
Rearrange a sequence of 12 integers by swapping two fixed-length blocks.
The input sequence is split after the 4th integer. The output sequence is
formed by concatenating the second block (integers 5 through 12) followed
by the first block (integers 1 through 4).
"""

def transform(input_str: str) -> str:
    """
    Rearranges a space-separated string of 12 integers.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the rearranged 12 space-separated integers.
    """
    # Parse the input string into a list of integers.
    # Use regular expression to find all sequences of digits, handling potential multiple spaces.
    numbers = [int(x) for x in re.findall(r'\d+', input_str)]

    # Ensure the input has exactly 12 numbers
    if len(numbers) != 12:
        raise ValueError("Input string must contain exactly 12 integers.")

    # Split the list into two parts.
    # Part 1: first 4 integers (indices 0 to 3)
    part1 = numbers[0:4]
    # Part 2: remaining 8 integers (indices 4 to 11)
    part2 = numbers[4:12]

    # Concatenate part2 followed by part1.
    output_numbers = part2 + part1

    # Convert the resulting list of integers back into a space-separated string.
    output_str = " ".join(map(str, output_numbers))

    return output_str

```
