## Perception of Task Elements

The task involves transforming a 2D grid of integers (representing colors) based on local neighborhood interactions. The core transformation appears to be a selective filtering or removal of certain colored cells based on the colors of their immediate neighbors.

1.  **Input/Output:** Both input and output are 2D grids of integers.
2.  **Colors:** Non-zero integers represent distinct colors or types. Zero represents the background.
3.  **Transformation:** The transformation modifies the input grid by changing some non-zero cells to zero. Cells that are initially zero remain zero.
4.  **Rule:** The decision to change a cell's value from non-zero to zero depends on the values of its adjacent cells (8 neighbours - Moore neighborhood). Specifically, a non-zero cell's value is reset to zero if it has at least one neighbour with a different, non-zero value that is *smaller* than its own value. Otherwise, the cell retains its original value. This implies a priority system where higher-valued colors "yield" to adjacent lower-valued colors by being removed at the interface.

## YAML Fact Document


```yaml
task_elements:
  - name: Grid
    type: 2D Array
    description: Represents the spatial layout containing cells with integer values (colors).
  - name: Cell
    type: Element
    description: A single location within the grid defined by row and column coordinates.
    properties:
      - value: Integer representing a color (0 for background, non-zero for specific colors).
      - coordinates: (row, column) pair.
  - name: Neighbourhood
    type: Relationship
    description: The set of 8 cells directly adjacent (horizontally, vertically, or diagonally) to a given cell.
    properties:
      - connectivity: Moore (8-way)

actions:
  - name: Filter Cell Value
    input: Cell (target) and its Neighbourhood
    output: Modified Cell value (potentially 0)
    logic: >
      Compare the target cell's value (V) with the values (VN) of its neighbours.
      If V is non-zero AND there exists at least one neighbour N such that VN is non-zero, VN is not equal to V, and VN < V,
      then the target cell's value becomes 0 in the output grid.
      Otherwise, the target cell's value remains V in the output grid.

relationships:
  - type: Adjacency
    between: [Cell, Cell]
    details: Defined by the Neighbourhood definition.
  - type: Value Comparison
    between: [Cell Value, Cell Value]
    details: Determines the outcome of the Filter Cell Value action based on relative magnitude (V > VN).

constants:
  - name: Background Value
    value: 0
    role: Represents empty space, does not participate in filtering comparisons other than being ignored (VN != 0).
```


## Natural Language Program

1.  Initialize the output grid as an identical copy of the input grid.
2.  Iterate through each cell `(r, c)` of the input grid. Let the value of this cell be `V`.
3.  If `V` is equal to 0, proceed to the next cell without changing the output grid.
4.  If `V` is not 0, examine the values of all 8 neighbouring cells (those at `(r-1, c-1)` to `(r+1, c+1)`, excluding `(r, c)` itself, and ensuring they are within the grid boundaries).
5.  Check if there is at least one neighbour `N` whose value `V_N` meets all the following conditions:
    *   `V_N` is not 0.
    *   `V_N` is not equal to `V`.
    *   `V_N` is less than `V`.
6.  If one or more neighbours satisfy these conditions, change the value of the cell `(r, c)` in the *output* grid to 0.
7.  If *no* neighbour satisfies all these conditions, the value of the cell `(r, c)` in the output grid remains unchanged (it keeps the original value `V`).
8.  After processing all cells, the final state of the output grid represents the result of the transformation.