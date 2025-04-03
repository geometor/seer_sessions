```python
import numpy as np
from collections import Counter

"""
Identify all horizontal contiguous blocks of azure (8) pixels in the input row.
Determine the lengths of these blocks and their frequencies.
Find the shortest block length present.
Exclude the shortest length from consideration. If only one length existed, or if excluding the shortest leaves no other lengths, make no changes.
Among the remaining lengths, find the length(s) that occur most frequently.
If there's a tie in frequency, choose the largest length among the most frequent ones.
This selected length is the 'target length'.
Change all azure blocks that have the 'target length' to yellow (4).
Leave all other pixels unchanged.
"""

def find_horizontal_blocks(row, color):
    """
    Finds contiguous horizontal blocks of a specific color in a 1D array (row).

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.
        color (int): The color value to search for blocks of.

    Returns:
        list: A list of dictionaries, where each dictionary contains 
              {'start': start_index, 'end': end_index, 'length': length}
              for each block found. end_index is inclusive. Returns an empty
              list if no blocks of the specified color are found.
    """
    blocks = []
    n = len(row)
    i = 0
    while i < n:
        if row[i] == color:
            # Start of a potential block
            start_index = i
            j = i
            # Find the end of the contiguous block
            while j < n and row[j] == color:
                j += 1
            # Block ends at index j-1 (inclusive)
            end_index = j - 1
            length = j - start_index
            blocks.append({'start': start_index, 'end': end_index, 'length': length})
            # Move past the current block
            i = j
        else:
            # Not the target color, move to the next pixel
            i += 1
    return blocks

def transform(input_grid):
    """
    Applies the transformation rule based on azure block length frequencies.
    """
    # Convert input to NumPy array
    input_grid_np = np.array(input_grid)
    
    # Ensure input is 1 row as per examples
    if input_grid_np.shape[0] != 1:
        # Task logic derived from single-row examples
        # Return original if shape is different, as rule is undefined
        return input_grid 
        
    output_grid = np.copy(input_grid_np)
    row = output_grid[0] # Work with the single row
    azure_color = 8
    target_color = 4

    # 1. Find all azure blocks
    azure_blocks = find_horizontal_blocks(row, azure_color)

    # 2. If no azure blocks, return original
    if not azure_blocks:
        return output_grid.tolist()

    # 3. Get list of lengths
    lengths = [block['length'] for block in azure_blocks]
    
    # If only one block, or all blocks are same length, no change based on frequency logic
    unique_lengths = sorted(list(set(lengths)))
    if len(unique_lengths) <= 1:
        return output_grid.tolist()

    # 4. Determine frequencies
    length_counts = Counter(lengths)

    # 5. Find shortest length
    shortest_length = min(unique_lengths)

    # 6. Filter out shortest length
    candidate_lengths = [l for l in unique_lengths if l != shortest_length]

    # If filtering leaves no lengths, no change
    if not candidate_lengths:
        return output_grid.tolist()

    # 7. Find max frequency among remaining lengths
    candidate_frequencies = {l: length_counts[l] for l in candidate_lengths}
    if not candidate_frequencies: # Should not happen if candidate_lengths is not empty, but safety check
         return output_grid.tolist()
         
    max_freq = max(candidate_frequencies.values())

    # 8. Identify lengths with max frequency
    most_frequent_lengths = [l for l, freq in candidate_frequencies.items() if freq == max_freq]

    # 9 & 10. Select target length (handle ties by choosing largest)
    target_length = max(most_frequent_lengths)
    
    # 11-13. Change blocks with target length to yellow
    for block in azure_blocks:
        if block['length'] == target_length:
            start = block['start']
            end = block['end'] # inclusive index
            # Modify the row in the output grid
            row[start:end+1] = target_color

    # 15. Return the modified grid as a list of lists
    return output_grid.tolist()
```