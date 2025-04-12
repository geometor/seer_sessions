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