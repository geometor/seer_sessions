
## train_1

**input:**
```
4 4 4 4 4 7 7
4 7 7 7 4 7 5
4 7 1 7 4 7 5
4 7 7 7 4 7 7
4 4 4 4 4 7 5
7 7 7 7 7 7 5
5 5 5 5 5 7 7
```


**output:**
```
7 7 7 7 7 7 4 4 4 4
7 7 5 5 5 7 4 4 4 4
7 7 5 5 5 7 4 4 4 4
1 7 5 5 5 7 4 4 4 4
```


## train_2

**input:**
```
9 9 9 9
7 7 9 7
9 9 9 9
7 7 7 7
7 6 7 6
7 6 7 6
7 7 7 7
```


**output:**
```
7 7 7 9 9 9
6 6 7 9 9 9
6 6 7 9 9 9
```

**INSTRUCTIONS**

above is an example pair for a task

this is your opportunity to perceive the underlying logic that transforms the
input into the output

respond with the following deliverables:

- your perception of the elements of the task
- a YAML block documenting facts - Focus on identifying objects, their properties, actions performed on them, and the relationships between them
- a natural language program - Be as clear and concise as possible, providing a complete description of the transformation rule.


your responses should be considered as information in a report - not a conversation
*code_execution_result:*
outcome: OUTCOME_OK
```
counts_1=Counter({np.int64(7): 23, np.int64(4): 16, np.int64(5): 9, np.int64(1): 1})
counts_2=Counter({np.int64(7): 15, np.int64(9): 9, np.int64(6): 4})

```
        *   Train 1: Counts: 7 (23), 4 (16), 5 (9), 1 (1). The least frequent digit is 1. The output contains a '1'. Let's assume the "target" digits are 1 and 5 (least frequent non-7/4?). Or maybe just the single '1'?
        *   Train 2: Counts: 7 (15), 9 (9), 6 (4). The least frequent digit is 6. Rows containing 6 were selected.
    2.  Select input rows containing the target digit(s).
        *   Train 2: Target digit = 6. Select Rows 4 and 5 (`7 6 7 6`, `7 6 7 6`).
    3.  Select one representative row containing the second most frequent digit (or maybe the most frequent non-background digit)?
        *   Train 2: Second most frequent = 9. Rows 0, 2 contain only 9s. Row 1 contains 9s. Most frequent = 7. Rows 3, 6 contain only 7s. Let's select Row 3 (`7 7 7 7`) as the representative row for the most frequent digit (7).
    4.  Order the selected rows: Representative row first, then rows with the target digit.
        *   Train 2: `[Row 3, Row 4, Row 5]` -> `[ (7 7 7 7), (7 6 7 6), (7 6 7 6) ]`
    5.  Determine the padding digit: The digit that is *not* the most frequent and *not* the target digit.
        *   Train 2: Most frequent = 7, Target = 6. Padding = 9.
    6.  Determine the output width: Seems fixed for the example? Or maybe related to input width + padding length? Output width = 6.
    7.  For each selected row:
        a.  Extract elements equal to the target digit.
        b.  Extract elements equal to the most frequent digit.
        c.  Concatenate the target digits, then the first N most frequent digits such that the total length doesn't exceed some value (maybe input width?).
        d.  Pad the result with the padding digit to the final output width.
    *   Let's re-test Train 2 with this refined logic:
        *   Target=6, Most Frequent=7, Padding=9, Output Width=6.
        *   Selected rows: `[ (7 7 7 7), (7 6 7 6), (7 6 7 6) ]`
        *   Row `7 7 7 7`:
            *   Target digits (6): `[]`
            *   Most Frequent digits (7): `[7, 7, 7, 7]`
            *   Concatenate: `[] + [7, 7, 7]` (take first 3?) = `7 7 7`. Length = 3.
            *   Pad with 9s to width 6: `7 7 7 9 9 9`. (Matches Output Row 0). Need to define how many '7's to take. Maybe related to the count of non-target digits? Or just fill up to a certain length? Let's try: take all target digits, then take non-target digits until length = 3 (output width / 2?).
        *   Row `7 6 7 6`:
            *   Target digits (6): `[6, 6]`
            *   Most Frequent digits (7): `[7, 7]`
            *   Concatenate (targets first): `[6, 6] + [7]` (take first non-target until length 3) = `6 6 7`. Length = 3.
            *   Pad with 9s to width 6: `6 6 7 9 9 9`. (Matches Output Rows 1, 2).

