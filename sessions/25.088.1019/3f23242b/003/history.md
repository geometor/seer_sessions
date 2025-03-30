
Previous Code:
```python
import numpy as np

"""
Transforms the input grid by performing the following steps:
1. Creates an output grid of the same dimensions as the input grid, initialized with white pixels (0).
2. Finds the coordinates (row, column) of all green pixels (color 3) in the input grid.
3. For each found green pixel coordinate:
    a. Defines a fixed 5x10 pattern centered conceptually at the green pixel's location.
    b. Iterates through the relative coordinates and colors specified by the pattern.
    c. For each point in the pattern, calculates its absolute coordinates in the output grid based on the green pixel's location.
    d. Checks if the calculated absolute coordinates are within the bounds of the grid.
    e. If the coordinates are valid, places the pattern's specified color at that location in the output grid, overwriting any existing value.
4. Returns the final output grid.

The pattern details relative to the center green pixel (dr=0, dc=0):
- Row dr=-2: Gray (5) from dc=-2 to dc=+2
- Row dr=-1: Red (2) at dc=-2, Gray (5) at dc=0, Red (2) at dc=+2
- Row dr=0:  Red (2) at dc=-2, Green (3) at dc=0, Red (2) at dc=+2
- Row dr=+1: Red (2) at dc=-2, Red (2) at dc=+2
- Row dr=+2: Red (2) at dc=-4 and dc=-3, Azure (8) from dc=-2 to dc=+2, Red (2) at dc=+3, dc=+4, and dc=+5
"""


def transform(input_grid):
    """
    Applies a fixed pattern centered around each green pixel found in the input grid.

    Args:
        input_grid (list of lists of int): The input grid.

    Returns:
        list of lists of int: The transformed grid.
    """
    # Convert input grid to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output grid with white pixels (0)
    output_np = np.zeros_like(input_np)

    # Define the pattern as a dictionary: { (relative_row, relative_col): color }
    pattern_map = {
        # Row -2
        (-2, -2): 5, (-2, -1): 5, (-2, 0): 5, (-2, 1): 5, (-2, 2): 5,
        # Row -1
        (-1, -2): 2, (-1, 0): 5, (-1, 2): 2,
        # Row 0 (Center)
        (0, -2): 2, (0, 0): 3, (0, 2): 2,
        # Row +1
        (1, -2): 2, (1, 2): 2,
        # Row +2
        (2, -4): 2, (2, -3): 2, (2, -2): 8, (2, -1): 8, (2, 0): 8, (2, 1): 8, (2, 2): 8, (2, 3): 2, (2, 4): 2, (2, 5): 2,
    }

    # Find coordinates of all green pixels (color 3)
    green_pixels = np.argwhere(input_np == 3)

    # Iterate through each green pixel found
    for r_center, c_center in green_pixels:
        # Apply the pattern centered at this green pixel
        for (dr, dc), color in pattern_map.items():
            # Calculate target coordinates
            target_r = r_center + dr
            target_c = c_center + dc

            # Check if the target coordinates are within the grid boundaries
            if 0 <= target_r < height and 0 <= target_c < width:
                # Place the pattern pixel onto the output grid
                output_np[target_r, target_c] = color

    # Convert the output numpy array back to a list of lists
    output_grid = output_np.tolist()
    return output_grid

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0
0 0 2 0 5 0 2 0 0 0
0 0 2 0 3 0 2 0 0 0
0 0 2 0 0 0 2 0 0 0
2 2 8 8 8 8 8 2 2 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0
0 0 2 0 5 0 2 0 0 0
0 0 2 0 3 0 2 0 0 0
0 0 2 0 0 0 2 0 0 0
2 2 8 8 8 8 8 2 2 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 2 0 5 0 2 0 0
0 0 0 0 0 0 0 0 0 2 0 3 0 2 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 2 0 0
2 2 2 2 2 2 2 2 2 8 8 8 8 8 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 2 0 5 0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 3 0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0
2 8 8 8 8 8 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 2 0 5 0 2 0 0
0 0 0 0 0 0 0 0 0 2 0 3 0 2 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 2 0 0
0 0 0 0 0 0 0 2 2 8 8 8 8 8 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 2 0 5 0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 3 0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0
2 8 8 8 8 8 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.9375
Okay, the code execution reveals several things:

1.  **Prompt Error**: The `Expected Output` grid displayed *inline* within the prompt for Example 2 was **different** from the `Expected Output` text block below it (which I used for my analysis initially). The calculation `num_diff_prompt=14` confirms that the code output differs from the text block by 14 pixels, matching the prompt's report.
2.  **Actual Discrepancy**: The code output `Transformed` differs from the *inline* `Expected Output` (`expected_output_ex2` in the tool code) by 21 pixels.
3.  **Nature of Difference**:
    *   **Row 6**:
        *   Expected (inline): `[2, 2, 8, 8, 8, 8, 8, 2, 2, 2, 0, 0, 0, 0, 0, 0]`
        *   Transformed: `[0, 0, 0, 0, 0, 0, 0, 2, 2, 8, 8, 8, 8, 8, 2, 2]`
        *   The `Transformed` row IS the correct pattern row `dr=+2` relative to the green pixel at (4, 11). `r=4+2=6`. `c=11+(-4)=7` to `c=11+(+5)=16`. So cols 7-15.
        *   The `Expected (inline)` row IS the correct pattern row `dr=+2` relative to the green pixel at (10, 3). `r=10+2=12`. `c=3+(-3)=0` to `c=3+(+5)=8`. So cols 0-8. **Wait**, the expected row 6 is identical to the pattern's `dr=+2` row relative to the *second* green pixel (10, 3), not the first one (4, 11)? That seems very strange. Why would the pattern from (4, 11) produce the row expected from (10, 3)? This suggests the pattern placement isn't solely based on the green pixel location, or the pattern itself changes.
    *   **Row 12**:
        *   Expected (inline): `[2, 8, 8, 8, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]`
        *   Transformed: `[2, 8, 8, 8, 8, 8, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0]`
        *   The `Transformed` row IS the correct pattern row `dr=+2` relative to the green pixel at (10, 3), but clipped at the right edge (col 8). `r=10+2=12`. `c=3+(-3)=0` to `c=3+(+5)=8`. So cols 0-8.
        *   The `Expected (inline)` row IS the correct pattern row `dr=+2` relative to the green pixel at (4, 11), shifted down? `r=4+2=6`. `c=11+(-4)=7` to `c=11+(+5)=16`. This row `[2, 8, 8, 8, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]` doesn't match *any* simple placement of the pattern.

4.  **Revisiting the Prompt's "Expected Output" Text Block**: Let's assume the text block `expected_output_ex2_prompt` *was* the correct target, despite the inline grid differing.
    *   Row 6:
        *   Prompt Exp: `[2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 8, 8, 8, 8, 2, 2]`
        *   Transformed: `[0, 0, 0, 0, 0, 0, 0, 2, 2, 8, 8, 8, 8, 8, 2, 2]`
        *   Difference: The first 7 `2`s in the Prompt Expected are `0`s in Transformed. These correspond to columns 0-6. Are these influenced by the *other* pattern? Pattern 2 (center 10, 3) has its `dr=+2` row at row 12. It doesn't directly affect row 6. This `Prompt Exp` row 6 looks like a *combination* or modification.
    *   Row 12:
        *   Prompt Exp: `[2, 8, 8, 8, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]`
        *   Transformed: `[2, 8, 8, 8, 8, 8, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0]`
        *   Difference: The last 7 `2`s in the Prompt Expected (cols 9-15) are `0`s in Transformed. These correspond to columns 9-15. Are these influenced by Pattern 1 (center 4, 11)? Pattern 1 has its `dr=+2` row at row 6. It doesn't directly affect row 12. This `Prompt Exp` row 12 also looks like a combination/modification.

**Hypothesis based on `expected_output_ex2_prompt` (14 errors):**

It seems like when patterns overlap, or perhaps just always, the `dr=+2` row (the bottom row with Azure) gets modified.
*   For the pattern centered at (4, 11), its `dr=+2` row is Row 6. In `Prompt Exp`, Row 6 is `[2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 8, 8, 8, 8, 2, 2]`. Compared to the standard `[0,0,0,0,0,0,0, 2, 2, 8, 8, 8, 8, 8, 2, 2]`, the first 7 `0`s have become `2`s.
*   For the pattern centered at (10, 3), its `dr=+2` row is Row 12. In `Prompt Exp`, Row 12 is `[2, 8, 8, 8, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]`. Compared to the standard `[2, 8, 8, 8, 8, 8, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0]`, the last 7 `0`s have become `2`s.

It looks like the `dr=+2` row pattern: `2 2 8 8 8 8 8 2 2 2` (relative columns -4 to +5) is being **extended** with Red (2) pixels to fill the entire width of the grid *on that specific row*.

Let's test this hypothesis:
*   Grid width = 16.
*   Pattern 1 (center 4, 11), `dr=+2` -> Row 6. Standard pattern covers columns 7 to 15 (`c=11+dc`). If we extend with Red(2) to fill cols 0-15: `[2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 8, 8, 8, 8, 2, 2]` -> This matches `Prompt Exp` Row 6!
*   Pattern 2 (center 10, 3), `dr=+2` -> Row 12. Standard pattern covers columns 0 to 8 (`c=3+dc`). If we extend with Red(2) to fill cols 0-15: `[2, 8, 8, 8, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]` -> This matches `Prompt Exp` Row 12!

This looks like the correct rule. The overwrite logic still applies, but the pattern itself is slightly different for the `dr=+2` row; it extends horizontally with Red pixels.

**Revised Strategy**: Modify the pattern application logic. For the `dr=+2` row specifically, after placing the standard pattern elements (`2`s and `8`s from dc=-4 to +5), fill the rest of that row (within grid bounds) with Red (2), potentially overwriting background (0) but not overwriting parts of *other* patterns placed later. A simpler way might be to fill the entire row with Red(2) *first*, then draw the `2 8 8 8 8 8 2 2 2` part on top.

Let's refine the plan:
1.  **General Assessment**: The core logic of finding green pixels and placing a pattern is correct. The issue lies in the exact definition/application of the pattern's bottom row (`dr=+2`), which seems to extend horizontally with Red pixels across the grid width. The simple overwrite logic appears correct, assuming the pattern modification is applied correctly.
2.  **Gather Metrics**: Confirmed grid dimensions and green pixel locations. The key finding is the difference between the simple overlay output and the target output, specifically on rows `r_center + 2`.
3.  **YAML Facts**: Update the pattern description to include the extension rule for the `dr=+2` row.
4.  **Natural Language Program**: Clearly state the pattern placement rule, including the modification for the bottom row.Okay, let's refine our understanding based on the analysis.

**General Assessment**

The previous code correctly identified the green pixels and applied a fixed pattern centered on them. Example 1, with a single green pixel, was solved correctly. Example 2, with two green pixels, revealed an issue. The comparison between the `Transformed Output` and the `Expected Output` (specifically, the version shown in the text block, which resulted in 14 errors as reported) indicates that the patterns don't just simply overwrite each other based on a fixed, static pattern definition.

The analysis using `tool_code` suggests that the bottom row of the pattern (at relative row `dr=+2`) behaves differently. Instead of just placing the sequence `Red Red Azure Azure Azure Azure Azure Red Red Red` (from `dc=-4` to `dc=+5`), this row appears to be extended with Red (2) pixels across the entire width of the grid *on that specific row*, while still containing the original Azure segment. The simple overwrite mechanism then applies when multiple patterns affect the same row.

The strategy is to modify the pattern application step: for the specific case of the pattern's bottom row (`dr=+2`), first fill the entire row with Red (2), and then draw the standard `2 2 8 8 8 8 8 2 2 2` sequence over it at the correct relative columns.

**Gather Metrics**


*code_execution:*
```python
import numpy as np

