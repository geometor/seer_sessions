
## train_1

**input:**
```
0 0 0 5 0 2 0 5 2 0 0
2 0 0 5 0 0 0 5 0 0 2
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
2 0 0 5 0 0 0 5 0 0 0
2 0 0 5 0 0 2 5 0 0 0
0 0 0 5 0 0 0 5 0 2 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
2 0 0 5 0 0 2 5 0 0 2
0 0 0 5 0 0 0 5 0 0 0
```


**output:**
```
0 0 0 5 0 0 0 5 2 2 2
0 0 0 5 0 0 0 5 2 2 2
0 0 0 5 0 0 0 5 2 2 2
5 5 5 5 5 5 5 5 5 5 5
2 2 2 5 0 0 0 5 0 0 0
2 2 2 5 0 0 0 5 0 0 0
2 2 2 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
```


## train_2

**input:**
```
0 0 0 5 0 0 0 5 0 0 0
1 0 0 5 0 0 0 5 0 1 0
0 0 0 5 0 0 1 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 1 5 0 0 0
0 0 0 5 0 0 0 5 0 1 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 1 0 0
0 1 0 5 0 0 0 5 0 0 1
0 0 0 5 0 0 0 5 0 0 0
```


**output:**
```
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 1 1 1
0 0 0 5 0 0 0 5 1 1 1
0 0 0 5 0 0 0 5 1 1 1
```


## train_3

**input:**
```
3 3 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 3 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 3 0 5 0 3 0 5 0 0 0
0 0 0 5 3 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 3 0 5 3 0 0 5 3 3 0
0 0 0 5 0 0 0 5 0 0 3
```


**output:**
```
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 3 3 3
0 0 0 5 0 0 0 5 3 3 3
0 0 0 5 0 0 0 5 3 3 3
```

Okay, let's analyze the task examples.

**Perception of Elements:**

1.  **Grid Structure:** All input and output grids are 11x11.
2.  **Background/Scaffolding:** A consistent structure of gray (5) lines exists in both input and output. Specifically, row 3, row 7, column 3, and column 7 are entirely gray. These lines divide the grid into nine 3x3 subgrids.
3.  **Objects/Colors:** Within the 3x3 subgrids, there are pixels of white (0) and one other distinct color per example (Red=2 in train\_1, Blue=1 in train\_2, Green=3 in train\_3). Let's call this the "dominant color".
4.  **Input State:** In the input grids, the dominant color pixels are scattered across various positions within the nine subgrids.
5.  **Output State:** In the output grids, the gray scaffolding remains unchanged. All pixels within one or two specific 3x3 subgrids are replaced entirely by the dominant color found in the input. All other subgrids (excluding the scaffolding) are filled with white (0).
6.  **Transformation:** The task involves identifying the dominant color, determining a target subgrid (or subgrids) based on the input configuration, and then consolidating all instances of the dominant color into those target subgrid(s) in the output.

**YAML Facts:**


```yaml
Grid_Dimensions:
  Input: [11, 11]
  Output: [11, 11]
Structural_Elements:
  - Type: Scaffolding
    Color: Gray (5)
    Location:
      Rows: [3, 7]
      Columns: [3, 7]
    Persistence: Unchanged between input and output
  - Type: Subgrids
    Quantity: 9
    Dimensions: [3, 3]
    Definition: Areas partitioned by the Gray scaffolding
Dynamic_Elements:
  - Type: Pixel_Set
    Name: Dominant_Color_Pixels
    Properties:
      Color: Varies per example (Red=2, Blue=1, Green=3), but only one type per grid (excluding Gray and White).
      Location_Input: Scattered within various Subgrids.
      Location_Output: Consolidated into one or two specific Subgrids, filling them completely.
    Relationships:
      - The specific Dominant_Color determines the transformation rule variation.
      - The location of the *last* instance (read-order) of a Dominant_Color pixel in the input determines the target Subgrid(s) for consolidation in the output, potentially modified by the color itself.
  - Type: Pixel_Set
    Name: Background_Pixels
    Properties:
      Color: White (0)
      Location_Input: Fills Subgrid areas not occupied by Dominant_Color_Pixels.
      Location_Output: Fills Subgrid areas not targeted for consolidation and not part of the scaffolding.
Transformation_Rule_Dependency:
  - Condition: Dominant_Color is Red (2)
    Action: Fills Subgrids TR (Top-Right) and ML (Middle-Left) in the output.
  - Condition: Dominant_Color is NOT Red (2)
    Action: Finds the Subgrid containing the last occurring pixel (read-order) of the Dominant_Color in the input, and fills that specific Subgrid in the output.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the "dominant color" present in the input grid, which is the single color other than gray (5) and white (0).
3.  Find the row and column index of the *last* occurrence of the dominant color pixel when scanning the input grid row by row from top to bottom, and column by column from left to right within each row.
4.  Determine the target 3x3 subgrid(s) based on the dominant color:
    *   If the dominant color is Red (2), the target subgrids are the Top-Right (rows 0-2, cols 8-10) and Middle-Left (rows 4-6, cols 0-2).
    *   If the dominant color is *not* Red (2), determine the single 3x3 subgrid that contains the last pixel identified in step 3. This is the target subgrid. The subgrids are defined by the gray lines (indices 0-2, 4-6, 8-10 for both rows and columns).
5.  Iterate through all nine 3x3 subgrids defined by the gray scaffolding:
    *   If a subgrid is one of the target subgrids identified in step 4, fill all nine pixels within that subgrid with the dominant color.
    *   If a subgrid is *not* a target subgrid, fill all nine pixels within that subgrid with white (0).
6.  Ensure the gray scaffolding pixels (rows 3, 7 and columns 3, 7) remain gray (5) in the final output grid.
