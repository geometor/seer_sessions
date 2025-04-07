```python
"""
The transformation rule involves identifying horizontal bands of 7 rows within the input grid. 
Within each band, the grid is composed of repeating 7x7 blocks (including boundary lines). 
The goal is to select one representative 7x7 block pattern for each band and stack these 
selected blocks vertically to form the output grid.

The selection rule for the representative block within a band is as follows:
1. Identify all unique 7x7 block patterns within the band.
2. Count the frequency of occurrence for each unique pattern.
3. Find the minimum frequency among all patterns in the band.
4. Identify all patterns that occur with this minimum frequency (the "least frequent" patterns).
5. Select the pattern corresponding to the *first* (leftmost) block in the band that matches one of these least frequent patterns.
6. Construct the output grid by vertically stacking the selected 7x7 blocks from each band. 
The output will have the same number of rows as the input but only 7 columns.
"""

import numpy as np
from collections import Counter

def get_block(grid_np, r_start, c_start, height=7, width=7):
    """Extracts a block of specified size from a NumPy grid."""
    return grid_np[r_start:r_start + height, c_start:c_start + width]

def block_to_tuple(block_np):
    """Converts a NumPy block to a hashable tuple of tuples."""
    return tuple(map(tuple, block_np.tolist()))

def transform(input_grid):
    """
    Transforms the input grid by selecting the least frequent 7x7 block pattern 
    from each 7-row band and stacking them vertically.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # We expect rows and columns to be divisible by 7 or handle edge cases appropriately.
    # Based on examples, the structure involves blocks of 7x7 including boundaries.
    block_size = 7 
    
    selected_blocks = []

    # Iterate through the grid in horizontal bands of 7 rows
    for r_start in range(0, rows, block_size):
        band_patterns = {} # Store {pattern_tuple: [list_of_col_starts]}
        block_list_ordered = [] # Store (col_start, pattern_tuple) pairs in order

        # Iterate through the band to find all 7x7 blocks
        for c_start in range(0, cols, block_size):
            # Ensure we don't go out of bounds
            if r_start + block_size <= rows and c_start + block_size <= cols:
                block = get_block(input_np, r_start, c_start, block_size, block_size)
                pattern_tuple = block_to_tuple(block)
                
                # Store pattern and its column start index
                if pattern_tuple not in band_patterns:
                    band_patterns[pattern_tuple] = []
                band_patterns[pattern_tuple].append(c_start)
                
                # Keep track of blocks in order for tie-breaking
                block_list_ordered.append((c_start, pattern_tuple, block)) # Store the actual block array too

        # If no blocks were found in the band (e.g., band too narrow), skip
        if not block_list_ordered:
            continue 
            
        # Count frequencies
        pattern_counts = Counter({pattern: len(cols_list) for pattern, cols_list in band_patterns.items()})
        
        # Find the minimum frequency
        if not pattern_counts: # Handle empty bands if necessary
             continue
        min_freq = min(pattern_counts.values())
        
        # Identify least frequent patterns
        least_frequent_patterns = {pattern for pattern, count in pattern_counts.items() if count == min_freq}
        
        # Select the first block (leftmost) matching a least frequent pattern
        selected_block_for_band = None
        for c_start, pattern_tuple, block_array in block_list_ordered:
            if pattern_tuple in least_frequent_patterns:
                selected_block_for_band = block_array
                break # Found the leftmost least frequent block

        # Add the selected block to our list for final stacking
        if selected_block_for_band is not None:
            selected_blocks.append(selected_block_for_band)
        # else: handle cases where no block was selected, though this shouldn't happen with valid inputs

    # Stack the selected blocks vertically to form the output grid
    if not selected_blocks:
        # Handle cases where no blocks were selected at all (e.g., input smaller than 7x7)
        # Returning an empty grid or a specific error might be options.
        # Based on ARC constraints, inputs are >= 1x1. 
        # If input < 7x7, the loops wouldn't run. Let's return first 7 cols if available, else the whole grid.
        # This edge case needs clarification, but sticking to the main logic:
        if rows > 0 and cols > 0:
             # Fallback: return the first block if input is smaller than 7x7
             return input_np[:, :min(cols, block_size)].tolist() 
        else:
             return [] # Empty input -> empty output

    output_np = np.vstack(selected_blocks)
    
    # Convert the final NumPy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```