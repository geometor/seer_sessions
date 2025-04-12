**General Assessment and Strategy**

The previous code execution failed because it implemented a standard priority flood fill where each non-background neighbor propagated its own color. Analysis of the input/output pairs revealed that a specific mapping from the initial "source" colors (S) adjacent to the background (BG) to the actual "fill" colors (F) is required.

The metrics gathered using `infer_mapping` (based on Hypothesis 15) confirmed that such a map exists and accurately predicts the observed fill colors for each training example. However, deriving this map *predictively* from the input grid alone remains the key challenge.

Several hypotheses for deriving the S->F map were explored:
*   Mapping to the closest source with a higher index (Hypothesis 16): Failed.
*   Mapping based on adjacency to higher-index sources (Hypothesis 20): Showed promise on Examples 2 and 4 but failed on 1 and 3.

Given these findings, the strategy is:
1.  Adopt the clearest hypothesis for map derivation, acknowledging its potential limitations. Hypothesis 20 (Map S -> adjacent S' if S' > S) seems the most structured attempt, despite not fitting all examples perfectly. Assume the default map is identity (S->S) unless this adjacency rule applies.
2.  Implement the transformation using this derived map within the priority flood fill framework identified earlier. The fill process uses the *mapped* color from the source influence.
3.  Gather metrics based on this refined approach (H20 map + mapped fill).
4.  Update the YAML and Natural Language program to reflect this specific mapping rule and the subsequent fill process.

**Metrics Gathering (Hypothesis 20 Map)**


*code_execution:*

