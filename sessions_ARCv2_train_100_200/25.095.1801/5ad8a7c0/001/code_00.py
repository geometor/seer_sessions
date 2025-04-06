import copy
import numpy as np # Although not strictly necessary for this logic, it's often useful for grid manipulations

"""
The transformation operates row by row, contingent on the overall pattern composition of the grid.

1.  **Identify Row Patterns:** Each row is classified based on the position and number of '2's:
    *   **Pattern 1 (P1):** Contains exactly two '2's, located at the very beginning and very end of the row (e.g., `[2, 0, ..., 0, 2]`).
    *   **Pattern 2 (P2):** Contains exactly two '2's, located at the second and second-to-last positions (e.g., `[0, 2, 0, ..., 0, 2, 0]`).
    *   **Other Pattern (OP):** Any row containing '2's that does not fit P1 or P2, or rows containing a number of '2's other than zero or two.
    *   **Zero Row (ZR):** A row containing only '0's.

2.  **Check for Inhibition:** If *any* row in the grid matches the Other Pattern (OP), the entire grid remains unchanged.

3.  **Apply Transformation (if not inhibited):**
    *   **P2 Priority:** If the grid contains *any* P2 rows (and potentially P1 and/or ZR rows, but no OP rows), then *only* the P2 rows are modified. The modification involves changing all '0's located strictly *between* the two '2's in the P2 row to '2'. P1 rows remain unchanged in this case.
    *   **P1 Fallback:** If the grid contains *only* P1 rows (and potentially ZR rows, but no P2 or OP rows), then the P1 rows are modified. The modification involves changing all '0's located strictly *between* the two '2's in the P1 row to '2'.

4.  Zero Rows (ZR) are never modified.
"""

# --- Helper Functions ---

def is_pattern_1(row: list[int]) -> bool:
    """Checks if a row matches Pattern 1: [2, 0, ..., 0, 2]."""
    n = len(row)
    if n < 2:
        return False
    # Check ends and count of 2s
    if row[0] == 2 and row[n-1] == 2 and row.count(2) == 2:
        # Check intermediates are all 0
        for i in range(1, n - 1):
            if row[i] != 0:
                return False
        return True
    return False

def is_pattern_2(row: list[int]) -> bool:
    """Checks if a row matches Pattern 2: [0, 2, 0, ..., 0, 2, 0]."""
    n = len(row)
    # Minimum length for pattern 2 is technically 4, e.g., [0, 2, 2, 0]
    if n < 4: 
        return False
    # Check second/second-to-last, ends, and count of 2s
    if row[1] == 2 and row[n-2] == 2 and row[0] == 0 and row[n-1] == 0 and row.count(2) == 2:
         # Check intermediates are all 0
        for i in range(2, n - 2):
            if row[i] != 0:
                return False
        return True
    return False

def fill_pattern_1(row: list[int]) -> list[int]:
    """Fills the zeros between the 2s in a Pattern 1 row."""
    n = len(row)
    new_row = list(row) # Copy the row to avoid modifying the original if passed directly
    for i in range(1, n - 1):
        new_row[i] = 2
    return new_row

def fill_pattern_2(row: list[int]) -> list[int]:
    """Fills the zeros between the 2s in a Pattern 2 row."""
    n = len(row)
    new_row = list(row) # Copy the row
    for i in range(2, n - 2):
        new_row[i] = 2
    return new_row

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on row patterns P1 and P2,
    inhibited by Other Patterns (OP), with P2 taking priority over P1.
    """
    # Create a deep copy to avoid modifying the original input
    output_grid = copy.deepcopy(input_grid)
    
    if not input_grid or not input_grid[0]:
        return output_grid # Handle empty grid case

    rows = len(input_grid)
    
    p1_indices = []
    p2_indices = []
    has_other_pattern = False

    # 1. Identify Row Patterns and Check for Inhibition
    for r, row in enumerate(input_grid):
        num_twos = row.count(2)
        
        if num_twos == 0:
            continue # Zero Row (ZR), no action needed, doesn't inhibit
        elif num_twos == 2:
            if is_pattern_1(row):
                p1_indices.append(r)
            elif is_pattern_2(row):
                p2_indices.append(r)
            else: # Two 2s, but not P1 or P2 -> Other Pattern (OP)
                has_other_pattern = True
                break # Stop checking if OP found, as it inhibits all changes
        else: # Not 0 or 2 '2's -> Other Pattern (OP)
             has_other_pattern = True
             break # Stop checking if OP found

    # 2. Apply Transformation Logic (if not inhibited)
    if has_other_pattern:
        # If any OP row exists, return the original grid unchanged
        return input_grid # Or return output_grid which is a copy

    if p2_indices: 
        # P2 Priority: If P2 rows exist, only fill them
        for r_idx in p2_indices:
             output_grid[r_idx] = fill_pattern_2(input_grid[r_idx])
             # Note: We modify output_grid based on the *original* input_grid[r_idx] pattern
             
    elif p1_indices: 
        # P1 Fallback: If only P1 (and maybe ZR) rows exist, fill P1 rows
        for r_idx in p1_indices:
            output_grid[r_idx] = fill_pattern_1(input_grid[r_idx])
            # Note: We modify output_grid based on the *original* input_grid[r_idx] pattern

    # If neither p1_indices nor p2_indices are non-empty (and no OP), 
    # it means the grid only contained ZR rows, so output_grid remains unchanged.
            
    return output_grid