
Previous Code:
```python
import numpy as np
from collections import Counter

"""
Transformation Rule:

1. Identify the most frequent color in the input grid ("passive color").
2. Identify all other colors present as "active colors".
3. Determine the "target color" (T) as the active color with the highest numerical value.
4. Identify the two "source colors" from the remaining active colors: Source A (lower value) and Source B (higher value).
5. Create an output grid, initially a copy of the input grid.
6. For each pixel in the input grid that has the target color T:
    a. Calculate the minimum Manhattan distance from this pixel to any pixel with color Source A (`dist_A`).
    b. Calculate the minimum Manhattan distance from this pixel to any pixel with color Source B (`dist_B`).
    c. If `dist_B` is less than or equal to `dist_A`, change the pixel's color in the output grid to Source B.
    d. Otherwise (if `dist_A` is strictly less than `dist_B`), change the pixel's color in the output grid to Source A.
7. Pixels that did not have the target color T remain unchanged in the output grid.
8. Return the modified output grid.
"""

def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_min_distance_to_color(target_pos, source_coords):
    """Finds the minimum Manhattan distance from target_pos to any coordinate in source_coords."""
    if not source_coords:
        return float('inf')
    min_dist = float('inf')
    for src_pos in source_coords:
        dist = manhattan_distance(target_pos, src_pos)
        if dist < min_dist:
            min_dist = dist
    return min_dist

def transform(input_grid):
    """Applies the transformation rule based on proximity to source colors."""
    
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Find unique colors and their frequencies
    unique_colors, counts = np.unique(input_grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    # Handle edge case: grid with only one color
    if len(unique_colors) <= 1:
        return output_grid

    # 2. Determine the passive color (most frequent)
    passive_color = max(color_counts, key=color_counts.get)
    
    # Check if there's a tie for most frequent, if so, maybe the rule needs refinement.
    # For now, assume a unique most frequent color as per examples.
    max_freq = color_counts[passive_color]
    tied_most_frequent = [c for c, freq in color_counts.items() if freq == max_freq]
    if len(tied_most_frequent) > 1:
        # If there's a tie, current logic might be insufficient.
        # Let's stick to the simple max for now based on observed examples.
        # If needed, a tie-breaking rule (e.g., lowest/highest color index) could be added.
        pass 

    # 3. Identify active colors
    active_colors = sorted([color for color in unique_colors if color != passive_color])

    # Check if the number of active colors matches the expected pattern (3 colors: T, A, B)
    if len(active_colors) < 2:
         # Not enough active colors to define T, A, and B. Return copy.
         # Or perhaps only T changes to a default if A/B missing?
         # Based on examples, assume at least T, A, B exist.
         return output_grid 
    if len(active_colors) == 2:
        # Only T and one source? Rule might simplify.
        # Assume 3 active colors for now.
        pass # Let's assume this case won't happen based on examples or requires different logic

    # 4. Determine Target (T) and Sources (A, B)
    # Assuming exactly 3 active colors based on examples. If more, this needs adjustment.
    target_color_T = max(active_colors)
    source_colors = [c for c in active_colors if c != target_color_T]
    
    # Ensure there are exactly two source colors
    if len(source_colors) != 2:
        # This case deviates from the observed pattern.
        # The logic below assumes exactly two sources, A and B.
        # If this happens, the assumption is wrong.
        # Maybe T is not max? Or A/B chosen differently?
        # For now, proceed assuming 2 sources. If errors occur, revisit this.
        print(f"Warning: Expected 2 source colors, found {len(source_colors)}. Proceeding with assumption...")
        if not source_colors: return output_grid # Cannot proceed without sources
        # If only one source, what happens? Let's default A and B?
        # This requires more definition. Sticking to 2 sources.
        # If more than 2, how to pick A and B? Min/max?
        # Let's stick to min/max of the sources found.
        color_A = min(source_colors)
        color_B = max(source_colors)
        
    else:
        color_A = min(source_colors)
        color_B = max(source_colors)

    # 5. Find coordinates of source color pixels
    coords_A = list(zip(*np.where(input_grid == color_A)))
    coords_B = list(zip(*np.where(input_grid == color_B)))

    # 6. Iterate through grid and apply transformation
    for r in range(height):
        for c in range(width):
            # 7. Check if current pixel is the target color
            if input_grid[r, c] == target_color_T:
                current_pos = (r, c)
                
                # a. Calculate min distance to color A
                min_dist_A = find_min_distance_to_color(current_pos, coords_A)
                
                # b. Calculate min distance to color B
                min_dist_B = find_min_distance_to_color(current_pos, coords_B)

                # c. & d. Apply transformation rule based on distances
                if min_dist_B <= min_dist_A:
                    output_grid[r, c] = color_B
                else: # min_dist_A < min_dist_B
                    output_grid[r, c] = color_A
            # Pixels that are not T remain unchanged (already handled by copy)

    # 8. Return the final grid
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
3 4 3 4 8 9 9 9 9 9 9 8 4 4 4 4
4 3 4 3 8 9 9 9 9 9 9 8 4 4 3 4
3 3 3 4 8 8 8 9 9 9 9 8 3 3 4 4
3 4 3 3 8 9 8 9 9 9 9 8 8 8 8 8
8 8 8 8 8 9 8 9 9 9 9 9 8 9 9 9
9 8 9 9 9 9 8 9 9 9 9 9 8 9 9 9
9 8 9 9 9 8 8 8 8 8 8 8 8 9 9 9
9 8 8 8 8 8 8 8 9 9 9 9 9 9 9 9
9 9 9 9 9 8 8 8 8 8 8 8 8 8 8 9
9 9 9 9 9 9 8 9 9 9 9 9 9 9 8 9
9 9 9 9 9 9 8 9 9 9 9 9 9 9 8 9
9 9 9 9 9 9 8 9 9 9 9 9 9 9 8 9
9 9 9 9 9 9 8 9 9 9 9 9 9 9 8 9
9 9 9 9 9 8 8 8 8 9 9 9 9 8 8 8
9 9 9 9 9 8 4 4 8 9 9 9 9 8 3 4
9 9 9 9 9 8 4 3 8 9 9 9 9 8 4 4
```
Expected Output:
```
3 4 3 4 3 9 9 9 9 9 9 4 4 4 4 4
4 3 4 3 3 9 9 9 9 9 9 4 4 4 3 4
3 3 3 4 3 3 3 9 9 9 9 4 3 3 4 4
3 4 3 3 3 9 3 9 9 9 9 4 4 4 4 4
3 3 3 3 3 9 3 9 9 9 9 9 4 9 9 9
9 3 9 9 9 9 3 9 9 9 9 9 4 9 9 9
9 3 9 9 9 8 8 8 4 4 4 4 4 9 9 9
9 3 3 3 3 8 4 8 9 9 9 9 9 9 9 9
9 9 9 9 9 8 8 8 4 4 4 4 4 4 4 9
9 9 9 9 9 9 4 9 9 9 9 9 9 9 4 9
9 9 9 9 9 9 4 9 9 9 9 9 9 9 4 9
9 9 9 9 9 9 4 9 9 9 9 9 9 9 4 9
9 9 9 9 9 9 4 9 9 9 9 9 9 9 4 9
9 9 9 9 9 4 4 4 4 9 9 9 9 4 4 4
9 9 9 9 9 4 4 4 4 9 9 9 9 4 3 4
9 9 9 9 9 4 4 3 4 9 9 9 9 4 4 4
```
Transformed Output:
```
3 4 3 4 4 9 9 9 9 9 9 4 4 4 4 4
4 3 4 3 3 9 9 9 9 9 9 4 4 4 3 4
3 3 3 4 4 4 4 9 9 9 9 3 3 3 4 4
3 4 3 3 3 9 3 9 9 9 9 3 3 3 4 4
3 4 3 3 3 9 3 9 9 9 9 9 3 9 9 9
9 4 9 9 9 9 3 9 9 9 9 9 3 9 9 9
9 4 9 9 9 3 3 3 3 3 3 3 3 9 9 9
9 4 3 3 3 3 4 4 9 9 9 9 9 9 9 9
9 9 9 9 9 4 4 4 4 4 3 3 3 3 4 9
9 9 9 9 9 9 4 9 9 9 9 9 9 9 3 9
9 9 9 9 9 9 4 9 9 9 9 9 9 9 3 9
9 9 9 9 9 9 4 9 9 9 9 9 9 9 3 9
9 9 9 9 9 9 4 9 9 9 9 9 9 9 3 9
9 9 9 9 9 4 4 4 4 9 9 9 9 3 3 4
9 9 9 9 9 4 4 4 4 9 9 9 9 3 3 4
9 9 9 9 9 4 4 3 3 9 9 9 9 4 4 4
```
Match: False
Pixels Off: 39
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 30.46875

