
Previous Code:
```python
"""
1.  **Identify Non-Black Rows:** Scan the entire input grid and identify all rows that contain at least one pixel that is *not* black (value not equal to 0).
2.  **Keep Track of Black Rows and Their Original Order:** Make not of the rows that contain only black (value equal to 0), and keep their top-down ordering.
3.  **Reverse Non-Black Rows:** Reverse the order of the identified non-black rows.
4.  **Construct Output:** Create the output grid by first placing the all-black rows in their original order, and stacking the reversed non-black rows at the bottom.
"""

import numpy as np

def transform(input_grid):
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # 1. Identify Non-Black Rows
    non_black_rows = []
    black_rows = []
    for i, row in enumerate(input_grid):
        if np.any(row != 0):
            non_black_rows.append(row)
        else:
          black_rows.append(row)

    # 2. Reverse Non-Black Rows
    non_black_rows.reverse()

    # 3. Construct Output
    output_grid = np.vstack(black_rows + non_black_rows) if len(black_rows) + len(non_black_rows) > 0 else input_grid

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
2 2 2 2 2
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```
Expected Output:
```
2 2 2 2 2
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
8 8 8 8 8
2 2 2 2 2
```
Transformed Output:
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
8 8 8 8 8
2 2 2 2 2
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 40.0

## Example 2:
Input:
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```
Expected Output:
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
3 3 3
2 2 2
2 2 2
```
Transformed Output:
```
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
3 3 3
2 2 2
2 2 2
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 60.0
Okay, here's a breakdown of the results and a plan to improve the natural language program and subsequently the code:

**General Assessment:**

The initial natural language program and code were on the right track, correctly identifying the need to separate black and non-black rows. However, it failed to fully account for the positioning of black rows. It seems all black rows are put on the top, and only then the non-black ones follow. The original program *almost* works. The problem is that the all-black rows need to maintain not only their original order, but also original position relative to other rows. In the given examples, the program places black rows at the top even when the original input had them in between non-black rows.

**Strategy:**

The core issue is that the original program treats all black rows as a single block to be placed at the top. Instead, we need to preserve the *original positions* of the all-black rows relative to the non-black rows. Instead of separating rows into two groups, we need to keep all rows together, reversing just the non-black ones and leave the black ones unchanged.

**Metrics and Observations:**

Let's analyze the results more formally:

*   **Example 1:**
    *   Input: Two non-black rows (red and blue) followed by eight black rows.
    *   Expected Output: original order
    *   Actual Output: Eight black rows, followed by the blue and red rows (reversed).
    *   Error: Black rows are moved to the top.
*    **Example 2:**
    *    Input: two red rows, one green row and seven black rows.
    *    Expected Output: original order
    *    Actual output: seven black rows, green row, and two red rows.
    *    Error: Black rows are moved to top.

**YAML Fact Block:**


```yaml
facts:
  - object: rows
    properties:
      - color: varied (black, red, blue, green)
      - type: black_row (all pixels are black) or non-black_row (contains at least one non-black pixel)
    actions:
      - non-black_rows: reversed in order
      - all-black_rows: maintain the original order AND the original position
  - object: grid
    properties:
      - structure: 2D array of pixels
    actions:
      - transform: reconstruct grid by re-inserting all-black rows in their original positions among the (reversed) non-black rows.

```


**Natural Language Program:**

1.  **Iterate** through the input grid's rows, top to bottom.
2. **Identify** if each row contains only black pixels or contains at least one non-black pixel.
3. **Store** the non-black rows in a list.
4. **Reverse** the order of the stored list of non-black rows.
5. Create a new empty result grid
6. **Iterate** through the original grid's row *indices*.
7. For current index `i`
   - if row `i` of original grid was black, add it to result grid
   - if row `i` of original grid was non-black, add the next element of the reversed non-black-row list to result grid.

This maintains the original *positions* of the black rows, rather than grouping them.

