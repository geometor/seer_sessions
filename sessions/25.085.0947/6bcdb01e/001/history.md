
## train_1

**input:**
```
8 7 7 8 7 8 7
7 8 8 7 7 7 8
7 7 7 7 7 7 7
7 7 7 7 7 7 8
7 7 7 7 7 8 7
3 3 7 7 8 7 7
7 7 7 8 7 7 7
```


**output:**
```
8 7 7 8 7 8 7
7 8 8 3 3 3 8
7 7 7 3 7 3 7
3 3 3 3 3 3 8
7 7 7 3 7 8 7
3 3 3 3 8 7 7
7 7 7 8 7 7 7
```


## train_2

**input:**
```
7 8 7 8 7
8 7 7 7 8
7 7 7 7 7
7 3 7 7 8
7 3 7 8 7
```


**output:**
```
7 8 7 8 7
8 3 3 3 8
7 3 7 3 7
3 3 3 3 8
7 3 7 8 7
```

Okay, let's analyze the provided task examples.

### Perception

1.  **Grid Structure:** Both input and output grids in the examples are square or rectangular grids of pixels. The dimensions remain the same between input and output for each example (7x7 for train_1, 5x5 for train_2).
2.  **Colors:** The primary colors involved are Orange (7), Green (3), and Azure (8). The background or majority color appears to be Orange (7). Azure (8) pixels appear scattered and seem fixed; their positions do not change from input to output. Green (3) pixels are present in the input, and their number increases significantly in the output.
3.  **Transformation:** The core transformation seems to involve the Green (3) color spreading into areas previously occupied by Orange (7) pixels.
4.  **Barriers:** The Azure (8) pixels act as barriers, preventing the Green color from spreading through or past them. The edges of the grid also act as boundaries for the spread.
5.  **Starting Points:** The initial Green (3) pixels present in the input grid appear to be the starting points or "seeds" for the spreading process.
6.  **Connectivity:** The spread occurs to orthogonally adjacent (up, down, left, right) pixels. It looks like a "flood fill" or region-growing process originating from the initial Green pixels.
7.  **Target Color:** Only Orange (7) pixels are susceptible to being changed to Green (3) by this process. Pixels that are initially Azure (8) or Green (3) remain unchanged. Orange (7) pixels that are not reachable from the initial Green (3) pixels without crossing an Azure (8) barrier also remain Orange (7).

### Facts


```yaml
task_description: "Perform a flood fill operation starting from initial Green pixels."

elements:
  - object: grid
    description: "A 2D array of pixels representing colors."
    properties:
      - height: integer
      - width: integer
      - pixels: list of lists of integers (0-9)

  - object: pixel
    description: "A single cell within the grid."
    properties:
      - color: integer (0-9)
      - location: tuple (row, column)

colors:
  - color: Green (3)
    role: [initial_source, fill_color]
    description: "Pixels with value 3. Act as starting points for the fill and are the color used to fill."
  - color: Orange (7)
    role: [fillable_area]
    description: "Pixels with value 7. These are the pixels eligible to be changed to Green during the fill."
  - color: Azure (8)
    role: [barrier]
    description: "Pixels with value 8. These act as barriers, blocking the spread of the Green fill."

actions:
  - action: identify_seeds
    description: "Locate all pixels in the input grid that have the Green (3) color."
    inputs: [input_grid]
    outputs: [list_of_seed_coordinates]

  - action: flood_fill
    description: "Starting from the seed coordinates, change adjacent Orange (7) pixels to Green (3), respecting Azure (8) barriers and grid boundaries."
    inputs: [input_grid, list_of_seed_coordinates]
    outputs: [output_grid]
    details:
      - The fill spreads orthogonally (up, down, left, right).
      - Only pixels that are initially Orange (7) in the input grid can be changed.
      - Azure (8) pixels in the input grid block the spread.
      - The grid boundaries block the spread.
      - Pixels initially Green (3) or Azure (8) remain unchanged.
      - Pixels changed during the fill become Green (3).

relationships:
  - relationship: adjacency
    description: "Orthogonal adjacency (sharing an edge) determines how the fill spreads."
  - relationship: barrier
    description: "Azure (8) pixels prevent the fill from spreading into or through them."
  - relationship: source
    description: "Initial Green (3) pixels are the origin points for the fill operation."
  - relationship: target
    description: "Orange (7) pixels are the only targets for the fill color change."
```


### Natural Language Program

1.  Create a copy of the input grid; this will become the output grid.
2.  Identify the coordinates of all pixels in the input grid that are Green (color 3). These are the initial "seed" locations for the fill.
3.  Initialize a data structure (like a queue or stack) to keep track of pixels to process, and add all seed coordinates to it.
4.  Initialize a data structure (like a set) to keep track of visited coordinates, and add all seed coordinates to it. This prevents reprocessing pixels and infinite loops.
5.  While the processing structure is not empty:
    a.  Remove a coordinate `(row, col)` from the structure.
    b.  Examine its four orthogonal neighbors: `(row-1, col)`, `(row+1, col)`, `(row, col-1)`, `(row, col+1)`.
    c.  For each neighbor `(nr, nc)`:
        i.  Check if `(nr, nc)` is within the bounds of the grid.
        ii. Check if `(nr, nc)` has already been visited.
        iii. Check if the pixel at `(nr, nc)` in the *original input grid* is Orange (color 7).
        iv. If the neighbor is within bounds, not visited, and was originally Orange (7):
            1.  Change the color of the pixel at `(nr, nc)` in the *output grid* to Green (color 3).
            2.  Mark `(nr, nc)` as visited.
            3.  Add `(nr, nc)` to the processing structure.
6.  Once the processing structure is empty, return the modified output grid.
