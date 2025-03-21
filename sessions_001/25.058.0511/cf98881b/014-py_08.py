"""
Condenses the input grid into a smaller output grid by prioritizing certain colors within vertical partitions.
The exact partitioning and color prioritization rules are still under investigation.
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

def prioritize_colors(partition):
    """
    Determines the output color for a partition based on a preliminary color priority.
    """
    unique_colors = np.unique(partition)
    if 4 in unique_colors:  # Yellow (4) has highest priority
        return 4
    elif 9 in unique_colors: # Maroon(9) has second priority
        return 9
    elif 1 in unique_colors:
        return 1
    elif 0 in unique_colors:
        return 0
    else:
        return 0
        
def transform(input_grid):
    """
    Transforms an input grid into a smaller, condensed output grid.
    The rule is still being refined, but involves partitioning and color prioritization.
    """
    input_height, input_width = input_grid.shape
    output_height = input_height  # Output height matches input height
    output_width = 4 # the example task uses an output grid with width 4
    output_grid = np.zeros((output_height, output_width), dtype=int)

    partitions = get_partitions(input_grid, output_width)

    for i, partition in enumerate(partitions):
      for row_index in range(0,output_height):
        row_partition = partition[row_index]
        output_color = prioritize_colors(row_partition)  # Determine color for the entire partition
        output_grid[row_index, i] = output_color

    return output_grid