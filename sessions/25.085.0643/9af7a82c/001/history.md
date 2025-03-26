
## train_1

**input:**
```
8 8 2
3 8 8
3 3 4
3 3 4
```


**output:**
```
3 8 4 2
3 8 4 0
3 8 0 0
3 8 0 0
3 0 0 0
```


## train_2

**input:**
```
3 1 1 4
2 2 2 4
4 4 4 4
```


**output:**
```
4 2 1 3
4 2 1 0
4 2 0 0
4 0 0 0
4 0 0 0
4 0 0 0
```


## train_3

**input:**
```
1 1 1
2 2 1
2 8 1
2 8 1
```


**output:**
```
1 2 8
1 2 8
1 2 0
1 2 0
1 0 0
1 0 0
```


## train_4

**input:**
```
2 2 1
2 3 1
1 1 1
```


**output:**
```
1 2 3
1 2 0
1 2 0
1 0 0
1 0 0
```

Okay, let's analyze the provided examples.

**Perception**

1.  **Input & Output Grids:** The task takes a small input grid and produces a potentially larger output grid. The output grid's dimensions seem dependent on the content of the input grid, specifically the colors present and their frequencies.
2.  **Color Analysis:** The core operation seems to involve analyzing the non-white (non-zero) colors within the input grid. White pixels (0) in the input seem to be ignored.
3.  **Counting:** The frequency (count) of each unique non-white color in the input grid appears crucial.
4.  **Sorting:** The unique non-white colors seem to be sorted based on certain criteria to determine the structure of the output. Observing the examples suggests a primary sort key of frequency (descending) and a secondary sort key of color value (ascending).
5.  **Output Structure:** The output grid resembles a vertical histogram or bar chart.
    *   **Columns:** Each column in the output corresponds to one of the unique non-white colors found in the input, ordered according to the sorting rule identified above.
    *   **Column Content:** Each column `j` (corresponding to sorted color `C`) is filled from the top with `N` pixels of color `C`, where `N` is the total count of color `C` in the *entire* input grid. The remaining cells below these `N` pixels in that column are filled with white (0).
    *   **Dimensions:**
        *   The width of the output grid is equal to the number of unique non-white colors in the input.
        *   The height of the output grid seems related to the maximum frequency (`MaxCount`) of any single color. Specifically, it appears to be `MaxCount` if `MaxCount` is greater than or equal to half the total number of cells in the input grid (`InputHeight * InputWidth / 2`), and `MaxCount + 1` otherwise.

**Facts**


```yaml
Input:
  type: grid
  properties:
    - contains pixels of various colors (0-9)
    - dimensions vary (height H, width W)

Output:
  type: grid
  properties:
    - derived from input grid's color counts and sorting
    - width equals the number of unique non-white colors in the input
    - height depends on the maximum color count (MaxCount) and input dimensions (H, W):
        - height = MaxCount if MaxCount >= (H * W / 2)
        - height = MaxCount + 1 otherwise
    - contains vertical bars representing sorted colors
    - background color is white (0)

Transformation:
  - name: Color Frequency Histogram Generation
  - steps:
    1. Identify all unique non-white colors present in the input grid.
    2. Count the total occurrences (frequency) of each unique non-white color across the entire input grid.
    3. Determine the maximum frequency (MaxCount) among all counted colors.
    4. Calculate the output grid height:
       - If MaxCount >= (InputHeight * InputWidth / 2), OutputHeight = MaxCount.
       - Otherwise, OutputHeight = MaxCount + 1.
    5. Sort the unique non-white colors based on two criteria:
       - Primary: Frequency (descending).
       - Secondary: Color value (ascending). Let the sorted list be SortedColors.
    6. Determine the output grid width: OutputWidth = number of unique non-white colors (length of SortedColors).
    7. Create an empty output grid of size OutputHeight x OutputWidth, filled with white (0).
    8. Iterate through the SortedColors list. For each color C at index j (0-based):
       - Retrieve its frequency N from the counts determined in step 2.
       - Fill the first N cells (rows 0 to N-1) of column j in the output grid with color C.
```


**Natural Language Program**

1.  Scan the input grid and identify all unique colors that are not white (0).
2.  For each unique non-white color found, count how many times it appears in the input grid. Store these colors and their counts.
3.  Find the highest count among all colors (`MaxCount`).
4.  Calculate a threshold value equal to half the total number of cells in the input grid (input height times input width, divided by 2).
5.  Determine the height of the output grid: if `MaxCount` is greater than or equal to the threshold, the output height is `MaxCount`; otherwise, the output height is `MaxCount + 1`.
6.  Arrange the unique non-white colors in a specific order: first, sort them from highest count to lowest count. If two colors have the same count, sort them by their color value from lowest to highest. This ordered list determines the sequence of columns in the output.
7.  Determine the width of the output grid: it is equal to the total number of unique non-white colors found in step 1.
8.  Create a new grid with the calculated output height and width, initially filled entirely with white (0) pixels.
9.  For each color in the sorted list (from step 6), starting with the first:
    a.  Take the corresponding column in the output grid (the first color corresponds to the first column, the second color to the second column, and so on).
    b.  Retrieve the count for this color (from step 2).
    c.  Fill the top cells of that column with the color, using a number of cells equal to its count. Leave the remaining cells below (if any) as white (0).
10. The resulting grid is the final output.
