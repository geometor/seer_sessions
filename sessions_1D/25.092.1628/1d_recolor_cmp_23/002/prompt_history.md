
## train_1

**input:**
```
0 0 8 0 0 8 8 8 8 0 8 8 8 8 8 8 8 0 8 8 8 8 8 8 8 0 0 0
```


**output:**
```
0 0 8 0 0 8 8 8 8 0 7 7 7 7 7 7 7 0 7 7 7 7 7 7 7 0 0 0
```


## train_2

**input:**
```
0 8 8 8 0 0 0 8 8 0 0 8 0 0 8 8 8 8 0 8 0 0 0 8 0 8 8 0
```


**output:**
```
0 8 8 8 0 0 0 8 8 0 0 8 0 0 7 7 7 7 0 8 0 0 0 8 0 8 8 0
```


## train_3

**input:**
```
0 0 0 8 0 0 8 8 0 0 0 8 8 8 8 8 0 8 8 0 0 8 8 0 0 0 0 0
```


**output:**
```
0 0 0 8 0 0 8 8 0 0 0 7 7 7 7 7 0 8 8 0 0 8 8 0 0 0 0 0
```

*   **Perception:** The task operates on 1D sequences (or single rows) of pixels. The input sequences contain white (0) and azure (8) pixels. The output sequences contain white (0), azure (8), and orange (7) pixels. The transformation involves changing the color of certain azure blocks to orange based on their properties and context. Specifically, the length of the azure block and its immediate neighbors (being white pixels) determine if a color change occurs.

*   **Facts:**
    
```yaml
    task_type: color_transformation
    grid_dimensionality: 1D # or single row within 2D
    colors_involved:
      - white (0)
      - azure (8)
      - orange (7)
    objects:
      - pixel: Basic unit with a color value.
      - block: A contiguous horizontal sequence of pixels of the same color.
        properties:
          - color: The color of the pixels in the block (azure in this focus).
          - length: The number of pixels in the block.
          - position: Start and end indices within the sequence.
          - context: Pixels immediately preceding and succeeding the block.
    actions:
      - identify_azure_blocks: Find all contiguous blocks of azure (8) pixels.
      - check_surroundings: For each azure block, determine if it is immediately preceded by white (0) and immediately followed by white (0). Handle boundary conditions as if they are not white (0).
      - find_max_length: Among the azure blocks surrounded by white (0), find the maximum length.
      - change_color: Change the color of all azure blocks that are surrounded by white (0) AND have the maximum length found in the previous step to orange (7).
    relationships:
      - adjacency: Pixels are adjacent horizontally.
      - grouping: Pixels of the same color form blocks.
      - conditionality: Color change depends on block length and adjacency to white pixels.
    invariants:
      - White (0) pixels always remain white (0).
      - Azure (8) pixels that are part of blocks not meeting the criteria (not surrounded by white OR not of maximum length among surrounded blocks) remain azure (8).
      - The length of the sequence remains unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize the output sequence as a copy of the input sequence.
    2.  Scan the input sequence to identify all contiguous horizontal blocks composed solely of azure (8) pixels. Record their start index, end index, and length.
    3.  Create a list of "candidate" blocks: Filter the identified azure blocks, keeping only those that are immediately preceded by a white (0) pixel AND immediately followed by a white (0) pixel. (A block at the very beginning or end of the sequence cannot be surrounded by white pixels).
    4.  If the list of candidate blocks is empty, the transformation is complete, and the initial copy of the input is the final output.
    5.  If there are candidate blocks, determine the maximum length among them.
    6.  Iterate through the list of candidate blocks again. For each candidate block whose length equals the determined maximum length, change the color of all pixels within that block's range (from its start index to its end index) in the output sequence to orange (7).
    7.  Return the modified output sequence.
```python
import numpy as np
from typing import List, Tuple, Dict

"""
Transforms a 1D sequence of pixels by identifying contiguous blocks of azure (8) pixels.
Among those blocks that are immediately surrounded by white (0) pixels on both sides,
it finds the block(s) with the maximum length. 
The color of the pixels within these maximum-length, surrounded azure blocks is changed to orange (7).
All other pixels retain their original color.
"""

def find_azure_blocks(grid: List[int]) -> List[Dict[str, int]]:
    """
    Identifies contiguous blocks of azure (8) pixels in a 1D grid.

    Args:
        grid: A list of integers representing the 1D grid.

    Returns:
        A list of dictionaries, where each dictionary represents an azure block
        and contains 'start', 'end', and 'length' keys.
    """
    blocks = []
    n = len(grid)
    i = 0
    while i < n:
        if grid[i] == 8:
            start = i
            while i < n and grid[i] == 8:
                i += 1
            end = i - 1
            length = end - start + 1
            blocks.append({'start': start, 'end': end, 'length': length})
        else:
            i += 1
    return blocks

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = list(input_grid)
    n = len(input_grid)

    # 1. Scan the input sequence to identify all contiguous horizontal blocks of azure (8)
    azure_blocks = find_azure_blocks(input_grid)

    # 2. Create a list of "candidate" blocks: Filter azure blocks surrounded by white (0)
    candidate_blocks = []
    for block in azure_blocks:
        start = block['start']
        end = block['end']
        
        # Check left boundary (must be white 0)
        is_left_surrounded = (start > 0 and input_grid[start - 1] == 0)
        
        # Check right boundary (must be white 0)
        is_right_surrounded = (end < n - 1 and input_grid[end + 1] == 0)

        if is_left_surrounded and is_right_surrounded:
            candidate_blocks.append(block)

    # 3. If the list of candidate blocks is empty, return the initial copy
    if not candidate_blocks:
        return output_grid

    # 4. Determine the maximum length among the candidate blocks
    max_length = 0
    for block in candidate_blocks:
        if block['length'] > max_length:
            max_length = block['length']

    # 5. Iterate through candidate blocks and change color for those with max length
    for block in candidate_blocks:
        if block['length'] == max_length:
            start = block['start']
            end = block['end']
            # Change the color of pixels within this block's range to orange (7)
            for i in range(start, end + 1):
                output_grid[i] = 7

    # 6. Return the modified output sequence
    return output_grid

```
