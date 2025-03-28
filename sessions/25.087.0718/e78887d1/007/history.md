
Previous Code:
```python
import numpy as np
from typing import List, Dict, Tuple, Optional

"""
Identifies horizontal strips in the input grid separated by all-white rows. 
Calculates the sum of pixel values and the count of non-white pixels for each strip.
Selects a target strip based on the following criteria:
1. Primary: Maximum sum of pixel values.
2. Tiebreaker 1: Maximum count of non-white pixels among strips tied for maximum sum.
3. Tiebreaker 2: Topmost position (minimum starting row index) among strips still tied.

Currently, the function returns the selected strip *without modification*. 
This successfully reproduces the output for Example 1 but fails for Examples 2, 3, and 4, 
where the expected output is a modified version of the selected strip. 
The exact transformation rule preserving shape and non-white count but potentially altering 
pixel values and sum remains undetermined.
"""

def find_strips(grid: np.ndarray) -> list:
    """
    Identifies horizontal strips separated by all-white rows.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each containing a 'strip' (np.ndarray),
              'start_row' (int), and 'end_row' (int). Returns empty list
              if grid is empty or invalid.
    """
    if grid is None or grid.size == 0:
        return []
        
    height, width = grid.shape
    strips = []
    
    # Find indices of rows that are entirely white (0)
    separator_rows = [-1] # Virtual separator before the first row
    for r in range(height):
        if np.all(grid[r, :] == 0):
            separator_rows.append(r)
    separator_rows.append(height) # Virtual separator after the last row

    # Extract strips based on separators
    for i in range(len(separator_rows) - 1):
        start_row = separator_rows[i] + 1
        end_row = separator_rows[i+1]

        # Ensure the strip has at least one row
        if start_row < end_row:
            strip_array = grid[start_row:end_row, :]
            strips.append({
                'strip': strip_array,
                'start_row': start_row,
                'end_row': end_row
            })
            
    return strips

def calculate_strip_properties(strip_array: np.ndarray) -> Tuple[int, int]:
    """
    Calculates the sum of pixel values and the count of non-white pixels for a strip.

    Args:
        strip_array (np.ndarray): The strip grid.

    Returns:
        Tuple[int, int]: A tuple containing (sum_of_pixels, non_white_count).
    """
    strip_sum = np.sum(strip_array)
    non_white_count = np.count_nonzero(strip_array)
    return strip_sum, non_white_count

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Selects a horizontal strip based on max sum, max non-white count, and topmost position.
    Note: Does not currently apply the final modification step needed for examples 2-4.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The selected horizontal strip as a list of lists.
                         Returns an empty list if no valid strips are found.
    """
    # Convert input to numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)

    if grid.size == 0:
        return []

    # 1. Identify Horizontal Strips
    identified_strips = find_strips(grid)

    if not identified_strips:
        return [] # No strips found

    # 2. Calculate Properties for each strip
    strips_data = []
    max_sum = -1
    for i, item in enumerate(identified_strips):
        strip_array = item['strip']
        strip_sum, non_white_count = calculate_strip_properties(strip_array)
        strips_data.append({
            'index': i,
            'strip': strip_array,
            'sum': strip_sum,
            'count': non_white_count,
            'start_row': item['start_row']
        })
        if strip_sum > max_sum:
            max_sum = strip_sum
            
    # 3. Select Target Strip based on criteria
    
    # Filter for max sum
    candidates = [s for s in strips_data if s['sum'] == max_sum]
    
    # Tiebreaker 1: Max non-white count
    if len(candidates) > 1:
        max_count_in_candidates = -1
        for c in candidates:
            if c['count'] > max_count_in_candidates:
                max_count_in_candidates = c['count']
        candidates = [c for c in candidates if c['count'] == max_count_in_candidates]
        
    # Tiebreaker 2: Topmost (min start_row)
    if len(candidates) > 1:
        # Sort candidates by start_row and pick the first one
        candidates.sort(key=lambda c: c['start_row'])
        
    # The first candidate after filtering/sorting is the selected one
    selected_strip_data = candidates[0]
    selected_strip_array = selected_strip_data['strip']

    # 4. Transform Selected Strip (Placeholder)
    # !!! This is where the unknown modification logic should go !!!
    # Currently, we just return the selected strip directly.
    # This works for Example 1 but not for 2, 3, 4.
    output_grid_array = selected_strip_array

    # 5. Output the result
    if output_grid_array is not None:
        # Convert the numpy array back to a list of lists for the output format
        return output_grid_array.tolist()
    else:
        # Should not happen if strips_data was populated
        return []
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 0 1 0 0 3 3 3
2 0 2 0 1 1 1 0 0 0 0
2 2 2 0 0 1 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 1 1 1 0 3 0 3
2 2 2 0 0 0 0 0 3 0 3
0 2 0 0 1 1 1 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 1 0 1 0 0 3 0
0 0 0 0 1 0 1 0 3 3 3
2 2 2 0 1 1 1 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
2 0 2 0 0 1 0 0 3 3 3
2 0 2 0 1 1 1 0 0 0 0
2 2 2 0 0 1 0 0 3 3 3
```
Transformed Output:
```
2 0 2 0 0 1 0 0 3 3 3
2 0 2 0 1 1 1 0 0 0 0
2 2 2 0 0 1 0 0 3 3 3
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
0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 3 0 0 0 1 1 1
0 2 0 0 3 3 3 0 0 1 0
2 0 2 0 0 0 3 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 3 3 3 0 1 0 1
2 2 2 0 0 3 0 0 0 1 0
0 0 2 0 0 3 0 0 1 0 1
0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
2 2 2 0 3 0 3 0 1 0 0
0 2 0 0 0 3 0 0 1 1 1
0 2 0 0 3 0 3 0 0 0 1
```
Transformed Output:
```
2 0 2 0 3 0 0 0 1 1 1
0 2 0 0 3 3 3 0 0 1 0
2 0 2 0 0 0 3 0 0 1 0
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 42.42424242424242

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 3 0 0 0 1 0 0 0 5 0 5
0 0 2 0 3 0 0 0 0 1 1 0 5 0 5
0 0 2 0 3 3 3 0 1 0 0 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
2 0 0 0 3 0 0 0 1 0 1 0 5 5 5
2 0 0 0 0 3 3 0 1 0 1 0 0 0 5
2 2 2 0 3 0 0 0 1 0 1 0 0 0 5
```
Transformed Output:
```
2 2 2 0 3 0 0 0 1 0 0 0 5 0 5
0 0 2 0 3 0 0 0 0 1 1 0 5 0 5
0 0 2 0 3 3 3 0 1 0 0 0 5 0 5
```
Match: False
Pixels Off: 18
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 80.0

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 3 0 3 0 1 0 1 0 0 5 0
2 2 2 0 0 3 0 0 1 1 1 0 5 5 5
0 0 2 0 3 0 3 0 0 1 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 3 0 3 0 0 1 0 0 5 0 0
0 2 0 0 3 3 3 0 1 1 1 0 5 5 5
2 0 2 0 0 3 0 0 0 1 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
2 0 2 0 0 3 0 0 1 0 0 0 5 0 5
2 2 2 0 3 3 3 0 1 1 1 0 0 5 0
0 2 0 0 0 3 0 0 0 0 1 0 5 0 5
```
Transformed Output:
```
2 0 2 0 3 0 3 0 0 1 0 0 5 0 0
0 2 0 0 3 3 3 0 1 1 1 0 5 5 5
2 0 2 0 0 3 0 0 0 1 0 0 0 0 5
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 71.11111111111111
**Analysis of Metrics:**