*   **Apply refined Hypothesis to Train 1:**
    *   Counts: 7 (23), 4 (16), 5 (9), 1 (1).
    *   Target digit(s): Least frequent = 1. Maybe also 5? Let's try just 1 first.
    *   Row containing 1: Row 2 (`4 7 1 7 4 7 5`).
    *   Most Frequent digit = 7.
    *   Representative row for 7? Rows 5 (`7 7 7 7 7 7 5`) contains mostly 7s. Row 3 (`4 7 7 7 4 7 7`) contains many 7s. Row 1 (`4 7 7 7 4 7 5`). What defines the representative row? Maybe the one with the *most* 7s? Row 5 has six 7s.
    *   Let's assume Row 5 is the representative for 7.
    *   What about 4 (second most frequent)? Row 0 (`4 4 4 4 4 7 7`), Row 4 (`4 4 4 4 4 7 5`). Let's take Row 0.
    *   What about 5 (third most frequent)? Row 6 (`5 5 5 5 5 7 7`).
    *   This selection logic is getting complicated. Let's rethink.

*   **Hypothesis 9: Focus on structure identified by specific digits.**
    *   Train 1: The digit '1' appears at (2, 2). The digit '5' appears at (1, 6), (2, 6), (4, 6), (5, 6), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4).
    *   The output grid has a '1' at (3, 0).
    *   The output grid has '5's at (1, 2), (1, 3), (1, 4), (2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4). This forms a 3x3 block of 5s.
    *   Input Grid:
        
```
        4 4 4 4 4 7 7
        4 7 7 7 4 7 5
        4 7 1 7 4 7 5
        4 7 7 7 4 7 7
        4 4 4 4 4 7 5
        7 7 7 7 7 7 5
        5 5 5 5 5 7 7
        ```

    *   Output Grid:
        
```
        7 7 7 7 7 7 4 4 4 4
        7 7 5 5 5 7 4 4 4 4
        7 7 5 5 5 7 4 4 4 4
        1 7 5 5 5 7 4 4 4 4
        ```

    *   Maybe the transformation involves finding the '1', extracting a region around it, and combining it with other regions?
    *   The '1' is at (2, 2). Let's look at a 4x4 window centered roughly around it, perhaps starting from (r-1, c-1)? Let's try starting at (1, 1):
        
