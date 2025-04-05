
## train_1

**input:**
```
2 0 4 4 4 4 4 4 4 4 0 0
```


**output:**
```
2 4 4 4 4 4 4 4 4 0 0 0
```


## train_2

**input:**
```
3 3 3 3 3 3 3 2 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 2 0 0 0 0
```


## train_3

**input:**
```
0 0 0 2 3 3 3 3 3 0 0 0
```


**output:**
```
0 0 0 2 3 3 3 3 3 0 0 0
```


## train_4

**input:**
```
7 7 7 7 7 7 7 0 2 0 0 0
```


**output:**
```
0 7 7 7 7 7 7 7 2 0 0 0
```


## train_5

**input:**
```
0 0 0 2 3 3 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 3 3 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 9 9 9 9 9 2 0 0 0 0
```


**output:**
```
0 0 9 9 9 9 9 2 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 2 0 0 3 3 3 3 3
```


**output:**
```
0 0 0 0 2 3 3 3 3 3 0 0
```

Okay, let's analyze the transformation.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are strings representing sequences of single-digit integers separated by spaces.
2.  **Key Element:** The digit '0' plays a crucial role in the transformation. Non-zero digits seem to maintain their relative order but might shift position due to the movement of zeros.
3.  **Transformation Trigger:** The transformation appears to be triggered when one or more '0's are located *between* two non-zero digits.
4.  **Transformation Action:** The '0's identified in the trigger condition are removed from their original position.
5.  **Destination Logic:** The destination of the removed '0's depends on the values of the non-zero digits that surrounded them.
    *   If the left non-zero neighbor is *less than* the right non-zero neighbor, the '0'(s) move to the *end* of the sequence.
    *   If the left non-zero neighbor is *greater than* the right non-zero neighbor, the '0'(s) move to the *beginning* of the sequence.
6.  **Inaction Cases:** If '0's are not strictly between two non-zero digits (e.g., at the ends, adjacent to another '0', or adjacent to only one non-zero digit), they remain in place relative to the non-zero elements.
7.  **Multiple Occurrences:** The process seems applicable to all instances where the trigger condition (non-zero / zero(s) / non-zero) is met within the sequence. Zeros identified for moving to the start are prepended, and those for moving to the end are appended.

**YAML Facts:**


```yaml
task_elements:
  - type: sequence
    format: space-separated single digits
    role: input & output
objects:
  - name: digit_sequence
    properties:
      - elements: single digits (0-9)
      - order: significant
  - name: zero_digit
    properties:
      - value: 0
      - role: potentially mobile element
  - name: non_zero_digit
    properties:
      - value: 1-9
      - role: triggers movement, anchors relative position
relationships:
  - type: adjacency
    between: digits in the sequence
  - type: comparison
    between: adjacent non-zero digits surrounding zero(s) (less than / greater than)
actions:
  - name: identify_mobile_zeros
    criteria: zero(s) located immediately between two non_zero_digits (L, R)
  - name: remove_zeros
    target: mobile_zeros identified
  - name: relocate_zeros
    condition: comparison of L and R
    outcomes:
      - if L < R: move removed zeros to the end of the sequence
      - if L > R: move removed zeros to the beginning of the sequence
  - name: maintain_relative_order
    target: non_zero_digits and non-mobile zeros
```


**Natural Language Program:**

1.  Parse the input string into a list of integers.
2.  Initialize two empty lists: `zeros_to_prepend` and `zeros_to_append`.
3.  Initialize an empty list `indices_to_remove`.
4.  Iterate through the list from the second element (index 1) to the second-to-last element (index length - 2).
5.  If the current element at index `i` is 0 and the elements at `i-1` (Left) and `i+1` (Right) are both non-zero:
    a.  Identify the contiguous block of zeros starting at index `i`. Let this block be `current_zeros`.
    b.  Add the indices of `current_zeros` to `indices_to_remove`.
    c.  Compare the Left and Right non-zero neighbors.
    d.  If Left < Right, add `current_zeros` to the `zeros_to_append` list.
    e.  If Left > Right, add `current_zeros` to the `zeros_to_prepend` list.
    f.  Advance the iteration index `i` past the identified block of zeros to avoid reprocessing.
6.  Create a new list `result_core` containing only the elements from the original list whose indices are *not* in `indices_to_remove`.
7.  Construct the final list by concatenating `zeros_to_prepend`, `result_core`, and `zeros_to_append`.
8.  Convert the final list back into a space-separated string.
```python
import math
import collections

"""
Transformation Rule:
Identify blocks of one or more zeros that are directly situated between two non-zero digits (Left and Right neighbors). 
Based on the comparison of the Left and Right non-zero neighbors, relocate these identified zeros.
If the Left neighbor is less than the Right neighbor, move the block of zeros to the end of the sequence.
If the Left neighbor is greater than the Right neighbor, move the block of zeros to the beginning of the sequence.
All other digits (non-zeros and zeros not meeting the criteria) maintain their relative order in the sequence after the mobile zeros are extracted.
The final sequence is constructed by prepending the 'start' zeros, followed by the remaining sequence elements, and finally appending the 'end' zeros.
"""

def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    return [int(x) for x in input_str.split()]

def format_output(output_list: list[int]) -> str:
    """Formats the list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.
    """
    nums = parse_input(input_str)
    n = len(nums)

    if n < 3:
        # Cannot have a L-0-R pattern with less than 3 elements
        return input_str

    zeros_to_prepend = []
    zeros_to_append = []
    indices_to_remove = set() # Use a set for efficient checking and removal

    # Iterate through the list to find L-0...0-R patterns
    i = 1
    while i < n - 1:
        # Check if the current element is a potential start of a mobile zero block
        if nums[i] == 0 and nums[i-1] != 0 and nums[i+1] != 0:
            left_neighbor = nums[i-1]
            
            # Find the extent of the contiguous block of zeros
            j = i
            # We need to ensure j+1 is a valid index and nums[j+1] is non-zero
            # The initial check already confirmed nums[i+1] != 0, so we need to find 
            # where the non-zero element *after* the zero block is.
            
            # Find the end of the zero block
            k = i
            while k + 1 < n and nums[k+1] == 0:
                k += 1
            
            # Now k is the index of the last zero in the block.
            # We need to check if the element *after* this block exists and is non-zero.
            if k + 1 < n and nums[k+1] != 0:
                 right_neighbor = nums[k+1]
                 num_zeros = k - i + 1 # Count of zeros in the block

                 # Add indices of this zero block to the removal set
                 for idx in range(i, k + 1):
                     indices_to_remove.add(idx)

                 # Decide where to move the zeros
                 if left_neighbor < right_neighbor:
                     zeros_to_append.extend([0] * num_zeros)
                 elif left_neighbor > right_neighbor:
                     zeros_to_prepend.extend([0] * num_zeros)
                 # If left_neighbor == right_neighbor, zeros are just removed, not relocated (implicitly handled)

                 # Advance the main loop index past this processed block
                 i = k + 1
            else:
                 # The zeros run to the end or are not followed by a non-zero, so they are not mobile
                 i += 1 
        else:
            # Current element is not the start of a mobile zero block, move to the next
            i += 1

    # Build the core result by filtering out the removed zeros
    result_core = [nums[idx] for idx in range(n) if idx not in indices_to_remove]

    # Construct the final list
    final_list = zeros_to_prepend + result_core + zeros_to_append

    # Format the output string
    return format_output(final_list)

```
