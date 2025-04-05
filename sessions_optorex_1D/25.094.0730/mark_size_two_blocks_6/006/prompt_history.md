
## train_1

**input:**
```
0 0 0 1 1 0 0 0 0 0 1 0
```


**output:**
```
0 0 3 1 1 3 0 0 0 0 1 0
```


## train_2

**input:**
```
1 1 0 0 0 0 0 0 0 1 0 0
```


**output:**
```
1 1 3 0 0 0 0 0 0 1 0 0
```


## train_3

**input:**
```
0 0 1 1 0 0 0 0 0 0 1 0
```


**output:**
```
0 3 1 1 3 0 0 0 0 0 1 0
```


## train_4

**input:**
```
1 0 0 0 0 0 0 0 0 0 1 0
```


**output:**
```
1 0 0 0 0 0 0 0 0 0 1 0
```


## train_5

**input:**
```
0 0 1 0 0 0 0 1 1 1 0 0
```


**output:**
```
0 0 1 0 0 0 0 1 1 1 0 0
```


## train_6

**input:**
```
1 0 0 0 0 0 1 0 0 0 0 0
```


**output:**
```
1 0 0 0 0 0 1 0 0 0 0 0
```


## train_7

**input:**
```
0 1 0 0 0 1 1 0 0 0 0 0
```


**output:**
```
0 1 0 0 3 1 1 3 0 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are both lists of single-digit integers.
    *   Input lists contain only 0s and 1s.
    *   Output lists can contain 0s, 1s, and 3s.
    *   The length of the input and output list is always the same for a given example.
    *   The transformation involves selectively changing some 0s in the input list to 3s in the output list.
    *   The change seems related to the presence of adjacent `1`s. Specifically, a pattern of exactly two consecutive `1`s (`1 1`) triggers the change.
    *   The 0s that change to 3s are those immediately preceding or immediately following such a `1 1` block.
    *   If a `1` is part of a longer sequence of `1`s (e.g., `1 1 1`), it does not trigger the change in adjacent 0s.
    *   If a `0` is adjacent to two separate `1 1` blocks, it doesn't seem to happen in the examples, but the rule implies it would still change to 3. (e.g., `1 1 0 1 1` -> `1 1 3 1 1`)

*   **YAML Facts:**
    
```yaml
    task_description: "Modify a sequence of 0s and 1s based on patterns of adjacent 1s."
    elements:
      - type: sequence
        name: input_list
        contains:
          - type: integer
            possible_values: [0, 1]
      - type: sequence
        name: output_list
        contains:
          - type: integer
            possible_values: [0, 1, 3]
        relationship: "Derived from input_list by conditional modification."
    objects:
      - name: digit_zero
        value: 0
        property: "Can be changed to 3 under specific conditions."
      - name: digit_one
        value: 1
        property: "Contributes to forming the trigger pattern."
      - name: digit_three
        value: 3
        property: "Result of transforming a specific digit_zero."
      - name: block_one_one
        value: "[1, 1]"
        property: "A sequence of exactly two consecutive 1s."
        relationship: "Triggers the transformation of adjacent 0s."
    actions:
      - name: identify_blocks
        input: input_list
        output: indices of all block_one_one instances
        condition: "The block must be exactly two 1s long (not preceded or followed by another 1)."
      - name: modify_neighbors
        input: input_list, indices of block_one_one
        output: modified_list (intermediate state)
        effect: "For each identified block_one_one at index i, i+1: if input_list[i-1] is 0, change it to 3 in the output; if input_list[i+2] is 0, change it to 3 in the output. Handle boundary conditions."
    relationships:
      - type: adjacency
        description: "A digit_zero is considered adjacent if it is immediately before the start or immediately after the end of a block_one_one."
      - type: transformation_trigger
        subject: block_one_one
        object: adjacent digit_zero
        action: change value to 3
    constraints:
      - "The length of the input and output sequences must be identical."
      - "Only 0s adjacent to a block of *exactly* two 1s are modified."
      - "1s and 0s not meeting the criteria remain unchanged."

    ```


*   **Natural Language Program:**
    1.  Initialize the output list as a copy of the input list.
    2.  Iterate through the input list from the first element up to the second-to-last element, examining each element and the one immediately following it. Let the current index be `i`.
    3.  Check if the element at index `i` is 1 and the element at index `i+1` is also 1.
    4.  If they are both 1, verify that this is a block of *exactly* two 1s:
        *   Check that the element *before* index `i` (if it exists, i.e., `i > 0`) is not 1.
        *   Check that the element *after* index `i+1` (if it exists, i.e., `i+1 < length - 1`) is not 1.
    5.  If both conditions in step 4 are met (it's exactly a `1 1` block):
        *   Check the element immediately *before* the block (at index `i-1`): If this element exists (`i > 0`) and its value in the *input* list is 0, change the corresponding element at index `i-1` in the *output* list to 3.
        *   Check the element immediately *after* the block (at index `i+2`): If this element exists (`i+1 < length - 1`) and its value in the *input* list is 0, change the corresponding element at index `i+2` in the *output* list to 3.
    6.  After iterating through all possible starting positions `i`, the final output list contains the transformed sequence.
```python
import copy
from typing import List

