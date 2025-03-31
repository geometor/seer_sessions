
## train_1

**input:**
```
5 5 5 5 5 7 7 7 7 7 7 9 9 9
5 5 5 5 5 7 7 7 7 7 7 9 9 9
5 5 5 5 5 7 7 7 7 7 7 9 9 9
5 5 5 5 5 7 7 7 7 7 7 9 9 9
5 5 5 5 5 7 7 7 7 7 7 9 9 9
5 5 9 5 5 7 7 9 7 7 7 9 9 9
5 5 7 5 5 7 7 7 7 7 7 9 7 9
5 5 5 5 5 7 7 7 7 5 7 9 5 9
5 5 5 5 5 7 7 7 7 7 7 9 9 9
```


**output:**
```
9 9 9 7 7 7 7 7 7 5 5 5 5 5
9 9 9 7 7 7 7 7 7 5 5 5 5 5
9 9 9 7 7 7 7 7 7 5 5 5 5 5
9 9 9 7 7 7 7 7 7 5 5 5 5 5
9 9 9 7 7 7 7 7 7 5 5 5 5 5
9 9 9 7 7 9 7 7 7 5 5 9 5 5
9 7 9 7 7 7 7 7 7 5 5 7 5 5
9 5 9 7 7 7 7 5 7 5 5 5 5 5
9 9 9 7 7 7 7 7 7 5 5 5 5 5
```


## train_2

**input:**
```
8 9 8 9 9 9 1 9 1 3 9 3
8 8 8 9 9 9 1 1 1 3 3 3
8 8 8 9 8 9 1 8 1 3 8 3
8 8 8 9 9 9 1 1 1 3 3 3
8 3 8 9 3 9 1 3 1 3 3 3
8 8 8 9 9 9 1 1 1 3 3 3
8 1 8 9 1 9 1 1 1 3 1 3
```


**output:**
```
9 9 9 1 9 1 3 9 3 8 9 8
9 9 9 1 1 1 3 3 3 8 8 8
9 8 9 1 8 1 3 8 3 8 8 8
9 9 9 1 1 1 3 3 3 8 8 8
9 3 9 1 3 1 3 3 3 8 3 8
9 9 9 1 1 1 3 3 3 8 8 8
9 1 9 1 1 1 3 1 3 8 1 8
```


## train_3

**input:**
```
8 8 8 8 8 2 2 2 2 1 1 1 1
8 8 8 1 8 2 2 2 2 1 1 1 1
8 8 8 2 8 2 2 2 2 1 1 1 1
8 8 8 8 8 2 2 2 2 1 1 1 1
8 8 8 8 8 2 2 8 2 1 8 1 1
8 8 8 8 8 2 1 2 2 1 1 2 1
8 8 8 8 8 2 2 2 2 1 1 1 1
8 8 8 8 8 2 2 2 2 1 1 1 1
```


**output:**
```
2 2 2 2 1 1 1 1 8 8 8 8 8
2 2 2 2 1 1 1 1 8 8 8 1 8
2 2 2 2 1 1 1 1 8 8 8 2 8
2 2 2 2 1 1 1 1 8 8 8 8 8
2 2 8 2 1 8 1 1 8 8 8 8 8
2 1 2 2 1 1 2 1 8 8 8 8 8
2 2 2 2 1 1 1 1 8 8 8 8 8
2 2 2 2 1 1 1 1 8 8 8 8 8
```


## train_4

**input:**
```
5 5 5 7 7 7 1 1 1 1
5 1 5 7 7 7 1 1 1 1
5 5 5 7 7 7 1 1 1 1
5 5 5 7 5 7 1 7 1 1
5 7 5 7 1 7 1 1 1 1
5 5 5 7 7 7 1 1 1 1
5 5 5 7 7 7 1 1 5 1
5 5 5 7 7 7 1 1 1 1
```


**output:**
```
7 7 7 1 1 1 1 5 5 5
7 7 7 1 1 1 1 5 1 5
7 7 7 1 1 1 1 5 5 5
7 5 7 1 7 1 1 5 5 5
7 1 7 1 1 1 1 5 7 5
7 7 7 1 1 1 1 5 5 5
7 7 7 1 1 5 1 5 5 5
7 7 7 1 1 1 1 5 5 5
```

*   **Perception**:
    *   Each input grid appears to be composed of distinct vertical stripes or blocks of columns.
    *   Within each example, the dominant color of each vertical stripe is consistent, though some individual pixels within a stripe might differ ("noise").
    *   The number of vertical stripes varies across examples (three or four).
    *   The output grid has the same dimensions as the input grid.
    *   The transformation seems to rearrange these vertical stripes.
    *   Comparing inputs and outputs, the leftmost vertical stripe and the rightmost vertical stripe appear to have swapped positions.
    *   The stripes located between the first and last ones remain in their original relative order and position between the swapped end stripes.
    *   The internal pattern of pixels within each stripe (including the "noise") is preserved during the swap.

*   **Facts**:
    