```python
import numpy as np
from collections import Counter
import json

# Helper function to convert numpy types to standard Python types for JSON
def convert_numpy_types(obj):
    if isinstance(obj, np.integer): return int(obj)
    if isinstance(obj, np.floating): return float(obj)
    if isinstance(obj, np.ndarray): return obj.tolist()
    if isinstance(obj, set): return sorted([convert_numpy_types(item) for item in obj])
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            key = int(k) if isinstance(k, np.integer) else k
            new_dict[key] = convert_numpy_types(v)
        return new_dict
    if isinstance(obj, list): return [convert_numpy_types(i) for i in obj]
    if isinstance(obj, np.bool_): return bool(obj)
    return obj

def get_neighbors(h, w, r, c):
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < h - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < w - 1: neighbors.append((r, c + 1))
    return neighbors

def find_background_color(grid_np):
    if grid_np.size == 0: return -1
    colors, counts = np.unique(grid_np, return_counts=True)
    if len(colors) == 0: return -1
    return colors[np.argmax(counts)]

def get_source_pixels_and_adjacency(grid_np, background_color):
    h, w = grid_np.shape
    sources = set()
    source_pixel_coords = {}
    source_adjacencies = {color: set() for color in np.unique(grid_np) if color != background_color}

    # First pass: identify all source colors and their locations
    all_non_bg_colors = set(np.unique(grid_np)) - {background_color}
    for color in all_non_bg_colors:
         source_pixel_coords[color] = []

    for r in range(h):
        for c in range(w):
            color = grid_np[r, c]
            if color != background_color:
                source_pixel_coords[color].append((r,c))
                # Check adjacency to background
                is_adj_to_bg = False
                for nr, nc in get_neighbors(h, w, r, c):
                    if grid_np[nr, nc] == background_color:
                        is_adj_to_bg = True
                        break
                if is_adj_to_bg:
                    sources.add(color)

    # Second pass: determine adjacencies between source colors
    for s_color in sources:
        if s_color not in source_pixel_coords: continue
        for r, c in source_pixel_coords[s_color]:
            for nr, nc in get_neighbors(h, w, r, c):
                neighbor_color = grid_np[nr, nc]
                # Check if neighbor is a *different* source color
                if neighbor_color != background_color and neighbor_color != s_color and neighbor_color in sources:
                    source_adjacencies[s_color].add(neighbor_color)

    return sources, source_pixel_coords, source_adjacencies


def derive_map_hypothesis20(sources, source_adjacencies):
    """ Maps S -> S' if S is adjacent to S' and S' > S. Default S -> S. """
    mapping = {}
    for s in sources:
        map_target = s # Default: map to self
        highest_adjacent_source = -1
        # Check adjacent sources
        if s in source_adjacencies:
            for adj_s in source_adjacencies[s]:
                if adj_s > s: # Found adjacent source with higher index
                    if adj_s > highest_adjacent_source:
                        highest_adjacent_source = adj_s

        # If a higher adjacent source was found, map to the highest one
        if highest_adjacent_source != -1:
             map_target = highest_adjacent_source

        mapping[s] = map_target
    return mapping


# --- Input Data ---
# [Same train_inputs and train_outputs]
train_inputs = [
    [[0,0,0,2,2,0,0,0,0,0],[0,0,0,2,0,0,0,0,0,0],[0,0,0,0,1,1,0,0,0,0],[0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,0,0,2,0,0],[0,0,0,0,0,0,2,2,0,0],[1,0,0,0,0,0,0,0,0,0],[2,3,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,4,4],[0,0,0,0,0,0,0,0,0,4],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,0,0],[0,1,3,0,4,0,1,1,0,0],[0,4,5,0,4,4,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]],
    [[3,3,5,5,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,5,3,3,3,3,5,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,5,5,3,3,3,3,3,3,3,3,3],[3,3,3,3,2,2,3,3,3,3,3,3,3,3,3,3,3],[3,3,3,3,2,3,4,4,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,4,3,3,1,1,3,3,2,3,3,3],[3,3,3,3,3,3,3,3,3,3,1,3,2,2,3,3,3],[3,3,3,3,3,3,3,3,3,4,3,3,3,3,3,3,3],[3,3,1,6,3,3,3,3,4,4,3,3,3,3,3,3,3],[3,3,2,9,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,4,0,3,3,3,1,3,3,3,3,3,3,3,3,3],[3,3,8,9,3,3,3,1,1,3,3,3,3,3,3,3,3]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,4],[0,0,0,0,0,0,6,6,0,0,0,0,0,0,0,0,4,4],[0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[3,3,0,0,0,0,0,0,0,0,6,0,0,0,7,7,0,0],[6,7,0,0,0,0,0,0,0,6,6,0,0,0,7,7,0,0],[4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[7,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
]
train_outputs = [ # Not used for map derivation, only for comparison
    [[0,0,0,2,2,3,3,3,0,0],[0,0,0,2,3,3,3,3,0,0],[0,0,0,3,1,1,0,3,0,0],[0,0,0,3,1,0,0,3,0,0],[0,0,0,3,0,0,1,3,0,0],[0,0,0,3,0,1,1,3,0,0],[0,0,0,3,3,3,3,2,0,0],[0,0,0,3,3,3,2,2,0,0],[1,0,0,0,0,0,0,0,0,0],[2,3,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,5,5,5,5,4,4],[0,0,0,0,5,5,5,5,5,4],[0,0,0,0,5,1,1,3,5,5],[0,0,0,0,5,1,3,3,5,5],[0,0,0,0,5,3,3,3,5,5],[0,0,0,0,5,3,3,3,5,5],[0,0,0,0,5,3,3,1,5,5],[0,1,3,0,4,3,1,1,5,5],[0,4,5,0,4,4,5,5,5,5],[0,0,0,0,0,0,0,0,0,0]],
    [[3,3,5,5,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,5,3,3,3,3,5,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,5,5,3,3,3,3,3,3,3,3,3],[3,3,3,3,2,2,9,9,9,9,9,9,9,9,3,3,3],[3,3,3,3,2,9,9,9,9,9,9,9,9,9,3,3,3],[3,3,3,3,9,9,9,6,6,1,1,9,9,2,3,3,3],[3,3,3,3,9,9,9,6,6,6,1,9,2,2,3,3,3],[3,3,3,3,3,3,3,6,6,6,6,3,3,3,3,3,3],[3,3,1,6,3,3,3,6,6,6,6,3,3,3,3,3,3],[3,3,2,9,3,3,3,6,6,6,6,3,3,3,3,3,3],[3,3,4,0,3,3,3,1,6,6,6,3,3,3,3,3,3],[3,3,8,9,3,3,3,1,1,6,6,3,3,3,3,3,3]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4],[0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4],[0,0,0,0,0,0,6,6,7,7,7,0,4,4,4,4,4,4],[0,0,0,0,0,0,6,7,7,7,7,0,0,0,0,0,0,0],[0,0,0,0,0,0,7,7,7,7,7,0,0,0,0,0,0,0],[3,3,0,0,0,0,7,7,7,7,6,0,0,0,6,6,0,0],[6,7,0,0,0,0,7,7,7,6,6,0,0,0,6,6,0,0],[4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[7,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
]

results = []
# Store maps derived by inference (H15) and hypothesis (H20) for comparison
inferred_maps_h15 = [ # From previous analysis
    {1: 3, 2: 3, 3: 3},
    {1: 3, 4: 5},
    {1: 6, 2: 9, 4: 6},
    {3: 3, 4: 4, 6: 7, 7: 7}
]

for i, (input_grid, output_grid) in enumerate(zip(train_inputs, train_outputs)): # Output only used for observed F
    input_np = np.array(input_grid)
    output_np = np.array(output_grid)

    bg_color = find_background_color(input_np)
    sources, source_coords, source_adj = get_source_pixels_and_adjacency(input_np, bg_color)

    # Derive map using Hypothesis 20
    h20_map = derive_map_hypothesis20(sources, source_adj)
    h20_fill_colors = set(h20_map.values())

    # Get the previously inferred map (H15) for this example
    h15_map = inferred_maps_h15[i]
    h15_fill_colors = set(h15_map.values())

    # Calculate observed fill colors directly for comparison
    mask = (input_np == bg_color)
    fill_colors_observed = set(output_np[mask]) - {bg_color} if np.any(mask) else set()

    results.append({
        "Example": i + 1,
        "Background (BG)": bg_color,
        "Sources (S)": sorted(list(sources)),
        # "Source Adjacencies": source_adj, # Too verbose for summary
        "Hypothesis 20 Map (H20)": h20_map,
        "H20 Fill Colors (F)": sorted(list(h20_fill_colors)),
        "Inferred Map (H15)": h15_map,
        "H15 Fill Colors (F)": sorted(list(h15_fill_colors)),
        "Observed Fill Colors": sorted(list(fill_colors_observed)),
        "H20 Map Correctly Predicts Observed Fills": h20_fill_colors == fill_colors_observed
    })

# Pretty print results using the converter
print(json.dumps(convert_numpy_types(results), indent=2))

```