"""
Transforms a list of 0s and 1s based on the presence of isolated '1 1' blocks.
Specifically, it identifies sequences of exactly two consecutive 1s ('1 1')
that are not part of a longer sequence of 1s (i.e., not preceded or followed
by another 1). For each such identified block, it changes the 0s immediately
preceding and immediately succeeding the block to 3s in the output list.
Other elements remain unchanged.
"""

def transform(input_list: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list containing only 0s and 1s.

    Returns:
        A new list where 0s adjacent to isolated '1 1' blocks
        in the input list have been changed to 3s.
    """
    n = len(input_list)
    if n < 2:
        # Cannot have a '1 1' block if length is less than 2
        return copy.deepcopy(input_list)

    # Initialize the output list as a copy of the input list.
    # Modifications are made to this list, while checks use the original input_list.
    output_list = copy.deepcopy(input_list)

    # Iterate through the input list to find potential start positions of '1 1' blocks.
    # The loop needs to go up to index n-2 to check elements at i and i+1.
    for i in range(n - 1):
        
        # Check if the elements at index i and i+1 form a '1 1' block.
        if input_list[i] == 1 and input_list[i+1] == 1:
            
            # Verify that this is an *isolated* '1 1' block, meaning it's not part of a '1 1 1' or longer sequence.
            
            # Check the element *before* the block (at index i-1).
            # It's isolated on the left if i is 0 (start of the list) or the element at i-1 is not 1.
            is_isolated_left = (i == 0) or (input_list[i-1] != 1)
            
            # Check the element *after* the block (at index i+2).
            # It's isolated on the right if i+2 is beyond the list end or the element at i+2 is not 1.
            is_isolated_right = (i + 2 >= n) or (input_list[i+2] != 1)
            
            # If the block is isolated on both sides (exactly '1 1')
            if is_isolated_left and is_isolated_right:
                
                # Check and modify the element *before* the block (at index i-1).
                # Ensure the index i-1 is valid (i > 0) and the element *in the original input* is 0.
                if i > 0 and input_list[i-1] == 0:
                    output_list[i-1] = 3
                    
                # Check and modify the element *after* the block (at index i+2).
                # Ensure the index i+2 is valid (i + 2 < n) and the element *in the original input* is 0.
                if i + 2 < n and input_list[i+2] == 0:
                    output_list[i+2] = 3

    # Return the modified list.
    return output_list
```
```python
"""
Transforms a list of 0s and 1s by changing 0s adjacent to specific '1 1' patterns to 3s.
Specifically, it identifies sequences of exactly two consecutive 1s ('1 1')
that are not part of a longer sequence of 1s (i.e., not preceded or followed
by another 1). For each such identified isolated block, it changes the 0s
immediately preceding and immediately succeeding the block in the original
input list to 3s in the output list. Other elements remain unchanged.
"""

import copy
from typing import List

def transform(input_list: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list containing only 0s and 1s.

    Returns:
        A new list where 0s adjacent to isolated '1 1' blocks
        in the input list have been changed to 3s.
    """
    n = len(input_list)
    if n < 2:
        # Cannot have a '1 1' block if length is less than 2, return a copy.
        return copy.deepcopy(input_list)

    # Initialize the output list as a copy of the input list.
    # Modifications will be made to this list.
    # Checks for conditions (like adjacent 0s) will use the original input_list.
    output_list = copy.deepcopy(input_list)

    # Iterate through the input list to find potential start positions of '1 1' blocks.
    # The loop needs to go up to index n-2 to check elements at i and i+1.
    for i in range(n - 1):

        # Check if the elements at index i and i+1 form a '1 1' block.
        if input_list[i] == 1 and input_list[i+1] == 1:

            # Verify that this is an *isolated* '1 1' block.
            # It must not be preceded by a 1 (unless at the start)
            # and not followed by a 1 (unless at the end).

            # Check the element *before* the block (at index i-1).
            # is_isolated_left is True if we are at the beginning (i=0) OR the preceding element is not 1.
            is_isolated_left = (i == 0) or (input_list[i-1] != 1)

            # Check the element *after* the block (at index i+2).
            # is_isolated_right is True if we are at the end (i+2 >= n) OR the succeeding element is not 1.
            is_isolated_right = (i + 2 >= n) or (input_list[i+2] != 1)

            # If the block is isolated on both sides (it's exactly '1 1')
            if is_isolated_left and is_isolated_right:

                # Modify the element *before* the block if applicable.
                # Check if the index i-1 is valid (i > 0) AND
                # if the element at that position *in the original input* is 0.
                if i > 0 and input_list[i-1] == 0:
                    # Update the corresponding position in the output list.
                    output_list[i-1] = 3

                # Modify the element *after* the block if applicable.
                # Check if the index i+2 is valid (i + 2 < n) AND
                # if the element at that position *in the original input* is 0.
                if i + 2 < n and input_list[i+2] == 0:
                    # Update the corresponding position in the output list.
                    output_list[i+2] = 3

    # Return the modified list.
    return output_list
```
```python
import copy
from typing import List

"""
Transforms a list of 0s and 1s by changing 0s adjacent to specific '1 1' patterns to 3s.
Specifically, it identifies sequences of exactly two consecutive 1s ('1 1')
that are not part of a longer sequence of 1s (i.e., not preceded or followed
by another 1). For each such identified isolated block, it changes the 0s
immediately preceding and immediately succeeding the block in the original
input list to 3s in the output list. Other elements remain unchanged.
"""

def transform(input_list: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list containing only 0s and 1s.

    Returns:
        A new list where 0s adjacent to isolated '1 1' blocks
        in the input list have been changed to 3s.
    """
    n = len(input_list)
    # Handle lists too short to contain a '1 1' block
    if n < 2:
        # Return a shallow copy as no transformation is possible
        return input_list[:] 

    # Create a shallow copy of the input list to modify.
    # Using input_list[:] is sufficient as the elements (ints) are immutable.
    # Checks will be performed on the original input_list.
    output_list = input_list[:] 

    # Iterate through the input list to find potential start positions of '1 1' blocks.
    # The loop needs to go up to index n-2 to allow checking i and i+1.
    for i in range(n - 1):

        # Check if the elements at index i and i+1 form a '1 1' block.
        if input_list[i] == 1 and input_list[i+1] == 1:

            # --- Verify that this is an *isolated* '1 1' block ---
            # It must not be preceded by a 1 (unless it's at the very start)
            # and not followed by a 1 (unless it's at the very end).

            # Check the element *before* the block (at index i-1).
            # It's isolated on the left if i is 0 (start of the list) OR the element at i-1 is not 1.
            is_isolated_left = (i == 0) or (input_list[i-1] != 1)

            # Check the element *after* the block (at index i+2).
            # It's isolated on the right if i+2 is beyond the list end (i+2 >= n) OR the element at i+2 is not 1.
            is_isolated_right = (i + 2 >= n) or (input_list[i+2] != 1)

            # --- If the block is confirmed to be isolated ---
            if is_isolated_left and is_isolated_right:

                # --- Modify neighbours in the output_list if they are 0 in the input_list ---

                # Check and modify the element *before* the block (at index i-1).
                # Condition: The index i-1 must be valid (i > 0) AND the element *in the original input* must be 0.
                if i > 0 and input_list[i-1] == 0:
                    # Update the corresponding position in the output list.
                    output_list[i-1] = 3

                # Check and modify the element *after* the block (at index i+2).
                # Condition: The index i+2 must be valid (i + 2 < n) AND the element *in the original input* must be 0.
                if i + 2 < n and input_list[i+2] == 0:
                    # Update the corresponding position in the output list.
                    output_list[i+2] = 3

    # Return the modified list.
    return output_list
```
