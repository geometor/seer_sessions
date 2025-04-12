## Perception

1.  **Input/Output Structure:** The input is a grid of numbers (15 columns wide, variable rows). The output is also a grid of numbers (7 columns wide, same number of rows as the input).
2.  **Separator Column:** Column index 7 (the 8th column) in the input grid consistently contains the digit '4' and appears to function as a separator between two regions of the input: the left region (columns 0-6) and the right region (columns 8-14).
3.  **Output Source:** The output grid seems primarily derived from the right region (columns 8-14) of the input grid.
4.  **Conditional Logic:** There appears to be a conditional rule based on the content of the right region (columns 8-14) of each input row.
    *   **Condition 1:** If the right region of an input row contains *any* non-zero digits, the corresponding output row is a direct copy of that right region.
    *   **Condition 2:** If the right region of an input row contains *only* zeros, the corresponding output row is derived from the left region (columns 0-6) of the input row through a more complex transformation.
5.  **Rule 2 Transformation (R=0 case):** When the right region is all zeros, the transformation of the left region involves identifying patterns or segments of non-zero numbers within the left 7 columns. The specific output generated seems to depend on the pattern found (e.g., `[2 2 2]`, `[3 3 3]`, `[6]`, `[1 1]`), often involving a change in the digit used (e.g., `2`s become `1`s, `6`s become `3`s, `1`s become `2`s) and potentially a shift in position or change in shape/length. The exact rules for this transformation appear complex and possibly context-dependent or based on a specific mapping key not immediately obvious.

## YAML Facts

```yaml
Grid:
  Input:
    Type: 2D array of integers
    Dimensions:
      Rows: variable (N)
      Columns: 15
    Structure:
      Left_Region: Columns 0-6
      Separator: Column 7 (Value typically '4')
      Right_Region: Columns 8-14
  Output:
    Type: 2D array of integers
    Dimensions:
      Rows: N (same as input)
      Columns: 7
Relationship: Row-wise transformation from Input to Output
TransformationRule:
  Type: Conditional
  Condition: Check if Input.Right_Region for the current row contains any non-zero values.
  Case_1: # Right_Region has non-zero values
    Action: Copy Input.Right_Region to the corresponding Output row.
  Case_2: # Right_Region contains only zero values
    Action:
      - Analyze Input.Left_Region for the current row.
      - Identify specific patterns or segments of non-zero digits within Input.Left_Region.
      - Generate the Output row based on the identified pattern(s).
      - This generation may involve:
          - Selecting a specific pattern from Input.Left_Region.
          - Mapping the pattern's digits to new digits (e.g., 2->1, 6->3, 1->2).
          - Arranging the transformed digits into the 7-column Output row, possibly with positional shifts or shape changes.
      - The precise mapping/transformation for Case_2 seems specific to the task patterns.
```

## Natural Language Program

1.  Initialize an empty output grid with the same number of rows as the input grid and 7 columns.
2.  For each row in the input grid (from top to bottom):
    a.  Extract the left region (columns 0 through 6).
    b.  Extract the right region (columns 8 through 14).
    c.  Check if any digit in the extracted right region is non-zero.
    d.  **If** the right region contains at least one non-zero digit:
        i.  Copy the right region directly into the corresponding row of the output grid.
    e.  **Else** (the right region contains only zeros):
        i.  Analyze the pattern of non-zero digits in the extracted left region.
        ii. Determine the appropriate 7-digit output sequence based on the specific pattern found in the left region (this involves a predefined transformation rule specific to the patterns encountered in this task, potentially changing digits and their arrangement).
        iii. Place this generated 7-digit sequence into the corresponding row of the output grid.
3.  Return the completed output grid.