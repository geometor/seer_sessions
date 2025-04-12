```python
import collections
import copy
from collections import deque

"""
The transformation identifies three key colors in the input grid based on frequency: Background (B, most frequent), Subject (S, less frequent non-B), and Reactant (R, more frequent non-B). It modifies only the Subject (S) pixels according to the following rules applied based on the initial state of the input grid:

1.  **S -> R Change:** An S pixel changes to color R if it is cardinally adjacent to an R pixel. This rule has the highest priority.
2.  **S -> B Change (Hypothesized Rule):** An S pixel that does *not* change to R changes to color B if it is cardinally adjacent to a B pixel AND it is *not* considered "protected".
3.  **Protection (Hypothesized Rule):** An S pixel P (not changing to R) is "protected" if it's cardinally adjacent to an S pixel P' changing to R, or if P is adjacent to another S pixel P'' which is itself protected. Protection propagates through contiguous S pixels starting from those adjacent to the S->R boundary.
4.  **S Remains S:** An S pixel remains S if it doesn't meet the conditions for changing to R or B (i.e., it's not adjacent to R, and if it is adjacent to B, it's "protected").

*Validation Note:* Implementations based on this hypothesized "protection" rule (Rule 2 & 3) failed to perfectly replicate the transformations in the provided training examples. The exact conditions governing the S->B change remain uncertain.
"""

def identify_colors(grid: list[list[int]]) -> tuple[int | None, int | None, int | None]:
    """
    Identifies the Background (B), Subject (S), and Reactant (R) colors based on frequency.
    - B = most frequent.
    - S = less frequent of top 2 non-B.
    - R = more frequent of top 2 non-B.
    Handles grids with < 3 colors.
    Returns (background_color, subject_color, reactant_color)
    """
    counts = collections.Counter(cell for row in grid for cell in row)
    
    if not counts:
        return 0, None, None # Default for empty grid

    # Sort colors by count (descending), then color index (ascending)
    sorted_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))

    if len(sorted_counts) < 3:
        background_color = sorted_counts[0][0]
        if len(sorted_counts) == 1:
             return background_color, None, None # Only background color
        else: # Exactly 2 colors
             # Assume the second color is Subject, Reactant is undefined
             subject_color = sorted_counts[1][0]
             return background_color, subject_color, None 

    # Standard case: 3 or more colors
    background_color = sorted_counts[0][0]
    
    # Isolate non-background colors and their counts
    non_background_counts = {k: v for k, v in counts.items() if k != background_color}
    
    # Sort non-background colors by count (ascending), then color index (ascending)
    sorted_non_bg = sorted(non_background_counts.items(), key=lambda item: (item[1], item[0]))

    # Assume S is the least frequent, R is the second least frequent (most frequent if only 2 non-bg)
    subject_color = sorted_non_bg[0][0]
    reactant_color = sorted_non_bg[1][0]

    # Ensure R has a count >= S count based on original counts
    if counts[subject_color] > counts[reactant_color]:
         subject_color, reactant_color = reactant_color, subject_color # Swap

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

    # If Subject or Reactant colors cannot be determined, return the input copy
    if subject_color is None or reactant_color is None:
        return output_grid

    # Define cardinal directions for neighbor checking
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # E, W, S, N

    # Step 2: Identify S pixels changing to R (Rule 1)
    changes_to_R = set()
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == subject_color:
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width and input_grid[nr][nc] == reactant_color:
                        changes_to_R.add((r, c))
                        break # Found R neighbor, mark and move to next pixel

    # Step 3: Identify Protected S Pixels (Hypothesized Rule 3) using BFS
    protected_S = set() 
    queue = deque() 

    # Seed the BFS with S pixels adjacent to S->R pixels
    for r_change, c_change in changes_to_R:
        for dr, dc in directions:
            nr, nc = r_change + dr, c_change + dc
            neighbor_coord = (nr, nc)
            # Check if neighbor is S, not changing to R, and not already protected
            if 0 <= nr < height and 0 <= nc < width and \
               input_grid[nr][nc] == subject_color and \
               neighbor_coord not in changes_to_R and \
               neighbor_coord not in protected_S:
                protected_S.add(neighbor_coord)
                queue.append(neighbor_coord)

    # Propagate protection via BFS
    while queue:
        pr, pc = queue.popleft() 
        for dr, dc in directions:
            nr, nc = pr + dr, pc + dc
            neighbor_coord = (nr, nc)
            # Check if neighbor is S, not changing to R, and not already protected
            if 0 <= nr < height and 0 <= nc < width and \
               input_grid[nr][nc] == subject_color and \
               neighbor_coord not in changes_to_R and \
               neighbor_coord not in protected_S:
                 protected_S.add(neighbor_coord)
                 queue.append(neighbor_coord)

    # Step 4: Apply Changes to Output Grid
    
    # Apply S -> R changes first (Rule 1)
    for r, c in changes_to_R:
        output_grid[r][c] = reactant_color

    # Apply S -> B changes based on the hypothesized rule (Rule 2)
    for r in range(height):
        for c in range(width):
            coord = (r, c)
            # Consider only pixels that were originally S and are NOT changing to R
            if input_grid[r][c] == subject_color and coord not in changes_to_R:
                is_adjacent_to_B = False
                # Check if adjacent to Background
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width and input_grid[nr][nc] == background_color:
                        is_adjacent_to_B = True
                        break
                
                # Change to Background if adjacent to B AND NOT protected
                if is_adjacent_to_B and coord not in protected_S:
                    output_grid[r][c] = background_color
            
            # Pixels remain unchanged if they were not S, changed to R, or were S but protected (Rule 4)
                    
    # Step 5: Return the final modified grid
    return output_grid
```