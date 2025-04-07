import numpy as np
from collections import Counter

"""
Transformation Rule:

1. Identify the background digit: Find the most frequent digit in the input grid.
2. Define the target pattern structure: A 6x6 grid with a specific "frame" shape. The frame consists of 8 cells filled with a "foreground" digit, and the remaining 28 cells filled with the background digit. The frame structure is:
   - Rows 0 and 5: F B F F B F
   - Rows 1 and 4: F F B B F F
   - Rows 2 and 3: F B B B B F
   (where F = foreground digit, B = background digit)
3. Scan the input grid: Iterate through all possible 6x6 subgrids.
4. Validate subgrids: For each 6x6 subgrid:
   a. Check if it contains exactly two distinct digits.
   b. One of these digits must be the background digit identified in step 1.
   c. The other digit (the foreground digit) must appear exactly 8 times.
   d. The arrangement of the foreground and background digits must match the target pattern structure defined in step 2.
5. Collect unique foreground digits: Store the foreground digit of each valid 6x6 pattern found. Keep only the unique foreground digits.
6. Sort foreground digits: Sort the collected unique foreground digits numerically in ascending order.
7. Construct the output grid: For each sorted unique foreground digit:
   a. Create a 6x6 grid representing the target pattern structure using the current foreground digit and the background digit.
   b. Append this 6x6 grid vertically to the output grid being built.
8. Return the final constructed output grid.
"""

def _get_background_digit(grid: np.ndarray) -> int:
    """Finds the most frequent digit in the grid."""
    counts = Counter(grid.flatten())
    # Find the digit with the highest count
    background_digit = counts.most_common(1)[0][0]
    return background_digit

def _is_valid_pattern(subgrid: np.ndarray, background_digit: int) -> tuple[bool, int | None]:
    """
    Checks if a 6x6 subgrid matches the required pattern structure.
    Returns (True, foreground_digit) if valid, otherwise (False, None).
    """
    if subgrid.shape != (6, 6):
        return False, None

    unique_digits = np.unique(subgrid)

    # Must have exactly two digits: background and one foreground
    if len(unique_digits) != 2:
        return False, None

    # One of the digits must be the background digit
    if background_digit not in unique_digits:
         return False, None

    # Identify the potential foreground digit
    foreground_digit = unique_digits[0] if unique_digits[1] == background_digit else unique_digits[1]

    # Count occurrences of the foreground digit
    if np.count_nonzero(subgrid == foreground_digit) != 8:
        return False, None
        
    # Verify the pattern structure exactly
    for r in range(6):
        for c in range(6):
            expected_digit = background_digit
            # Check positions that should have the foreground digit
            if (r in [0, 5] and c in [0, 2, 3, 5]) or \
               (r in [1, 4] and c in [0, 1, 4, 5]) or \
               (r in [2, 3] and c == 0) or \
               (r in [2, 3] and c == 5):
                expected_digit = foreground_digit
            
            if subgrid[r, c] != expected_digit:
                 return False, None

    # If all checks pass, it's a valid pattern
    return True, foreground_digit

def _create_pattern_grid(foreground_digit: int, background_digit: int) -> np.ndarray:
    """Creates a 6x6 grid with the specified foreground/background pattern."""
    pattern = np.full((6, 6), background_digit, dtype=int)
    # Set foreground digits based on the defined pattern structure
    pattern[[0, 5], [0, 2, 3, 5]] = foreground_digit
    pattern[[1, 4], [0, 1, 4, 5]] = foreground_digit
    pattern[[2, 3], [0, 5]] = foreground_digit
    return pattern

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies specific 6x6 patterns in the input grid, extracts their unique 
    foreground digits, sorts them, and constructs an output grid by stacking 
    the corresponding patterns vertically.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # 1. Identify the background digit
    background_digit = _get_background_digit(input_array)
    
    found_foreground_digits = set()

    # 3. Scan the input grid for 6x6 subgrids
    for r in range(rows - 5):
        for c in range(cols - 5):
            subgrid = input_array[r:r+6, c:c+6]
            
            # 4. Validate subgrids
            is_valid, foreground_digit = _is_valid_pattern(subgrid, background_digit)
            
            # 5. Collect unique foreground digits
            if is_valid:
                found_foreground_digits.add(foreground_digit)

    # 6. Sort foreground digits
    sorted_foreground_digits = sorted(list(found_foreground_digits))

    # 7. Construct the output grid
    output_patterns = []
    for fg_digit in sorted_foreground_digits:
        pattern_grid = _create_pattern_grid(fg_digit, background_digit)
        output_patterns.append(pattern_grid)

    # Stack the found patterns vertically
    if not output_patterns:
        return [] # Return empty list if no patterns found
        
    output_grid_np = np.vstack(output_patterns)
    
    # Convert back to list of lists for the expected output format
    return output_grid_np.tolist()