*   **Example 2:** Sum, Non-white count, and counts of each specific color are identical between the selected strip and the expected output. This implies the transformation is purely a rearrangement of existing pixels within the strip.
*   **Example 3:** Sum differs (59 -> 53). Non-white count is the same (20). Specific color counts change: Blue (1) increases (4->6), Green (3) decreases (5->4), Gray (5) decreases (6->5). Red (2) count is unchanged (5). This implies rearrangement *and* color changes. The net change in sum is -6. (Change: +2 * (1) - 1 * (3) - 1 * (5) = 2 - 3 - 5 = -6). This matches the sum difference.
*   **Example 4:** Sum differs (58 -> 57). Non-white count is the same (21). Specific color counts change: Red (2) increases (5->6), Green (3) decreases (6->5). Blue (1) and Gray (5) counts are unchanged. This implies rearrangement *and* color changes. Net change in sum: +1 * (2) - 1 * (3) = 2 - 3 = -1. Matches sum difference.

**Revisiting the Transformation Hypothesis:**

*   Since Ex2 only involves rearrangement, let's look closer there.
    *   Selected Strip (`Transformed Output`):
        
```
        2 0 2 | 0 | 3 0 0 | 0 | 1 1 1
        0 2 0 | 0 | 3 3 3 | 0 | 0 1 0
        2 0 2 | 0 | 0 0 3 | 0 | 0 1 0
        ```

    *   Expected Output:
        
