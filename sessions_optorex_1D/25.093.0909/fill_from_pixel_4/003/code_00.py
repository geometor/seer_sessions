import math # Not strictly necessary for this logic, but included as per template guide

"""
Transforms an input sequence of digits based on a local pattern.
1. Parse the input string into a list of integers.
2. Find the first occurrence of a pattern:
    - RunNeighborZero: NonZero(A), NonZero(B), Zero(C), A != B. (Neighbor B is right of Run A)
    - ZeroNeighborRun: Zero(A), NonZero(B), NonZero(C), B != C. (Neighbor B is left of Run C)
3. If a pattern is found:
    - Determine a 'TargetLength' based on the Run digit's value and the Neighbor's position relative to the Run.
        - Position='right': TargetLength=3 if Run=2; 4 if Run=3; 4 if Run=5.
        - Position='left': TargetLength=3 if Run=3; 4 if Run=5; 2 if Run=8.
    - The Neighbor digit expands into adjacent zeros (away from the Run).
    - Expansion stops when the total block of Neighbor digits reaches TargetLength, a non-zero is hit, or the grid boundary is reached.
4. Format the potentially modified sequence back into a space-separated string.
"""

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
    run_value = int(run_value) # Ensure comparison is between integers
    if position == 'right': # Neighbor is to the RIGHT of the Run
        if run_value == 2: return 3
        if run_value == 3: return 4
        if run_value == 5: return 4
    elif position == 'left': # Neighbor is to the LEFT of the Run
        if run_value == 3: return 3
        if run_value == 5: return 4
        if run_value == 8: return 2
    return -1 # Indicate no specific rule found for this combination (shouldn't happen based on examples)

def find_pattern_simplified(grid):
    """
    Scans the grid to find the first occurrence of the pattern:
    Run-Neighbor-Zero or Zero-Neighbor-Run.

    Args:
        grid (list): The input sequence of digits (as integers).

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
    """Applies the transformation rule described in the module docstring."""
    
    # Parse the input string into a list of integers
    try:
        # Handle potential numpy arrays or lists of objects that need casting
        grid = [int(x) for x in input_grid.split()] if isinstance(input_grid, str) else [int(x) for x in input_grid]
    except (ValueError, TypeError):
         # Handle cases where input might not be splittable or directly convertible
         # This might occur if the input format changes unexpectedly
         if isinstance(input_grid, list) and all(isinstance(x, int) for x in input_grid):
             grid = input_grid # Assume it's already a list of ints
         else:
             raise TypeError("Input must be a string of space-separated digits or a list of integers.")

    # Initialize output_grid as a copy of the input grid
    output_grid = list(grid)
    n = len(grid)

    # Find the first occurrence of the required pattern
    pattern_info = find_pattern_simplified(grid)

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

    # Format the output list back into a space-separated string
    return " ".join(map(str, output_grid))
