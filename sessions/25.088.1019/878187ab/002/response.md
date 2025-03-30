*   Input 2: Count non-orange pixels.

``` python
import numpy as np
input_grid_2 = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 4, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 4],
    [7, 7, 7, 7, 7, 7, 7, 7, 4, 5, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 4, 7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 4],
    [7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 4, 7, 7, 7, 7, 4, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
], dtype=int)
count2 = np.sum(input_grid_2 != 7)
print(f'{count2=}')
```
```
count2=np.int64(12)

```
Count vs Pattern Width:
*   15 non-background pixels -> Pattern width 10
*   12 non-background pixels -> Pattern width 7

Again, no simple relationship (like `count - 5`).

Let's re-examine the patterns themselves. They look like pixelated digits or characters.
Pattern 1 (5x10):

```
. . . . Y Y . . . .  (Could be '1' '0' ?)
. . . Y . . Y . . .
. . Y . . . . Y . .
. Y . . . . . . Y .
Y . . . . . . . . Y
```

Pattern 2 (5x7):

```
. . Y . Y . . (Could be '7' ?)
. . . Y . . .
. . Y . Y . .
. Y . . . Y .
Y . . . . . Y
```

(Using '.' for red/2 and 'Y' for yellow/4)

Could the pattern represent the *count* of non-background pixels?
*   Input 1 has 15 non-background pixels. Pattern 1 looks like "10"? No, maybe "15"?
    *   The '1' shape: column 0, row 4; col 1, row 3; col 2, row 2; col 3, row 1; col 4, row 0.
    *   The '5' shape: col 4, row 0; col 5, row 0; col 6, row 1; col 7, row 2; col 8, row 3; col 9, row 4.
    *   Let's map these coordinates to the pattern:
        *   1: (4,0), (3,1), (2,2), (1,3), (0,4) -> Pattern1[4,0]=Y, Pattern1[3,1]=Y, Pattern1[2,2]=Y, Pattern1[1,3]=Y, Pattern1[0,4]=Y. **MATCHES!**
        *   5: (0,4), (0,5), (1,6), (2,7), (3,8), (4,9) -> Pattern1[0,4]=Y, Pattern1[0,5]=Y, Pattern1[1,6]=Y, Pattern1[2,7]=Y, Pattern1[3,8]=Y, Pattern1[4,9]=Y. **MATCHES!**

*   Input 2 has 12 non-background pixels. Pattern 2 looks like "7"? No, maybe "12"?
    *   The '1' shape: col 0, row 4; col 1, row 3; col 2, row 2; col 3, row 1; col 4, row 0.
    *   The '2' shape: col 2, row 0; col 3, row 1; col 4, row 0; col 4, row 2; col 5, row 3; col 6, row 4. (Assuming a specific font/style).
    *   Let's map these coordinates to Pattern 2:
        *   1: (4,0), (3,1), (2,2), (1,3), (0,4) -> Pattern2[4,0]=Y, Pattern2[3,1]=Y, Pattern2[2,2]=Y, Pattern2[1,3]=Y, Pattern2[0,4]=Y. **MATCHES!** Wait, Pattern2[0,4] is red(2), not yellow(4). Let me check the pattern again.
        Pattern 2:
        
```
        . . Y . Y . .
        . . . Y . . .
        . . Y . Y . .
        . Y . . . Y .
        Y . . . . . Y
        ```

        Yellow pixels: (0,2), (0,4), (1,3), (2,2), (2,4), (3,1), (3,5), (4,0), (4,6).
        This doesn't cleanly map to "1" and "2" in the same way "1" and "5" mapped in Pattern 1.

Let's rethink the pattern generation. Maybe it's not digits representing the count.

What else changes between Input 1 and Input 2?
*   Input 1: 16x16. Non-background: 6, 8. Count: 15.
*   Input 2: 15x15. Non-background: 4, 5. Count: 12.

Is the *maximum* non-background color value important?
*   Input 1: max color = 8. Output pattern width = 10.
*   Input 2: max color = 5. Output pattern width = 7.

Relation: Max Color -> Pattern Width
*   8 -> 10
*   5 -> 7
Hypothesis: Pattern Width = Max Non-Background Color + 2?
Let's assume there was a third example:
*   Input 3: max color = 6. Pattern width = 6 + 2 = 8?
*   Input 4: max color = 4. Pattern width = 4 + 2 = 6?

This seems plausible. Now, how is the *content* of the pattern determined? It uses red(2) and yellow(4). The yellow(4) pixels seem to form *some* shape within the 5xW grid.

