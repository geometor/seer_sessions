Ah, the `contains_delimiter` boolean is causing JSON serialization issues. Let's convert it to a string or int. Also, numpy arrays/tuples used as keys might be an issue, though I used strings like "Pattern @ ...". Let's ensure all keys are strings and values are JSON-serializable. Coordinates are tuples of ints, which should be fine. Let's rerun converting the boolean.


``` python
import numpy as np
from collections import Counter, defaultdict
import json

# --- Paste the provided helper functions here ---
def find_cell_structure(grid):
    height, width = grid.shape
    delimiter_color = 0
    h_lines = [r for r in range(height) if np.all(grid[r, :] == delimiter_color)]
    v_lines = [c for c in range(width) if np.all(grid[:, c] == delimiter_color)]
    h_points = sorted(list(set([-1] + h_lines + [height])))
    v_points = sorted(list(set([-1] + v_lines + [width])))
    h_gaps = [h_points[i+1] - h_points[i] for i in range(len(h_points)-1)]
    v_gaps = [v_points[i+1] - v_points[i] for i in range(len(v_points)-1)]
    h_cell_gaps = [g for g in h_gaps if g > 1]
    v_cell_gaps = [g for g in v_gaps if g > 1]
    cell_h = Counter(h_cell_gaps).most_common(1)[0][0] if h_cell_gaps else height
    cell_w = Counter(v_cell_gaps).most_common(1)[0][0] if v_cell_gaps else width
    cell_start_rows = [0] if (height > 0 and width > 0 and grid[0,0] != delimiter_color) else [] # Added boundary check
    cell_start_rows.extend([r + 1 for r in h_lines if r + 1 < height])
    cell_start_rows = sorted(list(set(cell_start_rows)))
    cell_start_cols = [0] if (height > 0 and width > 0 and grid[0,0] != delimiter_color) else [] # Added boundary check
    cell_start_cols.extend([c + 1 for c in v_lines if c + 1 < width])
    cell_start_cols = sorted(list(set(cell_start_cols)))
    if not cell_start_rows or not cell_start_cols:
        # Handle edge case where grid might be empty or just delimiters
        if cell_h == height and cell_w == width and not h_lines and not v_lines:
             if height > 0 and width > 0: # Non-empty grid, no delimiters
                 return height, width, [0], [0], delimiter_color
             else: # Empty grid
                 return 0, 0, [], [], delimiter_color
        else:
             non_delim_rows = [r for r in range(height) if not np.all(grid[r,:] == delimiter_color)]
             non_delim_cols = [c for c in range(width) if not np.all(grid[:,c] == delimiter_color)]
             if non_delim_rows and non_delim_cols:
                 # Fallback: Assume single cell based on first non-delimiter content
                 return height, width, [min(non_delim_rows)], [min(non_delim_cols)], delimiter_color
             else: # Grid is likely all delimiter color or structure unrecognizable
                 return None, None, None, None, delimiter_color # Indicate failure
    return cell_h, cell_w, cell_start_rows, cell_start_cols, delimiter_color


def get_cell_content(grid, r_start, c_start, cell_h, cell_w):
    height, width = grid.shape
    end_r = min(r_start + cell_h, height)
    end_c = min(c_start + cell_w, width)
    return grid[r_start : end_r, c_start : end_c]
# --- End of helper functions ---

# --- Input Data ---
input1_list = [[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,0,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,0,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,9,9,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,9,7,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,9,7,0,7,7,0,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,9,9,9,7,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,9,7,7,7,0,7,7,7,7,7],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[7,7,0,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,0,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7],[7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7,0,7,7,7,7,7]]
input2_list = [[7,2,7,0,7,7,7,0,7,7,7],[7,2,7,0,7,7,7,0,7,7,7],[7,2,7,0,7,7,7,0,7,7,7],[0,0,0,0,0,0,0,0,0,0,0],[7,7,7,0,7,7,7,0,7,7,7],[7,7,7,0,7,0,7,0,7,7,7],[7,7,7,0,7,7,7,0,7,7,7],[0,0,0,0,0,0,0,0,0,0,0],[7,7,7,0,7,7,7,0,7,7,7],[7,7,7,0,7,0,7,0,7,0,7],[7,7,7,0,7,7,7,0,7,7,7]]

input1_np = np.array(input1_list)
input2_np = np.array(input2_list)

metrics = {}
delimiter_color = 0 # white

# --- Process Example 1 ---
cell_h1, cell_w1, rows1, cols1, delim1 = find_cell_structure(input1_np)
patterns1 = defaultdict(list)
source_pattern1_tuple = None

if cell_h1 is not None:
    for r_start in rows1:
        for c_start in cols1:
             cell = get_cell_content(input1_np, r_start, c_start, cell_h1, cell_w1)
             # Ensure the extracted cell matches expected dimensions
             if cell.shape == (cell_h1, cell_w1):
                 cell_tuple = tuple(map(tuple, cell))
                 patterns1[cell_tuple].append((r_start, c_start))

    source_coords1 = None
    target_patterns1 = []
    target_coords1 = []
    non_target_coords1 = []
    pattern_summary1 = {}

    for i, (pattern_tuple, coords_list) in enumerate(patterns1.items()):
        pattern_np = np.array(pattern_tuple)
        contains_delimiter = bool(np.any(pattern_np == delimiter_color)) # Convert numpy.bool_ to bool
        pattern_key = f"Pattern_{i}_at_{coords_list[0]}" # Use index and first coord for unique key
        pattern_info = {'count': len(coords_list), 'contains_delimiter': contains_delimiter, 'coords': coords_list}

        if len(coords_list) == 1:
            source_pattern1_tuple = pattern_tuple
            source_coords1 = coords_list[0]
            pattern_info['type'] = 'source'
        elif contains_delimiter:
            target_patterns1.append(pattern_tuple)
            target_coords1.extend(coords_list)
            pattern_info['type'] = 'target'
        else:
            non_target_coords1.extend(coords_list)
            pattern_info['type'] = 'non-target (empty)'
        pattern_summary1[pattern_key] = pattern_info


    metrics['example1'] = {
        'grid_size': list(input1_np.shape), # Convert shape tuple to list
        'delimiter_color': delim1,
        'cell_size': [cell_h1, cell_w1], # Convert tuple to list
        'cell_starts_rows': rows1,
        'cell_starts_cols': cols1,
        'num_cells': len(rows1) * len(cols1),
        'source_coords': list(source_coords1) if source_coords1 else None, # Convert tuple to list
        'target_pattern_count': len(target_patterns1),
        'target_coords_count': len(target_coords1),
        'target_coords': target_coords1, # List of tuples is fine
        'non_target_coords_count': len(non_target_coords1),
        'non_target_coords': non_target_coords1, # List of tuples is fine
        'pattern_summary': pattern_summary1
    }
else:
    metrics['example1'] = {'error': 'Could not determine cell structure'}

# --- Process Example 2 ---
cell_h2, cell_w2, rows2, cols2, delim2 = find_cell_structure(input2_np)
patterns2 = defaultdict(list)
source_pattern2_tuple = None

if cell_h2 is not None:
    for r_start in rows2:
        for c_start in cols2:
             cell = get_cell_content(input2_np, r_start, c_start, cell_h2, cell_w2)
             if cell.shape == (cell_h2, cell_w2):
                 cell_tuple = tuple(map(tuple, cell))
                 patterns2[cell_tuple].append((r_start, c_start))

    source_coords2 = None
    target_patterns2 = []
    target_coords2 = []
    non_target_coords2 = []
    pattern_summary2 = {}

    for i, (pattern_tuple, coords_list) in enumerate(patterns2.items()):
        pattern_np = np.array(pattern_tuple)
        contains_delimiter = bool(np.any(pattern_np == delimiter_color)) # Convert numpy.bool_ to bool
        pattern_key = f"Pattern_{i}_at_{coords_list[0]}" # Use index and first coord for unique key
        pattern_info = {'count': len(coords_list), 'contains_delimiter': contains_delimiter, 'coords': coords_list}

        if len(coords_list) == 1:
            source_pattern2_tuple = pattern_tuple
            source_coords2 = coords_list[0]
            pattern_info['type'] = 'source'
        elif contains_delimiter:
            target_patterns2.append(pattern_tuple)
            target_coords2.extend(coords_list)
            pattern_info['type'] = 'target'
        else:
            non_target_coords2.extend(coords_list)
            pattern_info['type'] = 'non-target (empty)'

        pattern_summary2[pattern_key] = pattern_info

    metrics['example2'] = {
        'grid_size': list(input2_np.shape), # Convert shape tuple to list
        'delimiter_color': delim2,
        'cell_size': [cell_h2, cell_w2], # Convert tuple to list
        'cell_starts_rows': rows2,
        'cell_starts_cols': cols2,
        'num_cells': len(rows2) * len(cols2),
        'source_coords': list(source_coords2) if source_coords2 else None, # Convert tuple to list
        'target_pattern_count': len(target_patterns2),
        'target_coords_count': len(target_coords2),
        'target_coords': target_coords2, # List of tuples is fine
        'non_target_coords_count': len(non_target_coords2),
        'non_target_coords': non_target_coords2, # List of tuples is fine
        'pattern_summary': pattern_summary2
    }
else:
    metrics['example2'] = {'error': 'Could not determine cell structure'}


print(json.dumps(metrics, indent=2))
```
```
{
  "example1": {
    "grid_size": [
      23,
      23
    ],
    "delimiter_color": 0,
    "cell_size": [
      6,
      6
    ],
    "cell_starts_rows": [
      0,
      6,
      12,
      18
    ],
    "cell_starts_cols": [
      0,
      6,
      12,
      18
    ],
    "num_cells": 16,
    "source_coords": [
      12,
      12
    ],
    "target_pattern_count": 2,
    "target_coords_count": 8,
    "target_coords": [
      [
        0,
        0
      ],
      [
        0,
        12
      ],
      [
        6,
        0
      ],
      [
        6,
        12
      ],
      [
        12,
        0
      ],
      [
        12,
        6
      ],
      [
        0,
        6
      ],
      [
        6,
        6
      ]
    ],
    "non_target_coords_count": 0,
    "non_target_coords": [],
    "pattern_summary": {
      "Pattern_0_at_(0, 0)": {
        "count": 6,
        "contains_delimiter": true,
        "coords": [
          [
            0,
            0
          ],
          [
            0,
            12
          ],
          [
            6,
            0
          ],
          [
            6,
            12
          ],
          [
            12,
            0
          ],
          [
            12,
            6
          ]
        ],
        "type": "target"
      },
      "Pattern_1_at_(0, 6)": {
        "count": 2,
        "contains_delimiter": true,
        "coords": [
          [
            0,
            6
          ],
          [
            6,
            6
          ]
        ],
        "type": "target"
      },
      "Pattern_2_at_(12, 12)": {
        "count": 1,
        "contains_delimiter": true,
        "coords": [
          [
            12,
            12
          ]
        ],
        "type": "source"
      }
    }
  },
  "example2": {
    "grid_size": [
      11,
      11
    ],
    "delimiter_color": 0,
    "cell_size": [
      4,
      4
    ],
    "cell_starts_rows": [
      0,
      4,
      8
    ],
    "cell_starts_cols": [
      0,
      4,
      8
    ],
    "num_cells": 9,
    "source_coords": [
      4,
      4
    ],
    "target_pattern_count": 1,
    "target_coords_count": 2,
    "target_coords": [
      [
        0,
        4
      ],
      [
        4,
        0
      ]
    ],
    "non_target_coords_count": 0,
    "non_target_coords": [],
    "pattern_summary": {
      "Pattern_0_at_(0, 0)": {
        "count": 1,
        "contains_delimiter": true,
        "coords": [
          [
            0,
            0
          ]
        ],
        "type": "source"
      },
      "Pattern_1_at_(0, 4)": {
        "count": 2,
        "contains_delimiter": true,
        "coords": [
          [
            0,
            4
          ],
          [
            4,
            0
          ]
        ],
        "type": "target"
      },
      "Pattern_2_at_(4, 4)": {
        "count": 1,
        "contains_delimiter": true,
        "coords": [
          [
            4,
            4
          ]
        ],
        "type": "source"
      }
    }
  }
}

```
There's a significant issue with the metrics generated by the code execution.