```
        2 2 2 | 0 | 3 0 3 | 0 | 1 0 0
        0 2 0 | 0 | 0 3 0 | 0 | 1 1 1
        0 2 0 | 0 | 3 0 3 | 0 | 0 0 1
        ```

    *   The grid seems segmented vertically by all-white columns. Let's check this idea across examples.
    *   Ex1 Input/Output (Selected Strip):
        
```
        2 0 2 | 0 | 0 1 0 | 0 | 3 3 3
        2 0 2 | 0 | 1 1 1 | 0 | 0 0 0
        2 2 2 | 0 | 0 1 0 | 0 | 3 3 3
        ```

        (Vertical separators at index 3 and 7)
    *   Ex2 Input has separators at index 3 and 7.
        Selected Strip (shown above)
        Expected Output (shown above)
    *   Ex3 Input has separators at index 3, 7, 11.
        Selected Strip:
        
```
        2 2 2 | 0 | 3 0 0 | 0 | 1 0 0 | 0 | 5 0 5
        0 0 2 | 0 | 3 0 0 | 0 | 0 1 1 | 0 | 5 0 5
        0 0 2 | 0 | 3 3 3 | 0 | 1 0 0 | 0 | 5 0 5
        ```

        Expected Output:
        
```
        2 0 0 | 0 | 3 0 0 | 0 | 1 0 1 | 0 | 5 5 5
        2 0 0 | 0 | 0 3 3 | 0 | 1 0 1 | 0 | 0 0 5
        2 2 2 | 0 | 3 0 0 | 0 | 1 0 1 | 0 | 0 0 5
        ```

    *   Ex4 Input has separators at index 3, 7, 11.
        Selected Strip:
        
```
        2 0 2 | 0 | 3 0 3 | 0 | 0 1 0 | 0 | 5 0 0
        0 2 0 | 0 | 3 3 3 | 0 | 1 1 1 | 0 | 5 5 5
        2 0 2 | 0 | 0 3 0 | 0 | 0 1 0 | 0 | 0 0 5
        ```

        Expected Output:
        
```
        2 0 2 | 0 | 0 3 0 | 0 | 1 0 0 | 0 | 5 0 5
        2 2 2 | 0 | 3 3 3 | 0 | 1 1 1 | 0 | 0 5 0
        0 2 0 | 0 | 0 3 0 | 0 | 0 0 1 | 0 | 5 0 5
        ```


*   It seems the transformation operates independently within each vertical segment defined by all-white columns within the *selected horizontal strip*.

**Transformation within Vertical Segments:**

Let's analyze the transformation within each segment for Ex2, Ex3, Ex4.

*   **Ex2, Segment 1 (Cols 0-2):**
    
```
    Sel:       Exp:
    2 0 2      2 2 2
    0 2 0      0 2 0
    2 0 2      0 2 0
    ```

    Looks like gravity? Pixels fall down within the column, stacking at the bottom.
*   **Ex2, Segment 2 (Cols 4-6):**
    
```
    Sel:       Exp:
    3 0 0      3 0 3
    3 3 3      0 3 0
    0 0 3      3 0 3
    ```

    Gravity again? Yes.
*   **Ex2, Segment 3 (Cols 8-10):**
    
```
    Sel:       Exp:
    1 1 1      1 0 0
    0 1 0      1 1 1
    0 1 0      0 0 1
    ```

    Gravity again? Yes.

**Hypothesis: Apply gravity column-wise within each vertical segment of the selected horizontal strip.**

Let's test this hypothesis on Ex3 and Ex4.

*   **Ex3, Segment 1 (Cols 0-2):**
    
```
    Sel:       Exp:
    2 2 2      2 0 0
    0 0 2      2 0 0
    0 0 2      2 2 2
    ```

    Gravity? Yes.
*   **Ex3, Segment 2 (Cols 4-6):**
    