# Example 1 Data
input_grid_ex1 = np.array([
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
])
expected_output_ex1 = np.array([
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,5,5,5,5,5,0,0,0],
    [0,0,2,0,5,0,2,0,0,0],
    [0,0,2,0,3,0,2,0,0,0],
    [0,0,2,0,0,0,2,0,0,0],
    [2,2,8,8,8,8,8,2,2,2],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
])

# Example 2 Data
input_grid_ex2 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0], # Green at (4, 11)
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0], # Green at (10, 3)
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
])
# Using the "Prompt Expected" version which aligns with the 14 errors reported
expected_output_ex2_prompt = np.array([
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,5,5,5,5,5,0,0],
 [0,0,0,0,0,0,0,0,0,2,0,5,0,2,0,0],
 [0,0,0,0,0,0,0,0,0,2,0,3,0,2,0,0],
 [0,0,0,0,0,0,0,0,0,2,0,0,0,2,0,0],
 [2,2,2,2,2,2,2,2,2,8,8,8,8,8,2,2], # Extended Red row
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0],
 [0,2,0,5,0,2,0,0,0,0,0,0,0,0,0,0],
 [0,2,0,3,0,2,0,0,0,0,0,0,0,0,0,0],
 [0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0],
 [2,8,8,8,8,8,2,2,2,2,2,2,2,2,2,2], # Extended Red row
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
])