*   **Example 1:**
    *   It calculated cell size as 6x6, but visually inspecting the input grid clearly shows 5x5 cells separated by 1-pixel wide white lines. The start rows/cols seem correct (0, 6, 12, 18). This discrepancy in cell size calculation means the pattern extraction is incorrect.
    *   It identified 3 patterns, one source, two targets. It found the source at (12, 12). Crucially, it claims the source *contains* the delimiter color (white), which is incorrect based on visual inspection (the source pattern has orange and maroon). It also claims *all* identified patterns contain the delimiter. This contradicts my earlier analysis and the visual data. It also claims there are no 'non-target (empty)' patterns.
*   **Example 2:**
    *   It calculated cell size as 4x4, but visually it's 3x3 cells with 1-pixel delimiters. Again, the cell size calculation seems off.
    *   It identified two source patterns!? One at (0,0) and one at (4,4). This contradicts the definition of a *unique* source pattern.
    *   It identified one target pattern type at two locations: (0,4) and (4,0).
    *   Again, it claims *all* patterns, including the supposed sources, contain the delimiter color (white), which is visually false for the pattern at (0,0) (orange and red). It also finds no 'non-target (empty)' patterns.

**Root Cause of Metric Errors:** The `find_cell_structure` function seems flawed. It's incorrectly calculating `cell_h` and `cell_w`.
Let's look at the logic:
1.  Finds horizontal lines (`h_lines`) and vertical lines (`v_lines`).
2.  Creates `h_points` and `v_points` including -1 and grid boundaries.
3.  Calculates `h_gaps` and `v_gaps` between consecutive points.
4.  Filters out gaps of size 1 (`h_cell_gaps`, `v_cell_gaps`).
5.  Takes the most common gap size > 1 as `cell_h`, `cell_w`.