```
    Sel:       Exp:
    3 0 0      3 0 0
    3 0 0      0 3 3
    3 3 3      3 0 0  <- Hmm, mistake in my manual copy? Let's recheck Exp3.
    ```

    Rechecking Exp3 Output:
    
```
    2 0 0 | 0 | 3 0 0 | 0 | 1 0 1 | 0 | 5 5 5
    2 0 0 | 0 | 0 3 3 | 0 | 1 0 1 | 0 | 0 0 5
    2 2 2 | 0 | 3 0 0 | 0 | 1 0 1 | 0 | 0 0 5 <- Mistake in manual copy of Exp3 Output Segment 4. Let's fix.
    ```

    Corrected Exp3 Output:
    
```
    2 0 0 | 0 | 3 0 0 | 0 | 1 0 1 | 0 | 5 5 5
    2 0 0 | 0 | 0 3 3 | 0 | 1 0 1 | 0 | 0 0 5
    2 2 2 | 0 | 3 0 0 | 0 | 1 0 1 | 0 | 0 0 5
    ```

    Okay, let's re-test gravity on Exp3 segments:
    *   **Ex3, Segment 1 (Cols 0-2):**
        
```
        Sel:       Exp (Gravity):   Exp (Actual):
        2 2 2      0 0 2           2 0 0  <- Mismatch
        0 0 2      0 0 2           2 0 0
        0 0 2      2 2 2           2 2 2
        ```

        Gravity alone doesn't work. What if we consider the *entire segment* as an object?
        Let's treat each vertical segment as a sub-grid and apply gravity to its columns.

Let's define a gravity function.


```python
import numpy as np

def apply_gravity_to_segment(segment: np.ndarray) -> np.ndarray:
    """Applies gravity column by column within a segment."""
    if segment is None or segment.size == 0:
        return segment
    rows, cols = segment.shape
    new_segment = np.zeros_like(segment)
    for c in range(cols):
        col_data = segment[:, c]
        non_zeros = col_data[col_data != 0]
        if len(non_zeros) > 0:
            new_segment[rows - len(non_zeros):rows, c] = non_zeros
    return new_segment
```


Let's test this function on the segments.

*   **Ex2, Segment 1 (Cols 0-2):**
    
```
    Sel:       Gravity(Sel):   Exp(Actual):
    2 0 2      0 0 0           2 2 2  <- Mismatch
    0 2 0      0 2 0           0 2 0
    2 0 2      2 2 2           0 2 0
    ```

    Okay, simple gravity isn't it.

Let's reconsider the comparison. What if pixels move based on their neighbors? Or maybe it's not gravity, but some other rearrangement?

Look at Ex2 again:
    
```
    Selected:                  Expected:
    2 0 2 | 0 | 3 0 0 | 0 | 1 1 1      2 2 2 | 0 | 3 0 3 | 0 | 1 0 0
    0 2 0 | 0 | 3 3 3 | 0 | 0 1 0      0 2 0 | 0 | 0 3 0 | 0 | 1 1 1
    2 0 2 | 0 | 0 0 3 | 0 | 0 1 0      0 2 0 | 0 | 3 0 3 | 0 | 0 0 1
    ```

Could it be sorting columns within segments?
Seg 1 Sel: [2,0,2], [0,2,0], [2,0,2] -> Col sums: 4, 2, 4
Seg 1 Exp: [2,0,0], [2,2,2], [2,0,0] -> Col sums: 4, 6, 2 - No clear sort order.

What if we analyze the transformation pixel by pixel?
Ex2:
(0,0) 2->2
(0,1) 0->2 (from (1,1) or (2,1)?)
(0,2) 2->2
(1,0) 0->0
(1,1) 2->2
(1,2) 0->0
(2,0) 2->0
(2,1) 0->2 (from (1,1) or (2,1)?)
(2,2) 2->0

This is getting confusing. Let's re-read the prompt and priors. Objectness, Goal-directedness, Numbers/Counting, Geometry/Topology.

Maybe we should identify "objects" within the selected strip first?
Objects are contiguous blocks of the same color.

Ex2 Selected Strip:

```
2 0 2 | 0 | 3 0 0 | 0 | 1 1 1
0 2 0 | 0 | 3 3 3 | 0 | 0 1 0
2 0 2 | 0 | 0 0 3 | 0 | 0 1 0
```

