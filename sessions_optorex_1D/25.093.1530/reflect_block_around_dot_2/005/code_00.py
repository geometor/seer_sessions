import numpy as np # Using numpy for potential array operations, though lists work fine

"""
Mirrors the position of a contiguous block of identical non-zero digits 
relative to a fixed pivot digit '2' within a sequence of 12 integers. 
The mirroring preserves the distance (number of zeros) between the pivot 
and the nearest edge of the block. If the block is initially before the 
pivot, it moves after the pivot in the output. If the block is initially 
after the pivot, it moves before the pivot in the output. All other positions 
in the output are filled with '0'.
"""

def find_pivot(grid):
  """Finds the index of the pivot element '2'."""
  # Convert to list if it's a numpy array for index method compatibility
  grid_list = list(grid) 
  try:
    return grid_list.index(2)
  except ValueError:
    # This should not happen based on task constraints
    raise ValueError("Pivot element '2' not found in the input grid.")

def find_block(grid):
  """
  Finds the non-zero, non-pivot block's value, start index, end index, 
  and length. Assumes exactly one such block exists per constraints.
  """
  block_val = -1
  block_start = -1
  block_end = -1
  n = len(grid)
  
  # Convert to list if it's a numpy array for easier iteration/checking
  grid_list = list(grid) 

  # Find the first non-zero, non-pivot element to determine block_val
  for i, val in enumerate(grid_list):
    if val != 0 and val != 2:
      block_val = val
      break
  
  if block_val == -1:
      # This case should not happen based on problem constraints/examples
      raise ValueError("No block value found (non-zero, non-2 digit).")

  # Find the start and end of the block
  in_block = False
  for i, val in enumerate(grid_list):
      # Start of the block
      if val == block_val and not in_block:
          block_start = i
          in_block = True
          block_end = i # Initialize end in case block has length 1
      # Continuation of the block
      elif val == block_val and in_block:
          block_end = i
      # End of the block (value changes or hits pivot)
      elif (val != block_val or val == 2) and in_block: 
          # block_end is already correctly set to the last index of the block
          break # Found the full block extent

  # Check if block was found        
  if block_start == -1:
      # This case should not happen
      raise ValueError(f"Block with value {block_val} not found or logic error.")

  block_len = block_end - block_start + 1
  return block_val, block_start, block_end, block_len

def transform(input_grid):
    """
    Transforms the input grid (list or numpy array) according to the mirroring rule.
    
    Args:
        input_grid: A list or numpy array of 12 integers representing the input state.

    Returns:
        A list of 12 integers representing the transformed output state.
    """
    # Ensure input is a list for consistent processing
    input_list = list(input_grid)
    n = len(input_list)

    # 1. Initialize output_grid with zeros
    output_grid = [0] * n

    # 2. Find Pivot and place it in the output
    pivot_idx = find_pivot(input_list)
    output_grid[pivot_idx] = 2

    # 3. Find Block details
    try:
        block_val, block_start_in, block_end_in, block_len = find_block(input_list)
    except ValueError as e:
        # Handle potential error if assumptions are violated, return grid with pivot only
        print(f"Error finding block: {e}. Returning grid with only pivot.")
        return output_grid

    # 4. Calculate Gap (distance)
    distance = -1
    new_block_start = -1
    
    # Case A: Block is AFTER the pivot in the input
    if block_start_in > pivot_idx: 
        distance = block_start_in - pivot_idx - 1 # Zeros between pivot and block start
        
        # 5. Determine New Position (Mirroring) - Block moves BEFORE pivot
        new_block_end = pivot_idx - distance - 1
        new_block_start = new_block_end - block_len + 1
        
    # Case B: Block is BEFORE the pivot in the input
    elif block_end_in < pivot_idx:
        distance = pivot_idx - block_end_in - 1 # Zeros between block end and pivot
        
        # 5. Determine New Position (Mirroring) - Block moves AFTER pivot
        new_block_start = pivot_idx + distance + 1
        
    # Case C: Block adjacent/overlapping (Error based on constraints)
    else: 
        raise ValueError("Block appears adjacent to or overlapping the pivot, violating constraints.")

    # --- Boundary Checks (Optional but good practice) ---
    new_block_end_calc = new_block_start + block_len - 1
    if new_block_start < 0 or new_block_end_calc >= n:
         # This indicates an issue with the logic or an unexpected input violating constraints
         raise ValueError(f"Calculated new block position [{new_block_start}-{new_block_end_calc}] is out of bounds [0-{n-1}]. Input: {input_list}")
    # --- End Boundary Checks ---

    # 6. Place Block in the output grid
    for i in range(block_len):
        current_idx = new_block_start + i
        # Ensure we don't overwrite the pivot (shouldn't happen with correct logic/constraints)
        if output_grid[current_idx] != 0:
             raise ValueError(f"Attempting to overwrite existing value {output_grid[current_idx]} at index {current_idx} with block value {block_val}. Output should be 0.")
        output_grid[current_idx] = block_val

    # 7. Finalize and return
    return output_grid