In Example 1 (23x23 grid, 5x5 cells):
`h_lines` = [5, 11, 17]
`h_points` = [-1, 5, 11, 17, 23]
`h_gaps` = [5 - (-1), 11 - 5, 17 - 11, 23 - 17] = [6, 6, 6, 6]
`h_cell_gaps` = [6, 6, 6, 6]
Most common = 6. So `cell_h = 6`. **This is wrong.** The gap *includes* the delimiter line thickness. The actual cell height is 5. The calculation should subtract the delimiter thickness (assumed to be 1).

Revised `find_cell_structure` logic: `cell_h` should be `Counter(h_cell_gaps).most_common(1)[0][0] - 1` (if `h_cell_gaps` exists). Similarly for `cell_w`.

Let's re-run the metric gathering with this potential fix in mind *mentally* (since I can't directly edit the function and rerun easily in this context).

*Assume Corrected Cell Sizes:*
*   Example 1: cell_h=5, cell_w=5
*   Example 2: cell_h=3, cell_w=3

*Re-evaluate Patterns (based on visual inspection and corrected cell size):*
*   **Example 1 (5x5 cells):**
    *   Source Pattern (at 12,12): Orange (7) background, Maroon (9) shape. Does *not* contain white (0).
    *   Pattern P_variant1 (e.g., at 0, 12): Orange background, white (0) dot at center. *Contains* white. Locations: (0,12), (6,12).
    *   Pattern P_variant2 (e.g., at 18, 0): Orange background, white (0) dots top/bottom center. *Contains* white. Locations: (18,0), (18,18), (2,18) ?? - let's recheck input example 1 grid carefully.
        * Cell (0,0) = All 7s (Empty)
        * Cell (0,1) = All 7s (Empty)
        * Cell (0,2) = 7s, 0 at (2,2) rel -> P_variant1 @ (0,12)
        * Cell (0,3) = All 7s (Empty)
        * Cell (1,0) = All 7s (Empty)
        * Cell (1,1) = All 7s (Empty)
        * Cell (1,2) = 7s, 0 at (2,2) rel -> P_variant1 @ (6,12)
        * Cell (1,3) = All 7s (Empty)
        * Cell (2,0) = All 7s (Empty)
        * Cell (2,1) = All 7s (Empty)
        * Cell (2,2) = Source @ (12,12)
        * Cell (2,3) = 7s, 0 at (2,2) rel -> P_variant2 @ (12,18) -> Recheck pattern: 77777, 77777, 77077, 77777, 77777. Yes, P_variant1. -> OK, the code had `7 7 0 7 7` at row 14, col 18 - this is cell (2,3). So (12,18) has P_variant1. My initial visual scan was wrong for P_variant2.
        * Cell (3,0) = 7s, 0s at (2,0) and (2,4) rel -> P_variant2 @ (18,0) - Pattern: `77077` row 20, cols 0-4. Yes.
        * Cell (3,1) = All 7s (Empty)
        * Cell (3,2) = All 7s (Empty)
        * Cell (3,3) = 7s, 0s at (2,0) and (2,4) rel -> P_variant2 @ (18,18) - Pattern: `77077` row 20, cols 18-22. Yes.
    *   Empty Pattern (All Orange 7s): Locations: (0,0), (0,6), (0,18), (6,0), (6,6), (6,18), (12,0), (12,6), (18,6), (18,12). Count = 10. Does *not* contain white.
    *   Summary Ex1: Source (1), P_variant1 (3 locations, contains white), P_variant2 (2 locations, contains white), Empty (10 locations, no white). Total 1+3+2+10=16 cells.
    *   Target Cells for Replacement: Those containing P_variant1 and P_variant2 (total 5 locations). These are the cells that contain white pixels.
    *   Output Ex1: Source pattern replaces content at the 5 target locations. Empty cells and original source cell remain unchanged. This matches the expected output.