Objects:
- Red '2' at (0,0), (1,1), (2,0), (0,2), (2,2) - these are 5 separate 1x1 objects.
- Green '3' at (0,4), (1,4), (1,5), (1,6), (2,6) - One L-shape, one 1x1.
- Blue '1' at (0,8)-(0,10), (1,9), (2,9) - One block and two 1x1s.

Ex2 Expected Output:

```
2 2 2 | 0 | 3 0 3 | 0 | 1 0 0
0 2 0 | 0 | 0 3 0 | 0 | 1 1 1
0 2 0 | 0 | 3 0 3 | 0 | 0 0 1
```

Objects:
- Red '2' at (0,0)-(0,2), (1,1), (2,1) - One line, two 1x1s.
- Green '3' at (0,4), (0,6), (1,5), (2,4), (2,6) - Five 1x1s.
- Blue '1' at (0,8), (1,8)-(1,10), (2,10) - Two 1x1s, one line.

The structure of objects changes significantly.

Let's rethink the "gravity" idea. What if it's gravity within each *object*, not each column? No, that doesn't make sense.

What if we rotate the strip 90 degrees, apply gravity, and rotate back?

Ex2 Selected Strip Rotated 90 deg clockwise:

```
2 0 2
0 2 0
2 0 2
0 0 0
3 3 0
0 3 0
0 3 3
0 0 0
1 0 0
1 1 1
1 0 0
```

Apply gravity (columnar):

```
0 0 0
0 0 0
0 0 0
0 0 0
2 2 2  <- from 2,0,2
0 2 0  <- from 0,2,0
2 0 2  <- from 2,0,2
3 3 0  <- from 3,3,0
0 3 3  <- from 0,3,3 ?? No, need to stack non-zeros
```

Let's re-apply gravity carefully:
Col 0: [2,0,2,0,3,0,0,0,1,1,1] -> [0,0,0,0,0,2,2,3,1,1,1]
Col 1: [0,2,0,0,3,3,3,0,0,1,1] -> [0,0,0,0,0,2,3,3,3,1,1]
Col 2: [2,0,2,0,0,0,3,0,0,1,0] -> [0,0,0,0,0,0,2,2,3,1,0]
Result after gravity:

```
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
2 2 0
2 3 2
3 3 2
1 3 3
1 1 1
1 1 0
```

Rotate back 90 deg counter-clockwise:

```
1 1 1 3 2 2 0 0 0 0 0
1 1 3 3 3 0 2 0 0 0 0
0 1 1 3 2 2 0 0 0 0 0
```

This doesn't match the expected output at all.

Let's abandon rotation.

Back to vertical segments and gravity. Maybe the gravity direction changes? Or maybe it's not gravity but some other pixel shuffling?

Look at the differences again.
Ex2:
Selected -> Expected
Row 0: (0,1) 0->2, (0,6) 0->3, (0,9) 1->0, (0,10) 1->0
Row 1: (1,4) 3->0, (1,6) 3->0, (1,8) 0->1
Row 2: (2,0) 2->0, (2,4) 0->3, (2,8) 0->0, (2,10) 0->1

It looks like pixels *move*.
Where did the '2' at (0,1) come from? Maybe (1,1) or (2,1)?
Where did the '3' at (0,6) come from? Maybe (1,6) or (2,6)?
Where did the '1' at (1,8) come from? Maybe (0,8)?
Where did the '3' at (2,4) come from? Maybe (1,4)?
Where did the '1' at (2,10) come from? Maybe (0,10)?

Let's track pixel counts per column within a segment.
Ex2, Segment 1 (Cols 0-2):
Col 0: Sel=[2,0,2] (Two 2s) -> Exp=[2,0,0] (One 2) !! ERROR in my previous analysis of Exp2 Output !! Let's re-check.

Expected Output 2:

```
2 2 2 | 0 | 3 0 3 | 0 | 1 0 0
0 2 0 | 0 | 0 3 0 | 0 | 1 1 1
0 2 0 | 0 | 3 0 3 | 0 | 0 0 1
```

Okay, let's re-verify my `calculate_metrics` call.

```python
import numpy as np
expected_output_2 = [[2, 2, 2, 0, 3, 0, 3, 0, 1, 0, 0], [0, 2, 0, 0, 0, 3, 0, 0, 1, 1, 1], [0, 2, 0, 0, 3, 0, 3, 0, 0, 0, 1]]
grid = np.array(expected_output_2)
print(np.sum(grid))
print(np.count_nonzero(grid))
unique, counts = np.unique(grid[grid != 0], return_counts=True)
print(dict(zip(unique, counts)))
```

