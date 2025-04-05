## General Assessment and Strategy

The initial analysis correctly identified the core components (background, source, hole) and the basic transformation (fill hole with source, change source to background). However, the implementation's method for identifying these components, particularly the background/source values (based purely on frequency) and the hole region (first valid BFS component found), proved insufficient for `train_2`.

The failure in `train_2` revealed ambiguities in the initial definitions:
1.  **Value Identification:** Relying solely on frequency is unreliable. The relationship between the source `Y` and background `X` (adjacency) seems more definitional. `Y` is the unique color that is adjacent to a different color `X`, which forms the main structure bordering the zeros.
2.  **Hole Identification:** The definition "zeros bordered only by background `X`" can apply to multiple disconnected regions of zeros (e.g., the internal hole and boundary-touching zeros in `train_2`). The key differentiator seems to be that the target hole is *internal* to the grid, not touching the boundaries.

**Strategy:**
1.  **Refine Identification:**
    *   Identify the Source `Y` value and its location `(r_y, c_y)` first. `Y` is likely the least frequent non-zero value, but crucially, it must be adjacent to another *different* non-zero value.
    *   Identify the Background `X` value as the non-zero value adjacent to `Y`.
    *   Identify the Hole `H` by finding *all* connected components of zeros. Filter these components to find the one(s) where *all* non-zero neighbors are `X`. From this filtered list, select the component that does *not* contain any cells on the grid boundary (row 0, col 0, max_row, max_col). Assume only one such internal hole exists.
2.  **Apply Transformation:** Use the correctly identified `Y`, `X`, `(r_y, c_y)`, and `H` to perform the fill and update steps.
3.  **Update Documentation:** Revise the Facts (YAML) and Natural Language Program to reflect these refined identification steps.

## Metrics Gathering

Let's gather data to confirm the revised hypotheses.


