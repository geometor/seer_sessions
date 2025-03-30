
Previous Code:
```python
import numpy as np

"""
Identify the main structure color (assumed to be the most frequent non-background color).
Identify the two pattern colors present in the input (either blue (1) and yellow (4), or green (3) and red (2)).
Iterate through each background (white, 0) pixel in the input grid.
If a background pixel is adjacent (including diagonals) to a pixel of the structure color:
  Calculate the sum of its row and column index (r + c).
  Determine the color based on the identified pattern and the parity of (r + c):
  - If the pattern colors are blue (1) and yellow (4):
    Change the pixel to blue (1) if (r + c) is even.
    Change the pixel to yellow (4) if (r + c) is odd.
  - If the pattern colors are green (3) and red (2):
    Change the pixel to red (2) if (r + c) is even.
    Change the pixel to green (3) if (r + c) is odd.
Leave all other pixels unchanged.
"""

def has_neighbor_color(grid, r, c, color):
    """
    Checks if cell (r, c) has any neighbor (including diagonals) 
    with the specified color.

    Args:
        grid (np.ndarray): The input grid.
        r (int): Row index of the cell.
        c (int): Column index of the cell.
        color (int): The color to check for in neighbors.

    Returns:
        bool: True if a neighbor with the specified color exists, False otherwise.
    """
    rows, cols = grid.shape
    # Iterate through the 3x3 neighborhood centered at (r, c)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue
            
            # Calculate neighbor coordinates
            nr, nc = r + dr, c + dc
            
            # Check if neighbor coordinates are within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor has the target color
                if grid[nr, nc] == color:
                    return True
    return False

def transform(input_grid):
    """
    Applies a checkerboard pattern fill to background pixels adjacent to a main structure.
    The specific pattern colors (blue/yellow or green/red) and their assignment based 
    on coordinate parity depend on the non-structure colors present in the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # --- Perception and Analysis ---

    # Find unique non-background (0) colors present in the grid
    unique_colors = np.unique(input_grid[input_grid != 0])

    # Handle edge cases: if only background or only one non-background color exists,
    # no transformation based on patterns is possible.
    if len(unique_colors) <= 1:
        # print("Edge case: No pattern colors found or only structure color exists.")
        return output_grid 

    # Identify the structure color - assumed to be the most frequent non-zero color
    counts = {color: np.sum(input_grid == color) for color in unique_colors}
    structure_color = max(counts, key=counts.get)
    # print(f"Identified structure color: {structure_color}")

    # Identify the pattern colors (non-structure, non-background)
    pattern_colors = {c for c in unique_colors if c != structure_color}
    # print(f"Identified potential pattern colors: {pattern_colors}")

    # Determine which pattern set to use (1/4 or 3/2) based on presence
    use_pattern_1_4 = 1 in pattern_colors or 4 in pattern_colors
    use_pattern_3_2 = 3 in pattern_colors or 2 in pattern_colors

    # If neither pattern set is indicated, return the original grid
    if not use_pattern_1_4 and not use_pattern_3_2:
         # print("No identifiable pattern color set (1/4 or 3/2) found.")
         return output_grid

    # --- Transformation ---
    
    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Focus on background pixels (color 0)
            if input_grid[r, c] == 0:
                # Check if this background pixel is adjacent to the structure color
                if has_neighbor_color(input_grid, r, c, structure_color):
                    # Calculate the parity of the coordinate sum (0 for even, 1 for odd)
                    parity = (r + c) % 2

                    # Apply the determined pattern based on parity
                    if use_pattern_1_4:
                       # Pattern blue(1)/yellow(4): Even sum -> blue(1), Odd sum -> yellow(4)
                       output_grid[r, c] = 1 if parity == 0 else 4
                    elif use_pattern_3_2:
                       # Pattern green(3)/red(2): Even sum -> red(2), Odd sum -> green(3)
                       output_grid[r, c] = 2 if parity == 0 else 3
                       
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 8 0 0 0 8 0 0 0 0 0 8
8 8 0 8 8 8 0 8 0 8 8 8 0 8
0 8 0 0 0 8 0 8 0 8 0 8 8 8
0 8 8 8 8 8 0 8 0 8 0 0 0 0
0 0 0 0 0 0 0 8 0 8 8 8 0 8
8 8 8 8 8 8 0 8 0 0 0 8 0 8
8 0 0 0 0 8 0 8 8 8 0 8 0 8
8 8 8 8 0 8 0 0 0 8 0 8 0 0
0 0 0 8 1 8 8 8 8 8 0 8 8 0
8 8 0 8 4 1 0 0 0 0 0 0 8 0
0 8 0 8 1 8 8 8 8 8 8 8 8 0
0 8 8 8 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 8 8 8 8 8 8 8
```
Expected Output:
```
0 0 0 8 0 0 0 8 1 4 1 4 1 8
8 8 0 8 8 8 0 8 4 8 8 8 4 8
0 8 0 0 0 8 0 8 1 8 0 8 8 8
0 8 8 8 8 8 0 8 4 8 0 0 0 0
0 0 0 0 0 0 0 8 1 8 8 8 0 8
8 8 8 8 8 8 0 8 4 1 4 8 0 8
8 4 1 4 1 8 0 8 8 8 1 8 0 8
8 8 8 8 4 8 0 0 0 8 4 8 0 0
0 0 0 8 1 8 8 8 8 8 1 8 8 0
8 8 0 8 4 1 4 1 4 1 4 1 8 0
1 8 0 8 1 8 8 8 8 8 8 8 8 0
4 8 8 8 4 8 0 0 0 0 0 0 0 0
1 4 1 4 1 8 0 8 8 8 8 8 8 8
```
Transformed Output:
```
1 4 1 8 1 4 1 8 1 4 1 4 1 8
8 8 4 8 8 8 4 8 4 8 8 8 4 8
1 8 1 4 1 8 1 8 1 8 1 8 8 8
4 8 8 8 8 8 4 8 4 8 4 1 4 1
1 4 1 4 1 4 1 8 1 8 8 8 1 8
8 8 8 8 8 8 4 8 4 1 4 8 4 8
8 4 1 4 1 8 1 8 8 8 1 8 1 8
8 8 8 8 4 8 4 1 4 8 4 8 4 1
1 4 1 8 1 8 8 8 8 8 1 8 8 4
8 8 4 8 4 1 4 1 4 1 4 1 8 1
1 8 1 8 1 8 8 8 8 8 8 8 8 4
4 8 8 8 4 8 4 1 4 1 4 1 4 1
1 4 1 4 1 8 1 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 54
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 59.34065934065933

## Example 2:
Input:
```
8 0 0 0 0 0 8 8 8 8 8 8 0 8 8 8 0 8 8 0 8 8 8 0
0 0 8 8 8 0 0 0 0 0 0 8 0 0 0 8 0 8 0 0 8 0 8 0
8 8 8 0 8 0 8 8 8 8 0 8 8 8 0 8 0 8 8 8 8 0 8 0
8 0 0 0 8 0 8 0 0 8 0 0 0 8 0 8 0 0 0 0 0 0 8 0
8 0 8 8 8 0 8 8 0 8 0 8 8 8 0 8 8 0 8 8 8 8 8 0
8 0 8 0 0 0 0 8 0 8 0 8 0 0 0 0 8 0 8 0 0 0 0 0
8 0 8 8 8 8 8 8 0 8 0 8 8 8 8 8 8 3 8 8 8 8 8 0
8 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 3 2 3 0 0 0 8 0
8 8 0 8 8 8 0 8 8 8 0 8 8 8 8 8 8 3 8 8 8 0 8 0
0 8 0 8 0 8 0 8 0 0 0 8 0 0 0 0 8 0 8 0 8 0 8 0
0 8 8 8 0 8 8 8 0 8 8 8 0 8 8 0 8 8 8 0 8 8 8 0
```
Expected Output:
```
8 3 2 3 2 3 8 8 8 8 8 8 0 8 8 8 2 8 8 0 8 8 8 0
3 2 8 8 8 2 3 2 3 2 3 8 0 0 0 8 3 8 0 0 8 2 8 0
8 8 8 0 8 3 8 8 8 8 2 8 8 8 0 8 2 8 8 8 8 3 8 0
8 0 0 0 8 2 8 0 0 8 3 2 3 8 0 8 3 2 3 2 3 2 8 0
8 0 8 8 8 3 8 8 0 8 2 8 8 8 0 8 8 3 8 8 8 8 8 0
8 0 8 2 3 2 3 8 0 8 3 8 0 0 0 0 8 2 8 0 0 0 0 0
8 0 8 8 8 8 8 8 0 8 2 8 8 8 8 8 8 3 8 8 8 8 8 0
8 0 0 0 0 0 0 0 0 8 3 2 3 2 3 2 3 2 3 2 3 2 8 0
8 8 0 8 8 8 0 8 8 8 2 8 8 8 8 8 8 3 8 8 8 3 8 0
0 8 0 8 0 8 0 8 3 2 3 8 0 0 0 0 8 2 8 0 8 2 8 0
0 8 8 8 0 8 8 8 2 8 8 8 0 8 8 0 8 8 8 0 8 8 8 0
```
Transformed Output:
```
8 3 2 3 2 3 8 8 8 8 8 8 2 8 8 8 2 8 8 3 8 8 8 3
3 2 8 8 8 2 3 2 3 2 3 8 3 2 3 8 3 8 3 2 8 2 8 2
8 8 8 3 8 3 8 8 8 8 2 8 8 8 2 8 2 8 8 8 8 3 8 3
8 2 3 2 8 2 8 2 3 8 3 2 3 8 3 8 3 2 3 2 3 2 8 2
8 3 8 8 8 3 8 8 2 8 2 8 8 8 2 8 8 3 8 8 8 8 8 3
8 2 8 2 3 2 3 8 3 8 3 8 3 2 3 2 8 2 8 2 3 2 3 2
8 3 8 8 8 8 8 8 2 8 2 8 8 8 8 8 8 3 8 8 8 8 8 3
8 2 3 2 3 2 3 2 3 8 3 2 3 2 3 2 3 2 3 2 3 2 8 2
8 8 2 8 8 8 2 8 8 8 2 8 8 8 8 8 8 3 8 8 8 3 8 3
3 8 3 8 3 8 3 8 3 2 3 8 3 2 3 2 8 2 8 2 8 2 8 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 3 8 8 8 3 8 8 8 3
```
Match: False
Pixels Off: 65
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 49.24242424242425
Example 2 Input:


*code_execution:*
```python
import numpy as np