*code_execution:*
```python
import numpy as np
expected_output_2 = [[2, 2, 2, 0, 3, 0, 3, 0, 1, 0, 0], [0, 2, 0, 0, 0, 3, 0, 0, 1, 1, 1], [0, 2, 0, 0, 3, 0, 3, 0, 0, 0, 1]]
grid = np.array(expected_output_2)
print(np.sum(grid))
print(np.count_nonzero(grid))
unique, counts = np.unique(grid[grid != 0], return_counts=True)
print(dict(zip(unique, counts)))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
30
15
{np.int64(1): np.int64(5), np.int64(2): np.int64(5), np.int64(3): np.int64(5)}

```
Okay, the metrics calculation was correct. Sum=30, Count=15, Colors={1:5, 2:5, 3:5}. These matched the selected strip.

Now, let's carefully compare the segments again for Ex2:
*   **Ex2, Segment 1 (Cols 0-2):**
    
```
    Sel:       Exp:
    2 0 2      2 2 2
    0 2 0      0 2 0
    2 0 2      0 2 0
    ```

    Col 0: [2,0,2] -> [2,0,0] (Lost a 2)
    Col 1: [0,2,0] -> [2,2,2] (Gained two 2s)
    Col 2: [2,0,2] -> [2,0,0] (Lost a 2)
    This CANNOT be right if the overall color counts are preserved. There must be an error in my manual transcription of either the selected strip or the expected output.

Let's re-get the selected strip for Ex2 from the problem description (`Transformed Output`):

```
2 0 2 0 3 0 0 0 1 1 1
0 2 0 0 3 3 3 0 0 1 0
2 0 2 0 0 0 3 0 0 1 0
```

Let's re-get the expected output for Ex2 from the problem description:

```
2 2 2 0 3 0 3 0 1 0 0
0 2 0 0 0 3 0 0 1 1 1
0 2 0 0 3 0 3 0 0 0 1
```

Okay, *now* compare the segments:

*   **Ex2, Segment 1 (Cols 0-2):**
    
```
    Sel:       Exp:
    2 0 2      2 2 2
    0 2 0      0 2 0
    2 0 2      0 2 0
    ```

    Sel Counts: Red=5. Exp Counts: Red=5. Okay.
    Transformation: The 2 at (2,0) moved to (0,1). The 2 at (2,2) moved to (0,2). The 2 at (0,2) stayed. The 2 at (0,0) stayed. The 2 at (1,1) stayed. It's a shuffle.

*   **Ex2, Segment 2 (Cols 4-6):**
    
```
    Sel:       Exp:
    3 0 0      3 0 3
    3 3 3      0 3 0
    0 0 3      3 0 3
    ```

    Sel Counts: Green=5. Exp Counts: Green=5. Okay.
    Transformation: (0,4) stayed. (1,4) moved to (2,4). (1,5) stayed. (1,6) moved to (0,6). (2,6) stayed.

*   **Ex2, Segment 3 (Cols 8-10):**
    
```
    Sel:       Exp:
    1 1 1      1 0 0
    0 1 0      1 1 1
    0 1 0      0 0 1
    ```

    Sel Counts: Blue=5. Exp Counts: Blue=5. Okay.
    Transformation: (0,8) stayed. (0,9) moved to (1,9). (0,10) moved to (1,10). (1,9) moved to (1,8). (2,9) moved to (2,10).

**The transformation preserves color counts within each vertical segment and rearranges the pixels.** How?

Look at the pattern of movement:
Seg 1: (2,0)->(0,1), (2,2)->(0,2). Others stay/shift slightly.
Seg 2: (1,4)->(2,4), (1,6)->(0,6). Others stay.
Seg 3: (0,9)->(1,9), (0,10)->(1,10), (1,9)->(1,8), (2,9)->(2,10). One stays.

This looks like **gravity** again, but maybe applied *iteratively* or with some stabilization?

Let's simulate simple columnar gravity on Ex2, Segment 1:

