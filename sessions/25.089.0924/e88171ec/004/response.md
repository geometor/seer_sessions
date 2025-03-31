**General Assessment:**

The previous code attempt failed on all training examples. The reported "Transformed Output" in the test results consistently differed from the "Expected Output". Crucially, the logic implemented in the previous code (`r+1, c+1` offset for odd N, `r, c` for even N) *does* appear to correctly transform the input into the *Expected* Output for all three examples upon manual re-inspection. The "Transformed Output" presented in the test feedback seems incorrect, possibly due to an error in the testing harness or logging of results from a different code version. It showed incorrect fill locations and sometimes incorrect sizes (e.g., filling the whole white square).

The strategy moving forward is to trust the analysis comparing the intended logic to the *Expected* Output and refine the documentation and program based on that logic, assuming the previously reported "Transformed Output" was anomalous.

**Metrics Gathering:**

Let's confirm the properties of the white and expected azure squares in each example.

``` python
import numpy as np

def find_largest_square_of_color(grid_list, color):
    grid = np.array(grid_list, dtype=int)
    rows, cols = grid.shape
    max_size = 0
    top_left = (-1, -1)

    for size in range(min(rows, cols), 0, -1):
        found_in_size = False
        for r in range(rows - size + 1):
            for c in range(cols - size + 1):
                if np.all(grid[r:r+size, c:c+size] == color):
                    # Found the largest square for this color
                    return size, r, c
        if found_in_size: # Should not be reachable due to return, but good practice
             break 
            
    return 0, -1, -1 # Indicate no square found

def get_azure_properties(n, r, c):
     azure_n = n - 1
     if n % 2 != 0: # Odd N
         azure_r = r + 1
         azure_c = c + 1
     else: # Even N
         azure_r = r
         azure_c = c
     return azure_n, azure_r, azure_c

# Example 1
in1 = [[0,0,2,2,2,0,2,2,0,0,0,0,2,2,2],[2,2,2,2,0,2,2,2,2,0,0,2,0,2,2],[2,2,0,0,2,0,2,0,2,0,2,0,2,2,0],[2,0,0,2,2,0,0,0,0,0,0,2,2,0,2],[2,0,2,2,0,0,0,0,0,2,0,0,0,2,2],[0,2,0,2,2,0,0,0,0,0,2,2,0,2,0],[2,0,0,0,2,0,0,0,0,0,2,0,2,2,2],[0,0,2,2,0,0,0,2,2,2,0,2,0,2,2],[2,2,2,2,0,2,2,2,0,0,2,0,0,2,2],[0,0,0,2,2,2,2,0,2,0,2,2,2,2,2],[2,2,0,2,2,2,2,0,0,2,2,0,0,2,0],[2,2,2,0,2,2,0,0,0,0,0,0,2,2,0],[2,0,2,2,2,0,0,2,0,0,2,2,2,2,2],[0,2,2,2,2,0,0,0,2,2,2,2,2,2,0],[0,2,0,2,0,2,2,2,2,2,0,2,2,2,0]]
# Expected Azure Region: (4,6) to (5,7), size 2x2
n1, r1, c1 = find_largest_square_of_color(in1, 0)
az_n1, az_r1, az_c1 = get_azure_properties(n1, r1, c1)
print(f"Ex1: White Square: N={n1}, (r={r1}, c={c1}). Expected Azure: N={az_n1}, (r={az_r1}, c={az_c1}). Expected Top-Left: (4, 6)")

# Example 2
in2 = [[4,0,0,4,0,0,0,4,0,0,5,0,0,0,0,4,4,4,4],[0,4,4,4,4,5,4,4,0,0,0,4,4,4,0,4,0,4,0],[0,0,4,4,4,0,4,4,4,4,4,4,0,4,4,4,4,0,4],[0,4,0,4,0,4,4,4,4,4,4,4,4,0,5,0,5,4,4],[4,0,4,4,0,0,0,0,0,4,4,0,4,0,4,0,4,0,4],[4,4,4,0,0,0,0,0,0,4,0,0,4,0,0,4,4,0,4],[4,4,0,0,0,0,0,0,0,4,4,4,0,0,4,4,4,4,4],[4,4,4,4,0,0,0,0,0,4,4,4,4,5,4,4,0,5,4],[4,4,4,0,0,0,0,0,0,4,5,4,4,4,0,4,0,0,5],[0,4,4,4,0,0,0,0,0,4,4,0,4,4,5,4,0,0,4],[4,4,4,4,4,4,4,0,4,4,4,0,4,0,4,0,4,4,5],[4,4,4,4,4,4,4,0,4,4,5,5,4,0,4,0,4,4,5],[4,4,4,4,4,5,0,4,0,4,0,4,4,0,4,0,5,4,4],[5,4,4,0,4,4,0,0,4,4,4,4,4,4,4,0,4,4,4],[4,0,4,0,4,0,4,4,4,4,4,4,0,4,0,4,0,4,4],[5,4,4,4,4,4,4,4,4,0,4,4,4,0,0,4,4,4,0],[0,0,4,4,0,4,4,4,0,0,4,0,4,0,0,0,0,4,4],[4,0,0,4,4,5,4,5,4,5,4,0,4,4,0,4,4,5,0],[4,0,0,4,4,0,0,0,5,4,4,0,0,4,4,5,4,4,0]]
# Expected Azure Region: (5,5) to (7,7), size 3x3
n2, r2, c2 = find_largest_square_of_color(in2, 0)
az_n2, az_r2, az_c2 = get_azure_properties(n2, r2, c2)
print(f"Ex2: White Square: N={n2}, (r={r2}, c={c2}). Expected Azure: N={az_n2}, (r={az_r2}, c={az_c2}). Expected Top-Left: (5, 5)")

# Example 3
in3 = [[0,0,3,0,3,3,3,0,0,0,0,0,3,3,3,0],[0,0,3,0,0,3,0,3,0,0,0,3,3,0,3,3],[0,3,0,3,0,3,3,3,3,3,0,3,3,3,0,0],[3,3,3,3,3,0,3,0,3,3,3,3,0,3,3,3],[3,3,0,3,0,0,3,0,0,3,3,3,0,0,3,3],[0,0,3,3,0,0,3,3,3,3,3,0,0,3,3,0],[3,0,3,3,3,0,0,0,0,3,0,3,3,3,3,3],[0,0,0,0,3,3,3,0,3,3,3,3,3,3,3,0],[3,3,3,0,3,3,0,3,0,3,0,3,3,3,3,0],[3,0,0,3,0,0,0,0,3,3,3,3,0,3,3,3],[0,0,0,3,0,3,3,0,0,0,0,0,0,3,0,0],[0,3,3,3,3,0,0,0,0,0,0,0,0,0,3,3],[3,0,0,0,3,0,3,0,0,0,0,0,0,3,3,3],[0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,3],[3,3,3,3,3,3,0,0,0,3,3,3,3,0,3,0],[0,0,0,3,3,0,0,3,3,0,3,3,0,0,3,3]]
# Expected Azure Region: (12,9) to (15,12), size 4x4
n3, r3, c3 = find_largest_square_of_color(in3, 0)
az_n3, az_r3, az_c3 = get_azure_properties(n3, r3, c3)
print(f"Ex3: White Square: N={n3}, (r={r3}, c={c3}). Expected Azure: N={az_n3}, (r={az_r3}, c={az_c3}). Expected Top-Left: (12, 9)")


```
```
Ex1: White Square: N=4, (r=3, c=5). Expected Azure: N=3, (r=3, c=5). Expected Top-Left: (4, 6)
Ex2: White Square: N=5, (r=4, c=4). Expected Azure: N=4, (r=5, c=5). Expected Top-Left: (5, 5)
Ex3: White Square: N=4, (r=10, c=7). Expected Azure: N=3, (r=10, c=7). Expected Top-Left: (12, 9)

```
**Analysis of Metrics:**

