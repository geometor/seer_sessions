## Perception

The input and output are 2D grids of integers. Each task involves modifying the input grid based on the spatial arrangement of numbers.
The key elements appear to be:
1.  A dominant non-zero number (e.g., 4 in train_1, 1 in train_2, 6 in train_3) that forms a connected region, often acting like a boundary or background.
2.  A region of zeros ('hole') enclosed or partially enclosed by the dominant number's region.
3.  A single cell with a different non-zero value (e.g., 3 in train_1, 5 in train_2, 5 in train_3) located adjacent to the dominant number's region.

The transformation seems to involve:
1.  Identifying the 'hole' region of zeros.
2.  Identifying the unique, adjacent, different non-zero value ('source value') and its location.
3.  Identifying the value of the dominant region ('background value').
4.  Filling the 'hole' region with the 'source value'.
5.  Changing the original location of the 'source value' to the 'background value'.

## Facts


```yaml
objects:
  - name: InputGrid
    type: 2D Array of Integers
  - name: OutputGrid
    type: 2D Array of Integers
  - name: BackgroundRegion
    description: The largest connected component of a single non-zero integer (X) that encloses or borders a region of zeros.
    properties:
      - value: X (integer)
      - cells: List of coordinates (row, col)
      - connectivity: Orthogonal
  - name: HoleRegion
    description: A connected component of zeros (0) where all adjacent non-zero cells belong to the BackgroundRegion.
    properties:
      - value: 0 (integer)
      - cells: List of coordinates (row, col)
      - connectivity: Orthogonal
      - relationship: Enclosed or bordered by BackgroundRegion
  - name: SourceCell
    description: A single cell containing a non-zero integer (Y) different from the BackgroundRegion's value (X), which is orthogonally adjacent to the BackgroundRegion.
    properties:
      - value: Y (integer, Y != 0, Y != X)
      - location: Coordinate (row, col)
      - relationship: Adjacent to BackgroundRegion

actions:
  - name: IdentifyRegions
    description: Analyze the InputGrid to find the BackgroundRegion, HoleRegion, and SourceCell based on their definitions and relationships.
  - name: FillHole
    description: Modify a copy of the InputGrid by setting the value of all cells within the HoleRegion to the value (Y) of the SourceCell.
  - name: UpdateSource
    description: In the modified grid, set the value of the cell at the SourceCell's original location to the value (X) of the BackgroundRegion.
  - name: GenerateOutput
    description: The final modified grid after FillHole and UpdateSource is the OutputGrid.

relationships:
  - type: Adjacency
    between: [SourceCell, BackgroundRegion]
    details: The SourceCell shares an orthogonal edge with at least one cell in the BackgroundRegion.
  - type: Enclosure/Bordering
    between: [HoleRegion, BackgroundRegion]
    details: All non-zero neighbors of any cell in the HoleRegion must belong to the BackgroundRegion.

constraints:
  - There is exactly one unique SourceCell value (Y) adjacent to the BackgroundRegion (X).
  - The HoleRegion is defined by zeros directly bordered by the BackgroundRegion (X).
```


## Natural Language Program

1.  **Initialize:** Create a copy of the `InputGrid` to serve as the `OutputGrid`.
2.  **Identify Background Value (X):** Find the non-zero integer `X` such that there exist zero-valued cells whose *only* non-zero orthogonal neighbors have the value `X`. This `X` defines the `BackgroundRegion`.
3.  **Identify Hole Region (H):** Find all connected zero-valued cells `H` such that every cell in `H` is orthogonally adjacent only to cells with value `X` or other cells within `H`.
4.  **Identify Source Cell (Y):** Scan the `InputGrid` to find the unique cell `(r_y, c_y)` containing a non-zero value `Y` such that `Y` is not equal to `X`, and the cell `(r_y, c_y)` is orthogonally adjacent to at least one cell belonging to the `BackgroundRegion` (i.e., a cell with value `X` identified in step 2).
5.  **Fill Hole:** Iterate through all cells `(r_h, c_h)` identified as part of the `HoleRegion` `H` in step 3. Set the value of `OutputGrid[r_h][c_h]` to `Y`.
6.  **Update Source Location:** Set the value of the `OutputGrid` at the original location of the source cell: `OutputGrid[r_y][c_y] = X`.
7.  **Finalize:** The `OutputGrid` now holds the final transformed state.