``` python
import numpy as np
import collections

def analyze_example(input_grid_list, output_grid_list):
    inp = np.array(input_grid_list)
    out = np.array(output_grid_list)
    rows, cols = inp.shape
    metrics = {'shape': (rows, cols)}

    # Values and Counts
    non_zero_vals = inp[inp != 0]
    counts = collections.Counter(non_zero_vals)
    metrics['value_counts'] = dict(counts)
    metrics['distinct_non_zero_values'] = sorted(counts.keys())

    # Tentative Source (Y) and Background (X) based on counts
    source_y = None
    background_x = None
    if len(counts) >= 2:
        sorted_counts = counts.most_common()
        background_x = sorted_counts[0][0]
        source_y = sorted_counts[-1][0]
    elif len(counts) == 1:
        background_x = list(counts.keys())[0]

    metrics['tentative_source_Y'] = source_y
    metrics['tentative_background_X'] = background_x

    source_coords = None
    background_neighbor_coords = []
    if source_y is not None:
        locs_y = np.argwhere(inp == source_y)
        if locs_y.size > 0:
            source_coords = tuple(locs_y[0]) # Assume unique source location
            metrics['source_Y_coords'] = source_coords
            # Find adjacent background X
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = source_coords[0] + dr, source_coords[1] + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor_val = inp[nr, nc]
                    if neighbor_val != 0 and neighbor_val != source_y:
                         # Found adjacent different non-zero: assume it's background X
                         if background_x is None or neighbor_val == background_x:
                              background_x = neighbor_val # Confirm/set background X
                              background_neighbor_coords.append((nr, nc))
                         # else: logic might need refinement if Y touches multiple other colors

    metrics['confirmed_background_X'] = background_x
    metrics['background_X_coords_near_Y'] = background_neighbor_coords

    # Identify Changed Cells (Input vs Output)
    changed_mask = inp != out
    changed_coords = np.argwhere(changed_mask)
    metrics['changed_cell_count'] = len(changed_coords)

    # Identify Filled Cells (Input 0 -> Output Y)
    filled_mask = (inp == 0) & (out == source_y)
    filled_coords = [tuple(coord) for coord in np.argwhere(filled_mask)]
    metrics['filled_hole_coords'] = filled_coords

    # Identify Source Cell Change (Input Y -> Output X)
    source_changed = False
    if source_coords is not None and background_x is not None:
       if inp[source_coords] == source_y and out[source_coords] == background_x:
           source_changed = True
    metrics['source_Y_changed_to_X'] = source_changed

    # Analyze Hole Properties (using filled_coords as proxy for hole)
    hole_on_boundary = False
    if filled_coords:
        for r, c in filled_coords:
            if r == 0 or c == 0 or r == rows - 1 or c == cols - 1:
                hole_on_boundary = True
                break
    metrics['hole_touches_boundary'] = hole_on_boundary

    # Verify hole neighbors in input
    hole_neighbors_valid = True
    invalid_neighbor_coords = []
    if filled_coords and background_x is not None:
        visited_hole_neighbors = set()
        q = collections.deque(filled_coords)
        processed_in_bfs = set(filled_coords)

        while q:
            r, c = q.popleft()
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                 nr, nc = r + dr, c + dc
                 neighbor_coord = (nr, nc)

                 if 0 <= nr < rows and 0 <= nc < cols:
                     # Check neighbors *not* part of the hole itself
                     if neighbor_coord not in processed_in_bfs:
                          # Avoid re-checking same neighbor cell
                          if neighbor_coord not in visited_hole_neighbors:
                               visited_hole_neighbors.add(neighbor_coord)
                               neighbor_val = inp[nr, nc]
                               if neighbor_val != 0 and neighbor_val != background_x:
                                    hole_neighbors_valid = False
                                    invalid_neighbor_coords.append(neighbor_coord)
                 # else: out of bounds neighbors are ok
    metrics['hole_only_borders_X_or_0'] = hole_neighbors_valid
    metrics['hole_invalid_neighbor_coords'] = invalid_neighbor_coords


    return metrics


# Example Data
train_1_in = [[4, 4, 4, 0, 0], [4, 0, 4, 0, 0], [3, 4, 4, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
train_1_out = [[4, 4, 4, 0, 0], [4, 3, 4, 0, 0], [4, 4, 4, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
train_2_in = [[0, 0, 0, 0, 0], [0, 1, 1, 1, 1], [0, 1, 0, 0, 1], [0, 1, 0, 0, 1], [0, 1, 1, 1, 5]]
train_2_out = [[0, 0, 0, 0, 0], [0, 1, 1, 1, 1], [0, 1, 5, 5, 1], [0, 1, 5, 5, 1], [0, 1, 1, 1, 1]]
train_3_in = [[6, 6, 6, 6, 6], [6, 0, 0, 0, 6], [6, 0, 0, 0, 6], [6, 0, 0, 0, 6], [6, 6, 6, 6, 5]]
train_3_out = [[6, 6, 6, 6, 6], [6, 5, 5, 5, 6], [6, 5, 5, 5, 6], [6, 5, 5, 5, 6], [6, 6, 6, 6, 6]]
test_1_in = [[0, 0, 0, 0, 0], [0, 8, 8, 4, 0], [0, 8, 0, 8, 0], [0, 8, 8, 8, 0], [0, 0, 0, 0, 0]]
test_1_out = [[0, 0, 0, 0, 0], [0, 8, 8, 8, 0], [0, 8, 4, 8, 0], [0, 8, 8, 8, 0], [0, 0, 0, 0, 0]]

results = {}
results['train_1'] = analyze_example(train_1_in, train_1_out)
results['train_2'] = analyze_example(train_2_in, train_2_out)
results['train_3'] = analyze_example(train_3_in, train_3_out)
results['test_1'] = analyze_example(test_1_in, test_1_out)

import json
print(json.dumps(results, indent=2))
```
``` failed
Traceback (most recent call last):
  File "<string>", line 126, in <module>
  File "__init__.py", line 238, in dumps
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "encoder.py", line 202, in encode
    chunks = list(chunks)
             ^^^^^^^^^^^^
  File "encoder.py", line 432, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 377, in _iterencode_dict
    raise TypeError(f'keys must be str, int, float, bool or None, '
TypeError: keys must be str, int, float, bool or None, not int64

```
Ah, the JSON dump failed because numpy integers (`int64`) are not directly serializable. Let's fix the tool code to convert numpy types to standard Python types before printing.


