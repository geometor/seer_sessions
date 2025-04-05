"""
Transforms an input sequence (list of integers) based on a local pattern.
1. Parse the input (expected as a string of space-separated digits, though the function now accepts a list of integers directly) into a list of integers (the `Grid`).
2. Scan the `Grid` to find the first occurrence of a specific three-element pattern centered at index `i` (where 0 < i < length-1). Let the elements be A (at i-1), B (at i, the 'Neighbor'), and C (at i+1).
3. The patterns are:
    - RunNeighborZero: A is non-zero, B is non-zero, C is zero, and A != B. The 'Run' value is A, and the Neighbor's position relative to the Run is 'right'.
    - ZeroNeighborRun: A is zero, B is non-zero, C is non-zero, and B != C. The 'Run' value is C, and the Neighbor's position relative to the Run is 'left'.
4. If a pattern is found:
    - Determine a 'TargetLength' for the final contiguous block of the Neighbor digit (B) based on the Run value and the Neighbor's relative position ('left'/'right'). The specific rules are:
        - Position 'right': (Run=2 -> Length=3), (Run=3 -> Length=4), (Run=5 -> Length=4)
        - Position 'left': (Run=3 -> Length=3), (Run=5 -> Length=4), (Run=8 -> Length=2)
    - The Neighbor digit (B) expands into adjacent zeros in the direction *away* from the Run (rightward for 'right' position, leftward for 'left' position).
    - Expansion modifies a copy of the input list. It replaces zeros with the Neighbor digit until the total count of the Neighbor digit in the expanding block (including the original Neighbor at index `i`) reaches the TargetLength, or a non-zero digit is encountered, or the list boundary is reached.
5. If no pattern is found, the original list is returned unchanged. The function returns the resulting list of integers.
"""

import math # Not used, but included as per standard practice

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
    # The central element 'B' is the potential Neighbor.
    for i in range(1, n - 1): 
        A = grid[i-1] # Element to the left of potential Neighbor
        B = grid[i]   # Potential Neighbor
        C = grid[i+1] # Element to the right of potential Neighbor
        
        # Skip if the potential neighbor B is zero, as it must be non-zero
        if B == 0: 
            continue
            
        # Check for Case 1: Run-Neighbor-Zero (A=Run, B=Neighbor, C=Zero)
        # Conditions: A is non-zero (Run), B is non-zero (Neighbor), C is zero, A is different from B
        if A != 0 and C == 0 and A != B:
            # Found the pattern: Neighbor B is to the right of Run A
            return {'neighbor_value': B, 'neighbor_index': i, 'run_value': A, 'position': 'right'}
            
        # Check for Case 2: Zero-Neighbor-Run (A=Zero, B=Neighbor, C=Run)
        # Conditions: A is zero, B is non-zero (Neighbor), C is non-zero (Run), B is different from C
        if A == 0 and C != 0 and B != C:
            # Found the pattern: Neighbor B is to the left of Run C
            return {'neighbor_value': B, 'neighbor_index': i, 'run_value': C, 'position': 'left'}
            
    # If the loop completes without finding a pattern
    return None 

def transform(input_grid):
    """
    Applies the transformation rule described in the module docstring.
    Expects input_grid to be a list of integers.
    """
    # Ensure input is a list (create a copy to avoid modifying the original if passed by reference)
    if not isinstance(input_grid, list):
         # If input is not a list, attempt to parse it as a space-separated string
         if isinstance(input_grid, str):
             try:
                 grid = list(map(int, input_grid.split()))
             except ValueError:
                 raise TypeError("Input string must contain space-separated integers.")
         else:
             raise TypeError("Input must be a list of integers or a string of space-separated integers.")
    else:
        # If it is already a list, make a copy to work with
        grid = list(input_grid) 
    
    # Initialize output_grid as a copy of the potentially parsed input grid
    output_grid = list(grid) 
    n = len(grid)

    # Find the first occurrence of the required pattern using the helper function
    pattern_info = find_pattern(grid)

    # If a pattern was found, proceed with the transformation
    if pattern_info:
        # Extract details from the found pattern
        neighbor_val = pattern_info['neighbor_value']
        neighbor_idx = pattern_info['neighbor_index']
        run_val = pattern_info['run_value']
        position = pattern_info['position']

        # Determine the target length for the final block of neighbor digits using the helper function
        target_length = get_target_length(run_val, position)

        # Only proceed with expansion if a valid target length rule exists (TargetLength > 0)
        if target_length > 0:
            
            # Apply expansion based on the neighbor's position relative to the run
            if position == 'right':
                # Neighbor is to the right of the run, so expand rightwards into zeros
                
                # The block starts with the neighbor itself, so initialize count to 1
                current_block_length = 1 
                
                # Iterate from the cell immediately to the right of the neighbor (index i+1) towards the end
                for k in range(neighbor_idx + 1, n):
                    # Stop expansion if the target length for the block is reached
                    if current_block_length >= target_length:
                        break
                    
                    # Check if the current cell contains a zero - only zeros are replaced
                    if grid[k] == 0: 
                        # Replace the zero with the neighbor's value in the output grid
                        output_grid[k] = neighbor_val
                        # Increment the count of digits in the expanding block
                        current_block_length += 1
                    else: 
                        # Stop expansion if a non-zero digit is encountered
                        break
                        
            elif position == 'left':
                # Neighbor is to the left of the run, so expand leftwards into zeros
                
                # The block starts with the neighbor itself, so initialize count to 1
                current_block_length = 1 
                
                # Iterate from the cell immediately to the left of the neighbor (index i-1) towards the beginning (index 0)
                for k in range(neighbor_idx - 1, -1, -1): # Step backwards from i-1 down to 0
                    # Stop expansion if the target length for the block is reached
                    if current_block_length >= target_length:
                        break
                        
                    # Check if the current cell contains a zero - only zeros are replaced
                    if grid[k] == 0:
                        # Replace the zero with the neighbor's value in the output grid
                        output_grid[k] = neighbor_val
                        # Increment the count of digits in the expanding block
                        current_block_length += 1
                    else:
                        # Stop expansion if a non-zero digit is encountered
                        break

    # Return the modified grid (or the original copy if no pattern was found/applied)
    return output_grid