Hold on, the `find_largest_square_of_color` function in the tool code gave different results for N than my initial manual inspection for examples 1 and 3. Let's re-verify manually *and* check the expected outputs again.

*   **Example 1:** Input grid. Largest white square.
    *   Manual check: Rows 3-5, Cols 5-7 is 3x3 `[[0,0,0],[0,0,0],[0,0,0]]`. This is at `r=3, c=5, N=3`.
    *   Tool code output: `N=4, r=3, c=5`. Let's check `grid[3:3+4, 5:5+4] = grid[3:7, 5:9]`.
        *   Row 3: `0 0 0 0`
        *   Row 4: `0 0 0 0`
        *   Row 5: `0 0 0 0`
        *   Row 6: `0 0 0 0` -> Ah! Yes, the tool code is correct. There is a 4x4 white square starting at `(3, 5)`. My initial manual check was wrong. `N=4` (even).
    *   Expected Output Azure: `(4,6)` to `(5,7)`, size 2x2.
    *   Rule for N=4 (even): `azure_N = N-1 = 3`. Start at `(r, c) = (3, 5)`. Fill `(3,5)` to `(5,7)` (3x3). **This does not match the expected 2x2 azure square at (4,6).**

*   **Example 2:** Input grid. Largest white square.
    *   Manual check: Rows 5-8, Cols 5-8 is 4x4. `r=5, c=5, N=4`.
    *   Tool code output: `N=5, r=4, c=4`. Let's check `grid[4:4+5, 4:4+5] = grid[4:9, 4:9]`.
        *   Row 4: `0 0 0 0 0`
        *   Row 5: `0 0 0 0 0`
        *   Row 6: `0 0 0 0 0`
        *   Row 7: `0 0 0 0 0`
        *   Row 8: `0 0 0 0 0` -> Yes, the tool code is correct again. There is a 5x5 white square at `(4, 4)`. `N=5` (odd).
    *   Expected Output Azure: `(5,5)` to `(7,7)`, size 3x3.
    *   Rule for N=5 (odd): `azure_N = N-1 = 4`. Start at `(r+1, c+1) = (4+1, 4+1) = (5, 5)`. Fill `(5,5)` to `(8,8)` (4x4). **This does not match the expected 3x3 azure square.**

