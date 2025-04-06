import numpy as np

"""
Identify patterns of '5's within 3x3 subgrids of a 3x9 input grid and replace each 
subgrid with a uniform 3x3 grid filled with a digit corresponding to the 
identified pattern.

The transformation involves:
1. Dividing the 3x9 input grid into three adjacent 3x3 subgrids.
2. Recognizing the pattern of '5's within each input subgrid.
3. Mapping each unique pattern to a specific output digit.
4. Creating a 3x9 output grid where each 3x3 subgrid is filled entirely with 
   the digit corresponding to the pattern found in the respective input subgrid.
"""

# Define the known patterns and their corresponding output digits
# Patterns are represented as tuples of tuples for hashability (use as dict keys)
PATTERN_MAP = {
    # Pattern for 6 (Top line)
    ((5, 5, 5), (0, 0, 0), (0, 0, 0)): 6,
    # Pattern for 3 ('3' shape) - based on examples
    ((5, 5, 5), (5, 0, 5), (5, 5, 5)): 3,
    # Pattern for 1 (Bottom line)
    ((0, 0, 0), (0, 0, 0), (5, 5, 5)): 1,
    # Pattern for 9 (Diagonal '\')
    ((0, 0, 5), (0, 5, 0), (5, 0, 0)): 9,
    # Pattern for 4 (Center dot)
    ((0, 0, 0), (0, 5, 0), (0, 0, 0)): 4,
}

def get_subgrid(grid: np.ndarray, index: int) -> np.ndarray:
    """
    Extracts the i-th 3x3 subgrid (0-indexed) from the input grid.
    """
    start_col = index * 3
    end_col = start_col + 3
    return grid[:, start_col:end_col]

def find_pattern_digit(subgrid: np.ndarray) -> int:
    """
    Identifies the pattern in the subgrid and returns the corresponding digit.
    """
    # Convert numpy subgrid to tuple of tuples for dictionary lookup
    subgrid_tuple = tuple(map(tuple, subgrid.tolist()))
    
    if subgrid_tuple in PATTERN_MAP:
        return PATTERN_MAP[subgrid_tuple]
    else:
        # Handle unknown patterns if necessary, though instructions assume known patterns
        raise ValueError(f"Unknown pattern encountered: {subgrid_tuple}")

def fill_output_subgrid(output_grid: np.ndarray, index: int, digit: int):
    """
    Fills the i-th 3x3 subgrid of the output grid with the given digit.
    """
    start_col = index * 3
    end_col = start_col + 3
    output_grid[:, start_col:end_col] = digit

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on 3x3 subgrid patterns.
    
    Args:
        input_grid: A 3x9 list of lists containing 0s and 5s.

    Returns:
        A 3x9 list of lists representing the transformed grid.
    """
    # Convert input list of lists to a NumPy array for easier slicing
    input_array = np.array(input_grid, dtype=int)
    
    # Get dimensions (expected to be 3x9)
    rows, cols = input_array.shape
    if rows != 3 or cols != 9:
        raise ValueError("Input grid must be 3x9")
        
    num_subgrids = cols // 3

    # Initialize the output grid (e.g., with zeros, although it will be overwritten)
    output_array = np.zeros_like(input_array)

    # Process each 3x3 subgrid
    for i in range(num_subgrids):
        # Extract the current 3x3 input subgrid
        input_subgrid = get_subgrid(input_array, i)
        
        # Determine the output digit based on the input subgrid's pattern
        output_digit = find_pattern_digit(input_subgrid)
        
        # Fill the corresponding 3x3 area in the output grid
        fill_output_subgrid(output_array, i, output_digit)

    # Convert the final NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