```
        7 7 7 4
        7 1 7 4
        7 7 7 4
        4 4 4 4
        ```

        This is 4x4. Doesn't look like the output directly.
    *   What if we select columns based on some criteria?
        *   Column 2 contains the '1'. `4 7 1 7 4 7 5`
        *   Column 6 contains '5's. `7 5 5 7 5 5 7`
        *   Column 0 contains '5' at the end. `4 4 4 4 4 7 5`
        *   Column 5 contains only '7's. `7 7 7 7 7 7 7`
        *   Column 1 contains '7's and '4'. `4 7 7 7 4 7 5`
    *   Let's look at the output columns again:
        *   `7 7 7 1` (Col 0)
        *   `7 7 7 7` (Col 1)
        *   `5 5 5 5` (Cols 2, 3, 4 - transposed?) No, it's `7 7 5 5 5...`
        *   Output columns:
            *   Col 0: `7 7 7 1`
            *   Col 1: `7 7 7 7`
            *   Col 2: `7 5 5 5`
            *   Col 3: `7 5 5 5`
            *   Col 4: `7 5 5 5`
            *   Col 5: `7 7 7 7`
            *   Col 6: `4 4 4 4`
            *   Col 7: `4 4 4 4`
            *   Col 8: `4 4 4 4`
            *   Col 9: `4 4 4 4`
    *   Notice the repetition in the output: `[7 5 5 5]` repeats 3 times (cols 2-4), `[7 7 7 7]` appears twice (cols 1, 5), `[4 4 4 4]` repeats 4 times (cols 6-9). Col 0 (`7 7 7 1`) is unique.
    *   Let's look at input columns, focusing on rows 1-4 (since output has 4 rows):
        *   Col 0 (rows 1-4): `4 4 4 4` -> relates to output cols 6-9
        *   Col 1 (rows 1-4): `7 7 7 4`
        *   Col 2 (rows 1-4): `7 1 7 4`
        *   Col 3 (rows 1-4): `7 7 7 4`
        *   Col 4 (rows 1-4): `4 4 4 4` -> relates to output cols 6-9
        *   Col 5 (rows 1-4): `7 7 7 7` -> relates to output cols 1, 5
        *   Col 6 (rows 1-4): `5 5 7 5` -> relates to output cols 2-4? Contains 5s.
    *   What if we take specific input columns based on their content in rows 1-4?
        *   Column containing '1' (Col 2): `7 1 7 4`. Let's call this C1.
        *   Column containing '5's (Col 6): `5 5 7 5`. Let's call this C5.
        *   Column containing only '7's (Col 5): `7 7 7 7`. Let's call this C7.
        *   Column containing only '4's (Col 0 or 4): `4 4 4 4`. Let's call this C4.
    *   Output construction attempt:
        *   Output Col 0: `7 7 7 1`. This looks like C1 (`7 1 7 4`) rearranged or modified. Maybe `[C1[0], C1[2], C7[0], C1[1]]`? -> `[7, 7, 7, 1]`. Yes.
        *   Output Col 1: `7 7 7 7`. This is C7.
        *   Output Col 2: `7 5 5 5`. Looks like `[C7[0], C5[0], C5[1], C5[3]]`? -> `[7, 5, 5, 5]`. Yes.
        *   Output Col 3: `7 5 5 5`. Same as Col 2.
        *   Output Col 4: `7 5 5 5`. Same as Col 2.
        *   Output Col 5: `7 7 7 7`. This is C7.
        *   Output Col 6: `4 4 4 4`. This is C4.
        *   Output Col 7: `4 4 4 4`. This is C4.
        *   Output Col 8: `4 4 4 4`. This is C4.
        *   Output Col 9: `4 4 4 4`. This is C4.
    *   This requires identifying specific columns based on their content within a specific row range (rows 1-4).
        *   Identify the unique digit (1) within rows 1-4. Find its column (Col 2). Extract rows 1-4 from this column: `C1 = [7, 1, 7, 4]`.
        *   Identify the digit 5 within rows 1-4. Find its column (Col 6). Extract rows 1-4 from this column: `C5 = [5, 5, 7, 5]`.
        *   Identify a column with only the most frequent digit (7) in rows 1-4 (Col 5). Extract rows 1-4: `C7 = [7, 7, 7, 7]`.
        *   Identify a column with only the second most frequent digit (4) in rows 1-4 (Col 0 or 4). Extract rows 1-4: `C4 = [4, 4, 4, 4]`.
        *   Assemble the output columns using rearranged/selected elements from C1, C5, C7, C4 as derived above.

*   **Apply Hypothesis 9 to Train 2:**
    *   Input: 7x4 grid. Output: 3x6 grid.
    *   Input rows:
        *   Row 0: `9 9 9 9`
        *   Row 1: `7 7 9 7`
        *   Row 2: `9 9 9 9`
        *   Row 3: `7 7 7 7`
        *   Row 4: `7 6 7 6`
        *   Row 5: `7 6 7 6`
        *   Row 6: `7 7 7 7`
    *   Output:
        
```
        7 7 7 9 9 9
        6 6 7 9 9 9
        6 6 7 9 9 9
        ```

    *   The output height is 3. Let's focus on a 3-row slice of the input. Which rows? Maybe rows containing the least frequent digit (6)? Rows 4, 5. And one other? Row 3? Let's try rows 3, 4, 5.
    *   Input slice (rows 3, 4, 5):
        
```
        7 7 7 7
        7 6 7 6
        7 6 7 6
        ```

    *   Unique digit in this slice: 6. Most frequent: 7.
    *   Identify columns based on content within this slice:
        *   Column containing 6 (Col 1 or 3). Let's take Col 1: `C6 = [7, 6, 6]`.
        *   Column containing only 7 (Col 0 or 2). Let's take Col 0: `C7 = [7, 7, 7]`.
        *   (No other digits in this slice).
    *   What about padding? The padding digit was 9. Where does 9 come from? It's the digit present in rows *outside* the slice (e.g., Row 0, 1, 2). Let's define `C9 = [9, 9, 9]` (taking 3 elements as output height is 3).
    *   Output construction attempt (Target width 6):
        *   Output Col 0: `7 6 6`. This is C6 rearranged? `[C6[0], C6[1], C6[2]]`? No. `[C7[0], C6[1], C6[2]]`? -> `[7, 6, 6]`. Yes.
        *   Output Col 1: `7 6 6`. Same as Col 0.
        *   Output Col 2: `7 7 7`. This is C7.
        *   Output Col 3: `9 9 9`. This is C9.
        *   Output Col 4: `9 9 9`. This is C9.
        *   Output Col 5: `9 9 9`. This is C9.
    *   Assemble these columns:
        