## Example 2:
Input:
```
0 0 0 0 0 0 0 5 2 2
0 0 0 0 5 5 5 5 2 1
0 0 0 0 5 0 0 5 5 5
0 0 0 5 5 5 0 0 0 0
0 5 5 5 5 5 5 5 5 0
0 5 0 5 5 5 0 0 5 0
0 5 0 0 0 0 0 0 5 0
5 5 5 5 0 0 0 5 5 5
2 1 1 5 0 0 0 5 2 2
1 2 1 5 0 0 0 5 1 2
```
Expected Output:
```
0 0 0 0 0 0 0 2 2 2
0 0 0 0 2 2 2 2 2 1
0 0 0 0 2 0 0 2 2 2
0 0 0 5 5 5 0 0 0 0
0 1 1 5 2 5 2 2 2 0
0 1 0 5 5 5 0 0 2 0
0 1 0 0 0 0 0 0 2 0
1 1 1 1 0 0 0 2 2 2
2 1 1 1 0 0 0 2 2 2
1 2 1 1 0 0 0 2 1 2
```
Transformed Output:
```
0 0 0 0 0 0 0 2 2 2
0 0 0 0 2 2 2 2 2 1
0 0 0 0 2 0 0 2 2 1
0 0 0 1 2 2 0 0 0 0
0 1 1 1 1 2 2 2 2 0
0 1 0 1 1 2 0 0 2 0
0 1 0 0 0 0 0 0 2 0
2 1 1 1 0 0 0 2 2 2
2 1 1 1 0 0 0 2 2 2
1 2 1 1 0 0 0 1 1 2
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.0

## Example 3:
Input:
```
6 6 6 6 6 7 8 8 8 8 7 5 6 5 7 8 8 8 8 8
6 6 5 6 6 7 8 8 8 8 7 6 5 5 7 8 8 8 8 8
5 6 6 6 6 7 7 7 8 8 7 7 7 7 7 8 8 8 8 8
6 6 6 6 6 7 8 7 8 8 8 7 8 8 8 8 8 8 8 8
6 6 6 6 6 7 8 7 7 8 8 7 8 8 8 8 8 8 8 8
7 7 7 7 7 7 8 8 7 8 7 7 8 8 8 8 8 7 7 7
8 8 8 7 8 8 8 8 7 8 7 8 8 8 8 8 8 7 5 6
8 8 8 7 8 8 8 8 7 8 7 8 8 7 7 7 7 7 5 5
8 8 8 7 7 7 7 7 7 7 7 7 7 7 8 8 8 7 5 6
8 8 8 8 8 8 8 8 7 7 7 8 8 8 8 8 8 7 6 5
8 8 8 7 7 7 7 7 7 7 7 8 8 8 8 8 8 7 7 7
8 8 8 7 8 8 8 8 7 8 7 8 8 8 8 8 8 8 8 8
8 8 8 7 8 8 8 8 7 8 7 8 8 8 8 8 8 8 8 8
7 7 7 7 7 7 7 8 7 8 7 8 8 8 8 8 8 8 8 8
6 5 6 6 6 6 7 7 7 8 7 8 8 8 8 8 8 8 8 8
6 6 6 6 6 6 7 8 8 8 7 8 8 8 8 8 8 8 8 8
6 6 6 6 6 6 7 8 8 8 7 8 8 8 8 8 8 8 8 8
6 6 6 6 6 5 7 8 8 7 7 7 7 7 7 7 8 8 8 8
6 5 6 6 5 6 7 8 8 7 6 5 5 6 5 7 8 8 8 8
6 6 6 6 6 6 7 8 8 7 6 5 5 6 5 7 8 8 8 8
```
Expected Output:
```
6 6 6 6 6 6 8 8 8 8 5 5 6 5 5 8 8 8 8 8
6 6 5 6 6 6 8 8 8 8 5 6 5 5 5 8 8 8 8 8
5 6 6 6 6 6 6 6 8 8 5 5 5 5 5 8 8 8 8 8
6 6 6 6 6 6 8 6 8 8 8 5 8 8 8 8 8 8 8 8
6 6 6 6 6 6 8 6 6 8 8 5 8 8 8 8 8 8 8 8
6 6 6 6 6 6 8 8 6 8 5 5 8 8 8 8 8 5 5 5
8 8 8 6 8 8 8 8 6 8 5 8 8 8 8 8 8 5 5 6
8 8 8 6 8 8 8 8 6 8 5 8 8 5 5 5 5 5 5 5
8 8 8 6 6 6 6 6 7 7 7 5 5 5 8 8 8 5 5 6
8 8 8 8 8 8 8 8 7 6 7 8 8 8 8 8 8 5 6 5
8 8 8 6 6 6 6 6 7 7 7 8 8 8 8 8 8 5 5 5
8 8 8 6 8 8 8 8 6 8 5 8 8 8 8 8 8 8 8 8
8 8 8 6 8 8 8 8 6 8 5 8 8 8 8 8 8 8 8 8
6 6 6 6 6 6 6 8 6 8 5 8 8 8 8 8 8 8 8 8
6 5 6 6 6 6 6 6 6 8 5 8 8 8 8 8 8 8 8 8
6 6 6 6 6 6 6 8 8 8 5 8 8 8 8 8 8 8 8 8
6 6 6 6 6 6 6 8 8 8 5 8 8 8 8 8 8 8 8 8
6 6 6 6 6 5 6 8 8 5 5 5 5 5 5 5 8 8 8 8
6 5 6 6 5 6 6 8 8 5 6 5 5 6 5 5 8 8 8 8
6 6 6 6 6 6 6 8 8 5 6 5 5 6 5 5 8 8 8 8
```
Transformed Output:
```
6 6 6 6 6 6 8 8 8 8 5 5 6 5 5 8 8 8 8 8
6 6 5 6 6 6 8 8 8 8 6 6 5 5 5 8 8 8 8 8
5 6 6 6 6 6 6 6 8 8 6 6 5 5 5 8 8 8 8 8
6 6 6 6 6 6 8 6 8 8 8 6 8 8 8 8 8 8 8 8
6 6 6 6 6 6 8 6 6 8 8 6 8 8 8 8 8 8 8 8
6 6 6 6 6 6 8 8 6 8 6 6 8 8 8 8 8 5 5 6
8 8 8 6 8 8 8 8 6 8 6 8 8 8 8 8 8 5 5 6
8 8 8 6 8 8 8 8 6 8 6 8 8 5 5 5 5 5 5 5
8 8 8 6 6 6 6 6 6 6 6 6 5 5 8 8 8 5 5 6
8 8 8 8 8 8 8 8 6 6 6 8 8 8 8 8 8 6 6 5
8 8 8 6 6 6 6 6 6 6 6 8 8 8 8 8 8 6 6 5
8 8 8 6 8 8 8 8 6 8 6 8 8 8 8 8 8 8 8 8
8 8 8 6 8 8 8 8 6 8 6 8 8 8 8 8 8 8 8 8
6 5 6 6 6 6 6 8 6 8 6 8 8 8 8 8 8 8 8 8
6 5 6 6 6 6 6 6 6 8 6 8 8 8 8 8 8 8 8 8
6 6 6 6 6 6 6 8 8 8 6 8 8 8 8 8 8 8 8 8
6 6 6 6 6 6 6 8 8 8 6 8 8 8 8 8 8 8 8 8
6 6 6 6 6 5 5 8 8 6 6 5 5 6 5 5 8 8 8 8
6 5 6 6 5 6 6 8 8 6 6 5 5 6 5 5 8 8 8 8
6 6 6 6 6 6 6 8 8 6 6 5 5 6 5 5 8 8 8 8
```
Match: False
Pixels Off: 35
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 17.5