``` python
import numpy as np
import collections
import json # Import json inside the tool_code block

# Custom encoder to handle numpy types
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.bool_, bool)):
             return bool(obj)
        if isinstance(obj, tuple) and len(obj) > 0 and isinstance(obj[0], np.integer):
             return [int(x) for x in obj] # Convert tuples of numpy ints
        return super(NpEncoder, self).default(obj)


def analyze_example(input_grid_list, output_grid_list):
    inp = np.array(input_grid_list)
    out = np.array(output_grid_list)
    rows, cols = inp.shape
    metrics = {'shape': (rows, cols)}

    # Values and Counts
    non_zero_vals = inp[inp != 0]
    counts = collections.Counter(non_zero_vals)
    # Convert numpy keys to standard ints for JSON serialization
    metrics['value_counts'] = {int(k): int(v) for k, v in counts.items()}
    metrics['distinct_non_zero_values'] = sorted([int(k) for k in counts.keys()])

    # Tentative Source (Y) and Background (X) based on counts
    source_y = None
    background_x = None
    if len(counts) >= 2:
        # Convert keys to int before sorting if necessary, Counter handles it internally though
        sorted_counts = counts.most_common()
        background_x = int(sorted_counts[0][0])
        source_y = int(sorted_counts[-1][0])
    elif len(counts) == 1:
        background_x = int(list(counts.keys())[0])

    metrics['tentative_source_Y'] = source_y
    metrics['tentative_background_X'] = background_x

    source_coords = None
    background_neighbor_coords = []
    if source_y is not None:
        locs_y = np.argwhere(inp == source_y)
        if locs_y.size > 0:
            source_coords = tuple(locs_y[0]) # Assume unique source location
            metrics['source_Y_coords'] = tuple(map(int, source_coords)) # Convert numpy int64 to int
            # Find adjacent background X
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = source_coords[0] + dr, source_coords[1] + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor_val = inp[nr, nc]
                    if neighbor_val != 0 and neighbor_val != source_y:
                         # Found adjacent different non-zero: assume it's background X
                         if background_x is None or neighbor_val == background_x:
                              background_x = int(neighbor_val) # Confirm/set background X
                              background_neighbor_coords.append(tuple(map(int, (nr, nc)))) # Convert numpy int64 to int
                         # else: logic might need refinement if Y touches multiple other colors

    metrics['confirmed_background_X'] = background_x
    metrics['background_X_coords_near_Y'] = background_neighbor_coords

    # Identify Changed Cells (Input vs Output)
    changed_mask = inp != out
    changed_coords = np.argwhere(changed_mask)
    metrics['changed_cell_count'] = len(changed_coords)

    # Identify Filled Cells (Input 0 -> Output Y)
    filled_mask = (inp == 0) & (out == source_y)
    filled_coords = [tuple(map(int, coord)) for coord in np.argwhere(filled_mask)] # Convert numpy int64 to int
    metrics['filled_hole_coords'] = filled_coords

    # Identify Source Cell Change (Input Y -> Output X)
    source_changed = False
    if source_coords is not None and background_x is not None:
       # Ensure source_coords are Python ints for indexing if necessary (numpy handles it)
       py_source_coords = tuple(map(int, source_coords))
       if inp[py_source_coords] == source_y and out[py_source_coords] == background_x:
           source_changed = True
    metrics['source_Y_changed_to_X'] = source_changed

    # Analyze Hole Properties (using filled_coords as proxy for hole)
    hole_on_boundary = False
    if filled_coords:
        for r, c in filled_coords:
            # Ensure r, c are standard ints
            r_int, c_int = int(r), int(c)
            if r_int == 0 or c_int == 0 or r_int == rows - 1 or c_int == cols - 1:
                hole_on_boundary = True
                break
    metrics['hole_touches_boundary'] = bool(hole_on_boundary) # Ensure boolean

    # Verify hole neighbors in input
    hole_neighbors_valid = True
    invalid_neighbor_coords = []
    if filled_coords and background_x is not None:
        visited_hole_neighbors = set()
        q = collections.deque(filled_coords)
        processed_in_bfs = set(filled_coords) # Use python tuples

        while q:
            r, c = q.popleft() # r, c are standard ints now
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                 nr, nc = r + dr, c + dc
                 neighbor_coord = (nr, nc)

                 if 0 <= nr < rows and 0 <= nc < cols:
                     # Check neighbors *not* part of the hole itself
                     if neighbor_coord not in processed_in_bfs:
                          # Avoid re-checking same neighbor cell
                          if neighbor_coord not in visited_hole_neighbors:
                               visited_hole_neighbors.add(neighbor_coord)
                               neighbor_val = inp[nr, nc]
                               if neighbor_val != 0 and int(neighbor_val) != background_x: # Convert numpy int
                                    hole_neighbors_valid = False
                                    invalid_neighbor_coords.append(neighbor_coord)
                 # else: out of bounds neighbors are ok
    metrics['hole_only_borders_X_or_0'] = bool(hole_neighbors_valid) # Ensure boolean
    metrics['hole_invalid_neighbor_coords'] = [tuple(map(int, coord)) for coord in invalid_neighbor_coords] # Ensure tuples of standard ints


    return metrics


# Example Data
train_1_in = [[4, 4, 4, 0, 0], [4, 0, 4, 0, 0], [3, 4, 4, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
train_1_out = [[4, 4, 4, 0, 0], [4, 3, 4, 0, 0], [4, 4, 4, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
train_2_in = [[0, 0, 0, 0, 0], [0, 1, 1, 1, 1], [0, 1, 0, 0, 1], [0, 1, 0, 0, 1], [0, 1, 1, 1, 5]]
train_2_out = [[0, 0, 0, 0, 0], [0, 1, 1, 1, 1], [0, 1, 5, 5, 1], [0, 1, 5, 5, 1], [0, 1, 1, 1, 1]]
train_3_in = [[6, 6, 6, 6, 6], [6, 0, 0, 0, 6], [6, 0, 0, 0, 6], [6, 0, 0, 0, 6], [6, 6, 6, 6, 5]]
train_3_out = [[6, 6, 6, 6, 6], [6, 5, 5, 5, 6], [6, 5, 5, 5, 6], [6, 5, 5, 5, 6], [6, 6, 6, 6, 6]]
test_1_in = [[0, 0, 0, 0, 0], [0, 8, 8, 4, 0], [0, 8, 0, 8, 0], [0, 8, 8, 8, 0], [0, 0, 0, 0, 0]]
test_1_out = [[0, 0, 0, 0, 0], [0, 8, 8, 8, 0], [0, 8, 4, 8, 0], [0, 8, 8, 8, 0], [0, 0, 0, 0, 0]]

results = {}
results['train_1'] = analyze_example(train_1_in, train_1_out)
results['train_2'] = analyze_example(train_2_in, train_2_out)
results['train_3'] = analyze_example(train_3_in, train_3_out)
results['test_1'] = analyze_example(test_1_in, test_1_out)


print(json.dumps(results, indent=2, cls=NpEncoder))
```
```
{
  "train_1": {
    "shape": [
      5,
      5
    ],
    "value_counts": {
      "4": 7,
      "3": 1
    },
    "distinct_non_zero_values": [
      3,
      4
    ],
    "tentative_source_Y": 3,
    "tentative_background_X": 4,
    "source_Y_coords": [
      2,
      0
    ],
    "confirmed_background_X": 4,
    "background_X_coords_near_Y": [
      [
        2,
        1
      ],
      [
        1,
        0
      ]
    ],
    "changed_cell_count": 2,
    "filled_hole_coords": [
      [
        1,
        1
      ]
    ],
    "source_Y_changed_to_X": true,
    "hole_touches_boundary": false,
    "hole_only_borders_X_or_0": true,
    "hole_invalid_neighbor_coords": []
  },
  "train_2": {
    "shape": [
      5,
      5
    ],
    "value_counts": {
      "1": 11,
      "5": 1
    },
    "distinct_non_zero_values": [
      1,
      5
    ],
    "tentative_source_Y": 5,
    "tentative_background_X": 1,
    "source_Y_coords": [
      4,
      4
    ],
    "confirmed_background_X": 1,
    "background_X_coords_near_Y": [
      [
        4,
        3
      ],
      [
        3,
        4
      ]
    ],
    "changed_cell_count": 5,
    "filled_hole_coords": [
      [
        2,
        2
      ],
      [
        2,
        3
      ],
      [
        3,
        2
      ],
      [
        3,
        3
      ]
    ],
    "source_Y_changed_to_X": true,
    "hole_touches_boundary": false,
    "hole_only_borders_X_or_0": true,
    "hole_invalid_neighbor_coords": []
  },
  "train_3": {
    "shape": [
      5,
      5
    ],
    "value_counts": {
      "6": 15,
      "5": 1
    },
    "distinct_non_zero_values": [
      5,
      6
    ],
    "tentative_source_Y": 5,
    "tentative_background_X": 6,
    "source_Y_coords": [
      4,
      4
    ],
    "confirmed_background_X": 6,
    "background_X_coords_near_Y": [
      [
        4,
        3
      ],
      [
        3,
        4
      ]
    ],
    "changed_cell_count": 10,
    "filled_hole_coords": [
      [
        1,
        1
      ],
      [
        1,
        2
      ],
      [
        1,
        3
      ],
      [
        2,
        1
      ],
      [
        2,
        2
      ],
      [
        2,
        3
      ],
      [
        3,
        1
      ],
      [
        3,
        2
      ],
      [
        3,
        3
      ]
    ],
    "source_Y_changed_to_X": true,
    "hole_touches_boundary": false,
    "hole_only_borders_X_or_0": true,
    "hole_invalid_neighbor_coords": []
  },
  "test_1": {
    "shape": [
      5,
      5
    ],
    "value_counts": {
      "8": 7,
      "4": 1
    },
    "distinct_non_zero_values": [
      4,
      8
    ],
    "tentative_source_Y": 4,
    "tentative_background_X": 8,
    "source_Y_coords": [
      1,
      3
    ],
    "confirmed_background_X": 8,
    "background_X_coords_near_Y": [
      [
        1,
        2
      ],
      [
        2,
        3
      ]
    ],
    "changed_cell_count": 2,
    "filled_hole_coords": [
      [
        2,
        2
      ]
    ],
    "source_Y_changed_to_X": true,
    "hole_touches_boundary": false,
    "hole_only_borders_X_or_0": true,
    "hole_invalid_neighbor_coords": []
  }
}

```
**Metrics Analysis:**

