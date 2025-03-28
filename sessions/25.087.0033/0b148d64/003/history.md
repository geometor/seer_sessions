
Previous Code:
```python
"""
Identify the horizontal separator band consisting entirely of white pixels (0) that spans the full width of the input grid. Extract the region of the grid located entirely below this separator band. The output grid is this extracted lower region.
"""

import numpy as np

def find_separator_end(grid):
    """
    Finds the index of the row immediately following the last row of the first 
    continuous horizontal separator band made entirely of white pixels (0).
    Returns -1 if no such separator is found or if it's at the very bottom.
    """
    grid_height = len(grid)
    grid_width = len(grid[0])
    
    first_separator_row = -1
    last_separator_row = -1

    # Find the first row that is all white
    for r in range(grid_height):
        if all(grid[r][c] == 0 for c in range(grid_width)):
            first_separator_row = r
            break # Found the start of the separator

    if first_separator_row == -1:
        return -1 # No separator found

    # Find the end of this continuous separator band
    last_separator_row = first_separator_row
    for r in range(first_separator_row + 1, grid_height):
        if all(grid[r][c] == 0 for c in range(grid_width)):
            last_separator_row = r
        else:
            break # End of the separator band

    # The lower region starts on the row after the last separator row
    start_of_lower_region = last_separator_row + 1

    # Check if the separator extends to the bottom or if there's nothing below it
    if start_of_lower_region >= grid_height:
        return -1 # Nothing below the separator

    return start_of_lower_region


def transform(input_grid):
    """
    Transforms the input grid by extracting the portion below the first
    horizontal all-white separator band.
    
    Args:
        input_grid (list of lists or numpy array): The input grid.
        
    Returns:
        numpy array: The extracted lower portion of the grid.
    """
    # Convert input to numpy array for easier slicing
    grid_np = np.array(input_grid, dtype=int)
    
    # Find the starting row index of the lower region
    start_row = find_separator_end(grid_np.tolist()) # Use list version for iteration convenience

    # Check if a valid lower region was found
    if start_row == -1:
        # Handle cases where no separator is found or nothing is below it
        # Based on examples, this shouldn't happen, but returning an empty grid or raising an error might be options.
        # For now, let's assume a valid structure based on examples and return the original if structure is unexpected.
        # A better approach might be needed if test cases violate this structure.
         print("Warning: Separator or lower region not found as expected.")
         # Returning an empty array might be safer depending on expected behavior for edge cases
         return np.array([[]], dtype=int) 

    # Extract the lower region
    # Slicing starts from start_row to the end of the array
    output_grid = grid_np[start_row:, :]

    return output_grid

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
2 0 2 2 2 2 0 0 0 0 2 0 2 2 2 2 0 0 2
2 2 2 2 0 2 2 0 0 0 0 2 2 2 2 2 0 0 0
0 0 2 2 0 2 0 0 0 0 2 2 2 0 2 2 2 2 2
2 0 2 0 2 2 0 0 0 0 0 2 2 2 2 2 2 0 0
0 2 0 2 2 2 2 0 0 0 0 0 0 2 2 0 2 2 2
2 2 2 0 2 0 2 0 0 0 2 0 2 2 2 2 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 0 0 2 0 0 0 0 3 3 3 3 3 0 3 3
0 2 2 0 0 2 2 0 0 0 3 3 3 0 0 0 3 3 0
0 2 2 0 0 2 0 0 0 0 3 3 3 0 3 0 3 0 0
2 2 2 0 0 2 2 0 0 0 3 3 0 0 0 3 3 3 3
2 0 0 2 2 2 0 0 0 0 3 0 0 0 3 0 3 0 3
2 0 2 0 0 0 2 0 0 0 0 3 3 0 3 3 3 0 3
0 2 2 0 2 2 0 0 0 0 0 3 3 0 0 3 0 3 0
```
Expected Output:
```
0 3 3 3 3 3 0 3 3
3 3 3 0 0 0 3 3 0
3 3 3 0 3 0 3 0 0
3 3 0 0 0 3 3 3 3
3 0 0 0 3 0 3 0 3
0 3 3 0 3 3 3 0 3
0 3 3 0 0 3 0 3 0
```
Transformed Output:
```
2 0 2 0 0 0 2 0 0 0 0 3 3 3 3 3 0 3 3
0 2 2 0 0 2 2 0 0 0 3 3 3 0 0 0 3 3 0
0 2 2 0 0 2 0 0 0 0 3 3 3 0 3 0 3 0 0
2 2 2 0 0 2 2 0 0 0 3 3 0 0 0 3 3 3 3
2 0 0 2 2 2 0 0 0 0 3 0 0 0 3 0 3 0 3
2 0 2 0 0 0 2 0 0 0 0 3 3 0 3 3 3 0 3
0 2 2 0 2 2 0 0 0 0 0 3 3 0 0 3 0 3 0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: False
Color Count Correct: False
Score: None

## Example 2:
Input:
```
8 8 8 8 8 0 8 8 8 8 0 0 0 0 8 8 8 8 0 8 8
8 0 0 8 0 8 0 8 8 8 0 0 0 0 8 8 8 0 0 0 8
8 8 8 0 0 0 8 8 8 8 0 0 0 0 8 8 0 8 8 8 8
8 8 0 8 8 8 8 0 8 8 0 0 0 0 8 8 0 0 0 8 8
8 8 8 8 0 8 8 0 8 8 0 0 0 0 8 8 8 0 8 8 8
0 0 0 8 8 0 8 0 0 8 0 0 0 0 8 0 0 0 8 0 0
8 8 8 8 0 0 8 0 8 0 0 0 0 0 8 8 8 0 8 8 8
8 0 0 8 0 0 8 8 0 8 0 0 0 0 8 0 8 8 8 8 8
8 8 8 8 8 8 0 8 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 2 0 0 0 0 8 8 0 8 8 0 8
2 0 2 2 2 0 0 2 2 2 0 0 0 0 8 8 8 8 0 8 0
0 2 2 2 2 2 2 0 2 0 0 0 0 0 8 8 8 0 0 0 8
2 2 2 2 0 2 2 2 2 2 0 0 0 0 8 8 0 8 8 8 0
2 2 2 2 2 2 0 2 0 0 0 0 0 0 8 8 8 8 8 0 0
2 2 2 2 2 0 2 0 2 2 0 0 0 0 8 0 8 0 8 8 8
2 2 0 2 2 0 0 0 0 0 0 0 0 0 8 8 0 8 0 0 8
0 2 2 0 0 2 2 0 0 2 0 0 0 0 8 0 0 0 8 8 0
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 8 8 0 0 8 8
2 0 2 2 0 2 2 2 2 2 0 0 0 0 8 8 8 0 8 8 8
```
Expected Output:
```
0 2 2 2 0 0 2 2 2 2
2 0 2 2 2 0 0 2 2 2
0 2 2 2 2 2 2 0 2 0
2 2 2 2 0 2 2 2 2 2
2 2 2 2 2 2 0 2 0 0
2 2 2 2 2 0 2 0 2 2
2 2 0 2 2 0 0 0 0 0
0 2 2 0 0 2 2 0 0 2
2 2 2 2 2 2 2 2 2 2
2 0 2 2 0 2 2 2 2 2
```
Transformed Output:
```
0 2 2 2 0 0 2 2 2 2 0 0 0 0 8 8 0 8 8 0 8
2 0 2 2 2 0 0 2 2 2 0 0 0 0 8 8 8 8 0 8 0
0 2 2 2 2 2 2 0 2 0 0 0 0 0 8 8 8 0 0 0 8
2 2 2 2 0 2 2 2 2 2 0 0 0 0 8 8 0 8 8 8 0
2 2 2 2 2 2 0 2 0 0 0 0 0 0 8 8 8 8 8 0 0
2 2 2 2 2 0 2 0 2 2 0 0 0 0 8 0 8 0 8 8 8
2 2 0 2 2 0 0 0 0 0 0 0 0 0 8 8 0 8 0 0 8
0 2 2 0 0 2 2 0 0 2 0 0 0 0 8 0 0 0 8 8 0
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 8 8 0 0 8 8
2 0 2 2 0 2 2 2 2 2 0 0 0 0 8 8 8 0 8 8 8
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: False
Color Count Correct: False
Score: None

