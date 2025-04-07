## Perception

The task involves processing a grid of integers. Each input grid is characterized by the presence of horizontal and vertical bands composed entirely of zeros, effectively dividing the grid into four distinct quadrants (Top-Left, Top-Right, Bottom-Left, Bottom-Right). These quadrants contain sub-patterns of non-zero numbers, potentially alongside zeros. The output is always a subgrid corresponding exactly to one of these four quadrants. The core challenge is to identify the dividing zero bands and then determine the specific rule used to select which of the four quadrants becomes the output. The selection logic appears based on the numerical values present within the quadrants.

## Facts


```yaml
- item: Input Grid
  properties:
    - type: 2D array of integers
    - structure: Contains four main quadrants separated by bands of zeros.
    - elements: Integers, including zero and other non-zero values.
    - zero_bands:
        - horizontal: One or more contiguous rows containing only zeros.
        - vertical: One or more contiguous columns containing only zeros.
        - function: Separate the grid into four quadrants.

- item: Quadrants
  properties:
    - count: 4 (Top-Left, Top-Right, Bottom-Left, Bottom-Right)
    - definition: Regions of the grid defined by the boundaries of the zero bands.
    - content: Subsets of the input grid's numbers.

- item: Output Grid
  properties:
    - type: 2D array of integers
    - relationship_to_input: Is an exact copy of one of the four quadrants from the input grid.

- item: Transformation Rule
  properties:
    - goal: Select one quadrant from the input grid.
    - steps:
        1.  Identify the largest contiguous block of all-zero rows (horizontal band). Record start row index `hr_start` and end row index `hr_end`.
        2.  Identify the largest contiguous block of all-zero columns (vertical band). Record start column index `vc_start` and end column index `vc_end`.
        3.  Define the four quadrants based on these indices:
            - TL: `input[0:hr_start, 0:vc_start]`
            - TR: `input[0:hr_start, vc_end+1:]`
            - BL: `input[hr_end+1:, 0:vc_start]`
            - BR: `input[hr_end+1:, vc_end+1:]`
        4.  Determine the set of unique non-zero numbers present in each quadrant.
        5.  Identify which non-zero numbers appear in *only one* of the four quadrants.
        6.  If such unique numbers exist:
            - Find the maximum value among these uniquely located numbers.
            - Select the quadrant containing this maximum unique value.
        7.  If no number is unique to a single quadrant:
            - Find the overall maximum non-zero value (`M`) present anywhere in the input grid.
            - Identify all quadrants that contain this value `M`.
            - Apply a tie-breaker based on quadrant position: Bottom-Right > Bottom-Left > Top-Right > Top-Left.
            - Select the highest-priority quadrant among those containing `M`.
    - output: The selected quadrant.

```


## Natural Language Program

1.  **Parse the Input:** Read the input grid into a 2D data structure (e.g., a list of lists or a NumPy array).
2.  **Locate Zero Bands:**
    a.  Find the largest contiguous block of rows where all elements are zero. Determine the starting row index (`hr_start`) and ending row index (`hr_end`) of this block.
    b.  Find the largest contiguous block of columns where all elements are zero. Determine the starting column index (`vc_start`) and ending column index (`vc_end`) of this block.
3.  **Define Quadrants:** Using the indices found in step 2, define the four subgrids corresponding to the Top-Left (TL), Top-Right (TR), Bottom-Left (BL), and Bottom-Right (BR) quadrants.
    *   TL: Rows 0 to `hr_start - 1`, Columns 0 to `vc_start - 1`.
    *   TR: Rows 0 to `hr_start - 1`, Columns `vc_end + 1` to end.
    *   BL: Rows `hr_end + 1` to end, Columns 0 to `vc_start - 1`.
    *   BR: Rows `hr_end + 1` to end, Columns `vc_end + 1` to end.
4.  **Analyze Quadrant Contents:**
    a.  For each quadrant, create a set of its unique non-zero integer values.
    b.  Identify all non-zero values present across the entire grid.
    c.  For each non-zero value, determine in which quadrants it appears.
5.  **Identify Unique Values:** Create a list of numbers that appear in exactly one quadrant.
6.  **Select Quadrant based on Uniqueness:**
    a.  If the list of uniquely located numbers is not empty:
        i.  Find the maximum value (`max_unique`) in this list.
        ii. Identify the single quadrant that contains `max_unique`. This is the target quadrant.
    b.  If the list of uniquely located numbers is empty (i.e., all non-zero numbers appear in multiple quadrants or no non-zero numbers exist):
        i.  Find the overall maximum non-zero value (`M`) present in the input grid.
        ii. Create a list of quadrants that contain this value `M`.
        iii. Apply a priority rule to select the target quadrant from this list: BR has the highest priority, followed by BL, then TR, then TL.
7.  **Generate Output:** Return the subgrid corresponding to the target quadrant identified in step 6.