*code_execution_result:*
outcome: OUTCOME_OK

```
[
  {
    "Example": 1,
    "Background (BG)": 0,
    "Sources (S)": [
      1,
      2,
      3
    ],
    "Hypothesis 20 Map (H20)": {
      "1": 1,
      "2": 2,
      "3": 3
    },
    "H20 Fill Colors (F)": [
      1,
      2,
      3
    ],
    "Inferred Map (H15)": {
      "1": 3,
      "2": 3,
      "3": 3
    },
    "H15 Fill Colors (F)": [
      3
    ],
    "Observed Fill Colors": [
      3
    ],
    "H20 Map Correctly Predicts Observed Fills": false
  },
  {
    "Example": 2,
    "Background (BG)": 0,
    "Sources (S)": [
      1,
      3,
      4,
      5
    ],
    "Hypothesis 20 Map (H20)": {
      "1": 3,
      "3": 3,
      "4": 5,
      "5": 5
    },
    "H20 Fill Colors (F)": [
      3,
      5
    ],
    "Inferred Map (H15)": {
      "1": 3,
      "4": 5
    },
    "H15 Fill Colors (F)": [
      3,
      5
    ],
    "Observed Fill Colors": [
      3,
      5
    ],
    "H20 Map Correctly Predicts Observed Fills": true
  },
  {
    "Example": 3,
    "Background (BG)": 3,
    "Sources (S)": [
      0,
      1,
      2,
      4,
      5,
      6,
      8,
      9
    ],
    "Hypothesis 20 Map (H20)": {
      "0": 0,
      "1": 6,
      "2": 9,
      "4": 6,
      "5": 6,
      "6": 8,
      "8": 9,
      "9": 9
    },
    "H20 Fill Colors (F)": [
      0,
      6,
      8,
      9
    ],
    "Inferred Map (H15)": {
      "1": 6,
      "2": 9,
      "4": 6
    },
    "H15 Fill Colors (F)": [
      6,
      9
    ],
    "Observed Fill Colors": [
      6,
      9
    ],
    "H20 Map Correctly Predicts Observed Fills": false
  },
  {
    "Example": 4,
    "Background (BG)": 0,
    "Sources (S)": [
      3,
      4,
      6,
      7
    ],
    "Hypothesis 20 Map (H20)": {
      "3": 3,
      "4": 4,
      "6": 7,
      "7": 7
    },
    "H20 Fill Colors (F)": [
      3,
      4,
      7
    ],
    "Inferred Map (H15)": {
      "3": 3,
      "4": 4,
      "6": 7,
      "7": 7
    },
    "H15 Fill Colors (F)": [
      3,
      4,
      7
    ],
    "Observed Fill Colors": [
      3,
      4,
      7
    ],
    "H20 Map Correctly Predicts Observed Fills": true
  }
]
```