## Example 3:
Input:
```
0 1 0 1 1 1 0 0 1 1 0 1 0 0 0 0 0
1 0 1 0 0 0 0 0 1 1 1 1 1 1 0 1 1
1 1 0 1 1 0 0 0 1 1 1 1 1 1 0 1 1
1 1 0 0 1 1 0 0 1 1 0 1 1 1 1 1 1
0 1 1 1 0 0 0 0 1 1 0 0 0 1 1 1 0
1 0 0 1 0 0 0 0 1 1 0 0 1 1 1 1 1
0 0 0 1 1 0 0 0 1 1 1 0 0 1 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 4 0 4 0 0 1 0 0 1 1 1 1 1 1
4 4 4 4 0 4 0 0 1 0 1 1 1 1 1 1 0
4 0 4 0 0 4 0 0 0 1 0 0 1 1 1 1 1
0 4 4 4 4 0 0 0 1 1 0 0 1 0 1 0 1
4 4 4 0 4 4 0 0 1 1 1 1 1 1 1 1 0
0 4 4 4 4 0 0 0 0 1 0 0 0 0 1 1 1
0 4 4 4 0 4 0 0 0 1 0 1 0 1 1 1 0
0 4 0 0 0 0 0 0 1 0 1 1 1 0 1 0 1
4 4 0 4 0 4 0 0 1 1 1 0 0 1 1 1 0
```
Expected Output:
```
4 0 0 4 0 4
4 4 4 4 0 4
4 0 4 0 0 4
0 4 4 4 4 0
4 4 4 0 4 4
0 4 4 4 4 0
0 4 4 4 0 4
0 4 0 0 0 0
4 4 0 4 0 4
```
Transformed Output:
```
4 0 0 4 0 4 0 0 1 0 0 1 1 1 1 1 1
4 4 4 4 0 4 0 0 1 0 1 1 1 1 1 1 0
4 0 4 0 0 4 0 0 0 1 0 0 1 1 1 1 1
0 4 4 4 4 0 0 0 1 1 0 0 1 0 1 0 1
4 4 4 0 4 4 0 0 1 1 1 1 1 1 1 1 0
0 4 4 4 4 0 0 0 0 1 0 0 0 0 1 1 1
0 4 4 4 0 4 0 0 0 1 0 1 0 1 1 1 0
0 4 0 0 0 0 0 0 1 0 1 1 1 0 1 0 1
4 4 0 4 0 4 0 0 1 1 1 0 0 1 1 1 0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: False
Color Count Correct: False
Score: None
*   **Analysis of Counts vs. Output:**
    *   Ex 1: Left=28, Right=36. Right has more non-white pixels. Output uses columns from the Right part (10-18). Matches.
    *   Ex 2: Left=60, Right=45. Left has more non-white pixels. Output uses columns from the Left part (0-9). Matches.
    *   Ex 3: Left=21, Right=44. Right has more non-white pixels. Output uses columns from the Left part (0-5). DOES NOT MATCH.

*   **Backtrack on Hypothesis 3.** The "more non-white pixels" rule doesn't work for Example 3.

*   **What else could determine Left vs Right?**
    *   Maybe compare the *area* (number of cells) of the Left vs Right parts?
        *   Ex 1: Left cols 0-6 (width 7). Right cols 10-18 (width 9). Right is wider. Output = Right.
        *   Ex 2: Left cols 0-9 (width 10). Right cols 14-20 (width 7). Left is wider. Output = Left.
        *   Ex 3: Left cols 0-5 (width 6). Right cols 8-16 (width 9). Right is wider. Output = Left. DOES NOT MATCH.

    *   Maybe compare the *colors* present?
        *   Ex 1: Upper Left (cols 0-6) has Red(2). Upper Right (cols 10-18) has Red(2). Tie. Output = Right.
        *   Ex 2: Upper Left (cols 0-9) has Azure(8). Upper Right (cols 14-20) has Azure(8). Tie. Output = Left.
        *   Ex 3: Upper Left (cols 0-5) has Blue(1). Upper Right (cols 8-16) has Blue(1). Tie. Output = Left.
        This doesn't seem deterministic.

    *   **Let's reconsider the vertical separator identification.** "Widest full-height vertical white band".
        *   Ex 1: Upper rows 0-5. Vertical white columns spanning rows 0-5: Col 1 (w=1), Cols 7-9 (w=3), Col 11 (w=1). Widest is 7-9.
        *   Ex 2: Upper rows 0-8. Vertical white columns spanning rows 0-8: Cols 10-13 (w=4). Widest is 10-13.
        *   Ex 3: Upper rows 0-6. Vertical white columns spanning rows 0-6: Cols 6-7 (w=2). Widest is 6-7.
        This identification seems consistent.

    *   **Revisit the decision logic (Left/Right):**
        *   Ex 1: Separator 7-9. Output Right (10-18).
        *   Ex 2: Separator 10-13. Output Left (0-9).
        *   Ex 3: Separator 6-7. Output Left (0-5).

    *   Is there some property of the *separator itself*? Or its position?
        *   Ex 1: Separator cols 7-9. Starts at col 7. Width 3.
        *   Ex 2: Separator cols 10-13. Starts at col 10. Width 4.
        *   Ex 3: Separator cols 6-7. Starts at col 6. Width 2.

    *   Is there a property of the *upper region as a whole*?
        *   Ex 1: Upper region width 19. Separator width 3.
        *   Ex 2: Upper region width 21. Separator width 4.
        *   Ex 3: Upper region width 17. Separator width 2.

    *   What if we compare the non-white counts *relative* to the area? Density?
        *   Ex 1: Left Area = 6*7 = 42. Left Count = 28. Density = 28/42 = 0.667. Right Area = 6*9 = 54. Right Count = 36. Density = 36/54 = 0.667. Densities are equal! Output = Right.
        *   Ex 2: Left Area = 9*10 = 90. Left Count = 60. Density = 60/90 = 0.667. Right Area = 9*7 = 63. Right Count = 45. Density = 45/63 = 0.714. Right Density is higher. Output = Left. DOES NOT MATCH (was based on count).
        *   Ex 3: Left Area = 7*6 = 42. Left Count = 21. Density = 21/42 = 0.5. Right Area = 7*9 = 63. Right Count = 44. Density = 44/63 = 0.698. Right Density is higher. Output = Left. MATCHES (unlike count).

    *   **Hypothesis 4 (Density):**
        1.  Find horizontal white separator -> Upper / Lower regions.
        2.  Find widest, leftmost, full-height vertical white separator in Upper -> `C_start`, `C_end`.
        3.  Define Left part (cols `0` to `C_start-1`) and Right part (cols `C_end+1` to `width-1`) in Upper region.
        4.  Calculate non-white pixel density for Left part (count/area) and Right part (count/area) in Upper region.
        5.  If Left density > Right density, select Left columns for output.
        6.  If Right density > Left density, select Right columns for output.
        7.  If densities are equal (like Ex 1), default to Right? Or maybe there's another tie-breaker?
            *   In Ex 1, densities were equal (0.667). Right part area (54) > Left part area (42). Output was Right.
            *   Let's refine step 7: If densities are equal, select the part with the larger area (width). If areas are also equal (unlikely unless grid width is odd and separator is single middle column), maybe default to Left or Right consistently? Let's assume default to Right for now based on Ex 1.
        8.  Extract the rows from the Lower region using the selected columns (Left or Right).

    *   **Test Hypothesis 4:**
        *   Ex 1: Densities equal (0.667). Right Area (54) > Left Area (42). Select Right columns (10-18). Output: Lower region rows, columns 10-18. **MATCH.**
        *   Ex 2: Right Density (0.714) > Left Density (0.667). Select Right columns (14-20). Output: Lower region rows, columns 14-20. **DOES NOT MATCH.** Expected output was Left columns (0-9).
        *   Ex 3: Right Density (0.698) > Left Density (0.5). Select Right columns (8-16). Output: Lower region rows, columns 8-16. **DOES NOT MATCH.** Expected output was Left columns (0-5).

*   **Hypothesis 4 is also wrong.** The density comparison seems backwards or incorrect. Let's revisit the counts and decisions:
    *   Ex 1: Left=28, Right=36. Right count higher. Output = Right.
    *   Ex 2: Left=60, Right=45. Left count higher. Output = Left.
    *   Ex 3: Left=21, Right=44. Right count higher. Output = Left. **This is the inconsistency.** Why choose Left when Right count is higher?

*   Maybe the comparison isn't between Left and Right counts directly. What if it relates to the *separator itself*?
    *   Ex 3: Separator cols 6-7. Left part cols 0-5. Right part cols 8-16. Output is Left. The separator is closer to the left edge (6 columns) than the right edge (17-8 = 9 columns). Does the output correspond to the side the separator is *closest* to?
    *   Ex 1: Separator cols 7-9. Left edge distance (7) < Right edge distance (19-10 = 9). Separator closer to Left. Output = Right. Doesn't match.
    *   Ex 2: Separator cols 10-13. Left edge distance (10) > Right edge distance (21-14 = 7). Separator closer to Right. Output = Left. Doesn't match.

*   **Let's look at the *content* of the lower region that gets selected.**
    *   Ex 1: Lower region cols 10-18 selected. Color Green(3).
    *   Ex 2: Lower region cols 0-9 selected. Color Red(2).
    *   Ex 3: Lower region cols 0-5 selected. Color Yellow(4).

*   **Compare with upper region content:**
    *   Ex 1: Upper Left has Red(2). Upper Right has Red(2). Lower Output (Right) has Green(3).
    *   Ex 2: Upper Left has Azure(8). Upper Right has Azure(8). Lower Output (Left) has Red(2).
    *   Ex 3: Upper Left has Blue(1). Upper Right has Blue(1). Lower Output (Left) has Yellow(4).

    This doesn't seem helpful. The colors below don't directly map to colors above.

*   **Final attempt: Revisit the simplest hypothesis that worked for 2/3 examples.**
    *   Hypothesis: Compare non-white counts in Upper Left vs Upper Right. Select the side with *more* non-white pixels.
        *   Ex 1: Right > Left -> Select Right. Matches.
        *   Ex 2: Left > Right -> Select Left. Matches.
        *   Ex 3: Right > Left -> Select Right. DOES NOT MATCH (Output is Left).

    *   What is special about Example 3?
        *   Input: 19x17
        *   Upper: 7x17, Blue(1)
        *   Separator: Rows 7-9 (3 rows)
        *   Lower: 9x17, Yellow(4) and Blue(1) mixed in cols 8-16
        *   Vertical Separator: Cols 6-7 (width 2)
        *   Upper Left (cols 0-5): 21 non-white. Upper Right (cols 8-16): 44 non-white.
        *   Output: Lower region, cols 0-5 (Left side).

    *   Why is Left chosen despite having fewer non-white pixels? Is there an *inversion* rule? Maybe if the dominant color in the upper region is Blue(1), the rule flips?
        *   Ex 1: Dominant upper color: Red(2). Rule: Higher count wins. Works.
        *   Ex 2: Dominant upper color: Azure(8). Rule: Higher count wins. Works.
        *   Ex 3: Dominant upper color: Blue(1). Rule: Lower count wins? Let's test. Left count (21) < Right count (44). Select Left. Works.

    *   **Hypothesis 5 (Color-based rule switch):**
        1.  Identify Horizontal Separator -> Upper/Lower regions.
        2.  Identify widest, leftmost, full-height Vertical White Separator in Upper -> `C_start`, `C_end`.
        3.  Define Upper Left (cols `0` to `C_start-1`) and Upper Right (cols `C_end+1` to `width-1`).
        4.  Count non-white pixels in Upper Left (`count_L`) and Upper Right (`count_R`).
        5.  Find the most frequent non-white color in the *entire* Upper region.
        6.  If the most frequent color is Blue (1): Select the side (Left or Right) with the *fewer* non-white pixels.
        7.  Otherwise (any other color): Select the side (Left or Right) with the *more* non-white pixels.
        8.  If counts are equal, use a tie-breaker. What is the tie-breaker?
            *   Ex 1: Red(2). Counts L=28, R=36. Select Right (more). Matches.
            *   Ex 2: Azure(8). Counts L=60, R=45. Select Left (more). Matches.
            *   Ex 3: Blue(1). Counts L=21, R=44. Rule flips: Select Left (fewer). Matches.
        9.  Need the tie-breaker rule. Let's assume if counts are equal, we select the side with the larger area (width), like we saw in Ex 1 density tie. If areas are also equal, default to Right? (Need to confirm this default).
        10. Extract the rows from the Lower region using the selected columns (Left or Right).

This hypothesis seems the most promising as it covers all examples.

**Refining Steps:**

*   **Finding Horizontal Separator:** Find the *first* row composed entirely of white pixels. Find the *last* consecutive row composed entirely of white pixels starting from the first one. Upper = rows above first white row. Lower = rows below last white row.
*   **Finding Vertical Separator:** In the Upper region, find all columns composed entirely of white pixels for the *full height* of the Upper region. Group consecutive columns into bands. Select the band with the maximum width. If tie in width, select the leftmost band.
*   **Finding Dominant Color:** In the Upper region, count occurrences of each non-white color. Find the color with the maximum count. (Need to handle ties if they occur, maybe lowest color index wins?).


*code_execution:*
```python
import numpy as np
from collections import Counter