```
Start:     Step 1:    Step 2:
2 0 2      2 0 2      0 0 0
0 2 0      0 2 0      2 2 2  <- Pixels from row 0 fall
2 0 2      2 0 2      2 0 2  <- Pixels from row 1 fall? No, stop at row above or bottom.

Let's try again. Move pixels down one step if the cell below is empty (0). Repeat until no moves.
Start:
2 0 2
0 2 0
2 0 2

Iter 1:
(0,0) 2 stays (below is 0) -> Moves to (1,0)? No, below is 0.
(0,1) 0 stays
(0,2) 2 stays (below is 0) -> Moves to (1,2)?
(1,1) 2 stays (below is 0) -> Moves to (2,1)?
(2,0) 2 stays (bottom)
(2,1) 0 stays
(2,2) 2 stays (bottom)

If a pixel at (r, c) is non-zero and (r+1, c) is zero (and r+1 < height): Move pixel from (r,c) to (r+1,c). Apply simultaneously? Or scan top-down?

Scan Top-Down:
(0,0)=2, (1,0)=0 -> Move (0,0) to (1,0). Grid becomes:
  0 0 2
  2 2 0
  2 0 2
(0,2)=2, (1,2)=0 -> Move (0,2) to (1,2). Grid becomes:
  0 0 0
  2 2 2
  2 0 2
(1,1)=2, (2,1)=0 -> Move (1,1) to (2,1). Grid becomes:
  0 0 0
  2 0 2
  2 2 2
End of Iter 1 scan.

Iter 2 Scan:
(1,0)=2, (2,0)=2 -> Stay.
(1,2)=2, (2,2)=2 -> Stay.
(2,*) -> Stay (bottom).
Stable state:
0 0 0
2 0 2
2 2 2

This matches the result of `apply_gravity_to_segment` I wrote earlier. And it doesn't match the expected output.

Hypothesis failed.

---
**New Idea: Reflection/Symmetry?**

Let's compare Selected vs Expected for Ex2 again.

*   **Ex2, Segment 1 (Cols 0-2):**
    ```

    Sel:       Exp:
    2 0 2      2 2 2
    0 2 0      0 2 0
    2 0 2      0 2 0
    
```
    Looks like the top row `[2 0 2]` is reflected vertically and OR-ed/combined with the rest?
    Reflect `[2 0 2]` -> `[2 0 2]`. Doesn't help.
    Reflect the whole segment vertically?
    ```

    2 0 2
    0 2 0
    2 0 2
    
```
    Still doesn't match `Exp`.

*   **Ex2, Segment 2 (Cols 4-6):**
    ```

    Sel:       Exp:
    3 0 0      3 0 3
    3 3 3      0 3 0
    0 0 3      3 0 3
    
```
    Reflect vertically?
    ```

    0 0 3
    3 3 3
    3 0 0
    
```
    Doesn't match.

---
**New Idea: Look at the non-white pixels as a single "pattern" within each segment.**

*   **Ex2, Segment 1:**
    Pattern Sel: `{(0,0), (0,2), (1,1), (2,0), (2,2)}`
    Pattern Exp: `{(0,0), (0,1), (0,2), (1,1), (2,1)}`
    Looks like the pattern is shifted upwards and maybe squashed?

*   **Ex2, Segment 2:**
    Pattern Sel: `{(0,4), (1,4), (1,5), (1,6), (2,6)}`
    Pattern Exp: `{(0,4), (0,6), (1,5), (2,4), (2,6)}`

*   **Ex2, Segment 3:**
    Pattern Sel: `{(0,8), (0,9), (0,10), (1,9), (2,9)}`
    Pattern Exp: `{(0,8), (1,8), (1,9), (1,10), (2,10)}`

This feels like Conway's Game of Life or some cellular automaton rule. But the problem description emphasizes core knowledge priors, which usually don't include complex CA rules unless they are very simple (like gravity).

---
**Revisit Ex3 and Ex4 differences:**

*   **Ex3:** Sum changes, Count same. Colors change: +2 Blue(1), -1 Green(3), -1 Gray(5). Net sum change = 2*1 - 1*3 - 1*5 = 2 - 3 - 5 = -6. Matches.
*   **Ex4:** Sum changes, Count same. Colors change: +1 Red(2), -1 Green(3). Net sum change = 1*2 - 1*3 = -1. Matches.

Where do these color changes happen?

*   **Ex3, Segment 1 (Cols 0-2):**
    ```

    Sel:       Exp:
    2 2 2      2 0 0
    0 0 2      2 0 0
    0 0 2      2 2 2
    
