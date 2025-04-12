**Perception:**

The task involves analyzing a 2D grid of integers and extracting a smaller pattern, either a single integer (1x1) or a 2x2 grid. The core logic appears to revolve around the frequency of occurrence of subgrids (patterns) within the input grid, specifically focusing on 1x1 and 2x2 non-zero patterns. The choice between outputting a 1x1 or 2x2 pattern seems to depend on whether a unique least frequent 2x2 pattern exists, and potentially on the size of the input grid. When multiple patterns share the same frequency (either minimum or maximum depending on the condition), specific tie-breaking rules based on position or value are needed.

**Facts:**

```yaml
task_elements:
  - object: input_grid
    properties:
      - type: 2D array of integers
      - dimensions: variable (e.g., 4x4, 5x5, 7x7)
      - values: non-negative integers, including 0
  - object: output_pattern
    properties:
      - type: 2D array of integers (subgrid) or single integer
      - dimensions: 1x1 or 2x2
      - source: extracted or derived from input_grid
      - constraint: appears to consist of non-zero numbers from the input
actions:
  - action: analyze_subgrids
    description: Identify and count occurrences of subgrids within the input grid.
    parameters:
      - size: 1x1 or 2x2
      - constraint: consider only subgrids composed entirely of non-zero numbers
  - action: find_frequency
    description: Determine the frequency of each unique subgrid.
  - action: find_minimum_frequency
    description: Identify the minimum frequency among specified subgrids (e.g., non-zero 1x1, non-zero 2x2).
  - action: find_maximum_frequency
    description: Identify the maximum frequency among specified subgrids (e.g., non-zero 2x2).
  - action: select_pattern
    description: Choose the output pattern based on frequency analysis and grid size.
    logic: involves comparison of minimum/maximum frequencies and tie-breaking rules.
  - action: apply_tie_breaking
    description: Resolve cases where multiple patterns meet the selection criteria.
    rules:
      - for minimum frequency 2x2 (F=1): select the pattern whose top-left corner occurs bottom-most, then right-most.
      - for minimum frequency 1x1: select the largest numerical value.
      - for maximum frequency 2x2 (F>1, size>4x4): select the pattern whose *first* top-left corner occurrence is bottom-most, then left-most.
relationships:
  - relationship: frequency_determines_output
    description: The frequency (minimum or maximum) of non-zero subgrids (1x1 or 2x2) is the primary factor in determining the output pattern.
  - relationship: size_determines_rule
    description: The dimensions of the input grid can influence which frequency rule (minimum vs maximum) and which pattern size (1x1 vs 2x2) is prioritized.
  - relationship: frequency_value_determines_priority
    description: A minimum frequency of 1 for 2x2 non-zero patterns takes precedence. Otherwise, grid size and other frequency comparisons dictate the logic.
```

**Natural Language Program:**

1.  Identify all unique 2x2 subgrids within the input grid that consist solely of non-zero numbers. If no such subgrids exist, proceed directly to step 4a.
2.  Count the frequency of occurrence for each unique non-zero 2x2 subgrid found in step 1. Determine the minimum frequency (`F_min_2x2`) among these counts. Identify the pattern(s) (`P_min_2x2`) associated with this minimum frequency.
3.  If `F_min_2x2` is exactly 1:
    a.  Select the single pattern `P_min_2x2` corresponding to this frequency.
    b.  If there are multiple patterns with frequency 1 (tie), select the one whose top-left corner appears latest in the grid (scan top-to-bottom, then left-to-right; choose the last one encountered).
    c.  Output the selected 2x2 pattern.
4.  If `F_min_2x2` is greater than 1, OR if no non-zero 2x2 subgrids were found in step 1, check the input grid dimensions (Rows x Columns). If Rows <= 4 and Columns <= 4:
    a.  Identify all unique non-zero numbers (1x1 patterns) in the input grid.
    b.  Count the frequency of each unique non-zero number. Determine the minimum frequency (`F_min_1x1`) among these counts. Identify the number(s) (`P_min_1x1`) associated with this minimum frequency.
    c.  Select the number `P_min_1x1` corresponding to the minimum frequency.
    d.  If there are multiple numbers with the same minimum frequency (tie), select the largest numerical value among them.
    e.  Output the selected 1x1 number.
5.  If `F_min_2x2` is greater than 1 AND the input grid dimensions are larger than 4x4 (either Rows > 4 or Columns > 4):
    a.  Using the unique non-zero 2x2 subgrids and their frequencies calculated in steps 1 and 2, determine the maximum frequency (`F_max_2x2`) among them. Identify the pattern(s) (`P_max_2x2`) associated with this maximum frequency.
    b.  Select the pattern `P_max_2x2` corresponding to the maximum frequency.
    c.  If there are multiple patterns with the same maximum frequency (tie), compare their first occurrences in the input grid (scan top-to-bottom, left-to-right). Select the pattern whose first occurrence has the largest row index. If there's still a tie in row index, select the one with the smallest column index among those tied rows.
    d.  Output the selected 2x2 pattern.