**Metrics Analysis (Hypothesis 20 Map)**

Hypothesis 20 (Map S -> highest adjacent S' if S' > S, else S->S) correctly predicts the observed fill colors for Examples 2 and 4, but **fails** for Examples 1 and 3.
*   Ex 1: H20 predicts fills {1, 2, 3}, observed is {3}.
*   Ex 3: H20 predicts fills {0, 6, 8, 9}, observed is {6, 9}.

Comparing H20 map to the H15 (inferred) map:
*   Ex 1: H20 {1:1, 2:2, 3:3} vs H15 {1:3, 2:3, 3:3}. H20 fails.
*   Ex 2: H20 {1:3, 3:3, 4:5, 5:5} vs H15 {1:3, 4:5}. H20 effectively matches the *fills* but maps extra sources.
*   Ex 3: H20 {0:0, 1:6, 2:9, 4:6, 5:6, 6:8, 8:9, 9:9} vs H15 {1:6, 2:9, 4:6}. H20 maps many more sources and predicts extra fill colors (0, 8). H20 fails.
*   Ex 4: H20 {3:3, 4:4, 6:7, 7:7} vs H15 {3:3, 4:4, 6:7, 7:7}. H20 matches perfectly.

**Revised Conclusion:** Hypothesis 20 is the best rule found so far, but it is not universally correct for this task set. No simple, consistent rule for deriving the Source->Fill map from the input alone is apparent across all examples.

Given this limitation, the most practical approach for the final Coder phase is to implement the fill process assuming a map is provided, and use the best hypothesis (H20) to generate that map, while documenting the known inconsistencies.

**YAML Fact Document**



```yaml
task_description: Fill background pixels using iterative propagation with priority. The fill color is determined by a mapping from source colors (adjacent to background) potentially influenced by adjacent higher-index source colors.

elements:
  - type: grid
    properties: Contains pixels with color values 0-9.
  - type: background_pixel
    properties:
      - color: The most frequent color in the input grid (BG).
      - role: Target pixels to be replaced during the transformation.
  - type: source_pixel
    properties:
      - color: A non-background color (S) in the input grid that is orthogonally adjacent to at least one background_pixel.
      - role: Influences the color of adjacent background pixels in the output, potentially mapping to a different fill color based on adjacency rules.
  - type: fill_pixel
    properties:
      - color: A color (F) that replaces a background_pixel in the output grid. It is determined by the source_pixel(s) adjacent to the original background_pixel via a derived mapping.
      - priority: Determined by the fill color's index (lower index = higher priority).
  - type: source_fill_map
    properties:
      - type: dictionary mapping source_color (S) -> fill_color (F).
      - derivation_rule (Hypothesis 20):
          - For each source color S:
            - Find all adjacent source colors S'.
            - If any adjacent S' exists such that S' > S:
              - Map S -> max(adjacent S' where S' > S).
            - Else (no adjacent S' > S):
              - Map S -> S (identity map).
      - limitations: This derivation rule matches observed fills in Examples 2 & 4, but not 1 & 3.
      - scope: Applies to the specific task instance.

relationships:
  - type: adjacency
    between: [pixel, pixel]
    properties: Orthogonal neighbors (up, down, left, right).
  - type: source_adjacency
    between: [source_pixel, source_pixel]
    properties: Orthogonal adjacency between pixels of different source colors.
  - type: determines_fill_via_map
    from: source_pixel_color (S)
    to: fill_pixel_color (F)
    using: source_fill_map
    properties: A source pixel S influences adjacent background pixels to become color F = source_fill_map[S].
  - type: overwrites
    from: lower_index_color
    to: higher_index_color or background_pixel
    properties: Occurs when multiple colors (original sources or propagating fills) compete for the same pixel location during propagation; the color with the lowest index prevails.

actions:
  - name: identify_background_color
    target: input_grid
    output: background_color_value (BG)
  - name: identify_sources_and_adjacency
    target: input_grid, background_color
    output: set of source_colors (S), dictionary of source_adjacencies (S -> set(adjacent S')).
  - name: derive_source_fill_map (Hypothesis 20)
    target: source_colors, source_adjacencies
    output: dictionary source_fill_map (S -> F)
    steps:
      - Initialize empty map M.
      - For each source color s in S:
        - Find max_higher_adj = -1
        - If s has adjacent sources in source_adjacencies:
           - For each adjacent source adj_s in source_adjacencies[s]:
             - If adj_s > s:
               - max_higher_adj = max(max_higher_adj, adj_s)
        - If max_higher_adj != -1:
           - M[s] = max_higher_adj
        - Else:
           - M[s] = s
  - name: iterative_mapped_priority_flood_fill
    target: input_grid
    using:
        - background_color (BG)
        - source_fill_map (M) derived via Hypothesis 20
        - priority_rule (lower color index wins)
    output: output_grid
    steps:
      - Initialize working_grid = input_grid.
      - Get the set of actual fill colors F_set = set(M.values()).
      - Repeat until no changes occur in an iteration:
        - Create next_grid = copy of working_grid.
        - For each pixel (r, c):
          - Get current_color = working_grid[r, c].
          - Find potential fill influences:
            - Initialize empty list `influences`.
            - For each neighbor `(nr, nc)` with color `C_neighbor` in working_grid:
              - If `C_neighbor == BG`: continue
              - If `C_neighbor` is a source color `s` in `M`: `influences.append(M[s])`
              - Else if `C_neighbor` is a fill color `f` in `F_set`: `influences.append(f)`
              # Note: Non-source, non-fill colors simply act as barriers implicitly
          - If `influences` is not empty:
            - Find `winning_fill = min(influences)`.
            - update_pixel = False
            - If `current_color == BG`: update_pixel = True
            - Else if `winning_fill < current_color`: update_pixel = True
            - If update_pixel and `next_grid[r, c] != winning_fill`:
              - Set `next_grid[r, c] = winning_fill`. Mark change occurred.
        - Update `working_grid = next_grid`.
    notes: The map derivation (Hypothesis 20) used here is the best fit found but is known to be imperfect for all training examples. The flood fill process itself uses the derived map.

```