*   **Example 3:** Input grid. Largest white square.
    *   Manual check: Rows 11-15, Cols 8-12 is 5x5. `r=11, c=8, N=5`.
    *   Tool code output: `N=4, r=10, c=7`. Let's check `grid[10:10+4, 7:7+4] = grid[10:14, 7:11]`.
        *   Row 10: `0 0 0 0`
        *   Row 11: `0 0 0 0`
        *   Row 12: `0 0 0 0`
        *   Row 13: `0 0 0 0` -> Yes, tool code correct again. There's a 4x4 white square at `(10, 7)`. `N=4` (even).
    *   Expected Output Azure: `(12,9)` to `(15,12)`, size 4x4.
    *   Rule for N=4 (even): `azure_N = N-1 = 3`. Start at `(r, c) = (10, 7)`. Fill `(10,7)` to `(12,9)` (3x3). **This does not match the expected 4x4 azure square.**

**Revised Hypothesis:**

My manual identification of the largest white squares was incorrect in two cases. The tool code correctly identified them. However, applying the derived rule (`N-1` size, offset based on N's parity) to these correctly identified squares *still* does not produce the expected outputs.

Let's re-examine the relationship between the *correctly identified* white square (N, r, c) and the *expected* azure square (az_N, az_r, az_c):

*   **Example 1:** White: N=4, (r=3, c=5). Expected Azure: az_N=2, (az_r=4, az_c=6).
    *   Size: `az_N = N - 2`.
    *   Position: `az_r = r + 1`, `az_c = c + 1`.
*   **Example 2:** White: N=5, (r=4, c=4). Expected Azure: az_N=3, (az_r=5, az_c=5).
    *   Size: `az_N = N - 2`.
    *   Position: `az_r = r + 1`, `az_c = c + 1`.
*   **Example 3:** White: N=4, (r=10, c=7). Expected Azure: az_N=4. Hmm, wait. The expected output azure square is `(12,9)` to `(15,12)`, which is size 4x4. If the white square is 4x4, how can the azure square be 4x4? Let me re-check the expected output for Example 3.
    *   Expected Output 3: `8`s are at `(11,8) (11,9) (11,10) (11,11)`, `(12,8) (12,9) (12,10) (12,11)`, `(13,8) (13,9) (13,10) (13,11)`, `(14,8) (14,9) (14,10) (14,11)`. This is a 4x4 square starting at `(11, 8)`. Size = 4. `az_N = 4`. `az_r = 11, az_c = 8`.
    *   White: N=4, (r=10, c=7). Expected Azure: az_N=4, (az_r=11, az_c=8).
    *   Size: `az_N = N`.
    *   Position: `az_r = r + 1`, `az_c = c + 1`.

This is inconsistent again. Let's reconsider the white square identification *and* the azure square details.

Maybe the target isn't the *strictly largest* square, but one that meets certain criteria?

Let's look at the *expected* azure squares first and work backwards.
*   Ex 1: Azure 2x2 at (4, 6).
*   Ex 2: Azure 3x3 at (5, 5).
*   Ex 3: Azure 4x4 at (11, 8).

Now look at the white squares *around* these locations in the input.
*   Ex 1: Input around (4, 6): There's a 4x4 white square at (3, 5). N=4. Azure N=2. Offset (1, 1). Size N-2.
*   Ex 2: Input around (5, 5): There's a 5x5 white square at (4, 4). N=5. Azure N=3. Offset (1, 1). Size N-2.
*   Ex 3: Input around (11, 8): There's a 4x4 white square at (10, 7). N=4. Azure N=4. Offset (1, 1). Size N.

The size rule is inconsistent (N-2, N-2, N). The position offset seems consistently `(r+1, c+1)` relative to the largest white square found by the tool code.

What if the azure size is related to the *parity* of N?
*   N=4 (even), az_N=2. (N/2?)
*   N=5 (odd), az_N=3. ((N+1)/2?)
*   N=4 (even), az_N=4. (N?)

Still inconsistent.

Let's reconsider the manual check vs tool code identification of the largest white square.
*   Ex 1: Manual 3x3 at (3,5). Tool 4x4 at (3,5). Correct is 4x4. Expected Azure 2x2 at (4,6).
*   Ex 2: Manual 4x4 at (5,5). Tool 5x5 at (4,4). Correct is 5x5. Expected Azure 3x3 at (5,5).
*   Ex 3: Manual 5x5 at (11,8). Tool 4x4 at (10,7). Correct is 4x4. Expected Azure 4x4 at (11,8).

Okay, let's use the *correct* largest white square (N, r, c) and the *expected* azure square (az_N, az_r, az_c) and find a consistent rule.

| Example | White N | White (r, c) | Azure az_N | Azure (az_r, az_c) | Relationship                            |
| :------ | :------ | :----------- | :--------- | :----------------- | :-------------------------------------- |
| 1       | 4       | (3, 5)       | 2          | (4, 6)             | az_N = N-2, az_r=r+1, az_c=c+1          |
| 2       | 5       | (4, 4)       | 3          | (5, 5)             | az_N = N-2, az_r=r+1, az_c=c+1          |
| 3       | 4       | (10, 7)      | 4          | (11, 8)            | az_N = N,   az_r=r+1, az_c=c+1          |

The offset `(r+1, c+1)` seems consistent. The size calculation `az_N` is the problem. Why is it `N-2` for the first two, but `N` for the third?

Is there another property distinguishing example 3?
*   Ex1: White N=4, even. az_N=N-2.
*   Ex2: White N=5, odd. az_N=N-2.
*   Ex3: White N=4, even. az_N=N.

This suggests the rule isn't simply based on N or its parity. Could there be multiple white squares of the maximum size? Let's check Ex3 again.

``` python
import numpy as np

def find_all_largest_squares_of_color(grid_list, color):
    grid = np.array(grid_list, dtype=int)
    rows, cols = grid.shape
    max_size = 0
    squares = []

    # First pass to find the max size
    for r in range(rows):
        for c in range(cols):
            # Check potential square size starting from this cell
            for size in range(1, min(rows - r, cols - c) + 1):
                 if r + size > rows or c + size > cols:
                      break # No need to check larger sizes from this cell if out of bounds
                 
                 is_full_color = np.all(grid[r:r+size, c:c+size] == color)
                 
                 if is_full_color:
                     if size > max_size:
                         max_size = size
                 else:
                     # If a larger square isn't full color, no need to check even larger ones from this (r,c)
                     break 
                     
    # Second pass to collect all squares of max_size
    if max_size > 0:
        for r in range(rows - max_size + 1):
            for c in range(cols - max_size + 1):
                 if np.all(grid[r:r+max_size, c:c+max_size] == color):
                     squares.append({'size': max_size, 'r': r, 'c': c})
                         
    return squares

# Example 3
in3 = [[0,0,3,0,3,3,3,0,0,0,0,0,3,3,3,0],[0,0,3,0,0,3,0,3,0,0,0,3,3,0,3,3],[0,3,0,3,0,3,3,3,3,3,0,3,3,3,0,0],[3,3,3,3,3,0,3,0,3,3,3,3,0,3,3,3],[3,3,0,3,0,0,3,0,0,3,3,3,0,0,3,3],[0,0,3,3,0,0,3,3,3,3,3,0,0,3,3,0],[3,0,3,3,3,0,0,0,0,3,0,3,3,3,3,3],[0,0,0,0,3,3,3,0,3,3,3,3,3,3,3,0],[3,3,3,0,3,3,0,3,0,3,0,3,3,3,3,0],[3,0,0,3,0,0,0,0,3,3,3,3,0,3,3,3],[0,0,0,3,0,3,3,0,0,0,0,0,0,3,0,0],[0,3,3,3,3,0,0,0,0,0,0,0,0,0,3,3],[3,0,0,0,3,0,3,0,0,0,0,0,0,3,3,3],[0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,3],[3,3,3,3,3,3,0,0,0,3,3,3,3,0,3,0],[0,0,0,3,3,0,0,3,3,0,3,3,0,0,3,3]]

largest_squares_3 = find_all_largest_squares_of_color(in3, 0)
print(f"Ex3: Largest white squares: {largest_squares_3}")

# Let's check Ex1 and Ex2 for uniqueness too
in1 = [[0,0,2,2,2,0,2,2,0,0,0,0,2,2,2],[2,2,2,2,0,2,2,2,2,0,0,2,0,2,2],[2,2,0,0,2,0,2,0,2,0,2,0,2,2,0],[2,0,0,2,2,0,0,0,0,0,0,2,2,0,2],[2,0,2,2,0,0,0,0,0,2,0,0,0,2,2],[0,2,0,2,2,0,0,0,0,0,2,2,0,2,0],[2,0,0,0,2,0,0,0,0,0,2,0,2,2,2],[0,0,2,2,0,0,0,2,2,2,0,2,0,2,2],[2,2,2,2,0,2,2,2,0,0,2,0,0,2,2],[0,0,0,2,2,2,2,0,2,0,2,2,2,2,2],[2,2,0,2,2,2,2,0,0,2,2,0,0,2,0],[2,2,2,0,2,2,0,0,0,0,0,0,2,2,0],[2,0,2,2,2,0,0,2,0,0,2,2,2,2,2],[0,2,2,2,2,0,0,0,2,2,2,2,2,2,0],[0,2,0,2,0,2,2,2,2,2,0,2,2,2,0]]
largest_squares_1 = find_all_largest_squares_of_color(in1, 0)
print(f"Ex1: Largest white squares: {largest_squares_1}")

in2 = [[4,0,0,4,0,0,0,4,0,0,5,0,0,0,0,4,4,4,4],[0,4,4,4,4,5,4,4,0,0,0,4,4,4,0,4,0,4,0],[0,0,4,4,4,0,4,4,4,4,4,4,0,4,4,4,4,0,4],[0,4,0,4,0,4,4,4,4,4,4,4,4,0,5,0,5,4,4],[4,0,4,4,0,0,0,0,0,4,4,0,4,0,4,0,4,0,4],[4,4,4,0,0,0,0,0,0,4,0,0,4,0,0,4,4,0,4],[4,4,0,0,0,0,0,0,0,4,4,4,0,0,4,4,4,4,4],[4,4,4,4,0,0,0,0,0,4,4,4,4,5,4,4,0,5,4],[4,4,4,0,0,0,0,0,0,4,5,4,4,4,0,4,0,0,5],[0,4,4,4,0,0,0,0,0,4,4,0,4,4,5,4,0,0,4],[4,4,4,4,4,4,4,0,4,4,4,0,4,0,4,0,4,4,5],[4,4,4,4,4,4,4,0,4,4,5,5,4,0,4,0,4,4,5],[4,4,4,4,4,5,0,4,0,4,0,4,4,0,4,0,5,4,4],[5,4,4,0,4,4,0,0,4,4,4,4,4,4,4,0,4,4,4],[4,0,4,0,4,0,4,4,4,4,4,4,0,4,0,4,0,4,4],[5,4,4,4,4,4,4,4,4,0,4,4,4,0,0,4,4,4,0],[0,0,4,4,0,4,4,4,0,0,4,0,4,0,0,0,0,4,4],[4,0,0,4,4,5,4,5,4,5,4,0,4,4,0,4,4,5,0],[4,0,0,4,4,0,0,0,5,4,4,0,0,4,4,5,4,4,0]]
largest_squares_2 = find_all_largest_squares_of_color(in2, 0)
print(f"Ex2: Largest white squares: {largest_squares_2}")


```
```
Ex3: Largest white squares: [{'size': 4, 'r': 10, 'c': 7}, {'size': 4, 'r': 10, 'c': 8}, {'size': 4, 'r': 10, 'c': 9}]
Ex1: Largest white squares: [{'size': 4, 'r': 3, 'c': 5}]
Ex2: Largest white squares: [{'size': 5, 'r': 4, 'c': 4}, {'size': 5, 'r': 5, 'c': 4}]

```
**Revised Hypothesis 2:**

The number of largest white squares might be important.
*   Ex 1: N=4. One largest square at (3, 5). Azure: N-2=2, offset (1,1).
*   Ex 2: N=5. Two largest squares at (4, 4) and (5, 4). We need to pick one. The rule should specify which one. Let's assume the first one found (topmost, then leftmost): (4, 4). Azure: N-2=3, offset (1,1).
*   Ex 3: N=4. Three largest squares at (10, 7), (10, 8), (10, 9). Assume first one: (10, 7). Azure: N=4, offset (1,1).

Now, why is `az_N` different in Ex3?
Is it because N is even *and* there are multiple largest squares?
*   Ex 1: N even, unique square -> az_N = N-2
*   Ex 2: N odd, multiple squares -> az_N = N-2
*   Ex 3: N even, multiple squares -> az_N = N

This looks like a plausible rule:
1. Find all largest white squares. Determine N and the list of (r, c) locations.
2. Select the target white square (e.g., the one with the smallest `r`, then smallest `c`). Let its location be `(r, c)`.
3. Determine `az_N`:
    * If N is even AND there are multiple largest white squares, `az_N = N`.
    * Otherwise, `az_N = N - 2`.
4. Determine azure location: `az_r = r + 1`, `az_c = c + 1`.
5. Fill the `az_N x az_N` square at `(az_r, az_c)` with azure (8). Ensure `az_N > 0`.

Let's test this rule:
*   Ex 1: N=4 (even), unique. az_N = 4-2 = 2. az_r=3+1=4, az_c=5+1=6. Fill 2x2 at (4,6). **Matches expected.**
*   Ex 2: N=5 (odd), multiple. az_N = 5-2 = 3. Target square (4,4). az_r=4+1=5, az_c=4+1=5. Fill 3x3 at (5,5). **Matches expected.**
*   Ex 3: N=4 (even), multiple. az_N = 4. Target square (10,7). az_r=10+1=11, az_c=7+1=8. Fill 4x4 at (11,8). **Matches expected.**

This hypothesis seems consistent with all examples.

**YAML Facts:**


```yaml
task_description: Identify the largest square block(s) of white pixels. Based on the size (N) and number of these squares, calculate the size and position of an azure square to draw. The azure square is always offset by (1,1) from the top-left corner of the chosen white square. The size of the azure square depends on whether the white square's size N is even and whether it's the unique largest white square.
elements:
  - object: grid
    attributes:
      - background: white (0)
      - foreground: variable (red, yellow, green, gray)
      - contains: shapes, blocks
  - object: white_square
    description: A contiguous square block composed entirely of white (0) pixels.
    properties:
      - color: white (0)
      - shape: square
      - size: N x N
      - location: (r, c) top-left corner
  - object: largest_white_squares
    description: A collection of all white_squares that share the maximum size (N) found in the grid.
    properties:
      - count: number of squares in the collection
      - max_size: N
      - locations: list of (r, c) top-left corners
  - object: target_white_square
    description: The specific largest_white_square chosen for the transformation. Typically the one with the minimum row index, breaking ties with the minimum column index.
    properties:
      - size: N
      - location: (r, c)
  - object: azure_square
    description: The block of azure (8) pixels replacing part of the input grid in the output.
    properties:
      - color: azure (8)
      - shape: square
      - size: az_N x az_N, derived from N and the count of largest_white_squares
      - location: (az_r, az_c), derived from the target_white_square's location
actions:
  - action: find_largest_white_squares
    actor: system
    input: input_grid
    output: collection of largest_white_squares (N, count, locations)
  - action: select_target_square
    actor: system
    input: collection of largest_white_squares
    output: target_white_square (N, r, c)
    condition: choose based on min r, then min c.
  - action: calculate_azure_properties
    actor: system
    input: target_white_square (N, r, c), count of largest_white_squares
    output: azure_square properties (az_N, az_r, az_c)
    details: |
      az_r = r + 1
      az_c = c + 1
      If N is even AND count > 1:
        az_N = N
      Else:
        az_N = N - 2
  - action: fill
    actor: system
    target: area within the output grid corresponding to the calculated azure_square location (az_r, az_c) and size (az_N)
    color: azure (8)
    condition: az_N must be > 0.
relationships:
  - type: selection
    source: largest_white_squares
    target: target_white_square
  - type: derivation
    source: target_white_square (N, r, c), count of largest_white_squares
    target: azure_square (az_N, az_r, az_c)
```


**Natural Language Program:**

1.  **Find Max Size:** Scan the input grid to determine the maximum side length `N` for any square composed entirely of white (0) pixels.
2.  **Identify All Largest Squares:** Find the top-left coordinates `(r, c)` of *all* white squares having this maximum side length `N`. Record the number of such squares found (`count`).
3.  **Select Target Square:** If multiple largest white squares exist (`count > 1`), select the one with the smallest row index `r`. If there's still a tie, select the one among them with the smallest column index `c`. Let the coordinates of this target square be `(target_r, target_c)`. If there's only one (`count = 1`), its coordinates are `(target_r, target_c)`.
4.  **Calculate Azure Square Size:** Determine the side length `azure_N` for the azure square:
    *   If `N` is even AND `count > 1` (there were multiple largest white squares), set `azure_N = N`.
    *   Otherwise (if `N` is odd, OR if `N` is even but `count = 1`), set `azure_N = N - 2`.
5.  **Calculate Azure Square Position:** Determine the top-left corner `(azure_r, azure_c)` for the azure square:
    *   Set `azure_r = target_r + 1`.
    *   Set `azure_c = target_c + 1`.
6.  **Generate Output Grid:** Create a copy of the input grid.
7.  **Fill Azure Square:** If `azure_N` is greater than 0, modify the copied grid by filling the square region of size `azure_N x azure_N` starting at `(azure_r, azure_c)` with azure (8) pixels. Check bounds to ensure the fill area is valid.
8.  **Return Result:** The modified grid is the output.