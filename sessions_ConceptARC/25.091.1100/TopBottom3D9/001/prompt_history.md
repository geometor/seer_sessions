
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 0
1 1 1 3 3 3 3 1 1 1
1 1 1 3 3 3 3 1 1 1
1 1 1 3 3 3 3 1 1 1
0 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
0 1 1 1 1 1 1 1 1 0
0 1 1 1 1 1 1 1 1 0
0 1 1 1 1 1 1 1 1 0
0 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
2 2 4 4 4 4 4 4 4 4 4 4 2 2
2 2 2 2 0 0 0 0 0 0 2 2 2 2
2 2 2 2 0 0 0 0 0 0 2 2 2 2
2 2 2 2 0 0 0 0 0 0 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 0 0 0 0 0 0 4 4 4 4
4 4 4 4 0 0 0 0 0 0 4 4 4 4
4 4 4 4 0 0 0 0 0 0 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 0
0 0 0 6 6 6 6 6 6 6 0
0 0 0 6 6 6 6 6 6 6 0
0 0 0 6 6 6 6 6 6 6 0
0 0 0 6 6 6 6 6 6 6 0
0 0 0 6 6 6 6 8 8 8 8
0 0 0 6 6 6 6 8 8 8 8
0 0 0 6 6 6 6 8 8 8 8
0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 8 8 8 8 8 8 8 8
0 0 0 8 8 8 8 8 8 8 8
0 0 0 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Perception of Elements

1.  **Grid Structure:** The inputs and outputs are 2D grids of pixels.
2.  **Colors:** Each task involves exactly three colors: a background color (white, 0) and two distinct non-background colors.
3.  **Objects:** The non-background colors form contiguous or near-contiguous regions (objects) within the grid. These regions are adjacent to each other. The background color forms the main canvas and potentially small isolated regions (holes) within the non-background objects.
4.  **Transformation:** The core transformation involves a color replacement. One of the two non-background colors completely replaces the other non-background color in the output grid. The background color remains unchanged.
5.  **Distinguishing Feature:** The key is to determine which non-background color replaces the other. This depends on specific properties of the color regions:
    *   **Hole Enclosure:** In one example (train\_2), one color region (yellow, 4) completely surrounds an internal region of the background color (a "hole"). This seems to be a deciding factor.
    *   **Pixel Count:** In the absence of such a hole, the relative pixel counts of the two non-background colors appear to determine the replacement rule.

## YAML Facts


```yaml
task_elements:
  common:
    - grid_representation: 2D array of integers (colors).
    - background_color: White (0) consistently present and mostly framing the content. Remains unchanged in output.
    - number_of_non_background_colors: Exactly two distinct colors per input grid.
    - transformation_type: Color replacement affecting only the non-background colors.
  entities:
    - object: Background
      properties:
        - color: 0 (White)
        - role: Canvas, Frame, Potential Hole Filler
    - object: Color Region 1 (C1)
      properties:
        - color: Varies (e.g., Blue(1), Red(2), Magenta(6))
        - count: Number of pixels of this color.
        - spatial_relation: Adjacent to Background and Color Region 2.
        - topology: May or may not surround a Background Hole.
    - object: Color Region 2 (C2)
      properties:
        - color: Varies (e.g., Green(3), Yellow(4), Azure(8))
        - count: Number of pixels of this color.
        - spatial_relation: Adjacent to Background and Color Region 1.
        - topology: May or may not surround a Background Hole.
    - object: Background Hole (Optional)
      properties:
        - color: 0 (White)
        - location: Completely surrounded by pixels of C1 or C2. Not connected to the outer Background.
  actions:
    - identify_colors: Find the Background color and the two non-background colors (C1, C2).
    - check_hole_enclosure: Determine if C1 exclusively surrounds a Background Hole, or if C2 does.
    - count_pixels: Calculate the number of pixels for C1 and C2.
    - compare_counts: Determine which color has maximum/minimum pixel count.
    - replace_color: Change pixels of one non-background color to the other non-background color based on the determined rule.
  rules_observed:
    - rule_1 (Hole Presence): If one non-background color (e.g., C_hole) exclusively surrounds a Background Hole, replace the other non-background color (C_other) with C_hole.
    - rule_2 (No Hole): If neither non-background color exclusively surrounds a Background Hole, find the color with the maximum pixel count (C_max) and the color with the minimum pixel count (C_min). Replace C_max with C_min.
```


## Natural Language Program

1.  Identify the three unique pixel colors present in the input grid. One is the background color (typically white, 0), and the other two are non-background colors (let's call them Color A and Color B).
2.  Examine the input grid to determine if any region of background-colored pixels exists that is *not* connected to the main outer background frame and is completely surrounded *only* by pixels of Color A. Perform the same check for Color B.
3.  **Condition 1: Hole Enclosure:** If exactly one non-background color (e.g., Color A) exclusively surrounds such a background hole, then the transformation rule is: Replace all pixels of Color B with Color A.
4.  **Condition 2: No Exclusive Hole Enclosure:** If neither Color A nor Color B exclusively surrounds a background hole (or if both do, or the hole borders both), then proceed as follows:
    a.  Count the total number of pixels of Color A in the input grid.
    b.  Count the total number of pixels of Color B in the input grid.
    c.  Identify the color with the maximum pixel count (let's call it Color Max) and the color with the minimum pixel count (let's call it Color Min).
    d.  The transformation rule is: Replace all pixels of Color Max with Color Min.
5.  Pixels originally having the background color remain unchanged. Pixels originally having the "replacing" color (Color A in Condition 1, Color Min in Condition 2) also remain unchanged.
6.  Output the modified grid.