The metrics strongly support the revised hypotheses:

1.  **Source (Y) and Background (X):** In all examples, the least frequent non-zero value (`tentative_source_Y`) is indeed the Source `Y`, and it is always adjacent to the most frequent non-zero value (`tentative_background_X`), which acts as the Background `X`. The `confirmed_background_X` matches `tentative_background_X` in all cases.
2.  **Hole Identification:**
    *   The `filled_hole_coords` correctly identify the cells that change from 0 in the input to `Y` in the output.
    *   Crucially, in all examples, `hole_touches_boundary` is `false`. This confirms that the target hole is always internal.
    *   Also, `hole_only_borders_X_or_0` is `true` for all examples, confirming that the identified hole region is only adjacent to the Background `X` value or other zeros within the hole.
3.  **Transformation:** `source_Y_changed_to_X` is `true` in all cases, confirming the second part of the transformation.

This confirms the refined strategy: identify `Y` (unique, adjacent to other non-zero `X`), identify `X` (adjacent to `Y`), find the *internal* hole `H` (component of zeros bordered only by `X`, not touching grid boundary), fill `H` with `Y`, change `Y`'s original location to `X`.

## Revised Facts


```yaml
objects:
  - name: InputGrid
    type: 2D Array of Integers
  - name: OutputGrid
    type: 2D Array of Integers
  - name: SourceCell
    description: >
      A unique cell containing a non-zero integer (Y) which is the least frequent
      non-zero value in the grid and is orthogonally adjacent to at least one cell
      containing a *different* non-zero integer (X).
    properties:
      - value: Y (integer, Y != 0)
      - location: Coordinate (row_y, col_y)
      - relationship: Is adjacent to at least one BackgroundCell
      - property: Least frequent non-zero value
  - name: BackgroundValue
    description: >
      The non-zero integer value (X) found in cells orthogonally adjacent to the
      SourceCell (Y). X != Y. X is typically the most frequent non-zero value.
    properties:
      - value: X (integer, X != 0, X != Y)
      - property: Adjacent to SourceCell
      - property: Usually most frequent non-zero value
  - name: InternalHoleRegion
    description: >
      A connected component of zero (0) valued cells where all orthogonally adjacent
      non-zero cells have the BackgroundValue (X), AND no cell within this component
      is located on the boundary of the grid (row 0, col 0, max_row, max_col).
    properties:
      - value: 0 (integer)
      - cells: List of coordinates (row_h, col_h)
      - connectivity: Orthogonal
      - relationship: All non-zero neighbors have BackgroundValue (X)
      - constraint: Does not touch grid boundary

actions:
  - name: IdentifySourceAndBackground
    description: >
      Scan the InputGrid to find the unique SourceCell (Y at (row_y, col_y)) based
      on its properties (least frequent non-zero, adjacent to a different non-zero).
      Identify the BackgroundValue (X) from the neighbors of the SourceCell.
  - name: IdentifyInternalHole
    description: >
      Find all connected components of zero-valued cells in the InputGrid.
      Filter these components to keep only those where all non-zero neighbors have
      the BackgroundValue (X). From the filtered set, select the single component
      where none of its cells lie on the grid boundary. This is the InternalHoleRegion (H).
  - name: FillHole
    description: >
      Modify a copy of the InputGrid (OutputGrid) by setting the value of all
      cells within the identified InternalHoleRegion (H) to the value (Y) of the SourceCell.
  - name: UpdateSourceLocation
    description: >
      In the OutputGrid, set the value of the cell at the SourceCell's original
      location (row_y, col_y) to the BackgroundValue (X).
  - name: GenerateOutput
    description: The final modified OutputGrid after FillHole and UpdateSourceLocation.

relationships:
  - type: Adjacency
    between: [SourceCell, Cell with BackgroundValue]
    details: The SourceCell shares an orthogonal edge with at least one cell having the BackgroundValue (X).
  - type: Bordering
    between: [InternalHoleRegion, Cells with BackgroundValue]
    details: All non-zero orthogonal neighbors of any cell in the InternalHoleRegion must have the BackgroundValue (X).
  - type: Spatial Constraint
    on: InternalHoleRegion
    details: No cell within the InternalHoleRegion can have a row or column index equal to 0 or the maximum row/column index of the grid.

constraints:
  - There is exactly one SourceCell value (Y).
  - The SourceCell (Y) is adjacent to cells with exactly one other non-zero value (X).
  - There is exactly one InternalHoleRegion satisfying the definition.
```