```
        7 7 7 9 9 9  (Row 0)
        6 6 7 9 9 9  (Row 1)
        6 6 7 9 9 9  (Row 2)
        ```

        This matches the output!

*   **Consolidated Steps:**
    1.  Determine the output grid dimensions (H_out, W_out). (Seems fixed per task? Output H=4, W=10 for T1; H=3, W=6 for T2). Let's assume they are derived. How?
        *   Maybe H_out = number of rows containing the "target" digits + 1 (for the representative most frequent)?
            *   T1: Target=1 (Row 2), Target=5 (Rows 1, 2, 4, 5, 6). Unique rows containing targets = 1, 2, 4, 5, 6. Plus representative for 7 (Row 5?) and 4 (Row 0?). This is too many.
            *   T2: Target=6 (Rows 4, 5). Representative for 7 (Row 3?). H_out = 2 + 1 = 3. Matches.
        *   Maybe W_out = derived somehow?
    2.  Let's reconsider the row selection. In T2, we selected rows 3, 4, 5. Rows 4, 5 contained the target (6). Row 3 was above them and contained only the most frequent (7).
    3.  In T1, target is 1 (Row 2). Rows containing 5 (Rows 1, 2, 4, 5, 6). Row 6 contains only 5s (and 7s). Row 2 contains 1 and 5.
        *   Output is 4 rows. Maybe select row with 1 (Row 2), rows with 5s (Rows 1, 6?), and row with 7s (Row 5)?
        *   Let's revisit the previous successful approach for T1: focus on input rows 1-4. `H_out = 4`.
        *   Rows 1-4:
            
```
            4 7 7 7 4 7 5
            4 7 1 7 4 7 5
            4 7 7 7 4 7 7
            4 4 4 4 4 7 5
            ```

        *   Digits present: 1, 4, 5, 7.
        *   Unique digit: 1 (in Col 2). `C1 = [7, 1, 7, 4]` (Values from Col 2, Rows 1-4).
        *   Other "special" digit: 5 (in Col 6). `C5 = [5, 5, 7, 5]` (Values from Col 6, Rows 1-4).
        *   Most frequent digit: 7. Column with only 7s? Col 5. `C7 = [7, 7, 7, 7]` (Values from Col 5, Rows 1-4).
        *   Second most frequent digit: 4. Column with only 4s? Col 0 or 4. `C4 = [4, 4, 4, 4]` (Values from Col 0/4, Rows 1-4).
        *   Padding digit? Not needed if we construct full width? Output width W=10.
        *   Output construction:
            *   Col 0: `[C1[0], C1[2], C7[0], C1[1]]` = `[7, 7, 7, 1]`
            *   Col 1: C7 = `[7, 7, 7, 7]`
            *   Col 2: `[C7[0], C5[0], C5[1], C5[3]]` = `[7, 5, 5, 5]`
            *   Col 3: Repeat Col 2 = `[7, 5, 5, 5]`
            *   Col 4: Repeat Col 2 = `[7, 5, 5, 5]`
            *   Col 5: C7 = `[7, 7, 7, 7]`
            *   Col 6: C4 = `[4, 4, 4, 4]`
            *   Col 7: C4 = `[4, 4, 4, 4]`
            *   Col 8: C4 = `[4, 4, 4, 4]`
            *   Col 9: C4 = `[4, 4, 4, 4]`
        *   Assemble:
            
