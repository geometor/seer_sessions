import numpy as np
from collections import Counter

def find_patterns_and_separator(grid, block_size=4, pattern_size=3):
    """
    Identifies the separator color and the two main patterns (target and trigger)
    by analyzing the grid structure.

    Args:
        grid (np.array): The input grid.
        block_size (int): The size of the repeating blocks including separators.
        pattern_size (int): The size of the pattern within each block.

    Returns:
        tuple: (separator_color, target_pattern, trigger_pattern)
               Returns None for patterns if only one type is found.
    """
    height, width = grid.shape
    patterns = []
    
    # Assuming separator is consistent on the block boundaries
    # Check a few potential separator locations
    sep_candidates = []
    if height > block_size -1:
        sep_candidates.extend(grid[block_size - 1, ::block_size - 1])
    if width > block_size - 1:
         sep_candidates.extend(grid[::block_size - 1, block_size - 1])
    if not sep_candidates: # Grid too small for standard block size logic
        # Fallback: maybe the whole grid is one block or less
        if height >= 1 and width >=1:
             sep_candidates.append(grid[0,0]) # Guess based on corner? Risky.
        else:
            return None, None, None # Cannot determine separator

    separator_color = Counter(sep_candidates).most_common(1)[0][0]

    pattern_offset = (block_size - pattern_size) // 2 # Assumes centered pattern

    # Collect all unique patterns
    unique_patterns = {}
    pattern_coords = []

    for r in range(0, height - block_size + 1, block_size):
        for c in range(0, width - block_size + 1, block_size):
            pattern_r_start = r + pattern_offset
            pattern_c_start = c + pattern_offset
            pattern_r_end = pattern_r_start + pattern_size
            pattern_c_end = pattern_c_start + pattern_size
            
            if pattern_r_end <= height and pattern_c_end <= width:
                pattern = grid[pattern_r_start:pattern_r_end, pattern_c_start:pattern_c_end]
                pattern_tuple = tuple(map(tuple, pattern)) # Make hashable
                if pattern_tuple not in unique_patterns:
                    unique_patterns[pattern_tuple] = pattern
                pattern_coords.append(((r, c), pattern_tuple)) # Store block corner and pattern

    if not unique_patterns:
        return separator_color, None, None

    # Count occurrences using the collected list
    pattern_counts = Counter(p_tuple for _, p_tuple in pattern_coords)
    
    sorted_patterns = sorted(pattern_counts.items(), key=lambda item: item[1], reverse=True)

    if len(sorted_patterns) == 0:
         return separator_color, None, None
    elif len(sorted_patterns) == 1:
        target_pattern_tuple = sorted_patterns[0][0]
        target_pattern = unique_patterns[target_pattern_tuple]
        return separator_color, target_pattern, None # Only one pattern type found
    else:
        target_pattern_tuple = sorted_patterns[0][0]
        trigger_pattern_tuple = sorted_patterns[1][0]
        target_pattern = unique_patterns[target_pattern_tuple]
        trigger_pattern = unique_patterns[trigger_pattern_tuple]
        return separator_color, target_pattern, trigger_pattern


def transform(input_grid):
    """
    Transforms the input grid based on a pattern propagation rule.
    Identifies a repeating grid structure defined by a separator color.
    Finds a common 'target' pattern and a less common 'trigger' pattern within the grid blocks.
    If a block contains the 'target' pattern and is orthogonally adjacent (sharing a separator line)
    to a block containing the 'trigger' pattern in the *input* grid, the 'target' pattern block
    is changed to the 'trigger' pattern in the output grid. Separator lines remain unchanged.
    """
    
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid_np = np.copy(input_grid_np)
    height, width = input_grid_np.shape
    
    # --- Parameters ---
    block_size = 4 # Size of the cell including borders
    pattern_size = 3 # Size of the pattern within the cell
    pattern_offset = (block_size - pattern_size) // 2 # Assumes centered
    
    # --- Identify patterns and separator ---
    separator_color, target_pattern, trigger_pattern = find_patterns_and_separator(
        input_grid_np, block_size, pattern_size
    )

    # If no trigger pattern exists, no transformation occurs
    if trigger_pattern is None or target_pattern is None:
        return output_grid_np.tolist()

    # --- Iterate through blocks and apply transformation ---
    for r in range(0, height - block_size + 1, block_size):
        for c in range(0, width - block_size + 1, block_size):
            
            # Define the current pattern's location
            pattern_r_start = r + pattern_offset
            pattern_c_start = c + pattern_offset
            pattern_r_end = pattern_r_start + pattern_size
            pattern_c_end = pattern_c_start + pattern_size

            # Ensure pattern bounds are valid (should be, given loop bounds)
            if not (pattern_r_end <= height and pattern_c_end <= width):
                continue

            # Extract the current pattern from the *input* grid
            current_pattern = input_grid_np[pattern_r_start:pattern_r_end, pattern_c_start:pattern_c_end]

            # Check if the current block contains the target pattern
            if np.array_equal(current_pattern, target_pattern):
                
                # Check orthogonal neighbors in the *input* grid
                triggered = False
                for dr, dc in [(0, -block_size), (0, block_size), (-block_size, 0), (block_size, 0)]:
                    nr, nc = r + dr, c + dc # Neighbor block top-left corner

                    # Check if neighbor block coordinates are valid
                    if 0 <= nr < height - block_size + 1 and 0 <= nc < width - block_size + 1:
                        
                         # Define the neighbor pattern's location
                        n_pattern_r_start = nr + pattern_offset
                        n_pattern_c_start = nc + pattern_offset
                        n_pattern_r_end = n_pattern_r_start + pattern_size
                        n_pattern_c_end = n_pattern_c_start + pattern_size

                        # Check neighbor pattern bounds are valid
                        if not (n_pattern_r_end <= height and n_pattern_c_end <= width):
                             continue

                        # Extract neighbor pattern from *input* grid
                        neighbor_pattern = input_grid_np[n_pattern_r_start:n_pattern_r_end, n_pattern_c_start:n_pattern_c_end]
                        
                        # Check if the neighbor contains the trigger pattern
                        if np.array_equal(neighbor_pattern, trigger_pattern):
                            triggered = True
                            break # Found a trigger neighbor, no need to check others
                
                # If triggered by any neighbor, update the *output* grid
                if triggered:
                    output_grid_np[pattern_r_start:pattern_r_end, pattern_c_start:pattern_c_end] = trigger_pattern

    return output_grid_np.tolist()