Look at the yellow pixels again:
Pattern 1 (5x10, max color 8):

```
. . . . Y Y . . . .
. . . Y . . Y . . .
. . Y . . . . Y . .
. Y . . . . . . Y .
Y . . . . . . . . Y
```

Pattern 2 (5x7, max color 5):

```
. . Y . Y . .
. . . Y . . .
. . Y . Y . .
. Y . . . Y .
Y . . . . . Y
```

The yellow pixels seem to form diagonal lines or 'X' shapes.

Consider the coordinates (row, col) of yellow pixels:
Pattern 1: (0,4), (0,5), (1,3), (1,6), (2,2), (2,7), (3,1), (3,8), (4,0), (4,9)
Pattern 2: (0,2), (0,4), (1,3), (2,2), (2,4), (3,1), (3,5), (4,0), (4,6)

Let's check the diagonal property: row + col = constant OR row - col = constant.
Pattern 1:
Sums: 4, 5, 4, 7, 4, 9, 4, 11, 4, 13
Diffs: -4, -5, -2, -5, 0, -5, 2, -5, 4, -5
There's a recurring sum of 4. Coordinates with sum 4: (0,4), (1,3), (2,2), (3,1), (4,0). This is the main anti-diagonal.
What about the other yellow pixels? (0,5), (1,6), (2,7), (3,8), (4,9). These also form an anti-diagonal (sum = 5, 7, 9, 11, 13). It looks like two anti-diagonals, offset.

Pattern 2:
Sums: 2, 4, 4, 4, 6, 4, 8, 4, 10
Diffs: -2, -4, -2, 0, -2, -2, -2, 4, -2
Recurring sum = 4: (0,4), (1,3), (2,2), (3,1), (4,0). This is the main anti-diagonal again.
Other yellow pixels: (0,2), (2,4), (3,5), (4,6). These don't form such a clean secondary line. (0,2 sum=2), (2,4 sum=6), (3,5 sum=8), (4,6 sum=10).

This isn't quite right either.

Let's go back to the simplest explanation: The code implements the logic correctly for Example 1, assuming a *fixed* pattern. The failure on Example 2 means the pattern is *not* fixed. How does it change?

The only differences between the runs are the input grid content and dimensions.
Input 1: 16x16, colors {6, 7, 8}
Input 2: 15x15, colors {4, 5, 7}

Output 1: 16x16, pattern 5x10
Output 2: 16x15, pattern 5x7

Maybe the pattern is related to the *set of unique non-background colors* present in the input?
Input 1: {6, 8} -> Pattern 1 (5x10)
Input 2: {4, 5} -> Pattern 2 (5x7)

If a hypothetical Input 3 had only {8}, what would the pattern be? If Input 4 had {4, 6, 8}? This isn't specified.

Let's reconsider the code structure: `PATTERN = np.array(...)`. This is hardcoded. The core error is assuming this pattern is constant.

How to *generate* the pattern based on the input?

Possibility: The task involves drawing something based on input properties.
Properties of Input 1: Width 16, Height 16, Non-bg colors {6, 8}, Count 15.
Properties of Input 2: Width 15, Height 15, Non-bg colors {4, 5}, Count 12.

Maybe the pattern itself is defined elsewhere, and we just select the correct one based on some input property?
If max(non-bg color) = 8, use Pattern_8 (which is 5x10).
If max(non-bg color) = 5, use Pattern_5 (which is 5x7).

Let's define these patterns based on the examples:
Pattern_8 (5x10):

```
[[2, 2, 2, 2, 4, 4, 2, 2, 2, 2],
 [2, 2, 2, 4, 2, 2, 4, 2, 2, 2],
 [2, 2, 4, 2, 2, 2, 2, 4, 2, 2],
 [2, 4, 2, 2, 2, 2, 2, 2, 4, 2],
 [4, 2, 2, 2, 2, 2, 2, 2, 2, 4]]
```

Pattern_5 (5x7):

```
[[2, 2, 4, 2, 4, 2, 2],
 [2, 2, 2, 4, 2, 2, 2],
 [2, 2, 4, 2, 4, 2, 2],
 [2, 4, 2, 2, 2, 4, 2],
 [4, 2, 2, 2, 2, 2, 4]]
```

Let's assume this selection logic is correct. We need to implement a way to:
1. Find the maximum non-background color in the input.
2. Select the corresponding pattern (Pattern_8, Pattern_5, etc. - we only know these two so far).
3. Place the selected pattern at (11, 0).