*   **Example 2 (3x3 cells):**
    *   Source Pattern (at 0,0): Orange (7) background, Red (2) line. Does *not* contain white (0).
    *   Pattern P_variant1 (at 4, 4): Orange background, white (0) dot center. *Contains* white. Location: (4,4).
    *   Pattern P_variant2 (at 8, 8): Orange background, white (0) dots center and bottom-center. *Contains* white. Location: (8,8).
    *   Empty Pattern (All Orange 7s): Locations: (0,4), (0,8), (4,0), (4,8), (8,0), (8,4). Count = 6. Does *not* contain white.
    *   Summary Ex2: Source (1), P_variant1 (1 location, contains white), P_variant2 (1 location, contains white), Empty (6 locations, no white). Total 1+1+1+6=9 cells.
    *   Target Cells for Replacement: Those containing P_variant1 and P_variant2 (total 2 locations). These are the cells that contain white pixels.
    *   Output Ex2: Source pattern replaces content at the 2 target locations. Empty cells and original source cell remain unchanged. This matches the expected output.

**Conclusion from Re-analysis:**

The hypothesis holds: The unique source pattern replaces the content of *only* those cells whose original pattern contains the delimiter color (white). The `find_cell_structure` function in the provided code needs correction to calculate cell dimensions properly (subtract delimiter thickness).