## Revised Natural Language Program

1.  **Initialize:** Create a copy of the `InputGrid` to serve as the `OutputGrid`.
2.  **Identify Source Cell (Y) and Background Value (X):**
    *   Count the occurrences of each non-zero value in the `InputGrid`.
    *   Identify the non-zero value `Y` that occurs least frequently.
    *   Find the unique coordinates `(r_y, c_y)` of the cell containing `Y`.
    *   Check the orthogonal neighbors of `(r_y, c_y)`. Identify the non-zero value `X` such that `X != Y` found in these neighbors. This is the `BackgroundValue`.
3.  **Identify Internal Hole Region (H):**
    *   Find all connected components of cells with value 0 in the `InputGrid`.
    *   For each zero component:
        *   Check if *all* its orthogonally adjacent non-zero neighbors have the `BackgroundValue` `X`.
        *   Check if *any* cell within the component lies on the grid boundary (row 0, col 0, max row, max col).
    *   Select the single zero component `H` that satisfies the neighbor condition (all non-zero neighbors are `X`) AND does *not* touch the grid boundary.
4.  **Fill Hole:** Iterate through all cells `(r_h, c_h)` identified as part of the `InternalHoleRegion` `H`. Set the value of `OutputGrid[r_h][c_h]` to the source value `Y`.
5.  **Update Source Location:** Set the value of the `OutputGrid` at the original location of the source cell: `OutputGrid[r_y][c_y] = X`.
6.  **Finalize:** The `OutputGrid` now holds the final transformed state.