If the input contains *only* the background color (e.g., orange/7), what is the max non-background color? It's undefined or could be considered 0 or -1. In this case, no pattern should be placed. The `has_non_background_pixels` check handles this.

Revised Plan:
1.  Identify background color (7).
2.  Check if any non-background pixels exist.
3.  If yes:
    a. Find the maximum value among the non-background pixels.
    b. Define a mapping (dictionary) from the max value to the specific pattern grid (numpy array). We currently know `8 -> Pattern_8` and `5 -> Pattern_5`.
    c. Select the correct pattern based on the max value.
    d. Create the 16xW output grid filled with background color.
    e. Place the selected pattern starting at row 11, column 0.
4.  If no non-background pixels, create the 16xW output grid filled with background color.

This seems like the most consistent explanation given the two examples and the failure mode. The core mistake was assuming the pattern placed was constant. It varies based on the maximum non-background color present in the input.

Need to extract the shapes and unique colors to confirm.

``` python
import numpy as np

# Example 1
input_grid_1 = np.array([
    [7, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7], [7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7, 7], [7, 7, 7, 6, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 7], [7, 7, 7, 8, 7, 7, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 8, 7], [7, 7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 7]], dtype=int)
output_grid_1 = np.array([[7]*16]*11 + [[2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7], [2, 2, 2, 4, 2, 2, 4, 2, 2, 2, 7, 7, 7, 7, 7, 7], [2, 2, 4, 2, 2, 2, 2, 4, 2, 2, 7, 7, 7, 7, 7, 7], [2, 4, 2, 2, 2, 2, 2, 2, 4, 2, 7, 7, 7, 7, 7, 7], [4, 2, 2, 2, 2, 2, 2, 2, 2, 4, 7, 7, 7, 7, 7, 7]], dtype=int)

# Example 2
input_grid_2 = np.array([[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 4, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 4], [7, 7, 7, 7, 7, 7, 7, 7, 4, 5, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 4, 7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 4], [7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7], [7, 4, 7, 7, 7, 7, 4, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]], dtype=int)
output_grid_2 = np.array([[7]*15]*11 + [[2, 2, 4, 2, 4, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7], [2, 2, 2, 4, 2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7], [2, 2, 4, 2, 4, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7], [2, 4, 2, 2, 2, 4, 2, 7, 7, 7, 7, 7, 7, 7, 7], [4, 2, 2, 2, 2, 2, 4, 7, 7, 7, 7, 7, 7, 7, 7]], dtype=int)

# Metrics Function
def get_metrics(name, input_grid, output_grid):
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    background_color = 7 # Assumed
    non_background_mask = input_grid != background_color
    has_non_background = np.any(non_background_mask)
    non_background_colors = sorted(list(np.unique(input_grid[non_background_mask]))) if has_non_background else []
    max_non_background_color = max(non_background_colors) if has_non_background else None
    
    # Extract pattern if output differs from input size or has non-background in the expected area
    pattern = None
    pattern_shape = None
    if output_shape[0] == 16 and has_non_background:
        # Assuming pattern starts at (11, 0) and has height 5
        potential_pattern_area = output_grid[11:16, :] 
        # Find the actual width by seeing where non-background ends
        pattern_width = 0
        if np.any(potential_pattern_area != background_color):
             non_bg_cols = np.where(np.any(potential_pattern_area != background_color, axis=0))[0]
             if len(non_bg_cols) > 0:
                 pattern_width = non_bg_cols.max() + 1
                 pattern = potential_pattern_area[:5, :pattern_width] # Height assumed 5
                 pattern_shape = pattern.shape
        
    print(f"--- {name} ---")
    print(f"Input Shape: {input_shape}")
    print(f"Output Shape: {output_shape}")
    print(f"Background Color: {background_color}")
    print(f"Has Non-Background Pixels: {has_non_background}")
    print(f"Non-Background Colors: {non_background_colors}")
    print(f"Max Non-Background Color: {max_non_background_color}")
    print(f"Output Pattern Shape: {pattern_shape}")
    # print(f"Output Pattern:\n{pattern}") # Too verbose for report

# Run metrics
get_metrics("Example 1", input_grid_1, output_grid_1)
get_metrics("Example 2", input_grid_2, output_grid_2)

# Define the patterns explicitly from outputs
PATTERN_8 = output_grid_1[11:16, 0:10]
PATTERN_5 = output_grid_2[11:16, 0:7]

print("\n--- Patterns ---")
print(f"Pattern for Max Color 8 (Shape {PATTERN_8.shape}):\n{PATTERN_8}")
print(f"Pattern for Max Color 5 (Shape {PATTERN_5.shape}):\n{PATTERN_5}")

# Check consistency: Does Pattern_8 correspond to Max Color 8? Yes.
# Check consistency: Does Pattern_5 correspond to Max Color 5? Yes.

# What if input has no non-background? Need a hypothetical example.
input_grid_3 = np.full((10, 12), 7, dtype=int)
# Expected output based on hypothesis: 16x12 grid of 7s
output_grid_3 = np.full((16, 12), 7, dtype=int)
get_metrics("Example 3 (Hypothetical - All Background)", input_grid_3, output_grid_3)

print("\nDone.")
```
```
--- Example 1 ---
Input Shape: (16, 16)
Output Shape: (16, 16)
Background Color: 7
Has Non-Background Pixels: True
Non-Background Colors: [np.int64(6), np.int64(8)]
Max Non-Background Color: 8
Output Pattern Shape: (5, 10)
--- Example 2 ---
Input Shape: (15, 15)
Output Shape: (16, 15)
Background Color: 7
Has Non-Background Pixels: True
Non-Background Colors: [np.int64(4), np.int64(5)]
Max Non-Background Color: 5
Output Pattern Shape: (5, 7)

--- Patterns ---
Pattern for Max Color 8 (Shape (5, 10)):
[[2 2 2 2 4 4 2 2 2 2]
 [2 2 2 4 2 2 4 2 2 2]
 [2 2 4 2 2 2 2 4 2 2]
 [2 4 2 2 2 2 2 2 4 2]
 [4 2 2 2 2 2 2 2 2 4]]
Pattern for Max Color 5 (Shape (5, 7)):
[[2 2 4 2 4 2 2]
 [2 2 2 4 2 2 2]
 [2 2 4 2 4 2 2]
 [2 4 2 2 2 4 2]
 [4 2 2 2 2 2 4]]
--- Example 3 (Hypothetical - All Background) ---
Input Shape: (10, 12)
Output Shape: (16, 12)
Background Color: 7
Has Non-Background Pixels: False
Non-Background Colors: []
Max Non-Background Color: None
Output Pattern Shape: None

Done.

```
The metrics confirm the hypothesis: The pattern placed depends on the *maximum* non-background color found in the input grid.