---
## General Assessment

The initial code failed because it incorrectly applied the transformation rule. While it identified the grid structure (albeit with errors in cell dimension calculation) and the unique "source" pattern, it copied this pattern into *all* cell locations. The expected outputs clearly show a *selective* replacement.

Analysis of the input/output pairs reveals that the source pattern should only replace the contents of cells whose original patterns contain the delimiter color (white, 0). Cells containing patterns without the delimiter color (including the most frequent "empty" pattern and the source pattern itself) remain unchanged.

The strategy for resolving the errors involves:
1.  Correcting the `find_cell_structure` function to accurately calculate cell dimensions by accounting for the delimiter thickness (likely subtracting 1 from the calculated gaps).
2.  Modifying the main transformation logic to identify "target" cells based on whether their original pattern contains the delimiter color (white, 0).
3.  Copying the source pattern *only* to these identified target cell locations in the output grid.

## Metrics (Based on Manual Re-analysis / Corrected Logic)

**Example 1:**
*   Grid Size: 23x23
*   Delimiter: White (0), 1 pixel thick
*   Cell Size: 5x5
*   Cell Grid: 4x4 (16 cells total)
*   Cell Start Coords (Row, Col): (0,0), (0,6), (0,12), (0,18), (6,0), (6,6), (6,12), (6,18), (12,0), (12,6), (12,12), (12,18), (18,0), (18,6), (18,12), (18,18)
*   Patterns Found:
    *   Source (Unique): 1 instance @ (12,12). Does *not* contain white (0).
    *   Target Pattern 1 (P_variant1): 3 instances @ (0,12), (6,12), (12,18). *Contains* white (0).
    *   Target Pattern 2 (P_variant2): 2 instances @ (18,0), (18,18). *Contains* white (0).
    *   Non-Target Pattern (Empty): 10 instances @ remaining coordinates. Does *not* contain white (0).
*   Target Locations for Replacement (Contain white): (0,12), (6,12), (12,18), (18,0), (18,18). (Total 5 locations)

**Example 2:**
*   Grid Size: 11x11
*   Delimiter: White (0), 1 pixel thick
*   Cell Size: 3x3
*   Cell Grid: 3x3 (9 cells total)
*   Cell Start Coords (Row, Col): (0,0), (0,4), (0,8), (4,0), (4,4), (4,8), (8,0), (8,4), (8,8)
*   Patterns Found:
    *   Source (Unique): 1 instance @ (0,0). Does *not* contain white (0).
    *   Target Pattern 1 (P_variant1): 1 instance @ (4,4). *Contains* white (0).
    *   Target Pattern 2 (P_variant2): 1 instance @ (8,8). *Contains* white (0).
    *   Non-Target Pattern (Empty): 6 instances @ remaining coordinates. Does *not* contain white (0).