def get_metrics(name, input_grid, output_grid):
    green_pixels = np.argwhere(input_grid == 3).tolist()
    return {
        "example": name,
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "green_pixels": green_pixels,
        "input_colors": sorted(list(np.unique(input_grid))),
        "output_colors": sorted(list(np.unique(output_grid))),
    }

metrics_ex1 = get_metrics("Example 1", input_grid_ex1, expected_output_ex1)
metrics_ex2 = get_metrics("Example 2", input_grid_ex2, expected_output_ex2_prompt)

print(metrics_ex1)
print(metrics_ex2)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
{'example': 'Example 1', 'input_shape': (10, 10), 'output_shape': (10, 10), 'green_pixels': [[4, 4]], 'input_colors': [np.int64(0), np.int64(3)], 'output_colors': [np.int64(0), np.int64(2), np.int64(3), np.int64(5), np.int64(8)]}
{'example': 'Example 2', 'input_shape': (16, 16), 'output_shape': (16, 16), 'green_pixels': [[4, 11], [10, 3]], 'input_colors': [np.int64(0), np.int64(3)], 'output_colors': [np.int64(0), np.int64(2), np.int64(3), np.int64(5), np.int64(8)]}

```
**YAML Facts**


```yaml
task_description: Place a specific pattern centered on each green pixel found in the input grid. Where patterns overlap, the later drawn pattern overwrites the earlier one. The bottom row of the pattern has a special extension rule.
grid_properties:
  background_color: 0 (white)
  output_size: Same as input size.
