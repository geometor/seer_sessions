# cf98881b • 018 • refine_coder

---
```python
"""
Transforms an input grid into a smaller output grid with a fixed width of 4. The
transformation involves vertically partitioning the input grid and preserving
contiguous blocks of non-black colors within each partition.
"""

import numpy as np

def get_partitions(input_grid, num_partitions):
    """
    Splits the input grid into approximately equal vertical partitions.
    """
    input_height, input_width = input_grid.shape
    partition_width = input_width // num_partitions
    partitions = []
    for i in range(num_partitions):
        start_col = i * partition_width
        # Adjust the end column for the last partition to include any remaining columns
        end_col = (i + 1) * partition_width if i < num_partitions - 1 else input_width
        partition = input_grid[:, start_col:end_col]
        partitions.append(partition)
    return partitions

def process_partition(partition):
    """
    Processes a single vertical partition to determine the output column.
    """
    input_height, _ = partition.shape
    unique_colors = np.unique(partition)

    if len(unique_colors) == 1 and unique_colors[0] == 0:
        # Entire partition is black
        return np.zeros(input_height, dtype=int)
    elif len(unique_colors) == 1 and unique_colors[0] != 0:
       # Entire partition is one solid non black color
        return np.full(input_height, unique_colors[0], dtype=int)
    else:
        # Mixed colors, or non-contiguous blocks, return all zeros for now, will need more examples
        first_non_zero = -1

        for row in range(input_height):
            if any(partition[row,:] != 0):
                first_non_zero = row
                break
        
        if first_non_zero == -1:
            # the entire partition is black
            return np.zeros(input_height, dtype=int)
        
        first_color = -1
        for col in range(partition.shape[1]):
            if partition[first_non_zero, col] != 0:
               first_color = partition[first_non_zero, col]
               break;
        
        contiguous = True
        for row in range(first_non_zero, input_height):
            for col in range(partition.shape[1]):
                if partition[row, col] != first_color and partition[row,col] != 0:
                    contiguous = False
                    break;
            if not contiguous:
                break
        
        if contiguous:

           return np.full(input_height, first_color, dtype=int)

        else:
            return np.zeros(input_height, dtype=int)


def transform(input_grid):
    """
    Transforms an input grid into a smaller, condensed output grid.
    """
    input_height, input_width = input_grid.shape
    output_height = input_height  # Output height matches input height
    output_width = 4  # Output width is fixed at 4
    output_grid = np.zeros((output_height, output_width), dtype=int)

    partitions = get_partitions(input_grid, output_width)

    for i, partition in enumerate(partitions):
        output_column = process_partition(partition)
        output_grid[:, i] = output_column

    return output_grid
```