grid = np.array([
    [8, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 8, 8, 8, 0, 8, 8, 0, 8, 8, 8, 0],
    [0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 8, 0, 0, 8, 0, 8, 0],
    [8, 8, 8, 0, 8, 0, 8, 8, 8, 8, 0, 8, 8, 8, 0, 8, 0, 8, 8, 8, 8, 0, 8, 0],
    [8, 0, 0, 0, 8, 0, 8, 0, 0, 8, 0, 0, 0, 8, 0, 8, 0, 0, 0, 0, 0, 0, 8, 0],
    [8, 0, 8, 8, 8, 0, 8, 8, 0, 8, 0, 8, 8, 8, 0, 8, 8, 0, 8, 8, 8, 8, 8, 0],
    [8, 0, 8, 0, 0, 0, 0, 8, 0, 8, 0, 8, 0, 0, 0, 0, 8, 0, 8, 0, 0, 0, 0, 0],
    [8, 0, 8, 8, 8, 8, 8, 8, 0, 8, 0, 8, 8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 3, 2, 3, 0, 0, 0, 8, 0],
    [8, 8, 0, 8, 8, 8, 0, 8, 8, 8, 0, 8, 8, 8, 8, 8, 8, 3, 8, 8, 8, 0, 8, 0],
    [0, 8, 0, 8, 0, 8, 0, 8, 0, 0, 0, 8, 0, 0, 0, 0, 8, 0, 8, 0, 8, 0, 8, 0],
    [0, 8, 8, 8, 0, 8, 8, 8, 0, 8, 8, 8, 0, 8, 8, 0, 8, 8, 8, 0, 8, 8, 8, 0]
])