objects:
  - type: trigger_pixel
    color: 3 (green)
    description: The location of each green pixel determines the center for placing a pattern.
  - type: pattern
    description: A fixed 5-row high pattern placed relative to each green pixel.
    colors_used: [2 (red), 3 (green), 5 (gray), 8 (azure)]
    relative_definition: # (dr, dc): color; dr=row_offset, dc=col_offset from green pixel
      # Row dr = -2
      (-2, -2): 5
      (-2, -1): 5
      (-2, 0): 5
      (-2, 1): 5
      (-2, 2): 5
      # Row dr = -1
      (-1, -2): 2
      (-1, 0): 5
      (-1, 2): 2
      # Row dr = 0 (center)
      (0, -2): 2
      (0, 0): 3 # Overwrites the original green pixel
      (0, 2): 2
      # Row dr = +1
      (1, -2): 2
      (1, 2): 2
      # Row dr = +2 (Special Rule Row)
      (2, -4): 2
      (2, -3): 2
      (2, -2): 8
      (2, -1): 8
      (2, 0): 8
      (2, 1): 8
      (2, 2): 8
      (2, 3): 2
      (2, 4): 2
      (2, 5): 2
actions:
  - action: initialize_output
    target: output_grid
    value: Create a grid of the same dimensions as the input, filled with white (0).
  - action: find_triggers
    source: input_grid
    object_type: trigger_pixel
    color: 3 (green)
    result: List of coordinates [(r1, c1), (r2, c2), ...].
  - action: apply_pattern
    trigger: Each green pixel coordinate (r_center, c_center).
    target: output_grid
    pattern: Use the relative_definition above.
    special_rule:
      condition: When drawing the row corresponding to dr = +2 (absolute row r_center + 2).
      steps:
        1. Determine the target row index: `target_r = r_center + 2`.
        2. If `target_r` is within the grid height:
           a. Fill the entire `target_r` row of the output grid with Red (2).
           b. Apply the specific pattern elements for `dr=+2` (from `dc=-4` to `dc=+5`) by drawing the sequence `Red Red Azure Azure Azure Azure Azure Red Red Red` at the corresponding columns `c_center + dc`, overwriting the Red pixels placed in step 2a. Ensure column indices are within grid bounds.
    standard_rule:
      condition: For all other rows of the pattern (dr = -2, -1, 0, +1).
      steps:
        1. For each relative coordinate (dr, dc) and color in the pattern definition for that row:
           a. Calculate the absolute target coordinate (target_r, target_c) = (r_center + dr, c_center + dc).
           b. If the target coordinate is within the grid bounds, set the color at output_grid[target_r, target_c].
    overlap_rule: If multiple patterns write to the same pixel, the last write determines the final color. (The order of processing green pixels might matter if not handled carefully, though simple overwrite often makes the final state order-independent if the full pattern is applied for each center).