```
            7 7 7 7 7 7 4 4 4 4
            7 7 5 5 5 7 4 4 4 4
            7 7 5 5 5 7 4 4 4 4
            1 7 5 5 5 7 4 4 4 4   <- Transposed? No, read row by row.
            ```

            Let's re-read the assembly:
            Row 0: `7 7 7 7 7 7 4 4 4 4` (Matches)
            Row 1: `1 7 5 5 5 7 4 4 4 4` (Doesn't match output row 1: `7 7 5 5 5 7 4 4 4 4`)
            Row 2: `7 7 5 5 5 7 4 4 4 4` (Matches output row 2)
            Row 3: `4 7 5 5 5 7 4 4 4 4` (Doesn't match output row 3: `1 7 5 5 5 7 4 4 4 4`)

*   **Mistake in Deriving Output Columns for T1:**
    *   Output:
        
```
        7 7 7 7 7 7 4 4 4 4
        7 7 5 5 5 7 4 4 4 4
        7 7 5 5 5 7 4 4 4 4
        1 7 5 5 5 7 4 4 4 4
        ```

    *   Let's re-derive the required columns based on the *actual* output:
        *   Out Col 0: `[7, 7, 7, 1]`
        *   Out Col 1: `[7, 7, 7, 7]`
        *   Out Col 2: `[7, 5, 5, 5]`
        *   Out Col 3: `[7, 5, 5, 5]`
        *   Out Col 4: `[7, 5, 5, 5]`
        *   Out Col 5: `[7, 7, 7, 7]`
        *   Out Col 6: `[4, 4, 4, 4]`
        *   Out Col 7: `[4, 4, 4, 4]`
        *   Out Col 8: `[4, 4, 4, 4]`
        *   Out Col 9: `[4, 4, 4, 4]`
    *   Input slice (Rows 1-4):
        
```
        4 7 7 7 4 7 5
        4 7 1 7 4 7 5
        4 7 7 7 4 7 7
        4 4 4 4 4 7 5
        ```

    *   `C1 = [7, 1, 7, 4]` (Col 2)
    *   `C5 = [5, 5, 7, 5]` (Col 6)
    *   `C7 = [7, 7, 7, 7]` (Col 5)
    *   `C4 = [4, 4, 4, 4]` (Col 0 or 4)
    *   Reconstruction again:
        *   Out Col 0 `[7, 7, 7, 1]`. How to get this from C1, C5, C7, C4? Maybe `[C7[0], C7[1], C5[2], C1[1]]`? -> `[7, 7, 7, 1]`. Yes.
        *   Out Col 1 `[7, 7, 7, 7]`. C7. Yes.
        *   Out Col 2 `[7, 5, 5, 5]`. Maybe `[C1[0], C5[0], C5[1], C6[3]]`? -> `[7, 5, 5, 5]`. Yes.
        *   Out Col 3: Repeat Col 2. Yes.
        *   Out Col 4: Repeat Col 2. Yes.
        *   Out Col 5: C7. Yes.
        *   Out Col 6: C4. Yes.
        *   Out Col 7: C4. Yes.
        *   Out Col 8: C4. Yes.
        *   Out Col 9: C4. Yes.
    *   This seems consistent now. The key is to select the right input rows, identify columns based on content within those rows, potentially rearrange/select elements from those columns, and assemble them (with repetition/padding) into the output grid.

*   **Final Logic Formulation:**
    1.  Determine the relevant slice of the input grid (a subset of rows).
        *   T1: Rows 1-4. (Output height is 4).
        *   T2: Rows 3-5. (Output height is 3).
        *   Rule: Find rows containing the least frequent non-background digit(s). Take these rows and potentially some adjacent rows (like the one above the first target row if it's monochromatic?). Or maybe just take a fixed number of rows (H_out) starting from the row containing the first instance of the rarest digit? Or starting from row 1? Needs clarification, but for now, assume rows 1 to H_out for T1 and rows 3 to 3+H_out-1 for T2. Let's assume the slice height is fixed for the task (4 for T1, 3 for T2). For T1, the slice is rows 1-4. For T2, the slice is rows 3-5.
    2.  Identify "key" digits within this slice:
        *   The most frequent digit (MFD). (T1: 7, T2: 7)
        *   The second most frequent digit (SMFD). (T1: 4, T2: N/A within slice?)
        *   The "unique" or least frequent digit(s) (LFD). (T1: 1, 5; T2: 6)
    3.  Identify representative columns within the slice:
        *   `C_MFD`: A column containing only MFD. (T1: Col 5 -> [7,7,7,7], T2: Col 0 -> [7,7,7])
        *   `C_SMFD`: A column containing only SMFD. (T1: Col 0 -> [4,4,4,4], T2: N/A)
        *   `C_LFD1`: Column containing the primary LFD. (T1: Col 2 -> [7,1,7,4], T2: Col 1 -> [7,6,6])
        *   `C_LFD2`: Column containing another LFD (if applicable). (T1: Col 6 -> [5,5,7,5], T2: N/A)
    4.  Determine the "padding" digit (PD) if needed. (T2: 9). This seems to be a digit present prominently outside the chosen slice.
    5.  Determine the output dimensions (H_out, W_out). H_out is the slice height. W_out seems fixed (10 for T1, 6 for T2).
    6.  Construct the output columns using elements from the representative input columns (C_MFD, C_SMFD, C_LFD1, C_LFD2) and potentially the padding digit (PD). The exact construction involves specific indexing and repetition rules derived from the examples.
        *   T1: Columns 0-9 constructed using C7, C4, C1, C5 based on specific index combinations and repetition.
        *   T2: Columns 0-5 constructed using C7, C6, and C9 (padding column `[9,9,9]`) based on specific index combinations and repetition.

*   **Structuring the Output:**
    *   Perception: Input is a grid, output is a grid with different dimensions. The transformation involves selecting a horizontal slice of the input, identifying columns within that slice based on the digits they contain, and rearranging/selecting elements from those columns, potentially padding/repeating them, to form the columns of the output grid.
    *   Facts (YAML): Focus on objects (grid, slice, columns, digits), properties (dimensions, frequency, location, values), and actions (select slice, identify digits, find columns, extract elements, rearrange, repeat, construct output).
    *   Natural Language Program: Describe the steps outlined in "Final Logic Formulation".## Perception

The user provided two examples (`train_1`, `train_2`) of a task transforming an input grid of digits into an output grid of digits.

1.  **Grid Transformation:** The core task is transforming an input grid into an output grid.
2.  **Dimension Change:** The dimensions (height and width) of the grid change between input and output.
    *   `train_1`: 7x7 input -> 4x10 output
    *   `train_2`: 7x4 input -> 3x6 output
3.  **Content Preservation/Rearrangement:** The digits present in the output grid are also present in the input grid, but they are significantly rearranged. New digits do not appear to be introduced, except potentially through a padding mechanism determined by the input.
4.  **Slice Selection:** The transformation seems to focus on a specific horizontal slice (subset of rows) from the input grid. The height of the output grid corresponds to the height of this slice.
    *   `train_1`: Output height is 4. The relevant input slice appears to be rows 1-4.
    *   `train_2`: Output height is 3. The relevant input slice appears to be rows 3-5.
5.  **Column Identification:** Within the selected input slice, specific columns are identified based on the digits they contain. Key columns seem to be those containing:
    *   Only the most frequent digit within the slice.
    *   Only the second most frequent digit within the slice (if applicable).
    *   A unique or rare digit within the slice.
6.  **Output Construction:** The output grid is constructed column by column. Each output column is derived from:
    *   Elements of the identified input columns (potentially rearranged or selected based on index).
    *   Repetition of previously constructed columns.
    *   Potentially padding with a digit determined from the input (often a digit prominent outside the selected slice).
7.  **Key Digits:** The process relies on identifying digits based on their frequency or uniqueness within the selected input slice.

## Facts


```yaml
task_elements:
  - object: input_grid
    properties:
      - type: 2D array of integers
      - dimensions: H_in x W_in (variable)
      - content: digits
  - object: output_grid
    properties:
      - type: 2D array of integers
      - dimensions: H_out x W_out (variable, derived from input)
      - content: digits (derived from input)
  - object: input_slice
    properties:
      - type: subgrid of input_grid (contiguous rows)
      - dimensions: H_out x W_in
      - location: determined by specific criteria (e.g., location of rare digits, fixed offset)
  - object: key_digits
    properties:
      - type: specific integer values
      - identified_based_on: frequency or uniqueness within input_slice
      - examples: most_frequent_digit (MFD), second_most_frequent_digit (SMFD), least_frequent_digit(s) (LFD)
  - object: representative_columns
    properties:
      - type: specific columns extracted from input_slice
      - dimensions: H_out x 1
      - selection_criteria: contain specific key_digits (e.g., column with only MFD, column containing LFD)
      - examples: C_MFD, C_SMFD, C_LFD1, C_LFD2
  - object: padding_digit
    properties:
      - type: integer value
      - determination: based on digits prominent outside the input_slice (if needed for output width)
actions:
  - select_slice:
      input: input_grid
      output: input_slice
      logic: Identify relevant rows (height H_out) based on input content (e.g., finding LFD).
  - identify_key_digits:
      input: input_slice
      output: key_digits (MFD, SMFD, LFDs)
      logic: Analyze digit frequencies within the slice.
  - find_representative_columns:
      input: input_slice, key_digits
      output: representative_columns (C_MFD, C_SMFD, C_LFDs)
      logic: Scan columns of the slice to find ones matching criteria based on key_digits.
  - determine_padding_digit:
      input: input_
