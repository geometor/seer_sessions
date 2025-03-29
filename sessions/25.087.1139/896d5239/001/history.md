
## train_1

**input:**
```
1 0 1 0 1 0 1 1 0 1 0 0
1 0 0 1 1 0 1 1 0 0 1 1
1 0 0 0 0 0 3 0 1 0 1 1
1 0 0 1 0 3 0 1 1 1 1 1
1 1 1 0 3 1 0 0 1 0 1 1
0 1 1 3 1 1 1 1 0 1 0 0
0 1 0 0 3 1 0 0 1 0 0 1
1 1 1 1 1 3 0 0 1 0 0 1
0 0 1 0 0 1 3 0 1 0 1 1
1 0 0 1 0 1 1 0 1 0 1 0
1 1 1 1 0 0 1 0 1 1 1 0
1 1 0 1 1 0 1 0 0 1 0 0
0 1 0 0 3 1 1 0 0 0 0 1
0 1 0 1 1 1 1 1 0 0 1 1
0 1 3 0 0 0 3 0 0 1 1 1
```


**output:**
```
1 0 1 0 1 0 1 1 0 1 0 0
1 0 0 1 1 0 1 1 0 0 1 1
1 0 0 0 0 0 3 0 1 0 1 1
1 0 0 1 0 3 8 1 1 1 1 1
1 1 1 0 3 8 8 0 1 0 1 1
0 1 1 3 8 8 8 1 0 1 0 0
0 1 0 0 3 8 8 0 1 0 0 1
1 1 1 1 1 3 8 0 1 0 0 1
0 0 1 0 0 1 3 0 1 0 1 1
1 0 0 1 0 1 1 0 1 0 1 0
1 1 1 1 0 0 1 0 1 1 1 0
1 1 0 1 1 0 1 0 0 1 0 0
0 1 0 0 3 1 1 0 0 0 0 1
0 1 0 8 8 8 1 1 0 0 1 1
0 1 3 8 8 8 3 0 0 1 1 1
```


## train_2

**input:**
```
0 0 1 0 1 0 0 1 1 0 1 1
1 0 1 0 1 1 0 1 1 1 0 1
1 0 0 0 3 0 0 1 0 0 0 0
0 0 1 3 1 3 0 0 0 0 0 0
1 0 3 1 1 1 3 0 1 0 1 0
1 1 0 1 1 0 0 1 1 0 1 0
1 1 0 1 0 0 0 1 1 0 0 0
0 0 1 1 1 0 1 0 1 0 0 0
0 0 0 0 0 3 0 1 0 0 0 0
0 0 0 0 3 0 3 0 1 0 1 0
0 0 0 3 1 0 1 1 0 0 1 0
1 0 3 1 0 1 0 0 1 0 0 1
0 0 1 0 1 0 1 0 0 1 0 1
```


**output:**
```
0 0 1 0 1 0 0 1 1 0 1 1
1 0 1 0 1 1 0 1 1 1 0 1
1 0 0 0 3 0 0 1 0 0 0 0
0 0 1 3 8 3 0 0 0 0 0 0
1 0 3 8 8 8 3 0 1 0 1 0
1 1 0 1 1 0 0 1 1 0 1 0
1 1 0 1 0 0 0 1 1 0 0 0
0 0 1 1 1 0 1 0 1 0 0 0
0 0 0 0 0 3 0 1 0 0 0 0
0 0 0 0 3 8 3 0 1 0 1 0
0 0 0 3 8 8 8 8 0 0 1 0
1 0 3 8 8 8 8 8 8 0 0 1
0 0 1 0 1 0 1 0 0 1 0 1
```


## train_3

**input:**
```
1 1 0 0 0 0 0 0 0 1 1 0 1 1 1 1
1 0 0 1 1 0 0 1 1 1 1 1 1 1 1 1
1 1 1 0 0 3 1 0 1 1 0 0 0 0 1 0
0 0 0 0 3 1 3 0 1 1 0 0 1 1 1 0
0 1 0 3 1 1 1 1 0 1 0 1 1 1 0 0
1 0 0 0 1 0 1 0 1 1 0 0 1 1 1 1
0 1 0 0 1 1 0 1 1 0 1 1 0 1 0 1
1 0 1 1 0 1 1 1 0 0 0 0 1 0 0 0
1 0 0 1 0 0 1 1 3 0 0 0 3 1 1 0
0 1 0 1 1 0 1 3 1 1 1 0 0 3 1 3
1 0 0 0 0 1 3 0 0 0 0 1 0 0 3 0
0 0 1 0 1 3 1 1 1 1 0 0 0 0 0 0
1 1 0 1 1 1 3 0 0 1 1 1 1 0 0 0
0 0 0 1 1 1 1 1 1 0 0 0 0 1 1 1
0 1 1 1 0 0 1 1 3 1 0 1 0 1 1 1
```


