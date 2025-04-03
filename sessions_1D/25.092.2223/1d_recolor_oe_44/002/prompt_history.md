
## train_1

**input:**
```
0 0 0 7 7 7 7 7 7 0 7 7 7 7 7 0
```


**output:**
```
0 0 0 9 9 9 9 9 9 0 6 6 6 6 6 0
```


## train_2

**input:**
```
0 7 7 7 7 0 0 7 7 7 0 7 7 7 0 0
```


**output:**
```
0 9 9 9 9 0 0 6 6 6 0 6 6 6 0 0
```


## train_3

**input:**
```
0 7 7 7 0 7 7 0 0 7 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 0 9 9 0 0 6 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Task Elements:**

1.  **Input/Output Format:** The examples use 1-dimensional arrays (or single rows) of integers representing pixel colors.
2.  **Key Colors:** The primary colors involved are white (0), orange (7), maroon (9), and magenta (6).
3.  **Structure:** The white pixels (0) appear to act as a background or separator, remaining unchanged in the output. The transformation focuses on contiguous blocks of orange pixels (7).
4.  **Transformation:** Contiguous blocks of orange pixels in the input are replaced by blocks of either maroon (9) or magenta (6) pixels in the output. The length of each block is preserved.
5.  **Rule Dependency:** The choice between maroon (9) and magenta (6) for a given block doesn't seem based *solely* on its position (e.g., "first block always becomes X") or *solely* on its length in isolation. It appears to depend on the *distribution* of lengths across *all* orange blocks within the input array. Specifically, properties like length uniqueness and median length seem crucial.

**YAML Facts:**


```yaml
Grid_Type: 1D array (row)
Input_Colors: [white(0), orange(7)]
Output_Colors: [white(0), maroon(9), magenta(6)]
Background_Color: white(0)
Objects:
  - type: contiguous_block
    input_color: orange(7)
    output_colors: [maroon(9), magenta(6)]
    properties:
      - length: integer
      - position: index range
      - order: integer (1st, 2nd, ...)
      - length_uniqueness: boolean (is this length unique among all orange blocks?)
      - is_median_length: boolean (does this block have the median length?)
Relationships:
  - white(0) pixels separate orange(7) blocks.
  - The output color of an orange(7) block depends on the statistical properties (uniqueness, median) of its length relative to all other orange(7) block lengths in the input.
Transformation:
  - type: color_replacement
    target: orange(7) blocks
    conditions:
      - rule_based_on_length_distribution:
          - if length is uniquely occurring: output is maroon(9)
          - if length is not uniquely occurring: output is magenta(6)
          - exception: if multiple lengths are unique (or none are unique), use median length rule
      - median_length_rule:
          - find median length M (use larger of middle two for even number of blocks)
          - if block length equals M: output is maroon(9)
          - otherwise: output is magenta(6)
    preserve_property: length
  - type: identity
    target: white(0) pixels
```


**Natural Language Program:**

1.  Scan the input array to identify all contiguous blocks of orange (7) pixels. Keep track of the start index, end index, and length of each block found, maintaining their original order.
2.  If no orange blocks are found, the output is identical to the input.
3.  If orange blocks are found, create a list of their lengths.
4.  Calculate the frequency of each length in the list.
5.  Identify the lengths that appear exactly once (unique lengths).
6.  Count how many distinct lengths are unique.
7.  **Determine the Target Length for Maroon Color:**

```python
import math
from collections import Counter

"""
Identify contiguous blocks of orange (7) pixels in the input 1D array.
Determine a 'target length' based on the distribution of the lengths of these blocks.
If exactly one block length occurs uniquely (only once), that length is the target length.
Otherwise (if zero or multiple lengths are unique), the target length is the median length of all blocks. When calculating the median for an even number of blocks, use the larger of the two middle lengths after sorting.
Replace orange blocks:
- If a block's length equals the target length, replace its pixels with maroon (9).
- Otherwise, replace its pixels with magenta (6).
White (0) pixels remain unchanged.
"""

def find_blocks_by_color(grid, color):
    """
    Finds contiguous blocks of a specific color in a 1D grid.

    Args:
        grid (list): The input 1D array.
        color (int): The color value to search for.

    Returns:
        list: A list of tuples, where each tuple represents a block
              and contains (start_index, end_index, length).
              Returns an empty list if no blocks are found.
    """
    blocks = []
    in_block = False
    start_index = -1
    for i, pixel in enumerate(grid):
        if pixel == color and not in_block:
            # Start of a new block
            in_block = True
            start_index = i
        elif pixel != color and in_block:
            # End of the current block
            in_block = False
            end_index = i - 1
            length = end_index - start_index + 1
            blocks.append((start_index, end_index, length))
            start_index = -1 # Reset start_index
        # Handle block ending at the very end of the grid
        if in_block and i == len(grid) - 1:
             end_index = i
             length = end_index - start_index + 1
             blocks.append((start_index, end_index, length))
    return blocks

def calculate_target_length(lengths):
    """
    Calculates the target length based on uniqueness or median.

    Args:
        lengths (list): A list of block lengths.

    Returns:
        int: The target length.
    """
    if not lengths:
        return None # Should not happen if called after finding blocks

    # Calculate frequency of each length
    length_counts = Counter(lengths)

    # Find lengths that appear exactly once (unique lengths)
    unique_lengths = [length for length, count in length_counts.items() if count == 1]

    # Determine target length based on uniqueness
    if len(unique_lengths) == 1:
        target_length = unique_lengths[0]
    else:
        # Calculate median length (custom rule for even count)
        sorted_lengths = sorted(lengths)
        n = len(sorted_lengths)
        mid_index = n // 2
        if n % 2 == 1:
            # Odd number of blocks, median is the middle element
            target_length = sorted_lengths[mid_index]
        else:
            # Even number of blocks, median is the larger of the two middle elements
            # Note: Python uses 0-based indexing, so middle elements are at mid_index-1 and mid_index
            target_length = sorted_lengths[mid_index] # The larger one due to 0-indexing

    return target_length


def transform(input_grid):
    """
    Transforms the input grid based on the rules derived from examples.
    Identifies orange (7) blocks, determines a target length based on
    length uniqueness or median, and replaces blocks with maroon (9) if
    their length matches the target, or magenta (6) otherwise.

    Args:
        input_grid (list): A 1D list of integers representing pixel colors.

    Returns:
        list: The transformed 1D list of integers.
    """
    # Initialize output_grid as a copy of the input
    output_grid = list(input_grid)

    # Find all contiguous blocks of orange (7) pixels
    orange_blocks = find_blocks_by_color(input_grid, 7)

    # If no orange blocks are found, return the original grid
    if not orange_blocks:
        return output_grid

    # Extract the lengths of the found blocks
    block_lengths = [block[2] for block in orange_blocks]

    # Calculate the target length based on the rules
    target_length = calculate_target_length(block_lengths)

    # Iterate through the identified orange blocks and modify the output grid
    for start, end, length in orange_blocks:
        # Determine the replacement color
        replacement_color = 9 if length == target_length else 6

        # Apply the color change to the output grid slice
        for i in range(start, end + 1):
            output_grid[i] = replacement_color

    return output_grid
```
