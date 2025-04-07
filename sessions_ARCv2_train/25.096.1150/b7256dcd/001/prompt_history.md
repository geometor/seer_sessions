
## train_1

**input:**
```
7 6 6 3 7
7 7 7 4 7
7 7 7 6 7
7 7 6 6 6
7 7 7 6 7
```


**output:**
```
7 3 3 7 7
7 7 7 7 7
7 7 7 4 7
7 7 4 4 4
7 7 7 4 7
```


## train_2

**input:**
```
7 7 7 6
3 7 6 6
7 7 6 7
7 7 7 7
1 6 6 6
7 7 6 7
```


**output:**
```
7 7 7 6
7 7 6 6
7 7 6 7
7 7 7 7
7 1 1 1
7 7 1 7
```

Okay, let's break down the transformation.

**Perception of Elements:**

*   The core elements are 2D grids containing numerical values.
*   The number '7' appears frequently and often acts as a stable background or default value.
*   The number '6' seems to be a mutable value, susceptible to change based on its neighbours.
*   Other numbers (e.g., '1', '3', '4' in the examples) act as "sources" or "influencers" that can propagate their value onto adjacent '6's.
*   The transformation involves two main types of changes:
    1.  Regions of '6's change their value based on a single, unique neighbouring non-6, non-7 value.
    2.  Some of the original "source" numbers (non-6, non-7) are changed to '7', either because they successfully influenced a region of '6's or because they were isolated (surrounded by '7's).
*   Connectivity (specifically 4-way adjacency) is crucial for defining regions of '6's and determining influence.

**Facts (YAML):**


```yaml
elements:
  - object: Grid
    properties:
      - type: 2D array of integers
      - dimensions: variable (height x width), preserved in transformation
  - object: Cell
    properties:
      - coordinates: (row, column)
      - value: integer
      - neighbors: adjacent cells (up, down, left, right)
  - object: Number (Value)
    properties:
      - role: specific roles based on value
        - 7: Background/Default (mostly stable)
        - 6: Mutable (changes based on context)
        - Others (1, 3, 4,...): Potential Sources/Influencers
  - object: Component
    properties:
      - type: Connected group of cells
      - criteria: cells have value '6', connected via 4-way adjacency
      - border_cells: cells adjacent to the component but not part of it
      - border_values: values of border_cells, filtered (non-6, non-7)

actions:
  - name: Identify_6_Components
    input: Input Grid
    output: Set of Components (each a set of cell coordinates)
  - name: Determine_Component_Fate
    input: Input Grid, Component
    process:
      - Find border_cells for the Component.
      - Get border_values (non-6, non-7) from border_cells in Input Grid.
      - If exactly one unique value 'v' exists in border_values:
        - Mark Component cells to become 'v'.
        - Identify source cells (border cells with value 'v').
    output: Updated values for component cells, Set of source cell coordinates
  - name: Update_Sources_And_Isolated
    input: Input Grid, Output Grid (partially updated), Set of source_cells
    process:
      - Iterate through Input Grid cells (r, c).
      - If input[r, c] is non-6, non-7:
        - If (r, c) is in source_cells, set output[r, c] = 7.
        - Else if all neighbors of input[r, c] are 7, set output[r, c] = 7.
    output: Final Output Grid

relationships:
  - type: Adjacency
    between: Cells (4-way: up, down, left, right)
  - type: Membership
    between: Cell, Component
  - type: Influence
    from: Source Cell (non-6, non-7)
    to: Adjacent Component of 6s
```


**Natural Language Program:**

1.  Initialize the `output_grid` as a direct copy of the `input_grid`.
2.  Find all distinct connected components of cells containing the value '6' in the `input_grid`, using 4-way adjacency.
3.  Create an empty set `source_cells` to keep track of the coordinates of cells that act as sources for changing '6' components.
4.  For each '6' component identified:
    a.  Determine the set of cells in the `input_grid` that are directly adjacent (4-way) to any cell within this component.
    b.  Collect the values of these adjacent cells, excluding any '6's and '7's. Let this collection be `neighbor_influences`.
    c.  Find the unique values present in `neighbor_influences`.
    d.  If there is exactly one unique value `v` found:
        i.  For every cell coordinate `(r, c)` within the current '6' component, update the `output_grid` at that position: `output_grid[r, c] = v`.
        ii. Identify all adjacent cells (from step 4a) whose value in the `input_grid` is `v`. Add the coordinates of these cells to the `source_cells` set.
5.  Iterate through every cell `(r, c)` in the `input_grid`:
    a.  Let `current_value = input_grid[r, c]`.
    b.  If `current_value` is not '6' and not '7':
        i.  If the coordinate `(r, c)` exists in the `source_cells` set, update `output_grid[r, c] = 7`.
        ii. Otherwise (if `(r, c)` is not a source cell), check all valid 4-way neighbors of `(r, c)` in the `input_grid`. If all neighbors have the value '7', update `output_grid[r, c] = 7`.
6.  The final `output_grid` contains the transformed result.
