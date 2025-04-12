
## train_1

**input:**
```
4 4 4 4 4 7 7
4 7 7 7 4 7 5
4 7 1 7 4 7 5
4 7 7 7 4 7 7
4 4 4 4 4 7 5
7 7 7 7 7 7 5
5 5 5 5 5 7 7
```


**output:**
```
7 7 7 7 7 7 4 4 4 4
7 7 5 5 5 7 4 4 4 4
7 7 5 5 5 7 4 4 4 4
1 7 5 5 5 7 4 4 4 4
```


## train_2

**input:**
```
9 9 9 9
7 7 9 7
9 9 9 9
7 7 7 7
7 6 7 6
7 6 7 6
7 7 7 7
```


**output:**
```
7 7 7 9 9 9
6 6 7 9 9 9
6 6 7 9 9 9
```

**INSTRUCTIONS**

above is an example pair for a task

this is your opportunity to perceive the underlying logic that transforms the
input into the output

respond with the following deliverables:

- your perception of the elements of the task
- a YAML block documenting facts - Focus on identifying objects, their properties, actions performed on them, and the relationships between them
- a natural language program - Be as clear and concise as possible, providing a complete description of the transformation rule.


your responses should be considered as information in a report - not a conversation
*code_execution_result:*
outcome: OUTCOME_OK
```
most_common_element=np.int64(7)
most_common_element_2=np.int64(7)

```
**INSTRUCTIONS**

- generate a Python module to represent the natural language program 
- follow the template below
- all common math and science libraries are available
- create docstring only at top - but comment the workflow in the function
- use helper functions for common operations like finding objects, counting,
  measuring, moving, etc. 

remember - we are working iteratively - so this code will inform your future
self as we converge on the solution

*template:*

```python
"""
{{ natural language description of the transformation rule }}
"""

{{ imports }}

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # initialize output_grid

    # perform transformations

    return output_grid

```*perception:*
The input is a 2D grid of integers. The output is also a 2D grid of integers, typically smaller than the input. The transformation seems to involve identifying a specific region within the input grid, extracting it, and then rotating it. The region appears to be defined by the elements that are *not* the most frequent element in the input grid. The rotation applied is 90 degrees counter-clockwise.

*facts:*
```yaml
objects:
  - name: input_grid
    type: 2D list of integers
  - name: output_grid
    type: 2D list of integers
  - name: most_frequent_element
    type: integer
    description: The integer that appears most often in the input_grid.
  - name: target_subgrid
    type: 2D list of integers
    description: The smallest rectangular subgrid within input_grid containing all elements not equal to the most_frequent_element.

actions:
  - name: find_most_frequent_element
    input: input_grid
    output: most_frequent_element
  - name: identify_target_subgrid_bounds
    input: input_grid, most_frequent_element
    output: min_row, max_row, min_col, max_col
    description: Find the top-left and bottom-right corners of the target_subgrid.
  - name: extract_subgrid
    input: input_grid, min_row, max_row, min_col, max_col
    output: target_subgrid
  - name: rotate_subgrid
    input: target_subgrid
    output: rotated_subgrid
    description: Rotate the target_subgrid 90 degrees counter-clockwise.

relationships:
  - The output_grid is the result of rotating the target_subgrid.
  - The target_subgrid contains all elements from the input_grid that are different from the most_frequent_element.
  - The dimensions of the output_grid depend on the dimensions of the target_subgrid after rotation.
```

*natural_language_program:*
1. Determine the most frequent integer value within the input grid.
2. Identify the coordinates of all cells in the input grid that do *not* contain the most frequent integer.
3. Find the minimum bounding box (smallest rectangle) that encloses all these identified cells.
4. Extract the subgrid defined by this bounding box from the input grid.
5. Rotate the extracted subgrid 90 degrees counter-clockwise.
6. The resulting rotated subgrid is the output grid.

*python_code:*
```python
"""
Transforms the input grid by finding the most frequent element, identifying the 
bounding box of all other elements, extracting this subgrid, and rotating it 
90 degrees counter-clockwise.
"""

import numpy as np
from collections import Counter

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Finds the subgrid containing non-most-frequent elements, extracts it, 
    rotates it 90 degrees counter-clockwise, and returns the result.

    Args:
        input_grid: A list of lists representing the input 2D grid of integers.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Convert input to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)

    # Find the most frequent element
    # Flatten the grid, count element occurrences, and find the most common one
    counts = Counter(grid.flatten())
    # Handle cases where the grid might be empty or have multiple most frequent elements (takes the first one)
    if not counts:
        return [] # Return empty list for empty input
    most_frequent_element = counts.most_common(1)[0][0]

    # Find the indices of elements *not* equal to the most frequent element
    non_frequent_indices = np.argwhere(grid != most_frequent_element)

    # If all elements are the same, there's nothing to extract/rotate
    if non_frequent_indices.size == 0:
         # Determine behavior for grids with only one type of element.
         # Based on examples, seems like it should return an empty grid or handle based on specific rules not fully clear yet.
         # Let's return an empty grid for now.
         return []


    # Determine the bounding box of these elements
    min_row = np.min(non_frequent_indices[:, 0])
    max_row = np.max(non_frequent_indices[:, 0])
    min_col = np.min(non_frequent_indices[:, 1])
    max_col = np.max(non_frequent_indices[:, 1])

    # Extract the subgrid defined by the bounding box
    # Note: slicing includes the start index but excludes the end index, so add 1 to max values
    subgrid = grid[min_row : max_row + 1, min_col : max_col + 1]

    # Rotate the extracted subgrid 90 degrees counter-clockwise
    # k=1 specifies one counter-clockwise rotation
    rotated_subgrid = np.rot90(subgrid, k=1)

    # Convert the resulting numpy array back to a list of lists
    output_grid = rotated_subgrid.tolist()

    return output_grid
```
