
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 4 4 0 0
0 0 4 0 0 0 0 0 4 0
0 4 0 4 0 0 0 4 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 0
0 0 4
0 4 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1
0 0 0 5 0 0 0 1 1 0
0 0 0 1 0 0 0 0 1 0
0 0 1 1 1 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 1 1 0 0
```


**output:**
```
0 1 0
1 1 1
0 1 1
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 5 0 0
0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2
2 2 0
0 2 0
```

Okay, let's break down the task.

**Perception of Elements:**

1.  **Input/Output Grids:** The task takes a 10x10 grid of single digits as input and produces a 3x3 grid of single digits as output.
2.  **Digits:** The grids contain digits 0-9. '0' appears to be a background color/digit.
3.  **Special Digit '5':** Each input grid contains exactly one digit '5'. This digit seems crucial, likely acting as a marker or reference point.
4.  **Target Digit:** Each input grid also contains multiple instances of another non-zero digit (4 in train_1, 1 in train_2, 2 in train_3). This digit is the *only* non-zero digit present in the corresponding output grid. This suggests it's the primary digit of interest, the 'target digit'.
5.  **Frequency:** Observing the inputs, the target digit (4, 1, or 2) is the most frequent non-zero digit *besides* the single '5'.
6.  **Transformation:** The core task is extracting a specific 3x3 region from the input and filtering it. The location of the '5' determines *which* 3x3 region is extracted, and the filtering process keeps only the identified 'target digit'.
7.  **Extraction Logic:** By comparing the location of the '5' in the input to the content of the output, it appears the output 3x3 grid is extracted from the input starting one row below and one column to the left of the '5's location.
8.  **Filtering Logic:** After extracting the 3x3 subgrid, any digit within it that is *not* the target digit is replaced with '0'.

**YAML Facts:**


```yaml
task_elements:
  - Input Grid:
      type: 2D array of integers
      size: 10x10
      properties:
        - Contains digits 0-9.
        - Contains exactly one instance of the digit 5.
        - Contains multiple instances of one other non-zero digit (target_digit).
        - Digit 0 acts as background.
  - Output Grid:
      type: 2D array of integers
      size: 3x3
      properties:
        - Contains only digit 0 and the target_digit from the input.
  - Marker Digit:
      value: 5
      role: Defines the reference point for extraction.
  - Target Digit:
      role: The primary digit to be preserved in the output.
      identification: The most frequent non-zero digit in the input, excluding the marker digit 5.
  - Background Digit:
      value: 0
      role: Fills empty space in input and non-target cells in output.
actions:
  - Find Marker: Locate the row (r5) and column (c5) of the digit 5 in the input grid.
  - Identify Target: Count frequencies of non-zero digits (excluding 5) to find the target_digit.
  - Calculate Extraction Origin: Determine the top-left corner (r_out, c_out) for the 3x3 extraction using the marker location: r_out = r5 + 1, c_out = c5 - 1.
  - Extract Subgrid: Copy the 3x3 portion of the input grid starting at (r_out, c_out).
  - Filter Subgrid: Create the output grid by iterating through the extracted 3x3 subgrid. Keep cells matching the target_digit; replace all others with 0.
relationships:
  - The position of the marker digit 5 dictates the position of the 3x3 subgrid extracted from the input.
  - The identity of the target digit dictates which values are preserved in the final output grid.
```


**Natural Language Program:**

1.  Examine the 10x10 input grid to find the row `r5` and column `c5` where the digit '5' is located.
2.  Determine the `target_digit` by identifying which non-zero digit (other than '5') occurs most frequently in the input grid.
3.  Calculate the starting row and column for extraction: `start_row = r5 + 1`, `start_col = c5 - 1`.
4.  Extract the 3x3 subgrid from the input grid, covering rows `start_row` to `start_row + 2` and columns `start_col` to `start_col + 2`.
5.  Initialize an empty 3x3 output grid filled with '0's.
6.  Iterate through each cell of the extracted 3x3 subgrid. If a cell's value is equal to the `target_digit`, place the `target_digit` in the corresponding position in the output grid. Otherwise, leave the '0'.
7.  Return the final 3x3 output grid.
