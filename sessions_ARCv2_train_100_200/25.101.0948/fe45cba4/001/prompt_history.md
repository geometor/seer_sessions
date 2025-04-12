
## train_1

**input:**
```
7 7 7 7 7 9 9 9
7 7 7 7 7 7 9 9
2 7 7 7 7 9 9 9
2 2 2 7 7 7 7 7
2 2 2 7 7 2 2 2
2 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
```


**output:**
```
7 7 7 7 7 9 9 9
7 7 7 7 7 7 9 9
7 7 7 7 7 9 9 9
7 7 7 7 7 7 7 7
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
```


## train_2

**input:**
```
7 7 7 7 7 9 9 9
9 7 7 7 7 7 9 9
9 9 7 7 7 9 9 9
9 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
```


**output:**
```
7 7 7 7 9 9 9 9
7 7 7 7 9 9 9 9
7 7 7 7 9 9 9 9
7 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
```

*   **Perception:**
    The task involves grids containing three colors: a background color (orange/7) and two other foreground colors (red/2 and maroon/9). In each example, one of the foreground colors is selected, and its pixels are rearranged into a solid rectangle placed in one of the four corners of the grid. The other foreground color remains unchanged. The background color fills the remaining space.

*   **Observations:**
    *   **Color Selection:** The foreground color chosen for rearrangement appears to be the one whose pixels, in the input grid, touch the most unique edges (Top, Bottom, Left, Right) of the grid.
        *   Example 1: Red (2) touches Left, Bottom, Right (3 edges). Maroon (9) touches Top, Right (2 edges). Red is chosen.
        *   Example 2: Red (2) touches Bottom, Right (2 edges). Maroon (9) touches Top, Left, Right (3 edges). Maroon is chosen.
    *   **Pixel Count:** The total number of pixels of the selected color remains the same between input and output.
    *   **Rectangle Shape:** The pixels are rearranged into a solid rectangle. The dimensions (Height R, Width C) of this rectangle are factors of the total pixel count (N), such that R * C = N, and the difference `abs(R - C)` is minimized. If multiple factor pairs minimize this difference, the pair with the smaller height (R) is chosen.
        *   Example 1: Red count = 16. Factors: (1,16), (2,8), (4,4), (8,2), (16,1). Min diff `abs(R-C)` is 0 for (4,4). Shape is 4x4.
        *   Example 2: Maroon count = 12. Factors: (1,12), (2,6), (3,4), (4,3), (6,2), (12,1). Min diff `abs(R-C)` is 1 for (3,4) and (4,3). Smaller R is 3, so choose (3,4). Shape is 3x4.
    *   **Rectangle Placement:** The rectangle is placed in one of the four corners. The corner seems determined by the two grid edges that the selected color's pixels touched most frequently in the input. The frequency is the count of pixels adjacent to that edge. Ties for the second most frequent edge seem broken by the order: Top > Bottom > Left > Right.
        *   Example 1: Red touches T=0, B=4, L=4, R=6. Highest counts are R(6) and B(4)/L(4). Tie-break B>L. Edges are Right and Bottom. Corner is Bottom-Right.
        *   Example 2: Maroon touches T=3, B=0, L=3, R=5. Highest counts are R(5) and T(3)/L(3). Tie-break T>L. Edges are Right and Top. Corner is Top-Right.
    *   **Other Color:** The foreground color *not* selected for rearrangement remains in its original position.
    *   **Background:** The background color (orange/7) fills all cells not occupied by the rearranged rectangle or the unchanged foreground color.

*   **YAML Facts:**
    
```yaml
    task_description: Rearrange pixels of one foreground color into a corner rectangle based on edge contact rules.
    
    elements:
      - element: grid
        properties:
          - background_color: 7 (orange)
          - foreground_colors: [2 (red), 9 (maroon)]
          - height: 8
          - width: 8
      - element: pixel_group
        properties:
          - color: one of the foreground_colors
          - location: various coordinates in the input grid
          - count: number of pixels N
          - edge_contacts: counts of pixels touching [Top, Bottom, Left, Right] edges
    
    actions:
      - action: select_color
        criteria: Choose the foreground color whose pixels touch the most unique grid edges in the input. (If tied, potentially choose the one with more pixels).
        variable: target_color
      - action: count_pixels
        input: target_color pixels in input grid
        output: count N
      - action: determine_rectangle_shape
        input: N
        computation: Find factors (R, C) of N minimizing abs(R-C). Tie-break: choose smaller R.
        output: Height R, Width C
      - action: determine_target_corner
        input: edge_contact counts for target_color
        computation: Find the two edges with the highest contact counts. Tie-break for second edge: T > B > L > R.
        output: target_corner (TL, TR, BL, BR)
      - action: transform_grid
        steps:
          - Copy input grid to output grid.
          - Change all original target_color pixels in output grid to background_color (7).
          - Draw a solid rectangle of target_color with shape (Height R, Width C) in the target_corner.
    
    relationships:
      - The choice of target_color depends on maximizing unique edge contacts in the input.
      - The shape (R, C) of the output rectangle depends on the pixel count N and minimizing abs(R-C).
      - The position (target_corner) of the output rectangle depends on the two most frequent edge contacts in the input.
      - The non-target foreground color pixels are unaffected by the transformation.
    ```


*   **Natural Language Program:**
    1.  Identify the two foreground colors (non-orange) present in the input grid.
    2.  For each foreground color, count how many unique grid edges (Top, Bottom, Left, Right) its pixels are adjacent to.
    3.  Select the foreground color that touches the most unique grid edges as the `target_color`. (If there's a tie in unique edges touched, select the color with the greater total number of pixels).
    4.  Count the total number of pixels (`N`) of the `target_color` in the input grid.
    5.  Find all pairs of integer factors (R, C) such that `R * C = N`. Select the pair (R, C) that minimizes the absolute difference `abs(R - C)`. If there is a tie (e.g., for N=12, both (3,4) and (4,3) give a difference of 1), choose the pair with the smaller value for R. Let the chosen dimensions be `Height = R` and `Width = C`.
    6.  Count how many pixels of the `target_color` touch each of the four grid edges (Top, Bottom, Left, Right) in the input grid.
    7.  Identify the two edges with the highest contact counts. If there is a tie for the second highest count, use the priority order Top > Bottom > Left > Right to break the tie.
    8.  Determine the `target_corner` based on the two selected edges (e.g., Top and Right edges imply the Top-Right corner).
    9.  Create a new grid, initially identical to the input grid.
    10. Change all pixels that originally had the `target_color` to the background color (orange/7).
    11. Draw a solid rectangle of `target_color` with dimensions `Height` x `Width` in the `target_corner` of the grid. The placement rules are:
        *   Top-Left: Rows 0 to `Height-1`, Columns 0 to `Width-1`.
        *   Top-Right: Rows 0 to `Height-1`, Columns `GridWidth-Width` to `GridWidth-1`.
        *   Bottom-Left: Rows `GridHeight-Height` to `GridHeight-1`, Columns 0 to `Width-1`.
        *   Bottom-Right: Rows `GridHeight-Height` to `GridHeight-1`, Columns `GridWidth-Width` to `GridWidth-1`.
    12. The final grid is the result of these modifications.