Final check on the logic:
- Background is orange (7).
- Output height is 16, width matches input.
- If input is all orange, output is all orange (16xW).
- If input has non-orange pixels:
    - Find the maximum color value `C` among non-orange pixels.
    - Look up a pre-defined 5xW pattern associated with `C`. (We know patterns for C=5 and C=8).
    - Place this pattern at row 11, col 0 in the orange 16xW output grid.

This covers all observations.## General Assessment

The previous code successfully implemented the logic derived from Example 1: identify the background color, create a 16-row high output grid, and conditionally place a *fixed* pattern at row 11, column 0 if the input contained any non-background pixels.

However, testing against Example 2 revealed that the pattern placed in the output is *not* fixed. The code failed because it always inserted the same 5x10 pattern derived from Example 1, whereas Example 2 required a different 5x7 pattern.

The key insight is that the specific pattern (both its content and width) placed in the output depends on the properties of the non-background pixels present in the *input* grid.

## Strategy for Resolution

1.  **Analyze Differences:** Compare Input 1 and Input 2, focusing on properties that might influence the output pattern (dimensions, non-background colors present, count of non-background pixels, maximum non-background color value).
2.  **Analyze Patterns:** Compare the output patterns from Example 1 (5x10) and Example 2 (5x7).
3.  **Identify Correlation:** Determine which input property correlates with the change in the output pattern. The analysis suggests the *maximum value* of the non-background colors in the input dictates which pattern is used.
4.  **Define Pattern Mapping:** Store the known patterns (the 5x10 pattern for max color 8, the 5x7 pattern for max color 5).
5.  **Update Logic:** Modify the transformation process to:
    *   Find the maximum non-background color in the input.
    *   Select the appropriate pre-defined pattern based on this maximum color.
    *   Place the selected pattern in the output grid.
6.  **Handle Edge Case:** Ensure the logic correctly handles inputs containing only the background color (no pattern is placed).

## Metrics and Observations

Based on the analysis using `tool_code`:

| Feature                     | Example 1                     | Example 2                       | Example 3 (Hypothetical) |
| :-------------------------- | :---------------------------- | :------------------------------ | :----------------------- |
| Input Shape                 | (16, 16)                      | (15, 15)                        | (10, 12)                 |
| Output Shape                | (16, 16)                      | (16, 15)                        | (16, 12)                 |
| Background Color            | 7 (Orange)                    | 7 (Orange)                      | 7 (Orange)               |
| Has Non-Background Pixels | True                          | True                            | False                    |
| Non-Background Colors     | {6 (Magenta), 8 (Azure)}      | {4 (Yellow), 5 (Gray)}          | {}                       |
| Max Non-Background Color  | 8                             | 5                               | None                     |
| Output Pattern Shape        | (5, 10)                       | (5, 7)                          | None                     |
| Output Pattern Colors       | {2 (Red), 4 (Yellow)}         | {2 (Red), 4 (Yellow)}           | N/A                      |
| Output Pattern Position     | Top-Left at (11, 0)           | Top-Left at (11, 0)             | N/A                      |

**Key Observations:**

*   The background color is consistently orange (7).
*   The output grid height is fixed at 16, while the width matches the input width.
*   A pattern is placed in the output *only if* the input contains non-background pixels.
*   The pattern always has a height of 5 and starts at row 11, column 0.
*   The *width* and *content* of the pattern correlate strongly with the *maximum non-background color value* found in the input grid.
    *   Max Color 8 -> Use Pattern 1 (5x10)
    *   Max Color 5 -> Use Pattern 2 (5x7)
*   The patterns themselves consist only of red (2) and yellow (4) pixels, regardless of the original non-background colors in the input.

## Facts (YAML)


```yaml
task_context:
  description: The task transforms an input grid into an output grid with a fixed height and conditional pattern placement.
  background_color: 7 # Orange
  output_grid_properties:
    height: 16
    width: Same as input grid width
    base_fill: background_color

transformation_rule:
  condition: Input grid contains at least one pixel color different from the background_color.
  action_if_true:
    - step: Identify all non-background pixels in the input grid.
    - step: Determine the maximum color value ('max_color') among these non-background pixels.
    - step: Select a predefined pattern object based on 'max_color'.
      pattern_details:
        height: 5
        width: Varies based on 'max_color' (e.g., 10 for max_color=8, 7 for max_color=5)
        colors: Contains only Red (2) and Yellow (4).
        position_in_output: Top-left corner at row 11, column 0.
    - step: Create the output grid (16xW) filled with the background color.
    - step: Place the selected pattern onto the output grid at the specified position.
  action_if_false:
    - step: Create the output grid (16xW) filled entirely with the background color.

known_patterns:
  - trigger_max_color: 8
    pattern_grid: # 5x10
      - [2, 2, 2, 2, 4, 4, 2, 2, 2, 2]
      - [2, 2, 2, 4, 2, 2, 4, 2, 2, 2]
      - [2, 2, 4, 2, 2, 2, 2, 4, 2, 2]
      - [2, 4, 2, 2, 2, 2, 2, 2, 4, 2]
      - [4, 2, 2, 2, 2, 2, 2, 2, 2, 4]
  - trigger_max_color: 5
    pattern_grid: # 5x7
      - [2, 2, 4, 2, 4, 2, 2]
      - [2, 2, 2, 4, 2, 2, 2]
      - [2, 2, 4, 2, 4, 2, 2]
      - [2, 4, 2, 2, 2, 4, 2]
      - [4, 2, 2, 2, 2, 2, 4]

assumptions:
  - There is a unique, predefined pattern associated with each possible maximum non-background color value that might appear in inputs.
  - The background color will always be orange (7).
```


## Natural Language Program

1.  Determine the dimensions (height H, width W) of the input grid.
2.  Identify the background color, which is consistently orange (7).
3.  Create a new output grid with height 16 and width W, filled entirely with the background color (orange/7).
4.  Scan the input grid to find all pixels that are *not* the background color.
5.  If no non-background pixels are found, the transformation is complete; return the orange-filled 16xW output grid.
6.  If non-background pixels *are* found:
    a.  Determine the maximum color value (`max_color`) among all the non-background pixels identified in step 4.
    b.  Select a specific, predefined 5-row high pattern grid based on the value of `max_color`. For example:
        *   If `max_color` is 8, select the predefined 5x10 pattern.
        *   If `max_color` is 5, select the predefined 5x7 pattern.
        *   (Assume similar predefined patterns exist for other possible `max_color` values).
    c.  Place the selected pattern onto the output grid such that its top-left corner is at row index 11 and column index 0, overwriting the existing background pixels in that area.
7.  Return the modified output grid.