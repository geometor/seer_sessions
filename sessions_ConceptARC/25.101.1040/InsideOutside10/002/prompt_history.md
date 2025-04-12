
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 0 0
0 0 2 0 0 0 0 0 0 2 0 0
0 0 2 0 0 3 3 3 3 3 3 3
0 0 2 0 0 0 0 0 0 2 0 0
0 0 2 0 0 0 0 0 0 2 0 0
3 3 3 3 3 3 0 0 0 2 0 0
0 0 2 0 0 0 0 0 0 2 0 0
0 0 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 0 0
0 0 2 0 0 0 0 0 0 2 0 0
0 0 2 0 0 3 3 3 3 2 0 0
0 0 2 0 0 0 0 0 0 2 0 0
0 0 2 0 0 0 0 0 0 2 0 0
0 0 2 3 3 3 0 0 0 2 0 0
0 0 2 0 0 0 0 0 0 2 0 0
0 0 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 1 4 0 0 0 0 0 0
0 0 0 0 1 0 4 0 0 0 0 0
0 0 0 4 1 0 0 4 0 0 0 0
0 0 4 0 1 0 0 0 4 0 0 0
0 4 0 0 1 0 1 1 1 1 1 1
0 0 4 0 0 0 0 0 4 0 0 0
0 0 0 4 1 1 1 4 0 0 0 0
0 0 0 0 4 0 4 0 0 0 1 0
0 0 0 0 0 4 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 1 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 4 0 4 0 0 0 0 0
0 0 0 4 1 0 0 4 0 0 0 0
0 0 4 0 1 0 0 0 4 0 0 0
0 4 0 0 1 0 0 1 1 4 0 0
0 0 4 0 0 0 0 0 4 0 0 0
0 0 0 4 1 1 1 4 0 0 0 0
0 0 0 0 4 0 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception of the elements:**
    *   The grids contain a background color (white, 0) and two other primary colors.
    *   One color acts as a "Subject" (green(3) in example 1, blue(1) in example 2), often forming lines or shapes.
    *   Another color acts as a "Reactant" (red(2) in example 1, yellow(4) in example 2), sometimes forming frames or scattered points.
    *   The transformation modifies only the Subject color pixels based on their cardinal neighbors.
    *   The Subject color changes to the Reactant color if adjacent to a Reactant pixel.
    *   The Subject color changes to the Background color if adjacent to the Background color *unless* it's "protected" by being adjacent to another Subject pixel that isn't changing.

*   **YAML block documenting facts:**
    
```yaml
    task_context:
      grid_properties:
        size: Variable (e.g., 12x12)
        background_color: White (0)
      objects:
        - type: Subject_Shape
          color: Green (3) in ex1, Blue (1) in ex2
          properties: Forms lines or contiguous regions. Changes based on neighbors.
        - type: Reactant_Shape
          color: Red (2) in ex1, Yellow (4) in ex2
          properties: Does not change. Influences adjacent Subject_Shape pixels.
        - type: Background
          color: White (0)
          properties: Does not change. Influences adjacent Subject_Shape pixels.
      relationships:
        - type: Adjacency (Cardinal)
          description: Determines the interaction between pixels.
      actions:
        - name: Color_Change
          target: Subject_Shape pixels
          conditions:
            - rule: If a Subject pixel is cardinally adjacent to a Reactant pixel, it changes to the Reactant color.
            - rule: If a Subject pixel is cardinally adjacent to the Background color AND NOT cardinally adjacent to a "stable" Subject pixel (one that is not changing color due to Reactant adjacency), it changes to the Background color.
            - rule: Otherwise, the Subject pixel remains its original color.
          priority: Reactant adjacency takes priority over Background adjacency. Protection by stable Subject neighbors takes priority over changing to Background.
    ```


*   **Natural language program:**
    1.  Identify the three primary colors present in the input grid: the Background color (B, typically white/0), the Subject color (S, the one that changes), and the Reactant color (R, the one that causes S to change to R).
    2.  Initialize the output grid as a copy of the input grid.
    3.  Create a list/set of coordinates, `changes_to_R`, to store Subject pixels that will change to the Reactant color.
    4.  Iterate through each pixel `(r, c)` of the input grid. If the pixel `input[r][c]` has color S, check its 4 cardinal neighbors in the input grid. If any neighbor has color R, add the coordinate `(r, c)` to the `changes_to_R` list.
    5.  Create a list/set of coordinates, `changes_to_B`, to store Subject pixels that will change to the Background color.
    6.  Iterate again through each pixel `(r, c)` of the input grid. If `input[r][c]` has color S AND its coordinate `(r, c)` is NOT in `changes_to_R`:
        a.  Check its 4 cardinal neighbors in the input grid.
        b.  Determine if it has at least one neighbor with color B (`has_B_neighbor`).
        c.  Determine if it has at least one neighbor `(nr, nc)` that is color S AND the coordinate `(nr, nc)` is NOT in `changes_to_R` (`has_protecting_S_neighbor`).
        d.  If `has_B_neighbor` is true AND `has_protecting_S_neighbor` is false, add the coordinate `(r, c)` to the `changes_to_B` list.
    7.  Modify the output grid based on the collected changes:
        a.  For each coordinate `(r, c)` in `changes_to_R`, set `output[r][c]` to color R.
        b.  For each coordinate `(r, c)` in `changes_to_B`, set `output[r][c]` to color B.
    8.  Return the final output grid.