unique_colors, counts = np.unique(grid[grid != 0], return_counts=True)
color_counts = dict(zip(unique_colors, counts))
structure_color = max(color_counts, key=color_counts.get)
pattern_colors = {c for c in unique_colors if c != structure_color}

print(f"Example 2 Input:")
print(f"  Unique non-background colors & counts: {color_counts}")
print(f"  Structure color (most frequent): {structure_color}")
print(f"  Pattern colors (seeds): {pattern_colors}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 2 Input:
  Unique non-background colors & counts: {np.int64(2): np.int64(1), np.int64(3): np.int64(4), np.int64(8): np.int64(137)}
  Structure color (most frequent): 8
  Pattern colors (seeds): {np.int64(2), np.int64(3)}

```
The metrics confirm the assumptions: Azure (8) is the structure color in both cases. The remaining non-background colors (1/4 in Ex1, 2/3 in Ex2) are the pattern/seed colors.

---

## General Assessment

The previous code correctly identified the structure color and the pattern colors (blue/yellow or red/green). It also correctly applied the checkerboard logic based on coordinate parity (r+c). However, it incorrectly applied the pattern to *all* background (white) pixels adjacent to the structure color.

The analysis of the expected outputs reveals that the checkerboard pattern should only be applied to a subset of these adjacent background pixels. Specifically, the filling seems to originate from the pre-existing pattern-colored pixels in the input grid and spreads outwards like a flood fill or region growing algorithm. The fill only affects background pixels that are adjacent (including diagonals) to both the structure color and a pixel that is already part of the pattern (either an initial seed pixel or a newly filled pixel).

The strategy is to modify the transformation logic to implement this flood-fill approach, starting from the identified seed pixels.

## Metrics

**Example 1:**

*   **Input Size:** 13x14
*   **Output Size:** 13x14
*   **Structure Color:** Azure (8) (Count: 89)
*   **Seed Colors:** Blue (1) (Count: 3), Yellow (4) (Count: 1)
*   **Background Color:** White (0)
*   **Checkerboard Pattern:** Blue (1) for even (r+c), Yellow (4) for odd (r+c).
*   **Pixels Off (Previous Code):** 54. The previous code overfilled the background areas.

**Example 2:**

*   **Input Size:** 11x24
*   **Output Size:** 11x24
*   **Structure Color:** Azure (8) (Count: 137)
*   **Seed Colors:** Red (2) (Count: 1), Green (3) (Count: 4)
*   **Background Color:** White (0)
*   **Checkerboard Pattern:** Red (2) for even (r+c), Green (3) for odd (r+c).
*   **Pixels Off (Previous Code):** 65. The previous code overfilled the background areas.

## Facts


```yaml
task_description: Fill specific background areas adjacent to a main structure with a checkerboard pattern, starting from existing 'seed' pixels of the pattern colors.

definitions:
  - object: grid
    description: A 2D array of pixels with colors 0-9.
  - object: structure
    description: The dominant object(s) in the grid, identified by the most frequent non-background color (Azure/8 in examples).
  - object: background
    description: Pixels with the background color (White/0).
  - object: pattern_colors
    description: Two specific colors that form a checkerboard pattern. Determined by the non-structure, non-background colors present in the input. Either Blue(1)/Yellow(4) or Red(2)/Green(3).
  - object: seed_pixels
    description: Pixels in the input grid that already have one of the pattern_colors. These act as starting points for the fill.
  - object: target_pixels
    description: Background (White/0) pixels that need to be filled.
  - property: adjacency
    description: Pixels are adjacent if they share a side or a corner (8-connectivity).
  - property: coordinate_parity
    description: The sum of the row (r) and column (c) index, specifically whether it's even or odd ((r+c) % 2).
  - property: pattern_type
    description: Determines which color corresponds to even or odd parity.
      - Type 1: Blue(1) for even, Yellow(4) for odd.
      - Type 2: Red(2) for even, Green(3) for odd.

actions:
  - action: identify_structure_color
    description: Find the most frequent color in the input grid, excluding the background color (White/0).
  - action: identify_pattern_colors_and_seeds
    description: Find all non-background, non-structure colors in the input grid. These define the pattern colors and their initial locations (seed_pixels). Determine the pattern_type (1/4 or 2/3) based on which colors are present.
  - action: perform_flood_fill
    description: Starting from the seed_pixels, iteratively fill adjacent background (White/0) pixels that are *also* adjacent to the structure_color.
    - input: seed_pixels, structure_color, background_color, pattern_type, input_grid
    - process:
        - Initialize a queue or set with the coordinates of all seed_pixels.
        - Initialize a set to keep track of visited/processed background coordinates to avoid infinite loops. Add seed coordinates to visited.
        - Create a copy of the input grid to modify.
        - While the queue/set of pixels to process is not empty:
            - Get a coordinate (r, c) from the queue/set.
            - Examine its 8 neighbors (nr, nc).
            - For each neighbor (nr, nc):
                - Check if it's within grid bounds.
                - Check if it's a background pixel (color 0) in the original input grid.
                - Check if it has NOT been visited/processed yet.
                - Check if it is adjacent (8-connectivity) to the structure_color in the original input grid.
                - If all conditions are met:
                    - Calculate parity = (nr + nc) % 2.
                    - Determine the fill_color based on parity and pattern_type.
                    - Update the copied grid at (nr, nc) with the fill_color.
                    - Add (nr, nc) to the queue/set to process its neighbors later.
                    - Mark (nr, nc) as visited/processed.
    - output: The modified grid with the filled pattern.
```


## Natural Language Program

1.  **Analyze Input:**
    *   Identify the background color (White/0).
    *   Find all unique non-background colors and their counts.
    *   Determine the `structure_color` (the most frequent non-background color).
    *   Identify the `pattern_colors` (any non-background, non-structure colors present). These are the `seed_pixels`.
    *   Determine the `pattern_type`: If Blue(1) or Yellow(4) are present, use Type 1 (Blue=even, Yellow=odd). If Red(2) or Green(3) are present, use Type 2 (Red=even, Green=odd). If neither pattern pair is indicated by the seeds, return the input grid unchanged.
2.  **Initialize Fill Process:**
    *   Create a copy of the input grid (`output_grid`).
    *   Initialize a queue (`process_queue`) with the coordinates (row, col) of all `seed_pixels`.
    *   Initialize a set (`visited_coords`) to store coordinates of background pixels that have been processed or added to the queue. Add the coordinates of the `seed_pixels` to `visited_coords`.
3.  **Flood Fill Execution:**
    *   While `process_queue` is not empty:
        *   Dequeue a coordinate `(r, c)`.
        *   Iterate through all 8 neighbors `(nr, nc)` of `(r, c)`.
        *   For each neighbor `(nr, nc)`:
            *   **Check Validity:** Ensure `(nr, nc)` is within the grid boundaries.
            *   **Check Target:** Verify that the pixel at `(nr, nc)` in the *original input grid* is a background pixel (White/0).
            *   **Check Visited:** Ensure `(nr, nc)` is not already in `visited_coords`.
            *   **Check Structure Adjacency:** Check if the neighbor `(nr, nc)` is adjacent (including diagonals) to at least one pixel with the `structure_color` in the *original input grid*.
            *   **Fill and Enqueue:** If all checks pass:
                *   Calculate the coordinate sum parity: `parity = (nr + nc) % 2`.
                *   Determine the `fill_color` based on `pattern_type` and `parity`.
                *   Set the pixel at `(nr, nc)` in the `output_grid` to the `fill_color`.
                *   Add `(nr, nc)` to `visited_coords`.
                *   Enqueue `(nr, nc)` into `process_queue`.
4.  **Return Output:** Return the modified `output_grid`.