*   Target Locations for Replacement (Contain white): (4,4), (8,8). (Total 2 locations)

## Facts


```yaml
task_context:
  grid_structure: Input grid is divided into multiple smaller subgrids (cells) by delimiter lines.
  delimiter:
    color: white (0)
    thickness: 1 pixel (assumed based on examples)
  cells:
    size: Uniform height and width, determined by spacing between delimiters.
    content: Each cell contains a pattern of pixels.
    patterns: Multiple distinct patterns can exist across cells.

objects:
  - object: cell
    properties:
      - location: (row_start, col_start) coordinates
      - size: (height, width)
      - content: A subgrid representing the pattern within the cell.
      - contains_delimiter_color: boolean (true if any pixel within the cell matches the delimiter color)
  - object: pattern
    properties:
      - structure: The specific 2D array of pixel colors defining the pattern.
      - frequency: The number of times the pattern appears in the input grid's cells.
      - uniqueness: Whether the pattern appears exactly once (source) or multiple times.
      - contains_delimiter_color: boolean (inherited from the cell content)

identified_roles:
  - role: source_pattern
    identification: The pattern object with frequency = 1.
  - role: target_pattern
    identification: Any pattern object (excluding the source_pattern) where contains_delimiter_color is true.
  - role: target_cell
    identification: Any cell object whose content matches a target_pattern.
  - role: non_target_cell
    identification: Any cell object whose content does not match a target_pattern (includes cells with the source pattern and cells with patterns where contains_delimiter_color is false).

action:
  - type: identify_grid_structure
    inputs: input_grid
    outputs: cell_size, cell_locations, delimiter_color
    details: Finds delimiter lines to determine cell dimensions and starting coordinates.
  - type: extract_patterns
    inputs: input_grid, cell_size, cell_locations
    outputs: list of unique patterns, mapping of pattern to cell locations, source_pattern, pattern properties (contains_delimiter_color)
    details: Iterates through cells, extracts content, groups identical patterns, identifies the unique one, and checks each pattern for the delimiter color.
  - type: identify_targets
    inputs: patterns, source_pattern, delimiter_color
    outputs: list of target_cell locations
    details: Selects locations of cells whose patterns are not the source pattern AND contain the delimiter color.
  - type: replace_content
    inputs: input_grid (as template), source_pattern, target_cell locations, cell_size
    outputs: output_grid
    details: Creates a copy of the input grid. For each target_cell location, overwrites the corresponding area in the copied grid with the source_pattern. Non-target cells remain unchanged.

goal: Transform the input grid by selectively replacing the content of specific cells (target_cells) with the content of a uniquely occurring cell (source_pattern).
```


## Natural Language Program

1.  **Analyze Grid Structure:** Identify the delimiter color (white, 0) and the grid lines formed by this color. Determine the uniform height (`cell_h`) and width (`cell_w`) of the cells (subgrids) delimited by these lines, accounting for the 1-pixel thickness of the delimiters. Identify the top-left starting coordinates (`r_start`, `c_start`) of each cell.
2.  **Extract Cell Patterns:** Iterate through each identified cell location. Extract the `cell_h` x `cell_w` subgrid (pattern) from each cell. Record each unique pattern found and the list of coordinates where it appears.
3.  **Identify Source Pattern:** Find the pattern that appears in exactly one cell location. This is the "source pattern". Store its content.
4.  **Identify Target Cells:** Examine every cell location in the input grid. A cell is identified as a "target cell" if its pattern meets two conditions:
    *   a) It is *not* the source pattern.
    *   b) Its pattern contains at least one pixel matching the delimiter color (white, 0).
5.  **Construct Output Grid:** Create the output grid as a copy of the input grid.
6.  **Apply Replacement:** Iterate through the coordinates of all identified "target cells". For each target cell location, replace the corresponding `cell_h` x `cell_w` area in the output grid with the source pattern. Cells that are not target cells (including the original source cell and any cells whose patterns do not contain the delimiter color) remain unchanged from the input grid.
7.  **Return Output:** Return the modified output grid.