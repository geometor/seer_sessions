
## train_1

**input:**
```
0 3 0 0 0 3 3 0 0 3 3 3 0 0 0 3 3 0 3 3 3 3 3 0
```


**output:**
```
0 3 0 0 0 3 3 0 0 3 3 3 0 0 0 3 3 0 2 2 2 2 2 0
```


## train_2

**input:**
```
0 0 3 3 0 0 0 3 3 0 0 3 3 3 0 0 3 3 3 3 0 0 3 0
```


**output:**
```
0 0 3 3 0 0 0 3 3 0 0 3 3 3 0 0 2 2 2 2 0 0 3 0
```


## train_3

**input:**
```
0 0 3 3 0 3 3 3 3 3 3 3 0 3 3 3 3 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 0 2 2 2 2 2 2 2 0 3 3 3 3 0 0 0 0 0 0 0
```

## Perception

The input and output are presented as one-dimensional arrays of integers, representing pixel colors. The primary colors involved are white (0), green (3), and red (2). The transformation appears to involve identifying specific sequences of green pixels in the input and changing their color to red in the output.

Observing the examples:
1.  **train_1:** The longest sequence of green pixels (`3 3 3 3 3`, length 5) is changed to red (`2 2 2 2 2`).
2.  **train_2:** The longest sequence of green pixels (`3 3 3 3`, length 4) is changed to red (`2 2 2 2`).
3.  **train_3:** The longest sequence of green pixels (`3 3 3 3 3 3 3`, length 7) is changed to red (`2 2 2 2 2 2 2`).

The core operation is locating the single longest contiguous block of green pixels (value 3) within the 1D input array and replacing all pixels in that block with red pixels (value 2). Other green pixels and pixels of other colors remain unchanged. If there happened to be multiple sequences of the same maximal length, the examples suggest the *first* such sequence encountered (reading left-to-right) is the one modified, though this scenario isn't explicitly demonstrated in the provided examples.

## Facts


```yaml
Task: Color replacement based on sequence length

Input:
  Type: 1D array of integers (pixels)
  Colors:
    - White (0)
    - Green (3)
    - Other colors (potentially, though not modified in examples)

Output:
  Type: 1D array of integers (pixels) - Modified version of input.

Elements:
  - Pixels: Individual cells with color values.
  - Sequences: Contiguous runs of pixels with the same color value. Specifically interested in sequences of Green (3) pixels.

Properties:
  - Sequence Length: The number of pixels in a contiguous sequence.

Actions:
  - Identify: Find all contiguous sequences of Green (3) pixels in the input array.
  - Measure: Determine the length of each Green sequence.
  - Compare: Find the maximum length among all Green sequences.
  - Select: Choose the first sequence encountered that has the maximum length.
  - Replace: Change the color value of every pixel within the selected sequence from Green (3) to Red (2).

Relationships:
  - The transformation targets the Green sequence that is longer than any other Green sequence in the input array.
  - Only the pixels within the single longest Green sequence are modified.
  - All other pixels retain their original color.
```


## Natural Language Program

1.  Receive the input as a one-dimensional array of pixel colors.
2.  Iterate through the input array to identify all contiguous sequences (runs) of green pixels (value 3). Keep track of the starting index and length of each green sequence found.
3.  Determine the maximum length found among all identified green sequences.
4.  Identify the specific green sequence that has this maximum length. If multiple sequences share the maximum length, select the one that appears earliest (smallest starting index) in the array.
5.  Create a copy of the input array to serve as the output array.
6.  Modify the output array by changing the color of all pixels within the selected longest green sequence from green (3) to red (2).
7.  Return the modified output array.
```python
import copy

"""
Identifies all contiguous sequences of green pixels (value 3) in the input 1D array. 
Determines the maximum length among these sequences. 
Selects the first sequence encountered that has this maximum length. 
Changes the color of all pixels within this selected sequence from green (3) to red (2) in the output array.
All other pixels retain their original color.
"""

def find_sequences(data, target_value):
    """
    Finds all contiguous sequences of a target value in a 1D list.

    Args:
        data (list): The input 1D list of values.
        target_value: The value to search for sequences of.

    Returns:
        list: A list of tuples, where each tuple is (start_index, length)
              representing a sequence found. Returns an empty list if no
              sequences are found.
    """
    sequences = []
    in_sequence = False
    start_index = -1
    current_length = 0

    for i, value in enumerate(data):
        if value == target_value:
            if not in_sequence:
                # Start of a new sequence
                in_sequence = True
                start_index = i
                current_length = 1
            else:
                # Continue existing sequence
                current_length += 1
        else:
            if in_sequence:
                # End of the current sequence
                sequences.append((start_index, current_length))
                in_sequence = False
                start_index = -1
                current_length = 0

    # Check if the list ends with a sequence
    if in_sequence:
        sequences.append((start_index, current_length))

    return sequences

def transform(input_grid):
    """
    Transforms the input grid by finding the longest contiguous sequence of 
    green pixels (3) and changing them to red pixels (2). If multiple 
    sequences have the same maximum length, the first one encountered is chosen.

    Args:
        input_grid (list): A 1D list representing the input grid pixels.

    Returns:
        list: A 1D list representing the transformed output grid pixels.
    """
    
    # Find all sequences of green (3) pixels
    green_sequences = find_sequences(input_grid, 3)

    # If no green sequences are found, return the input grid unchanged
    if not green_sequences:
        return copy.deepcopy(input_grid) # Return a copy to avoid modifying original

    # Find the maximum length among the found sequences
    max_length = 0
    for _, length in green_sequences:
        if length > max_length:
            max_length = length

    # Find the first sequence that has the maximum length
    longest_sequence_info = None
    for start, length in green_sequences:
        if length == max_length:
            longest_sequence_info = (start, length)
            break # Stop after finding the first one

    # Create a copy of the input grid to modify
    output_grid = copy.deepcopy(input_grid)

    # If a longest sequence was identified (should always be true if green_sequences wasn't empty)
    if longest_sequence_info:
        start_index, length = longest_sequence_info
        # Change the pixels in the identified sequence to red (2)
        for i in range(start_index, start_index + length):
            output_grid[i] = 2

    return output_grid

```
