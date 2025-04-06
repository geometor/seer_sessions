## Perception of Elements

The task involves transforming a 2D grid of single digits into another grid of the same dimensions. The transformation rule appears to be consistent across all examples but depends on the statistical properties (specifically, digit frequencies) of the *entire* input grid. Each cell's transformation is determined by whether its digit belongs to a dynamically calculated "stable set". All digits not in the stable set are replaced by a constant digit, 7.

## Documented Facts


```yaml
task_elements:
  - name: input_grid
    type: 2D array of integers (0-9)
  - name: output_grid
    type: 2D array of integers (0-9)
    description: Same dimensions as input_grid.
  - name: transformation_rule
    type: conditional replacement
    description: Replaces certain digits based on global grid statistics.
  - name: stable_set
    type: set of integers
    description: Digits that remain unchanged during transformation. Determined by frequency analysis.
  - name: replacement_value
    type: integer
    value: 7
    description: The constant digit used to replace non-stable digits.

relationships:
  - type: determination
    source: input_grid
    target: stable_set
    details: The stable_set is determined by the frequency distribution of digits within the input_grid.
  - type: transformation
    input: input_grid cell value
    condition: cell value NOT IN stable_set
    output: replacement_value (7)
  - type: transformation
    input: input_grid cell value
    condition: cell value IN stable_set
    output: input_grid cell value (no change)

stable_set_determination:
  - step: Calculate frequency of each digit (0-9) in the input_grid.
  - step: Identify M, the smallest digit with the highest frequency.
  - step: Identify D2, the smallest digit with the second highest frequency.
  - step: Initialize stable_set S = {1}.
  - step: If M is not 1, add M to S.
  - step: Add D2 to S.
```


## Natural Language Program

1.  Analyze the input grid to count the frequency of each digit from 0 to 9.
2.  Determine the digit `M` that occurs most frequently. If multiple digits share the highest frequency, choose the smallest among them.
3.  Determine the digit `D2` that occurs second most frequently. If multiple digits share the second highest frequency, choose the smallest among them.
4.  Define a set of "stable" digits, `S`. Start by adding the digit `1` to `S`.
5.  If the most frequent digit `M` is different from `1`, add `M` to the stable set `S`.
6.  Add the second most frequent digit `D2` to the stable set `S`. (Note: `S` automatically handles duplicates if `D2` is already present).
7.  Construct the output grid by examining each digit in the input grid:
    *   If the input digit is present in the stable set `S`, keep the digit unchanged in the corresponding position in the output grid.
    *   If the input digit is *not* present in the stable set `S`, place the digit `7` in the corresponding position in the output grid.