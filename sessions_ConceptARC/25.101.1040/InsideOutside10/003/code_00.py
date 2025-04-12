import collections
import copy
from collections import deque

"""
The transformation rule identifies three key colors in the input grid: Background (B), Subject (S), and Reactant (R).
- Background (B) is the most frequent color.
- Subject (S) is the less frequent of the two most common non-background colors.
- Reactant (R) is the more frequent of the two most common non-background colors.

The transformation modifies only the Subject (S) pixels based on their cardinal neighbors in the input grid:

1.  **Change to Reactant (R):** An S pixel changes to R if it is cardinally adjacent to an R pixel. This rule has the highest priority.
2.  **Protection:** An S pixel P (that is not changing to R) is considered "protected" if it is cardinally adjacent to another S pixel P' which IS changing to R (Rule 1), OR if P is cardinally adjacent to another S pixel P'' which is itself "protected". Protection propagates through contiguous S pixels originating from those adjacent to S->R pixels.
3.  **Change to Background (B):** An S pixel changes to B if it is NOT changing to R (Rule 1), IS cardinally adjacent to a B pixel, AND is NOT "protected" (Rule 2).
4.  **Remain Subject (S):** If an S pixel does not meet the conditions to change to R or B, it remains S.
"""

def identify_colors(grid: list[list[int]]) -> tuple[int | None, int | None, int | None]:
    """
    Identifies the Background (B), Subject (S), and Reactant (R) colors.
    Assumes B is most frequent.
    Assumes S is less frequent non-B, R is more frequent non-B.
    
    Args:
        grid: The input grid.
        
    Returns:
        A tuple (background_color, subject_color, reactant_color).
        Returns (None, None, None) if roles cannot be determined (e.g., < 3 colors).
    """
    counts = collections.Counter(cell for row in grid for cell in row)
    
    if not counts:
        return 0, None, None # Default for empty grid

    # Sort by count descending, then color value ascending
    sorted_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))

    if len(sorted_counts) < 3:
        # Handle cases with 1 or 2 colors
        background_color = sorted_counts[0][0]
        if len(sorted_counts) == 1:
             return background_color, None, None
        else: # Exactly 2 colors
             # Treat the second color as S? Or R? The logic requires S and R.
             # Let's assume the less frequent non-bg is S. Here there's only one non-bg.
             subject_color = sorted_counts[1][0]
             return background_color, subject_color, None # No Reactant

    background_color = sorted_counts[0][0]
    
    # Consider the top two most frequent non-background colors
    non_background_counts = {k: v for k, v in counts.items() if k != background_color}
    
    # Sort non-background by count ascending, then color index ascending
    sorted_non_bg = sorted(non_background_counts.items(), key=lambda item: (item[1], item[0]))

    # S is the one with the lower count, R is the one with the higher count among the two main ones
    # If counts are equal, lower color index is S, higher is R.
    subject_color = sorted_non_bg[0][0]
    reactant_color = sorted_non_bg[1][0]

    # Verify assumption: S is less frequent than R
    if counts[subject_color] > counts[reactant_color]:
         subject_color, reactant_color = reactant_color, subject_color # Swap

    return background_color, subject_color, reactant_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    height = len(input_grid)
    width = len(input_grid[0])
    
    # Initialize output_grid as a deep copy
    output_grid = [row[:] for row in input_grid]

    # 1. Identify Colors
    background_color, subject_color, reactant_color = identify_colors(input_grid)

    # If S or R cannot be determined, no transformation occurs based on the rules
    if subject_color is None or reactant_color is None:
        return output_grid

    # Define cardinal directions
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # 2. Identify S->R Changes
    changes_to_R = set()
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == subject_color:
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width and input_grid[nr][nc] == reactant_color:
                        changes_to_R.add((r, c))
                        break # Move to next pixel once an R neighbor is found

    # 3. Identify Protected S Pixels using BFS
    protected_S = set()
    queue = deque()

    # Initial protected set: S pixels (not changing to R) adjacent to S->R pixels
    for r_change, c_change in changes_to_R:
        for dr, dc in directions:
            nr, nc = r_change + dr, c_change + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbor_coord = (nr, nc)
                if input_grid[nr][nc] == subject_color and neighbor_coord not in changes_to_R and neighbor_coord not in protected_S:
                    protected_S.add(neighbor_coord)
                    queue.append(neighbor_coord)

    # Propagate protection
    while queue:
        pr, pc = queue.popleft()
        for dr, dc in directions:
            nr, nc = pr + dr, pc + dc
            neighbor_coord = (nr, nc)
            if 0 <= nr < height and 0 <= nc < width:
                 if input_grid[nr][nc] == subject_color and neighbor_coord not in changes_to_R and neighbor_coord not in protected_S:
                     protected_S.add(neighbor_coord)
                     queue.append(neighbor_coord)

    # 4. Apply Changes to Output Grid
    # Apply S->R changes first
    for r, c in changes_to_R:
        output_grid[r][c] = reactant_color

    # Apply S->B changes
    for r in range(height):
        for c in range(width):
            coord = (r, c)
            # Consider only S pixels that did NOT change to R
            if input_grid[r][c] == subject_color and coord not in changes_to_R:
                is_adjacent_to_B = False
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width and input_grid[nr][nc] == background_color:
                        is_adjacent_to_B = True
                        break
                
                # Change to B if adjacent to B AND not protected
                if is_adjacent_to_B and coord not in protected_S:
                    output_grid[r][c] = background_color
                    
    # 5. Return the final output grid
    return output_grid