```yaml
    task_type: rearrangement
    grid_properties:
      - dimensions_preserved: True
      - content_preserved: True # Pixels are rearranged, not changed
    objects:
      - type: vertical_stripe
        definition: A block of adjacent columns characterized by a dominant color, especially in the top row.
        properties:
          - width: The number of columns in the stripe.
          - internal_pattern: The specific arrangement of pixels within the stripe's columns.
          - position: Identified as first, last, or middle.
    actions:
      - name: identify_stripes
        inputs: input_grid
        outputs: list_of_stripes_with_widths_and_column_indices
        description: Determine the vertical stripes by analyzing column blocks, likely using the top row as a guide for dominant colors and boundaries.
      - name: swap_stripes
        inputs: first_stripe_block, last_stripe_block
        outputs: rearranged_grid_sections
        description: Exchange the position of the first identified vertical stripe block with the last identified vertical stripe block.
      - name: reconstruct_grid
        inputs: last_stripe_block, middle_stripe_block(s), first_stripe_block
        outputs: output_grid
        description: Assemble the final grid by horizontally concatenating the last stripe block, followed by any middle stripe blocks in their original relative order, followed by the first stripe block.
    relationships:
      - The output grid is formed by rearranging column blocks (stripes) from the input grid.
      - The first and last vertical stripes of the input are swapped to become the last and first stripes of the output, respectively.
      - Middle stripes retain their relative order but shift position due to the end stripe swap.
    ```


*   **Natural Language Program**:
    1.  Identify the distinct vertical stripes in the input grid. Determine the columns belonging to the first stripe and the columns belonging to the last stripe. Note the columns belonging to any middle stripes.
    2.  Extract the block of columns corresponding to the first vertical stripe.
    3.  Extract the block of columns corresponding to the last vertical stripe.
    4.  Extract the block of columns corresponding to the middle stripes (if any), maintaining their internal order.
    5.  Construct the output grid by placing the extracted last stripe block first, followed by the extracted middle stripe block(s) (if any), followed by the extracted first stripe block last.
```python
import numpy as np
from typing import List, Tuple

"""
Identifies vertical stripes in the input grid based on contiguous blocks of color
in the top row. Swaps the first identified vertical stripe block with the last
identified vertical stripe block. Any stripes between the first and last retain
their relative order and are positioned between the swapped end stripes.
"""

def find_stripes_from_top_row(grid: np.ndarray) -> List[Tuple[int, int]]:
    """
    Identifies vertical stripe boundaries based on color changes in the top row.

    Args:
        grid: The input grid as a NumPy array.

    Returns:
        A list of tuples, where each tuple represents a stripe
        as (start_column_index, end_column_index).
    """
    if grid.shape[1] == 0:
        return []

    top_row = grid[0, :]
    width = len(top_row)
    stripes = []
    start_col = 0
    current_color = top_row[0]

    for col in range(1, width):
        if top_row[col] != current_color:
            # End of a stripe detected
            stripes.append((start_col, col))
            # Start of a new stripe
            start_col = col
            current_color = top_row[col]

    # Add the last stripe
    stripes.append((start_col, width))

    return stripes


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by swapping the first and last vertical stripes.

    The vertical stripes are identified based on contiguous blocks of the same
    color in the top row of the input grid. The first stripe and the last
    stripe are swapped, while any intermediate stripes maintain their relative
    order between the swapped stripes.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input to NumPy array for easier slicing
    np_grid = np.array(input_grid, dtype=int)
    height, width = np_grid.shape

    # If the grid is empty or has no width, return it as is
    if height == 0 or width == 0:
        return input_grid

    # 1. Identify the distinct vertical stripes based on the top row.
    stripes = find_stripes_from_top_row(np_grid)
    num_stripes = len(stripes)

    # If there's only one stripe or fewer (e.g., empty grid handled earlier),
    # no swap is needed.
    if num_stripes <= 1:
        return input_grid

    # 2. Extract the block of columns corresponding to the first stripe.
    first_stripe_cols = stripes[0]
    first_block = np_grid[:, first_stripe_cols[0]:first_stripe_cols[1]]

    # 3. Extract the block of columns corresponding to the last stripe.
    last_stripe_cols = stripes[-1]
    last_block = np_grid[:, last_stripe_cols[0]:last_stripe_cols[1]]

    # 4. Extract the block of columns for middle stripes (if any).
    middle_block = None
    if num_stripes > 2:
        # The middle block starts at the beginning of the second stripe
        middle_start_col = stripes[1][0]
        # and ends at the beginning of the last stripe.
        middle_end_col = stripes[-1][0]
        middle_block = np_grid[:, middle_start_col:middle_end_col]

    # 5. Construct the output grid by concatenating the blocks in the new order.
    blocks_to_concat = []
    blocks_to_concat.append(last_block) # Last block comes first
    if middle_block is not None:
        blocks_to_concat.append(middle_block) # Middle block(s) in the middle
    blocks_to_concat.append(first_block) # First block comes last

    output_np = np.concatenate(blocks_to_concat, axis=1)

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```