**Natural Language Program**

1.  **Identify Background:** Determine the most frequent pixel color in the input grid; this is the "background color" (BG).
2.  **Identify Sources and Adjacencies:**
    a.  Identify all non-background colors in the input grid that are orthogonally adjacent to at least one background pixel. These are the "source colors" (S).
    b.  For each source color, determine which other *different* source colors it is orthogonally adjacent to in the input grid.
3.  **Derive Source-to-Fill Map (Hypothesis 20):** Create a mapping (M) from source colors (S) to fill colors (F) as follows:
    a.  For each source color `s`:
        i.  Check if it is adjacent to any other source color `s'` where `s'` has a higher color index than `s`.
        ii. If such adjacent higher-index sources exist, map `s` to the *highest* index among them (M[s] = max(adjacent s' > s)).
        iii. If no such adjacent higher-index source exists, map `s` to itself (M[s] = s).
4.  **Initialize Output:** Create a working copy of the input grid.
5.  **Iterative Filling using Map:** Repeatedly iterate through the grid until no pixel changes color in a full pass:
    a.  Create a temporary grid for the next state, copying the current working grid.
    b.  Determine the set of all possible fill colors (F_set) that appear as values in the map M.
    c.  For each pixel location `(r, c)`:
        i.   Get the `current_color` from the working grid.
        ii.  Examine the orthogonal neighbors `(nr, nc)` in the *current* working grid.
        iii. Determine potential "fill influences" from neighbors:
            *   Initialize an empty list of influences.
            *   For each neighbor's color `C_neighbor`:
                *   If `C_neighbor` is the background color, ignore it.
                *   If `C_neighbor` is a source color `s` present as a key in the map M, add the mapped fill color `M[s]` to the influences list.
                *   Else if `C_neighbor` is a fill color `f` present in the set F_set, add `f` to the influences list.
        iv. If the influences list is not empty:
            1.  Select the "winning fill color" from the influences by choosing the color with the lowest numerical index (highest priority).
            2.  Compare the `winning_fill_color` with the `current_pixel_color`.
            3.  Determine if an update is needed: Update if `current_pixel_color` is BG, OR if `winning_fill_color` has a higher priority (lower index) than `current_pixel_color`.
            4.  If an update is needed and the `winning_fill_color` is different from the color already in the temporary grid at `(r, c)`, update the temporary grid at `(r, c)` to the `winning_fill_color` and note that a change occurred in this iteration.
    d.  After checking all pixels, update the working grid to be the temporary grid for the next iteration.
6.  **Final Output:** Once an iteration completes with no changes, the working grid is the final output.

**(Caveat):** The rule used to derive the source-to-fill map in step 3 is based on the best-fit hypothesis (Hypothesis 20) but is known not to perfectly replicate the mapping for all provided training examples (specifically Examples 1 and 3). The subsequent flood fill process (steps 4-6) operates based on this derived map.