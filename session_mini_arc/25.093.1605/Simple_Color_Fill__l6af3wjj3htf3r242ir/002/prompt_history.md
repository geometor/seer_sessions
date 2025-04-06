
## train_1

**input:**
```
4 4 4 0 0
4 0 4 0 0
3 4 4 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
4 4 4 0 0
4 3 4 0 0
4 4 4 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0
0 1 1 1 1
0 1 0 0 1
0 1 0 0 1
0 1 1 1 5
```


**output:**
```
0 0 0 0 0
0 1 1 1 1
0 1 5 5 1
0 1 5 5 1
0 1 1 1 1
```


## train_3

**input:**
```
6 6 6 6 6
6 0 0 0 6
6 0 0 0 6
6 0 0 0 6
6 6 6 6 5
```


**output:**
```
6 6 6 6 6
6 5 5 5 6
6 5 5 5 6
6 5 5 5 6
6 6 6 6 6
```

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
```python
import numpy as np
import collections

"""
Transforms the input grid based on identifying background, source, and hole regions.

The transformation identifies a 'background' value (X), a 'source' value (Y), 
and a 'hole' region (H) of zeros. The hole region is defined as a connected 
component of zeros where all adjacent non-zero cells have the background value X.
The source value Y is typically a unique, non-zero value different from X, located 
at cell (r_y, c_y). The transformation fills the hole region H with the source 
value Y and changes the value at the original source cell location (r_y, c_y) 
to the background value X.

1.  **Initialize:** Create a copy of the `InputGrid` to serve as the `OutputGrid`.
2.  **Identify Background (X) and Source (Y) Values:** Determine the most frequent 
    non-zero value (X) and the least frequent non-zero value (Y).
3.  **Identify Source Cell Location:** Find the coordinates (r_y, c_y) of the cell 
    containing the source value Y.
4.  **Identify Hole Region (H):** Find the connected component of zero-valued cells (H) 
    such that every non-zero orthogonal neighbor of any cell in H has the value X.
5.  **Fill Hole:** Update the `OutputGrid` by setting the value of all cells within 
    the identified Hole Region H to the source value Y.
6.  **Update Source Location:** Set the value of the `OutputGrid` at the original 
    location of the source cell (r_y, c_y) to the background value X.
7.  **Finalize:** Return the modified `OutputGrid`.
"""

def _get_value_counts(grid):
    """Counts occurrences of non-zero values in the grid."""
    counts = collections.Counter(val for val in grid.flat if val != 0)
    return counts

def _find_background_and_source_values(grid):
    """
    Finds background (most frequent non-zero) and source (least frequent non-zero) values.
    Assumes there are exactly two distinct non-zero values based on problem constraints.
    """
    counts = _get_value_counts(grid)
    if not counts:
        return None, None # No non-zero values
    if len(counts) == 1:
        # Only one non-zero value, cannot determine distinct background and source
        # Based on task structure, assume this case implies no change or is invalid input.
        # Returning the single value as background, None as source.
        background_value = list(counts.keys())[0]
        return background_value, None

    # Assume len(counts) >= 2. Find most and least frequent.
    # Using most_common directly relies on insertion order for ties, which is fine here.
    sorted_counts = counts.most_common()
    background_value = sorted_counts[0][0]
    source_value = sorted_counts[-1][0] # Least frequent

    # Verify source is not same as background if counts were equal
    if background_value == source_value and len(sorted_counts) > 1:
        # This case shouldn't happen if frequencies truly differ.
        # If frequencies are equal, need a tie-breaker rule not specified.
        # The problem implies unique Y != X. Let's assume counts are distinct.
         pass # Or potentially raise an error / log warning.

    return background_value, source_value

def _find_cell_location(grid, value):
    """Finds the coordinates (r, c) of the first cell with the given value."""
    # np.argwhere returns an array of [row, col] pairs. Get the first one.
    locations = np.argwhere(grid == value)
    if locations.size > 0:
        return tuple(locations[0])
    return None # Value not found

def _find_hole_region(grid, background_value):
    """
    Finds the connected region of zeros bordered only by the background value using BFS.
    Returns a list of (row, col) tuples for the hole cells.
    """
    rows, cols = grid.shape
    visited_zeros = set() # Keep track of zeros visited across different potential components
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0 and (r, c) not in visited_zeros:
                # Found an unvisited zero, start BFS to find its connected component
                component_coords = []
                q = collections.deque([(r, c)])
                component_visited_bfs = set([(r, c)]) # Zeros visited in *this* BFS run
                is_target_hole_component = True # Assume true initially for this component

                processed_in_bfs = set() # Track cells added to queue during this BFS

                bfs_q = collections.deque([(r,c)])
                processed_in_bfs.add((r,c))


                while bfs_q:
                    curr_r, curr_c = bfs_q.popleft()
                    
                    # Check if this zero is valid (part of the potential hole)
                    # We need to check neighbors *before* adding to component_coords
                    
                    is_current_cell_valid = True
                    for dr_check, dc_check in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                         nr_check, nc_check = curr_r + dr_check, curr_c + dc_check
                         if 0 <= nr_check < rows and 0 <= nc_check < cols:
                              neighbor_val_check = grid[nr_check, nc_check]
                              if neighbor_val_check != 0 and neighbor_val_check != background_value:
                                   is_target_hole_component = False
                                   is_current_cell_valid = False
                                   break # This component touches a non-background value
                         # else: out of bounds is fine
                    
                    if not is_current_cell_valid:
                         # If the cell itself invalidates the component, mark component and continue BFS only to mark visited
                         continue # Don't add invalid cell coords, but keep exploring its zero neighbors for visited marking

                    # If current cell is valid so far, add it to potential component
                    component_coords.append((curr_r, curr_c))

                    # Explore valid neighbors for BFS
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        if 0 <= nr < rows and 0 <= nc < cols:
                            neighbor_val = grid[nr, nc]
                            if neighbor_val == 0 and (nr, nc) not in processed_in_bfs:
                                # Found an unvisited zero neighbor, add to queue
                                processed_in_bfs.add((nr, nc))
                                bfs_q.append((nr, nc))
                            # Non-zero neighbors were already checked for validity calculation above

                # After BFS for the component starting at (r,c) is complete:
                # Mark all explored zeros in this component as globally visited
                visited_zeros.update(processed_in_bfs)

                # If the flag remained true throughout the component exploration, it's our hole
                if is_target_hole_component and component_coords:
                    # We found the hole region defined by the background value
                    return component_coords 

    return [] # Return empty list if no such hole region is found

def transform(input_grid_list):
    """
    Applies the hole-filling transformation to the input grid.
    """
    # Convert list of lists to numpy array for easier processing
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    
    # Step 2: Identify Background (X) and Source (Y) Values
    background_value, source_value = _find_background_and_source_values(input_grid)

    if background_value is None or source_value is None:
        # If values couldn't be determined (e.g., grid empty, only one non-zero type)
        # return the original grid copy
        print("Warning: Could not determine distinct background and source values.")
        return output_grid.tolist() 

    # Step 3: Identify Source Cell Location (r_y, c_y)
    source_location = _find_cell_location(input_grid, source_value)
    
    if source_location is None:
         # Should not happen if source_value was determined correctly
        print("Warning: Source value found, but location not found.")
        return output_grid.tolist()
    
    source_r, source_c = source_location

    # Step 4: Identify Hole Region (H) - zeros bordered only by X
    hole_coordinates = _find_hole_region(input_grid, background_value)

    # Step 5: Fill Hole
    if hole_coordinates:
        for r_h, c_h in hole_coordinates:
            output_grid[r_h, c_h] = source_value
            
    # Step 6: Update Source Location
    output_grid[source_r, source_c] = background_value
            
    # Step 7: Finalize - Convert back to list of lists
    return output_grid.tolist()

```