```


**Natural Language Program**

1.  Create a new output grid with the same dimensions as the input grid, filling it entirely with white pixels (color 0).
2.  Identify the row and column coordinates of every green pixel (color 3) in the input grid.
3.  For each identified green pixel coordinate (let's call it the 'center'):
    a.  Apply a specific 5-row pattern onto the output grid, conceptually centered at the green pixel's location.
    b.  **Pattern Application - Row by Row (relative to center):**
        i.  **Row -2:** Place gray pixels (5) at relative columns -2, -1, 0, 1, 2.
        ii. **Row -1:** Place red pixels (2) at relative columns -2 and +2, and a gray pixel (5) at relative column 0.
        iii. **Row 0:** Place red pixels (2) at relative columns -2 and +2, and a green pixel (3) at relative column 0 (overwriting the original trigger pixel position).
        iv. **Row +1:** Place red pixels (2) at relative columns -2 and +2.
        v.  **Row +2 (Special Rule):**
            1.  Determine the absolute row index in the output grid (`center_row + 2`).
            2.  Fill this entire row with red pixels (2), from the first column to the last column of the grid.
            3.  Then, specifically place the sequence: Red (2), Red (2), Azure (8), Azure (8), Azure (8), Azure (8), Azure (8), Red (2), Red (2), Red (2) at relative columns -4, -3, -2, -1, 0, 1, 2, 3, 4, 5 respectively, overwriting the red pixels placed in the previous step.
    c.  **Boundary Check:** When calculating the absolute coordinates for placing any pattern pixel, ensure the coordinates fall within the bounds of the output grid. Do not attempt to draw pixels outside the grid.
    d.  **Overlap Rule:** If multiple patterns are drawn (due to multiple green pixels), pixels from later patterns will overwrite pixels from earlier patterns if they fall on the same location.
4.  Return the modified output grid.