**output:**
```
1 1 0 0 0 0 0 0 0 1 1 0 1 1 1 1
1 0 0 1 1 0 0 1 1 1 1 1 1 1 1 1
1 1 1 0 0 3 1 0 1 1 0 0 0 0 1 0
0 0 0 0 3 8 3 0 1 1 0 0 1 1 1 0
0 1 0 3 8 8 8 8 0 1 0 1 1 1 0 0
1 0 0 0 1 0 1 0 1 1 0 0 1 1 1 1
0 1 0 0 1 1 0 1 1 0 1 1 0 1 0 1
1 0 1 1 0 1 1 1 0 0 0 0 1 0 0 0
1 0 0 1 0 0 1 1 3 0 0 0 3 8 8 8
0 1 0 1 1 0 1 3 8 1 1 0 0 3 8 3
1 0 0 0 0 1 3 8 8 0 0 1 0 0 3 0
0 0 1 0 1 3 8 8 8 1 0 0 0 0 0 0
1 1 0 1 1 1 3 8 8 1 1 1 1 0 0 0
0 0 0 1 1 1 1 8 8 0 0 0 0 1 1 1
0 1 1 1 0 0 1 1 3 1 0 1 0 1 1 1
```

**Perception of Elements:**

1.  **Grid Structure:** The input and output grids have the same dimensions in each example.
2.  **Colors:** The primary colors involved are white (0 - background), blue (1 - static structures), green (3 - boundaries/markers), and azure (8 - fill color, appears only in output).
3.  **Static Elements:** The positions of white (0) and blue (1) pixels that are *not* changed to azure (8) remain the same between input and output. The positions of green (3) pixels also remain unchanged.
4.  **Transformation:** The core transformation is the introduction of azure (8) pixels in the output grid. These azure pixels replace existing white (0) or blue (1) pixels from the input grid.
5.  **Role of Green Pixels:** Green (3) pixels appear to act as boundaries or barriers. They themselves are never changed.
6.  **Filling Mechanism:** Azure (8) pixels fill connected regions. These regions are adjacent to green (3) pixels and seem to be "contained" or "bordered" by them. The fill propagates through white (0) and blue (1) pixels until it hits a green (3) boundary or the edge of the grid. The fill uses 4-way adjacency (up, down, left, right).

**YAML Facts:**


```yaml
Grid:
  Properties:
    - Dimensions: Same for input and output pairs.
    - BackgroundColor: Primarily white (0).
Objects:
  - Type: Static Structures
    Color: blue (1)
    Property: Unchanged unless overwritten by fill.
  - Type: Boundary Markers
    Color: green (3)
    Property: Unchanged between input and output. Define regions for filling.
  - Type: Fill Regions
    InitialColor: white (0) or blue (1)
    FinalColor: azure (8)
    Property: Connected areas adjacent to green (3) pixels.
Relationships:
  - Adjacency: Green (3) pixels are adjacent (4-way) to the starting points of azure (8) fill regions.
  - Containment: Azure (8) fills propagate within regions bounded by green (3) pixels and/or grid edges.
Actions:
  - Identify: Locate all green (3) pixels in the input.
  - Seed: Identify all non-green pixels adjacent (4-way) to any green pixel. These are potential fill starting points.
  - FloodFill:
      From: Each unique seed pixel identified above.
      Color: azure (8)
      Propagation: 4-way adjacency.
      StopCondition: Encountering a green (3) pixel (from the input grid) or the grid boundary.
      Overwrite: Fill replaces original white (0) or blue (1) pixels.
      Constraint: Do not overwrite green (3) pixels.
```


**Natural Language Program:**

1.  Initialize the output grid as an exact copy of the input grid.
2.  Identify all pixels in the input grid that have the color green (3). These are boundary pixels.
3.  Find all unique pixel locations that are adjacent (up, down, left, or right) to any green (3) boundary pixel, *and* are themselves *not* green (3). These locations are the "seed" pixels for filling.
4.  For each identified seed pixel:
    a.  If this seed pixel has already been colored azure (8) in the output grid (because it was part of a previous fill operation), skip to the next seed pixel.
    b.  Start a flood fill operation from this seed pixel's location on the output grid.
    c.  Use the color azure (8) for filling.
    d.  The fill should spread to adjacent pixels (up, down, left, right).
    e.  The fill continues to spread as long as it encounters pixels that were *not* green (3) in the original *input* grid and are within the grid boundaries.
    f.  Color all pixels visited by the flood fill (including the starting seed) with azure (8) in the output grid.
5.  The final output grid contains the original green (3) pixels, the newly added azure (8) filled regions, and any remaining original blue (1) and white (0) pixels that were not part of the filled regions.