# Example 1 Upper region (rows 0-5)
upper1 = np.array([
    [2, 0, 2, 2, 2, 2, 0, 0, 0, 0, 2, 0, 2, 2, 2, 2, 0, 0, 2],
    [2, 2, 2, 2, 0, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
    [0, 0, 2, 2, 0, 2, 0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2, 2, 2],
    [2, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0],
    [0, 2, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 2],
    [2, 2, 2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 2, 2, 2, 2, 0, 2, 0]
])
colors1 = upper1[upper1 != 0]
count1 = Counter(colors1)
print(f"Ex 1 Upper Colors: {count1.most_common()}")

# Example 2 Upper region (rows 0-8)
upper2 = np.array([
    [8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 0, 0, 0, 0, 8, 8, 8, 8, 0, 8, 8],
    [8, 0, 0, 8, 0, 8, 0, 8, 8, 8, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 8],
    [8, 8, 8, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0, 8, 8, 0, 8, 8, 8, 8],
    [8, 8, 0, 8, 8, 8, 8, 0, 8, 8, 0, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8],
    [8, 8, 8, 8, 0, 8, 8, 0, 8, 8, 0, 0, 0, 0, 8, 8, 8, 0, 8, 8, 8],
    [0, 0, 0, 8, 8, 0, 8, 0, 0, 8, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 0],
    [8, 8, 8, 8, 0, 0, 8, 0, 8, 0, 0, 0, 0, 0, 8, 8, 8, 0, 8, 8, 8],
    [8, 0, 0, 8, 0, 0, 8, 8, 0, 8, 0, 0, 0, 0, 8, 0, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 0, 8, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0]
])
colors2 = upper2[upper2 != 0]
count2 = Counter(colors2)
print(f"Ex 2 Upper Colors: {count2.most_common()}")

# Example 3 Upper region (rows 0-6)
upper3 = np.array([
    [0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1]
])
colors3 = upper3[upper3 != 0]
count3 = Counter(colors3)
print(f"Ex 3 Upper Colors: {count3.most_common()}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Ex 1 Upper Colors: [(np.int64(2), 64)]
Ex 2 Upper Colors: [(np.int64(8), 105)]
Ex 3 Upper Colors: [(np.int64(1), 65)]

```
The dominant colors are indeed Red(2), Azure(8), and Blue(1) respectively. Hypothesis 5 holds.

**Final Check on Tie-breaking (Counts Equal):**
We don't have an example where counts are equal. The density tie-breaker (larger area wins) was based on Ex 1 where densities were equal. Let's assume if counts are equal, the side with the larger area (width) wins. If areas are also equal, default to Right.


```yaml
facts:
  - setup: The input grid is divided into three main regions based on horizontal and vertical separators.
  - region_horizontal: A horizontal band composed entirely of white pixels (0) separates the grid into an Upper Region and a Lower Region.
    - identification: Find the first row index `r_start` where all pixels are white. Find the last consecutive row index `r_end` starting from `r_start` where all pixels are white.
    - upper_region: Consists of all rows above `r_start`.
    - lower_region: Consists of all rows below `r_end`.
  - region_vertical: A vertical band composed entirely of white pixels (0) within the Upper Region acts as a separator.
    - identification: Identify all columns in the Upper Region that consist entirely of white pixels for the full height of the Upper Region.
    - selection: Group consecutive white columns. Select the group (band) with the maximum width. If there is a tie in width, select the leftmost band. Let the columns of this band be `c_start` to `c_end`.
  - subregions: The vertical separator divides the Upper Region into an Upper Left subregion (columns `0` to `c_start - 1`) and an Upper Right subregion (columns `c_end + 1` to `width - 1`).
  - properties:
    - upper_left_count: Number of non-white pixels in the Upper Left subregion.
    - upper_right_count: Number of non-white pixels in the Upper Right subregion.
    - upper_dominant_color: The non-white color that appears most frequently in the entire Upper Region.
    - upper_left_width: Width of the Upper Left subregion (`c_start`).
    - upper_right_width: Width of the Upper Right subregion (`width - (c_end + 1)`).
  - action_selection: Determine which set of columns (Left or Right) to use for the output grid based on the Upper Region properties.
    - rule_standard: If the `upper_dominant_color` is NOT Blue (1), select the side (Left or Right) corresponding to the subregion with the higher non-white pixel count (`upper_left_count` vs `upper_right_count`).
    - rule_blue: If the `upper_dominant_color` IS Blue (1), select the side (Left or Right) corresponding to the subregion with the lower non-white pixel count.
    - tie_breaker_count: If the counts are equal, select the side with the larger width (`upper_left_width` vs `upper_right_width`).
    - tie_breaker_width: If the widths are also equal, select the Right side.
  - action_extraction: Create the output grid.
    - rows: Use all rows from the Lower Region.
    - columns: Use the columns selected in `action_selection` (either columns `0` to `c_start - 1` or columns `c_end + 1` to `width - 1`).
```


**Natural Language Program:**

1.  **Identify Regions:**
    a.  Locate the first continuous horizontal band composed entirely of white pixels that spans the full width of the input grid.
    b.  Define the area above this band as the "Upper Region" and the area below this band as the "Lower Region".
2.  **Find Vertical Separator:**
    a.  Within the Upper Region, identify all columns that consist entirely of white pixels from the top to the bottom of the Upper Region.
    b.  Group consecutive such columns to find vertical white bands.
    c.  Select the vertical white band that has the maximum width. If multiple bands share the maximum width, choose the leftmost one. Let the starting column index be `c_start` and the ending column index be `c_end`.
3.  **Analyze Upper Subregions:**
    a.  Define the "Upper Left" subregion as the portion of the Upper Region with columns from `0` to `c_start - 1`.
    b.  Define the "Upper Right" subregion as the portion of the Upper Region with columns from `c_end + 1` to the last column.
    c.  Count the number of non-white pixels in the Upper Left subregion (`count_L`) and the Upper Right subregion (`count_R`).
    d.  Determine the most frequent non-white color (`dominant_color`) present in the entire Upper Region.
4.  **Select Output Columns:**
    a.  **Blue Rule:** If `dominant_color` is Blue (1), compare `count_L` and `count_R`. Select the side (Left or Right) corresponding to the *smaller* count.
    b.  **Standard Rule:** If `dominant_color` is not Blue (1), compare `count_L` and `count_R`. Select the side (Left or Right) corresponding to the *larger* count.
    c.  **Tie-breaking:** If `count_L` equals `count_R`: Compare the widths of the Upper Left and Upper Right subregions. Select the side corresponding to the *wider* subregion. If the widths are also equal, select the Right side.
5.  **Construct Output:**
    a.  Create a new grid using all rows from the Lower Region.
    b.  Include only the columns corresponding to the side (Left or Right) selected in Step 4.

This program seems robust across the examples provided.## General Assessment

The initial code failed because it assumed the output was *everything* below a horizontal white separator. The examples show the output is a *specific sub-section* of the region below the separator. The key insight missed was that a *vertical* structure within the *upper* part of the grid determines *which columns* are extracted from the *lower* part. The failures highlight the need to analyze both upper and lower regions and their relationship, mediated by both horizontal and vertical separators.

The strategy is to refine the logic by:
1.  Precisely identifying the upper and lower regions based on the horizontal white separator.
2.  Identifying a key vertical white separator within the upper region.
3.  Analyzing the content of the upper region on either side of this vertical separator.
4.  Using properties derived from this analysis (pixel counts, dominant color) to decide whether to extract the left or right corresponding columns from the lower region.

## Metrics and Analysis

Let's gather metrics for each example based on the refined understanding.

**Helper Definitions:**
*   **Horizontal Separator:** First maximal continuous block of all-white rows.
*   **Upper Region:** Rows above the horizontal separator.
*   **Lower Region:** Rows below the horizontal separator.
*   **Vertical Separator:** Widest, leftmost, full-height band of white columns within the Upper Region.
*   **Upper Left/Right:** Subregions of the Upper Region to the left/right of the Vertical Separator.



*code_execution:*
```python
import numpy as np
from collections import Counter

def analyze_example(input_grid):
    grid = np.array(input_grid)
    height, width = grid.shape
    metrics = {}

    # 1. Find Horizontal Separator
    h_sep_start = -1
    h_sep_end = -1
    for r in range(height):
        if np.all(grid[r, :] == 0):
            if h_sep_start == -1:
                h_sep_start = r
            h_sep_end = r
        elif h_sep_start != -1:
            # Found the end of the first continuous separator
            break
    
    if h_sep_start == -1 or h_sep_end == height - 1:
        metrics['error'] = "Horizontal separator not found or no lower region."
        return metrics

    metrics['h_sep_rows'] = (h_sep_start, h_sep_end)
    upper_region = grid[:h_sep_start, :]
    lower_region = grid[h_sep_end + 1:, :]
    metrics['upper_shape'] = upper_region.shape
    metrics['lower_shape'] = lower_region.shape
    
    if upper_region.shape[0] == 0:
         metrics['error'] = "No upper region found."
         return metrics


    # 2. Find Vertical Separator in Upper Region
    upper_height, upper_width = upper_region.shape
    white_cols = []
    for c in range(upper_width):
        if np.all(upper_region[:, c] == 0):
            white_cols.append(c)

    if not white_cols:
        metrics['error'] = "No full-height white columns in upper region."
        return metrics

    bands = []
    if white_cols:
        current_band = [white_cols[0]]
        for i in range(1, len(white_cols)):
            if white_cols[i] == white_cols[i-1] + 1:
                current_band.append(white_cols[i])
            else:
                bands.append(current_band)
                current_band = [white_cols[i]]
        bands.append(current_band)

    best_band = max(bands, key=len) if bands else None
    
    # If tie in length, choose leftmost
    max_len = len(best_band)
    leftmost_best_band = best_band
    for band in bands:
        if len(band) == max_len:
            if band[0] < leftmost_best_band[0]:
                 leftmost_best_band = band

    if not leftmost_best_band:
         metrics['error'] = "Could not determine vertical separator band."
         return metrics
         
    v_sep_start = leftmost_best_band[0]
    v_sep_end = leftmost_best_band[-1]
    metrics['v_sep_cols'] = (v_sep_start, v_sep_end)
    metrics['v_sep_width'] = len(leftmost_best_band)

    # 3. Analyze Upper Subregions
    upper_left = upper_region[:, :v_sep_start]
    upper_right = upper_region[:, v_sep_end + 1:]
    
    metrics['upper_left_shape'] = upper_left.shape
    metrics['upper_right_shape'] = upper_right.shape

    count_L = np.count_nonzero(upper_left)
    count_R = np.count_nonzero(upper_right)
    metrics['upper_left_count'] = count_L
    metrics['upper_right_count'] = count_R

    upper_colors = upper_region[upper_region != 0]
    if upper_colors.size > 0:
        color_counts = Counter(upper_colors)
        dominant_color = color_counts.most_common(1)[0][0]
        metrics['upper_dominant_color'] = dominant_color
    else:
         metrics['upper_dominant_color'] = None # Handle case of all white upper region?

    # 4. Determine Selection based on Hypothesis 5
    selection = "N/A"
    if metrics['upper_dominant_color'] is not None:
        if metrics['upper_dominant_color'] == 1: # Blue Rule
            if count_L < count_R:
                selection = "Left"
            elif count_R < count_L:
                selection = "Right"
            else: # Tie break counts
                 if upper_left.shape[1] > upper_right.shape[1]:
                     selection = "Left"
                 elif upper_right.shape[1] > upper_left.shape[1]:
                      selection = "Right"
                 else: # Tie break widths
                      selection = "Right" # Default to Right
        else: # Standard Rule
            if count_L > count_R:
                selection = "Left"
            elif count_R > count_L:
                selection = "Right"
            else: # Tie break counts
                 if upper_left.shape[1] > upper_right.shape[1]:
                     selection = "Left"
                 elif upper_right.shape[1] > upper_left.shape[1]:
                      selection = "Right"
                 else: # Tie break widths
                      selection = "Right" # Default to Right
    metrics['predicted_selection'] = selection
    
    # 5. Determine Expected Selection based on Output Size/Position
    # This requires the expected output grid for comparison. Cannot do in this isolated function.
    # We'll infer it based on the Hypothesis 5 logic matching the previous manual analysis.
    if metrics.get('example_num') == 1: metrics['expected_selection'] = 'Right'
    if metrics.get('example_num') == 2: metrics['expected_selection'] = 'Left'
    if metrics.get('example_num') == 3: metrics['expected_selection'] = 'Left'


    return metrics

# --- Inputs ---
input1 = [
    [2, 0, 2, 2, 2, 2, 0, 0, 0, 0, 2, 0, 2, 2, 2, 2, 0, 0, 2], [2, 2, 2, 2, 0, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0], [0, 0, 2, 2, 0, 2, 0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2, 2, 2], [2, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0], [0, 2, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 2], [2, 2, 2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 2, 2, 2, 2, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 3, 3], [0, 2, 2, 0, 0, 2, 2, 0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 3, 0], [0, 2, 2, 0, 0, 2, 0, 0, 0, 0, 3, 3, 3, 0, 3, 0, 3, 0, 0], [2, 2, 2, 0, 0, 2, 2, 0, 0, 0, 3, 3, 0, 0, 0, 3, 3, 3, 3], [2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 3, 0, 3], [2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 3, 0, 3, 3, 3, 0, 3], [0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 3, 3, 0, 0, 3, 0, 3, 0]
]
input2 = [
    [8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 0, 0, 0, 0, 8, 8, 8, 8, 0, 8, 8], [8, 0, 0, 8, 0, 8, 0, 8, 8, 8, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 8], [8, 8, 8, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0, 8, 8, 0, 8, 8, 8, 8], [8, 8, 0, 8, 8, 8, 8, 0, 8, 8, 0, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8], [8, 8, 8, 8, 0, 8, 8, 0, 8, 8, 0, 0, 0, 0, 8, 8, 8, 0, 8, 8, 8], [0, 0, 0, 8, 8, 0, 8, 0, 0, 8, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 0], [8, 8, 8, 8, 0, 0, 8, 0, 8, 0, 0, 0, 0, 0, 8, 8, 8, 0, 8, 8, 8], [8, 0, 0, 8, 0, 0, 8, 8, 0, 8, 0, 0, 0, 0, 8, 0, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 0, 8, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 8, 8, 0, 8, 8, 0, 8], [2, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 8, 8, 8, 8, 0, 8, 0], [0, 2, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 8], [2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 8, 8, 0, 8, 8, 8, 0], [2, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0], [2, 2, 2, 2, 2, 0, 2, 0, 2, 2, 0, 0, 0, 0, 8, 0, 8, 0, 8, 8, 8], [2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 0, 8, 0, 0, 8], [0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 0, 0, 0, 0, 8, 0, 0, 0, 8, 8, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 8, 8, 0, 0, 8, 8], [2, 0, 2, 2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 8, 8, 8, 0, 8, 8, 8]
]
input3 = [
    [0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1], [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1], [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0], [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [4, 0, 0, 4, 0, 4, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1], [4, 4, 4, 4, 0, 4, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0], [4, 0, 4, 0, 0, 4, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1], [0, 4, 4, 4, 4, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1], [4, 4, 4, 0, 4, 4, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 4, 4, 4, 4, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1], [0, 4, 4, 4, 0, 4, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0], [0, 4, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1], [4, 4, 0, 4, 0, 4, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0]
]

metrics1 = analyze_example(input1)
metrics1['example_num'] = 1
metrics1['expected_selection'] = 'Right'

metrics2 = analyze_example(input2)
metrics2['example_num'] = 2
metrics2['expected_selection'] = 'Left'

metrics3 = analyze_example(input3)
metrics3['example_num'] = 3
metrics3['expected_selection'] = 'Left'


print(f"Example 1 Metrics:\n{metrics1}\n")
print(f"Example 2 Metrics:\n{metrics2}\n")
print(f"Example 3 Metrics:\n{metrics3}\n")

# Verify predicted vs expected
print(f"Ex 1 Match: {metrics1['predicted_selection'] == metrics1['expected_selection']}")
print(f"Ex 2 Match: {metrics2['predicted_selection'] == metrics2['expected_selection']}")
print(f"Ex 3 Match: {metrics3['predicted_selection'] == metrics3['expected_selection']}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 1 Metrics:
{'h_sep_rows': (6, 10), 'upper_shape': (6, 19), 'lower_shape': (7, 19), 'v_sep_cols': (7, 9), 'v_sep_width': 3, 'upper_left_shape': (6, 7), 'upper_right_shape': (6, 9), 'upper_left_count': 28, 'upper_right_count': 36, 'upper_dominant_color': np.int64(2), 'predicted_selection': 'Right', 'example_num': 1, 'expected_selection': 'Right'}

Example 2 Metrics:
{'h_sep_rows': (9, 10), 'upper_shape': (9, 21), 'lower_shape': (10, 21), 'v_sep_cols': (10, 13), 'v_sep_width': 4, 'upper_left_shape': (9, 10), 'upper_right_shape': (9, 7), 'upper_left_count': 60, 'upper_right_count': 45, 'upper_dominant_color': np.int64(8), 'predicted_selection': 'Left', 'example_num': 2, 'expected_selection': 'Left'}

Example 3 Metrics:
{'h_sep_rows': (7, 9), 'upper_shape': (7, 17), 'lower_shape': (9, 17), 'v_sep_cols': (6, 7), 'v_sep_width': 2, 'upper_left_shape': (7, 6), 'upper_right_shape': (7, 9), 'upper_left_count': 21, 'upper_right_count': 44, 'upper_dominant_color': np.int64(1), 'predicted_selection': 'Left', 'example_num': 3, 'expected_selection': 'Left'}

Ex 1 Match: True
Ex 2 Match: True
Ex 3 Match: True

```
The metrics confirm the analysis and Hypothesis 5 holds for all three examples.

## Facts (YAML)


```yaml
facts:
  - setup: The input grid is divided into three main regions based on horizontal and vertical separators.
  - region_horizontal: A horizontal band composed entirely of white pixels (0) separates the grid into an Upper Region and a Lower Region.
    - identification: Find the first row index `r_start` where all pixels are white. Find the last consecutive row index `r_end` starting from `r_start` where all pixels are white.
    - upper_region: Consists of all rows above `r_start`.
    - lower_region: Consists of all rows below `r_end`.
  - region_vertical: A vertical band composed entirely of white pixels (0) within the Upper Region acts as a separator.
    - identification: Identify all columns in the Upper Region that consist entirely of white pixels for the full height of the Upper Region.
    - selection: Group consecutive white columns into bands. Select the band with the maximum width. If there is a tie in width, select the leftmost band. Let the columns of this band be `c_start` to `c_end`.
  - subregions: The vertical separator divides the Upper Region into an Upper Left subregion (columns `0` to `c_start - 1`) and an Upper Right subregion (columns `c_end + 1` to `width - 1`).
  - properties:
    - upper_left_count: Number of non-white pixels in the Upper Left subregion.
    - upper_right_count: Number of non-white pixels in the Upper Right subregion.
    - upper_dominant_color: The non-white color that appears most frequently in the entire Upper Region. (Assumes a single dominant color exists).
    - upper_left_width: Width of the Upper Left subregion (`c_start`).
    - upper_right_width: Width of the Upper Right subregion (`width - (c_end + 1)`).
  - action_selection: Determine which set of columns (Left or Right) to use for the output grid based on the Upper Region properties.
    - rule_standard: If the `upper_dominant_color` is NOT Blue (1), select the side (Left or Right) corresponding to the subregion with the strictly higher non-white pixel count (`upper_left_count` vs `upper_right_count`).
    - rule_blue: If the `upper_dominant_color` IS Blue (1), select the side (Left or Right) corresponding to the subregion with the strictly lower non-white pixel count.
    - tie_breaker_count: If the counts are equal, select the side with the larger width (`upper_left_width` vs `upper_right_width`).
    - tie_breaker_width: If the widths are also equal (implying counts were also equal), select the Right side.
  - action_extraction: Create the output grid.
    - rows: Use all rows from the Lower Region.
    - columns: Use the columns corresponding to the selected side (either columns `0` to `c_start - 1` for Left, or columns `c_end + 1` to `width - 1` for Right).
```


## Natural Language Program

1.  **Identify Horizontal Split:** Find the first continuous horizontal band of all-white pixels spanning the grid width. Define the rows above this band as the 'Upper Region' and the rows below as the 'Lower Region'.
2.  **Identify Vertical Split:** In the Upper Region, find all vertical columns that are entirely white for the height of the Upper Region. Group adjacent white columns into bands. Select the band with the greatest width; if there's a tie for width, choose the leftmost band. Note the start (`c_start`) and end (`c_end`) column indices of this selected vertical white band.
3.  **Analyze Upper Sides:** Divide the Upper Region into a 'Left Side' (columns `0` to `c_start - 1`) and a 'Right Side' (columns `c_end + 1` to the end). Count the non-white pixels on the Left Side (`count_L`) and Right Side (`count_R`). Determine the most frequent non-white color (`dominant_color`) in the entire Upper Region.
4.  **Choose Output Columns:**
    *   If `dominant_color` is Blue (1), choose the side (Left or Right) with the *smaller* non-white count (`count_L` vs `count_R`).
    *   If `dominant_color` is *not* Blue (1), choose the side (Left or Right) with the *larger* non-white count.
    *   If the counts are equal, choose the side that is wider.
    *   If the counts *and* widths are equal, choose the Right side.
5.  **Extract Output:** Create the output grid by taking all rows from the Lower Region and only the columns corresponding to the side chosen in the previous step.