```python
import collections
import copy

"""
This transformation rule identifies three key colors in the input grid: Background (B), Subject (S), and Reactant (R).
The Background color is assumed to be the most frequent color (typically white/0). 
Among the two other dominant non-background colors, the Subject (S) color is identified as the one that occurs less frequently in the input grid, and the remaining color is the Reactant (R).

The transformation proceeds in two main steps, modifying only the pixels with the Subject color:

1.  **Change to Reactant Color:** Any Subject pixel that is cardinally adjacent (up, down, left, right) to a Reactant pixel changes its color to the Reactant color.

2.  **Change to Background Color:** Any Subject pixel that did *not* change in step 1 is then considered. If such a pixel is cardinally adjacent to a Background pixel AND it is *not* cardinally adjacent to any "stable" Subject pixel (i.e., another Subject pixel that is also *not* changing to the Reactant color in step 1), then it changes its color to the Background color.

Pixels that are not Subject color, or Subject pixels that do not meet the conditions for changing to Reactant or Background color, remain unchanged. The changes identified in step 1 take precedence.
"""

def identify_colors(grid: list[list[int]]) -> tuple[int, int, int]:
    """
    Identifies the Background (B), Subject (S), and Reactant (R) colors.
    Assumes Background is the most frequent color.
    Assumes Subject is the less frequent of the two other main colors.
    
    Args:
        grid: The input grid.
        
    Returns:
        A tuple (background_color, subject_color, reactant_color).
        Returns (None, None, None) if fewer than 3 distinct colors are present.
    """
    counts = collections.Counter(cell for row in grid for cell in row)
    
    if len(counts) < 3:
        # Cannot determine B, S, R if fewer than 3 colors exist.
        # Or handle specific cases? For now, assume task always has 3+.
         # Find the most frequent color anyway for B
        if not counts: return (0, -1, -1) # Empty grid defaults
        background_color = counts.most_common(1)[0][0]
        
        non_background_colors = [c for c in counts if c != background_color]
        if len(non_background_colors) == 1:
            # Only B and one other color. Let's call the other S. No R.
            return (background_color, non_background_colors[0], -1) 
        elif len(non_background_colors) == 0:
             # Only B color
             return (background_color, -1, -1)
        else: # Should not happen based on initial check, but defensive coding
            return (background_color, -1, -1)


    # More than 3 colors, but let's focus on the top 3 frequencies
    # B is the most frequent
    background_color = counts.most_common(1)[0][0]
    
    # Find the two most frequent non-background colors
    non_background_counts = {k: v for k, v in counts.items() if k != background_color}
    
    if len(non_background_counts) < 2:
         # Handle cases with only B and one other color, or just B
        if len(non_background_counts) == 1:
             return (background_color, list(non_background_counts.keys())[0], -1)
        else:
             return (background_color, -1, -1)


    # Sort non-background colors by frequency (ascending)
    sorted_non_background = sorted(non_background_counts.items(), key=lambda item: item[1])
    
    # Assume Subject (S) is the least frequent of the two main non-background colors
    # Assume Reactant (R) is the more frequent of the two
    # This handles cases where there might be other minor colors present.
    # We consider the two *most frequent* non-background colors.
    if len(sorted_non_background) >= 2:
        subject_color = sorted_non_background[0][0]
        reactant_color = sorted_non_background[1][0]
        # Check if R might actually be less frequent than S among top 2 non-bg
        if counts[subject_color] > counts[reactant_color]:
             subject_color, reactant_color = reactant_color, subject_color # Swap
    else: # Only one non-background color
         subject_color = sorted_non_background[0][0]
         reactant_color = -1 # Indicate no reactant color

    return background_color, subject_color, reactant_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on neighbor interactions.
    Identifies Background (B), Subject (S), and Reactant (R) colors.
    S pixels change to R if adjacent to R.
    Remaining S pixels change to B if adjacent to B and not adjacent to a stable S pixel.
    """
    
    output_grid = [row[:] for row in input_grid] # Deep copy
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # 1. Identify the three primary colors
    background_color, subject_color, reactant_color = identify_colors(input_grid)

    # Handle edge cases where colors couldn't be identified properly
    if subject_color == -1: # No subject color found
        return output_grid # Return copy of input as no transformation applies

    changes_to_R = set()
    changes_to_B = set()
    
    # Define cardinal directions
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # 3. First Pass: Identify Subject pixels changing to Reactant color
    # Skip this pass if no reactant color identified
    if reactant_color != -1:
        for r in range(height):
            for c in range(width):
                if input_grid[r][c] == subject_color:
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < height and 0 <= nc < width:
                            if input_grid[nr][nc] == reactant_color:
                                changes_to_R.add((r, c))
                                break # Found an R neighbor, mark for change and stop checking neighbors for this pixel

    # 4. Second Pass: Identify Subject pixels changing to Background color
    for r in range(height):
        for c in range(width):
            # Consider only Subject pixels that are NOT already changing to R
            if input_grid[r][c] == subject_color and (r, c) not in changes_to_R:
                has_B_neighbor = False
                has_protecting_S_neighbor = False
                
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width:
                        neighbor_color = input_grid[nr][nc]
                        # Check for Background neighbor
                        if neighbor_color == background_color:
                            has_B_neighbor = True
                        # Check for stable Subject neighbor
                        elif neighbor_color == subject_color and (nr, nc) not in changes_to_R:
                            has_protecting_S_neighbor = True
                            
                # Apply the rule: Change to B if adjacent to B AND NOT protected by a stable S
                if has_B_neighbor and not has_protecting_S_neighbor:
                    changes_to_B.add((r, c))

    # 5. Modify the output grid based on the collected changes
    for r, c in changes_to_R:
        output_grid[r][c] = reactant_color
        
    for r, c in changes_to_B:
        output_grid[r][c] = background_color

    # 6. Return the final output grid
    return output_grid
```
