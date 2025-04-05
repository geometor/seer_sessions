
## train_1

**input:**
```
1 1 0 0 0 0 0 8 2 8 3 7
```


**output:**
```
2 8 3 7 1 1 0 0 0 0 0 8
```


## train_2

**input:**
```
0 0 0 9 8 2 7 1 3 0 0 0
```


**output:**
```
3 0 0 0 0 0 0 9 8 2 7 1
```


## train_3

**input:**
```
0 0 0 0 0 2 3 8 5 2 9 0
```


**output:**
```
5 2 9 0 0 0 0 0 0 2 3 8
```


## train_4

**input:**
```
0 0 0 9 4 7 7 6 1 0 0 0
```


**output:**
```
1 0 0 0 0 0 0 9 4 7 7 6
```


## train_5

**input:**
```
0 0 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 4 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 4 1 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 4 1 0 0
```


## train_7

**input:**
```
5 6 0 0 0 0 2 1 2 7 9 4
```


**output:**
```
2 7 9 4 5 6 0 0 0 0 2 1
```

*   **Perception:**
    *   The input and output are both sequences of 12 space-separated single digits.
    *   The transformation rearranges the elements of the input sequence to produce the output sequence.
    *   Observing the examples, it appears the sequence is split into two parts. The split occurs after the 8th element.
    *   The first part consists of the first 8 elements, and the second part consists of the last 4 elements.
    *   In the output, the order of these two parts is reversed: the last 4 elements from the input appear first, followed by the first 8 elements from the input.
    *   The internal order of elements within each part remains unchanged.

*   **Facts:**
    
```yaml
    task_type: sequence_manipulation
    input:
        type: list
        element_type: integer
        length: 12
    output:
        type: list
        element_type: integer
        length: 12
        relationship: rearrangement_of_input
    transformation:
        actions:
            - split:
                description: Divide the input list into two sub-lists.
                parameters:
                    - split_point: index 8 (after the 8th element)
                results:
                    - part_1: elements from index 0 to 7
                    - part_2: elements from index 8 to 11
            - concatenate:
                description: Combine the two sub-lists in a specific order.
                parameters:
                    - order: [part_2, part_1]
                result: output_list
    ```


*   **Natural Language Program:**
    1.  Take the input sequence of 12 numbers.
    2.  Divide the sequence into two parts: the first 8 numbers (Part 1) and the last 4 numbers (Part 2).
    3.  Construct the output sequence by placing Part 2 first, followed by Part 1.
    4.  Format the resulting sequence as space-separated digits.
```python
import math # not strictly needed for this task, but included as per template example

# Helper functions

def parse_input_string(input_str: str) -> list[int]:
    """Parses a space-separated string of digits into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output_list(output_list: list[int]) -> str:
    """Formats a list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

# Main transformation function

def transform(input_str: str) -> str:
    """
    Takes a sequence of 12 space-separated digits, splits it into two parts
    (the first 8 digits and the last 4 digits), and returns a new sequence
    formed by concatenating the last 4 digits followed by the first 8 digits.
    """

    # Parse the input string into a list of numbers
    numbers = parse_input_string(input_str)

    # Define the split point
    split_index = 8

    # Check if the input list has the expected length (optional, for robustness)
    if len(numbers) != 12:
        # Handle error or unexpected input length if necessary
        # For this task, we assume valid input based on examples
        pass 

    # Split the list into two parts based on the split index
    part1 = numbers[:split_index] # First 8 elements
    part2 = numbers[split_index:] # Last 4 elements

    # Concatenate the parts in the reverse order: part2 then part1
    rearranged_list = part2 + part1

    # Format the rearranged list back into a space-separated string
    output_str = format_output_list(rearranged_list)

    return output_str

```
