Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
import math
from copy import deepcopy

"""
Processes a 2D grid containing digit patterns based on identified object types:
1. Identifies Horizontal Lines (HL): Contiguous horizontal blocks of the same non-zero digit.
2. Identifies Horizontal Patterns (HP): Sequences like D 0 D 0 D in a single row, where D is a non-zero digit. Priority is given to HLs first.
3. Identifies Scattered Digits (SD): Any remaining non-zero digits not classified as part of an HL or HP.
4. Transformation Rules:
    - HP: The entire pattern is moved horizontally to the right. The distance of the move is equal to the numerical value of the digit D constituting the pattern. The original location is cleared.
    - SD: If a Horizontal Line (HL) exists in the grid, the scattered digits are repositioned. They are cleared from their original locations and placed in a diagonal pattern starting one row below the HL and centered horizontally relative to the HL's center. The diagonal steps are (+2 rows, -2 columns) for each subsequent digit. If multiple HLs exist, the first one identified is used as the reference.
    - HL: Horizontal Lines generally remain stationary unless they are overwritten by a moved HP or serve as the reference point for repositioning SDs.
"""

# ==================================
# Helper Functions for Object Identification
# ==================================

def _is_valid(r, c, rows, cols):
    """Check if coordinates are within grid bounds."""
    return 0 <= r < rows and 0 <= c < cols

def _find_horizontal_lines(grid, visited):
    """
    Finds contiguous horizontal blocks of the same non-zero digit.
    Marks the cells of found lines as visited.
    Args:
        grid (np.array): The input grid.
        visited (np.array): Boolean mask of visited cells.
    Returns:
        list: A list of dictionaries, each representing an HL with its properties.
    """
    lines = []
    rows, cols = grid.shape
    for r in range(rows):
        c = 0
        while c < cols:
            digit = grid[r, c]
            # Look for start of a potential line (non-zero, not visited)
            if digit != 0 and not visited[r, c]:
                start_c = c
                line_coords_potential = [(r, c)]
                
                # Extend to the right as long as the digit is the same and not visited
                current_c = c + 1
                while current_c < cols and grid[r, current_c] == digit and not visited[r, current_c]:
                    line_coords_potential.append((r, current_c))
                    current_c += 1
                
                # Found a sequence of at least one cell
                end_c = current_c - 1
                
                # Mark the found cells as visited *only* after confirming the full extent
                for rr, cc in line_coords_potential:
                    visited[rr, cc] = True

                lines.append({
                    "type": "HL",
                    "digit": digit,
                    "row": r,
                    "start_col": start_c,
                    "end_col": end_c,
                    "length": len(line_coords_potential),
                    "coords": line_coords_potential
                })
                # Continue scanning *after* the identified line
                c = current_c 
            else:
                # Move to the next cell if current is 0 or already visited
                c += 1
                
    return lines

def _find_horizontal_patterns(grid, visited):
    """
    Finds horizontal patterns like D 0 D 0 D, using only unvisited cells.
    Marks the cells of found patterns as visited.
    Args:
        grid (np.array): The input grid.
        visited (np.array): Boolean mask of visited cells.
    Returns:
        list: A list of dictionaries, each representing an HP with its properties.
    """
    patterns = []
    rows, cols = grid.shape
    for r in range(rows):
        c = 0
        while c < cols:
            # Check for potential start: non-zero digit D, not visited
            if grid[r, c] != 0 and not visited[r, c]:

---
