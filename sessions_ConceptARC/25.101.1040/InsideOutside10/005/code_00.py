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

*Note: This implementation reflects the described logic, but validation against provided examples indicated this logic does not perfectly match the target transformation.*
"""

def identify_colors(grid: list[list[int]]) -> tuple[int | None, int | None, int | None]:
    """
    Identifies the Background (B), Subject (S), and Reactant (R) colors based on frequency.
    - B = most frequent.
    - S = less frequent of top 2 non-B.
    - R = more frequent of top 2 non-B.
    Handles grids with < 3 colors.
    """
    counts = collections.Counter(cell for row in grid for cell in row)
    
    if not counts:
        return 0, None, None # Default for empty grid: Background 0, S/R unknown

    # Sort colors by count (descending), then color index (ascending)
    sorted_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))

    # If fewer than 3 distinct colors are present
    if len(sorted_counts) < 3:
        background_color = sorted_counts[0][0]
        if len(sorted_counts) == 1:
             # Only background color exists
             return background_color, None, None
        else: # Exactly 2 colors
             # Assume the second color is Subject, Reactant is undefined
             subject_color = sorted_counts[1][0]
             return background_color, subject_color, None 

    # Standard case: 3 or more colors
    background_color = sorted_counts[0][0]
    
    # Isolate non-background colors and their counts
    non_background_counts = {k: v for k, v in counts.items() if k != background_color}
    
    # Sort non-background colors by count (ascending), then color index (ascending)
    # This helps determine S (less frequent) and R (more frequent) among the top 2
    sorted_non_bg = sorted(non_background_counts.items(), key=lambda item: (item[1], item[0]))

    # Assume S is the least frequent, R is the second least frequent (which is the most frequent if only 2 non-bg)
    subject_color = sorted_non_bg[0][0]
    reactant_color = sorted_non_bg[1][0]

    # Double-check: Ensure R has a count >= S count based on original counts
    # (This handles cases where counts might be equal, relying on color index sorting)
    if counts[subject_color] > counts[reactant_color]:
         subject_color, reactant_color = reactant_color, subject_color # Swap if S count > R count

    return background_color, subject_color, reactant_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    height = len(input_grid)
    width = len(input_grid[0])
    
    # Initialize output_grid as a deep copy of the input
    output_grid = [row[:] for row in input_grid]

    # Step 1: Identify Colors (Background, Subject, Reactant)
    background_color, subject_color, reactant_color = identify_colors(input_grid)

    # If Subject or Reactant colors cannot be determined (e.g., < 3 colors),
    # the transformation rules involving S and R cannot apply. Return the copy.
    if subject_color is None or reactant_color is None:
        return output_grid

    # Define cardinal directions for neighbor checking
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # E, W, S, N

    # Step 2: Identify S pixels changing to R (Rule 1)
    changes_to_R = set()
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is Subject color
            if input_grid[r][c] == subject_color:
                # Check its cardinal neighbors
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    # Ensure neighbor is within grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # If any neighbor is Reactant color, mark for change and stop checking neighbors
                        if input_grid[nr][nc] == reactant_color:
                            changes_to_R.add((r, c))
                            break 

    # Step 3: Identify Protected S Pixels (Rule 2 - Protection) using BFS
    protected_S = set() # Set to store coordinates of protected S pixels
    queue = deque() # Queue for BFS traversal

    # Find initial S pixels that are protected:
    # These are S pixels NOT changing to R, but adjacent to S pixels that ARE changing to R.
    for r_change, c_change in changes_to_R:
        for dr, dc in directions:
            nr, nc = r_change + dr, c_change + dc
            neighbor_coord = (nr, nc)
            # Check bounds and if the neighbor is S, not changing to R, and not already protected
            if 0 <= nr < height and 0 <= nc < width:
                if input_grid[nr][nc] == subject_color and \
                   neighbor_coord not in changes_to_R and \
                   neighbor_coord not in protected_S:
                    # Add to protected set and queue for propagation
                    protected_S.add(neighbor_coord)
                    queue.append(neighbor_coord)

    # Propagate protection through contiguous S pixels
    while queue:
        pr, pc = queue.popleft() # Get a protected pixel coordinate
        # Check its neighbors
        for dr, dc in directions:
            nr, nc = pr + dr, pc + dc
            neighbor_coord = (nr, nc)
            # Check bounds and if neighbor is S, not changing to R, and not already protected
            if 0 <= nr < height and 0 <= nc < width:
                 if input_grid[nr][nc] == subject_color and \
                    neighbor_coord not in changes_to_R and \
                    neighbor_coord not in protected_S:
                     # Add to protected set and queue for further propagation
                     protected_S.add(neighbor_coord)
                     queue.append(neighbor_coord)

    # Step 4: Apply Changes to Output Grid
    
    # Apply S -> R changes first (Rule 1)
    for r, c in changes_to_R:
        output_grid[r][c] = reactant_color

    # Apply S -> B changes (Rule 3)
    for r in range(height):
        for c in range(width):
            coord = (r, c)
            # Consider only pixels that were originally S and are NOT changing to R
            if input_grid[r][c] == subject_color and coord not in changes_to_R:
                is_adjacent_to_B = False
                # Check if this pixel is adjacent to the background
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width and input_grid[nr][nc] == background_color:
                        is_adjacent_to_B = True
                        break
                
                # If adjacent to Background AND NOT protected, change to Background
                if is_adjacent_to_B and coord not in protected_S:
                    output_grid[r][c] = background_color
            
            # Otherwise (originally S but protected, or originally not S), the pixel
            # either remains S (Rule 4) or was never S, so no change needed from the copy.
                    
    # Step 5: Return the final modified grid
    return output_grid