```
    Sel: 5 Reds. Exp: 5 Reds. No color change here.

*   **Ex3, Segment 2 (Cols 4-6):**
    ```

    Sel:       Exp:
    3 0 0      3 0 0
    3 0 0      0 3 3
    3 3 3      3 0 0
    
```
    Sel: 5 Greens. Exp: 4 Greens. Lost a Green. Sum change -3.

*   **Ex3, Segment 3 (Cols 8-10):**
    ```

    Sel:       Exp:
    1 0 0      1 0 1
    0 1 1      1 0 1
    1 0 0      1 0 1
    
```
    Sel: 4 Blues. Exp: 6 Blues. Gained 2 Blues. Sum change +2.

*   **Ex3, Segment 4 (Cols 12-14):**
    ```

    Sel:       Exp:
    5 0 5      5 5 5
    5 0 5      0 0 5
    5 0 5      0 0 5
    
```
    Sel: 6 Grays. Exp: 5 Grays. Lost a Gray. Sum change -5.

Total Sum Change = 0 - 3 + 2 - 5 = -6. Matches overall.
Total Count Change = 0 + (-1) + 2 + (-1) = 0. Matches overall.

*   **Ex4, Segment 1 (Cols 0-2):**
    ```

    Sel:       Exp:
    2 0 2      2 0 2
    0 2 0      2 2 2
    2 0 2      0 2 0
    
```
    Sel: 5 Reds. Exp: 6 Reds. Gained 1 Red. Sum change +2.

*   **Ex4, Segment 2 (Cols 4-6):**
    ```

    Sel:       Exp:
    3 0 3      0 3 0
    3 3 3      3 3 3
    0 3 0      0 3 0
    
```
    Sel: 6 Greens. Exp: 5 Greens. Lost 1 Green. Sum change -3.

*   **Ex4, Segment 3 (Cols 8-10):**
    ```

    Sel:       Exp:
    0 1 0      1 0 0
    1 1 1      1 1 1
    0 1 0      0 0 1
    
```
    Sel: 5 Blues. Exp: 5 Blues. No change.

*   **Ex4, Segment 4 (Cols 12-14):**
    ```

    Sel:       Exp:
    5 0 0      5 0 5
    5 5 5      0 5 0
    0 0 5      5 0 5
    
```
    Sel: 5 Grays. Exp: 5 Grays. No change.

Total Sum Change = +2 - 3 + 0 + 0 = -1. Matches overall.
Total Count Change = 1 + (-1) + 0 + 0 = 0. Matches overall. Non-white count *is* preserved in Ex4! My earlier calculation was wrong. Let's re-run metrics for Ex4.

```
python
import numpy as np

def calculate_metrics(grid_list):
    if not grid_list: return 0, 0, {}
    grid = np.array(grid_list)
    grid_sum = np.sum(grid)
    non_white_count = np.count_nonzero(grid)
    unique, counts = np.unique(grid[grid != 0], return_counts=True)
    color_counts = dict(zip(unique, counts))
    return grid_sum, non_white_count, color_counts

selected_strip_4 = [[2, 0, 2, 0, 3, 0, 3, 0, 0, 1, 0, 0, 5, 0, 0], [0, 2, 0, 0, 3, 3, 3, 0, 1, 1, 1, 0, 5, 5, 5], [2, 0, 2, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 5]]
expected_output_4 = [[2, 0, 2, 0, 0, 3, 0, 0, 1, 0, 0, 0, 5, 0, 5], [2, 2, 2, 0, 3, 3, 3, 0, 1, 1, 1, 0, 0, 5, 0], [0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 5, 0, 5]]
sum_sel_4, count_sel_4, colors_sel_4 = calculate_metrics(selected_strip_4)
sum_exp_4, count_exp_4, colors_exp_4 = calculate_metrics(expected_output_4)

print(f"Ex4 Sel: Sum={sum_sel_4}, Count={count_sel_4}, Colors={colors_sel_4}")
print(f"Ex4 Exp: Sum={sum_exp_4}, Count={count_exp_4}, Colors={colors_exp_4}")
print(f"Ex4 Count Match: {count_sel_4 == count_exp_4}")
print(f"Ex4 Colors Match: {colors_sel_4 == colors_exp_4}")

