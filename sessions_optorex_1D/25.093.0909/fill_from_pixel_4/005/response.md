```python
"""
Transforms an input sequence (list of integers) based on a local pattern.
1. Scan the input list to find the first occurrence of a specific three-element pattern centered at index `i` (where 0 < i < length-1). Let the elements be A (at i-1), B (at i, the 'Neighbor'), and C (at i+1).
2. The patterns are:
    - RunNeighborZero: A is non-zero, B is non-zero, C is zero, and A != B. The 'Run' value is A, and the Neighbor's position relative to the Run is 'right'.
    - ZeroNeighborRun: A is zero, B is non-zero, C is non-zero, and B != C. The 'Run' value is C, and the Neighbor's position relative to the Run is 'left'.
3. If a pattern is found:
    - Determine a 'TargetLength' for the final contiguous block of the Neighbor digit (B) based on the Run value and the Neighbor's relative position ('left'/'right'). The specific rules are:
        - Position 'right': (Run=2 -> Length=3), (Run=3 -> Length=4), (Run=5 -> Length=4)
        - Position 'left': (Run=3 -> Length=3), (Run=5 -> Length=4), (Run=8 -> Length=2)
    - The Neighbor digit (B) expands into adjacent zeros in the direction *away* from the Run (rightward for 'right' position, leftward for 'left' position).
    - Expansion modifies a copy of the input list. It replaces zeros with the Neighbor digit until the total count of the Neighbor digit in the expanding block (including the original Neighbor at index `i`) reaches the TargetLength, or a non-zero digit is encountered, or the list boundary is reached.
4. If no pattern is found, the original list is returned unchanged.
"""

import math # Not used, but included as per template guide

def get_target_length(run_value, position):
    """
    Calculates the target length of the expanded block based on the 
    adjacent run's value and the relative position of the neighbor.
    
    Args:
        run_value (int): The digit value of the adjacent run.
        position (str): 'left' if the neighbor is left of the run, 
                        'right' if the neighbor is right of the run.
                        
    Returns:
        int: The calculated target length for the final block of neighbor digits,
             or -1 if no specific rule is found.
    """
    # Ensure comparison is between integers if run_value comes as str or other type
    try:
        run_value = int(run_value) 
    except (ValueError, TypeError):
        return -1 # Invalid run_value type

    if position == 'right': # Neighbor is to the RIGHT of the Run
        if run_value == 2: return 3
        if run_value == 3: return 4
        if run_value == 5: return 4
    elif position == 'left': # Neighbor is to the LEFT of the Run
        if run_value == 3: return 3
        if run_value == 5: return 4
        if run_value == 8: return 2
        
    return -1 # Indicate no specific rule found for this combination

def find_pattern(grid):
    """
    Scans the grid to find the first occurrence of the pattern:
    Run-Neighbor-Zero or Zero-Neighbor-Run.

    Args:
        grid (list): The input sequence of integers.

    Returns:
        dict: A dictionary containing pattern details ('neighbor_value', 
              'neighbor_index', 'run_value', 'position') if found, 
              otherwise None.
              'position' indicates if the neighbor is 'left' or 'right' of the run.
    """
    n = len(grid)
    # Iterate through possible neighbor positions (requires elements to the left and right)
    for i in range(1, n - 1): 
        A = grid[i-1]
        B = grid[i]   # Potential neighbor
        C = grid[i+1]
        
        # Skip if the potential neighbor is zero
        if B == 0: 
            continue
            
        # Case 1: Run-Neighbor-Zero (Neighbor right of Run)
        # Conditions: A!=0, B!=0 (checked above), C=0, A!=B
        if A != 0 and C == 0 and A != B:
            return {'neighbor_value': B, 'neighbor_index': i, 'run_value': A, 'position': 'right'}
            
        # Case 2: Zero-Neighbor-Run (Neighbor left of Run)
        # Conditions: A=0, B!=0 (checked above), C!=0, B!=C
        if A == 0 and C != 0 and B != C:
            return {'neighbor_value': B, 'neighbor_index': i, 'run_value': C, 'position': 'left'}
            
    return None # No pattern found

def transform(input_grid):
    """
    Applies the transformation rule described in the module docstring.
    Expects input_grid to be a list of integers.
    """
    # Ensure input is a list (create a copy to avoid modifying the original if passed by reference)
    if not isinstance(input_grid, list):
         raise TypeError("Input must be a list of integers.")
         
    grid = list(input_grid) # Work on a copy
    output_grid = list(grid) # Initialize output_grid as a copy to be modified
    n = len(grid)

    # Find the first occurrence of the required pattern
    pattern_info = find_pattern(grid)

    # If a pattern is found, apply the transformation
    if pattern_info:
        neighbor_val = pattern_info['neighbor_value']
        neighbor_idx = pattern_info['neighbor_index']
        run_val = pattern_info['run_value']
        position = pattern_info['position']

        # Determine the target length for the final block of neighbor digits
        target_length = get_target_length(run_val, position)

        # Only proceed if a valid target length rule exists (TargetLength > 0)
        if target_length > 0:
            
            # Apply expansion based on the neighbor's position relative to the run
            if position == 'right':
                # Neighbor is to the right of the run, expand rightwards into zeros
                # The block includes the neighbor, so we need to fill target_length-1 more cells
                current_block_length = 1 # Start with the neighbor itself
                # Iterate from the first zero to the right
                for k in range(neighbor_idx + 1, n):
                    # Stop if target length is reached
                    if current_block_length >= target_length:
                        break
                    # Only replace zeros
                    if grid[k] == 0: 
                        output_grid[k] = neighbor_val
                        current_block_length += 1
                    else: 
                        # Stop expansion if a non-zero is encountered
                        break
                        
            elif position == 'left':
                # Neighbor is to the left of the run, expand leftwards into zeros
                # The block includes the neighbor, so we need to fill target_length-1 more cells
                current_block_length = 1 # Start with the neighbor itself
                # Iterate from the first zero to the left (going backwards)
                for k in range(neighbor_idx - 1, -1, -1):
                    # Stop if target length is reached
                    if current_block_length >= target_length:
                        break
                    # Only replace zeros
                    if grid[k] == 0:
                        output_grid[k] = neighbor_val
                        current_block_length += 1
                    else:
                        # Stop expansion if a non-zero is encountered
                        break

    # Return the modified grid (or the original copy if no pattern was found/applied)
    return output_grid
```