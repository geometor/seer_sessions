**Perception**

1.  **Grid Structure:** The input grids are characterized by a clear grid structure formed by solid horizontal and vertical lines of a single, non-background color (Red=2 in train_1, Magenta=6 in train_2). This color acts as a frame or separator.
2.  **Regions:** These grid lines partition the grid into multiple rectangular sub-regions.
3.  **Region Content:** Some regions are empty (filled with the background color, White=0), while others contain distinct patterns or shapes composed of one or more non-background, non-grid-line colors (Green=3/Blue=1 in train_1, Yellow=4 in train_2).
4.  **Transformation:** The core transformation is a selective swapping of content between pairs of regions. The grid lines themselves, empty regions, and regions with unique patterns remain unchanged.
5.  **Pairing Logic:** The swapping occurs between regions that contain *identical* patterns (considering both shape and color).
6.  **Grouping and Ordering:** Regions with the same pattern are grouped. Within each group, regions are conceptually ordered (e.g., top-to-bottom, left-to-right based on their top-left corner).
7.  **Swapping Mechanism:** The swapping happens between consecutive regions in the ordered list within each group (the 1st swaps with the 2nd, the 3rd swaps with the 4th, and so on). If a group has an odd number of regions, the last one remains in its original place.

**Facts**


```yaml
grid_structure:
  description: Input grid is partitioned by solid horizontal and vertical lines of a single dominant color (grid_line_color).
  grid_line_color: Variable (e.g., Red=2, Magenta=6). Defines boundaries for regions.
  grid_lines_preserved: True. The positions and color of grid lines remain unchanged in the output.
regions:
  definition: Rectangular areas bounded by grid lines and/or the overall grid borders.
  properties:
    - location: Defined by top-left and bottom-right coordinates.
    - content: A subgrid containing pixels. Can be empty (background color only) or contain a pattern.
patterns:
  definition: The specific arrangement and colors of non-background pixels within a region's content. Excludes the grid_line_color.
  role: Used as the key for identifying regions to be potentially swapped. Identity requires matching shape, colors, and relative positions within the region.
transformation:
  type: Swapping content between pairs of regions.
  conditions:
    - Regions must contain identical patterns (shape and color).
    - Regions must belong to the same group of identical patterns.
  process:
    1. Identify grid lines and define regions.
    2. Extract the pattern from each non-empty region.
    3. Group regions based on identical patterns.
    4. For each group with 2 or more regions:
       a. Sort regions by position (e.g., row-major order of top-left corners).
       b. Form pairs: (1st, 2nd), (3rd, 4th), etc.
       c. Swap the *entire content* of the regions within each pair.
  unaffected_elements:
    - Grid lines.
    - Empty regions (containing only background color).
    - Regions with unique patterns (group size 1).
    - The last region in a group with an odd number of members.
```


**Natural Language Program**

1.  **Identify Grid Structure:** Detect the dominant non-background color forming complete horizontal and vertical lines; this is the `grid_line_color`. Find the row and column indices (`grid_rows`, `grid_cols`) corresponding to these lines.
2.  **Define Regions:** Use the `grid_rows` and `grid_cols` (along with the grid boundaries 0, H-1, 0, W-1) to define the bounding boxes of all rectangular regions within the grid.
3.  **Extract and Characterize Region Contents:** For each defined region:
    a.  Extract the subgrid representing its content.
    b.  Determine if the region is empty (contains only background color) or if it contains a pattern (includes non-background, non-`grid_line_color` pixels).
    c.  Store the pattern (the subgrid content) and the region's location/index.
4.  **Group Regions by Identical Patterns:** Create groups where each group contains the locations/indices of regions having identical non-empty patterns.
5.  **Identify Swap Pairs:** For each group of regions with identical patterns:
    a.  If the group contains fewer than two regions, do nothing with this group.
    b.  If the group contains two or more regions, sort the region locations/indices based on their top-left corner (primarily by row, secondarily by column).
    c.  Iterate through the sorted list, pairing the first with the second, the third with the fourth, and so on. Record these pairs (e.g., `(region_index_A, region_index_B)`).
6.  **Perform Swaps:** Create a copy of the input grid to serve as the output grid. For each identified pair `(region_A, region_B)`:
    a.  Get the content (subgrid) of `region_A` from the *input* grid.
    b.  Get the content (subgrid) of `region_B` from the *input* grid.
    c.  Place the content of `region_A` into the location of `region_B` in the *output* grid.
    d.  Place the content of `region_B` into the location of `region_A` in the *output* grid.
7.  **Finalize Output:** The modified output grid, containing the swapped region contents and all original unchanged elements (grid lines, empty regions, unswapped pattern regions), is the result.