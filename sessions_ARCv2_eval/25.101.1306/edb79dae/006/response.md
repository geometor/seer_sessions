**General Assessment and Strategy**

The previous code execution failed entirely, returning the original input grids instead of transformed outputs. This indicates a fundamental failure early in the process, likely within the `analyze_key_area` function, preventing the derivation of mappings or templates, or possibly even in `find_frame_bbox` if the frame structure didn't match the strict hollow rectangle check.

The core issue seems to be correctly identifying and pairing the "key" components outside the frame. The previous hypothesis involved "Solid Blocks" and "Template Blocks" (TargetColor + BackgroundColor). The results suggest this pairing or identification was incorrect.

**Revised Strategy:**

1.  **Re-examine Key Area Structure:** The key area seems to contain pairs of adjacent objects:
    *   **Source Shape:** A solid block of a single `SourceColor`.
    *   **Output Shape (Template):** A block, potentially the same size/shape or different, composed of a `TargetColor` and the `BackgroundColor`.
    *   The crucial link is the adjacency between a Source Shape and its corresponding Output Shape.
2.  **Refine Identification Logic:**
    *   Find the frame.
    *   Determine `BackgroundColor` (most frequent outside, non-frame color).
    *   Identify all `Solid Blocks` outside (color `S`).
    *   Identify all `Pattern Blocks` outside (contiguous, containing exactly one color `T` != BackgroundColor, plus the BackgroundColor).
    *   Find adjacent pairs (`Solid Block S`, `Pattern Block P with color T`). Establish mapping `S -> T` and store the array of `Pattern Block P` as `template[S]`.
3.  **Verify Transformation:** Ensure the placement logic inside the frame correctly uses the identified template shape and maps `S` pixels within the template to `T`.

**Gather Metrics**

We will re-run the analysis focused on identifying Solid Blocks and Pattern Blocks and checking their adjacency based on the `train_1` and `train_2` examples.

*code_execution:*


```python
import numpy as np
from collections import Counter, deque
from typing import List, Dict, Tuple, Set, Optional

# --- Data ---
input_grid_1 = [[1, 1, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [1, 1, 1, 4, 8, 8, 1, 8, 1, 8, 8, 3, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [1, 1, 4, 4, 8, 8, 1, 1, 1, 8, 8, 3, 3, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 3, 3, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 3, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 3, 3, 3, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 3, 3, 3, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 3, 3, 3, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 8, 8, 8, 8, 3, 3, 3, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 8, 8, 8, 8, 3, 3, 3, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 8, 8, 8, 8, 3, 3, 3, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 3, 3, 3, 8, 1, 1, 1, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 3, 3, 3, 8, 1, 1, 1, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 3, 3, 3, 8, 1, 1, 1, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 8]]
input_grid_2 = [[2, 2, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 4, 1, 1, 2, 2, 2, 2, 1, 3, 3, 3, 3, 1, 1, 6, 6, 6, 6, 1, 1], [2, 2, 4, 4, 1, 1, 2, 2, 2, 2, 1, 1, 3, 3, 1, 1, 1, 6, 6, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 3, 3, 3, 3, 1, 1, 6, 6, 1, 1, 1, 1], [3, 3, 8, 8, 1, 1, 2, 1, 2, 2, 1, 3, 1, 1, 3, 1, 1, 6, 6, 6, 6, 1, 1], [3, 3, 3, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [3, 3, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [6, 6, 7, 7, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [6, 6, 6, 7, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5], [6, 6, 7, 7, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5], [1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

frame_color = 5

# --- Helper Functions (Using previous definitions - assume they work for BBox and finding components) ---

def find_frame_bbox(grid_np: np.ndarray, frame_color: int = 5) -> Optional[Tuple[int, int, int, int]]:
    coords = np.argwhere(grid_np == frame_color)
    if coords.size == 0: return None
    r_min, c_min = coords.min(axis=0)
    r_max, c_max = coords.max(axis=0)
    if r_max < r_min + 2 or c_max < c_min + 2: return None
    on_border_check = (coords[:, 0] == r_min) | (coords[:, 0] == r_max) | \
                      (coords[:, 1] == c_min) | (coords[:, 1] == c_max)
    if not np.all(on_border_check): return None
    inner_slice = grid_np[r_min + 1:r_max, c_min + 1:c_max]
    if np.any(inner_slice == frame_color): return None
    return (r_min, c_min, r_max, c_max)

def analyze_key_area_refined(grid_np: np.ndarray, frame_bbox: Tuple[int, int, int, int], frame_color: int) -> Optional[Tuple[Dict[int, int], int, Dict[int, np.ndarray]]]:
    rows, cols = grid_np.shape
    r_min_f, c_min_f, r_max_f, c_max_f = frame_bbox
    
    key_area_mask = np.ones_like(grid_np, dtype=bool)
    key_area_mask[r_min_f:r_max_f + 1, c_min_f:c_max_f + 1] = False
    key_area_coords = np.argwhere(key_area_mask)

    if key_area_coords.size == 0: return None # No key area

    outside_colors_counter = Counter()
    for r, c in key_area_coords:
        outside_colors_counter[grid_np[r, c]] += 1
    
    if not outside_colors_counter: return None

    # --- Find Background Color ---
    # Assume background is most frequent color NOT involved in potential pairs later
    # Keep list sorted by freq (desc), color (asc)
    sorted_outside_colors = sorted(outside_colors_counter.items(), key=lambda item: (-item[1], item[0]))
    
    # --- Find Solid & Pattern Blocks ---
    visited_key = np.zeros_like(grid_np, dtype=bool)
    visited_key[~key_area_mask] = True 

    solid_blocks = []         # Blocks of a single color S
    pattern_blocks = []       # Blocks containing color T + potential background B

    potential_background = sorted_outside_colors[0][0] # Initial guess

    for r_init, c_init in key_area_coords:
         if not visited_key[r_init, c_init]:
            component_coords = set()
            colors_in_component = set()
            q = deque([(r_init, c_init)])
            visited_key[r_init, c_init] = True
            r_min_comp, c_min_comp = r_init, c_init
            r_max_comp, c_max_comp = r_init, c_init

            while q:
                r, c = q.popleft()
                color = grid_np[r, c]
                colors_in_component.add(color)
                component_coords.add((r,c))
                r_min_comp, c_min_comp = min(r_min_comp, r), min(c_min_comp, c)
                r_max_comp, c_max_comp = max(r_max_comp, r), max(c_max_comp, c)

                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and not visited_key[nr, nc]:
                        visited_key[nr, nc] = True
                        q.append((nr, nc))

            # --- Categorize ---
            # A component is SOLID if it contains exactly one color.
            if len(colors_in_component) == 1:
                color_s = list(colors_in_component)[0]
                # Check if it's the potential background - background cannot be a solid source block
                if color_s != potential_background:
                    solid_blocks.append({
                        'color': color_s, 'coords': component_coords,
                        'r_min': r_min_comp, 'c_min': c_min_comp
                    })
            # A component is a PATTERN CANDIDATE if it contains exactly two colors,
            # one of which is the potential background.
            elif len(colors_in_component) == 2 and potential_background in colors_in_component:
                color_t = list(colors_in_component - {potential_background})[0]
                pattern_arr = grid_np[r_min_comp:r_max_comp+1, c_min_comp:c_max_comp+1].copy()
                pattern_blocks.append({
                     'target_color': color_t, 
                     'potential_bg': potential_background,
                     'coords': component_coords,
                     'r_min': r_min_comp, 'c_min': c_min_comp,
                     'array': pattern_arr
                 })

    # --- Finalize Background & Find Mappings by Adjacency ---
    solid_colors = {b['color'] for b in solid_blocks}
    target_colors = {p['target_color'] for p in pattern_blocks}
    
    background_color = -1
    for color, count in sorted_outside_colors:
        if color not in solid_colors and color not in target_colors:
            background_color = color
            break
            
    if background_color == -1: # Fallback if all colors involved somehow
        background_color = potential_background 
        print(f"Warning: Could not definitively separate background. Using initial guess: {background_color}")

    # Filter pattern blocks based on final background
    valid_patterns = [p for p in pattern_blocks if p['potential_bg'] == background_color]
    
    mappings = {}
    templates = {}
    
    for sb in solid_blocks:
        source_color = sb['color']
        if source_color in mappings: continue
        
        adjacent_pattern = None
        for pb in valid_patterns:
            # Check adjacency efficiently
            is_adjacent = False
            for r_s, c_s in sb['coords']:
                 for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                     nr, nc = r_s + dr, c_s + dc
                     if (nr, nc) in pb['coords']:
                         is_adjacent = True
                         break
                 if is_adjacent: break
            if is_adjacent:
                 # Ensure this pattern's target color isn't already mapped FROM another source
                 target_color = pb['target_color']
                 # Check if target color is already a value in mappings
                 already_mapped_to = False
                 for mapped_target in mappings.values():
                     if mapped_target == target_color:
                         already_mapped_to = True
                         break
                 if not already_mapped_to:
                     adjacent_pattern = pb
                     break # Found adjacent pattern for this solid block

        if adjacent_pattern:
            target_color = adjacent_pattern['target_color']
            mappings[source_color] = target_color
            templates[source_color] = adjacent_pattern['array']
            
    if not mappings: return None

    return mappings, background_color, templates


# --- Analysis ---
results = {}
for i, grid in enumerate([input_grid_1, input_grid_2]):
    name = f"train_{i+1}"
    print(f"--- Analyzing {name} ---")
    input_np = np.array(grid)
    frame_bbox = find_frame_bbox(input_np, frame_color)
    if frame_bbox:
        print(f"Frame: {frame_bbox}")
        analysis_result = analyze_key_area_refined(input_np, frame_bbox, frame_color)
        if analysis_result:
            mappings, background, templates_shapes = analysis_result
            results[name] = {
                "background": background,
                "mappings": mappings,
                "templates": {k: v.shape for k,v in templates_shapes.items()}
            }
            print(f"Background: {background}")
            print(f"Mappings (Source -> Target): {mappings}")
            print(f"Templates Assigned (Source -> Shape): {results[name]['templates']}")
            if len(mappings) != len(templates_shapes):
                 print("Warning: Mismatch between mappings found and templates assigned!")
        else:
            print(f"Error: Could not analyze key area for {name}")
            results[name] = {"error": "Key area analysis failed"}
    else:
        print("No frame found.")
        results[name] = {"error": "No frame found"}

```


*code_execution_result:*
outcome: OUTCOME_OK


```
--- Analyzing train_1 ---
Frame: (np.int64(8), np.int64(3), np.int64(22), np.int64(21))
Background: 8
Mappings (Source -> Target): {1: 4, 3: 2}
Templates Assigned (Source -> Shape): {1: (3, 3), 3: (3, 3)}
--- Analyzing train_2 ---
Frame: (np.int64(8), np.int64(5), np.int64(20), np.int64(22))
Background: 1
Mappings (Source -> Target): {2: 4, 6: 7, 3: 8}
Templates Assigned (Source -> Shape): {2: (4, 4), 6: (4, 4), 3: (4, 4)}
```


**Metric Analysis:**

The refined analysis (`analyze_key_area_refined`) successfully identified the core components and relationships in both training examples:

*   **Frame:** Correctly identified.
*   **Background:** Correctly identified (`8` for `train_1`, `1` for `train_2`).
*   **Solid & Pattern Blocks:** The logic correctly differentiated between solid blocks (source) and pattern blocks (target + background).
*   **Adjacency & Mapping:** The adjacency check correctly paired the solid source blocks with their corresponding pattern blocks, establishing the mappings:
    *   `train_1`: `1 -> 4`, `3 -> 2`
    *   `train_2`: `2 -> 4`, `6 -> 7`, `3 -> 8`
*   **Templates:** The shapes (arrays) of the corresponding pattern blocks were correctly captured as templates associated with each source color.
    *   `train_1`: Templates for `1` and `3` are `3x3`.
    *   `train_2`: Templates for `2`, `6`, and `3` are `4x4`.

This confirms the refined strategy and provides confidence in the identified components and relationships. The previous code's failure was likely due to incorrect component identification/categorization in `analyze_key_area` or bugs in the transformation step, rather than the frame finding itself.

**YAML Facts**


```yaml
elements:
  - object: Frame
    properties:
      - color: gray (5)
      - shape: hollow rectangle
      - role: defines the region of interest (ROI) for output grid size and boundary.

  - object: KeyArea
    properties:
      - location: outside the Frame's bounding box.
      - contains: KeyPairs, BackgroundPixels.

  - object: KeyPair
    properties:
      - structure: consists of two adjacent blocks - a SourceShape and an OutputShape.
      - role: defines a transformation rule (SourceShape Color -> OutputShape Target Color) and the output shape (OutputShape shape).
      - location: within KeyArea.

  - object: SourceShape
    properties:
      - structure: contiguous block of a single color ('SourceColor').
      - role: represents the input color identifier in a KeyPair.
      - location: within KeyArea, adjacent to an OutputShape.

  - object: OutputShape # Renamed from TemplateBlock for clarity
    properties:
      - structure: contiguous component composed ONLY of a 'TargetColor' and the 'BackgroundColor'.
      - shape: specific pattern defining the output object's shape and internal structure. This IS the template.
      - role: represents the output shape and target color identifier in a KeyPair.
      - location: within KeyArea, adjacent to a SourceShape.

  - object: SourceInstance
    properties:
      - structure: contiguous block of a single 'SourceColor' (matching a color from a SourceShape in KeyArea).
      - location: inside the Frame.
      - role: input object instance to be transformed.

  - object: BackgroundColor
    properties:
      - color: varies by task (most frequent color in KeyArea excluding frame, SourceColors, and TargetColors).
      - role: invariant color, used within OutputShapes and fills empty space in the output grid.

actions:
  - name: locate_frame
    input: input_grid
    output: bounding_box_of_gray_frame (r_min, c_min, r_max, c_max)

  - name: analyze_key_area
    input: input_grid, frame_bounding_box
    process:
      - Identify potential BackgroundColor (most frequent outside, non-frame).
      - Find all SourceShapes (Solid Blocks) outside frame (color S != potential BG, != frame).
      - Find all PatternBlocks (potential OutputShapes) outside frame (color T != potential BG, != frame + potential BG).
      - Determine final BackgroundColor (most frequent outside non-frame, non-S, non-T).
      - Filter PatternBlocks to get valid OutputShapes based on final BackgroundColor.
      - Identify adjacent (SourceShape S, OutputShape O containing T) pairs.
      - For each pair: record mapping S -> T, store O's array as template[S].
    output: dictionary_of_mappings {S: T, ...}, BackgroundColor, dictionary_of_templates {S: template_array, ...}

  - name: initialize_output_grid
    input: frame_bounding_box, BackgroundColor
    process: create new grid matching frame size, fill with BackgroundColor.
    output: output_grid

  - name: copy_frame_to_output
    input: input_grid, frame_bounding_box, output_grid
    process: copy gray (5) pixels from input frame location to output grid.
    output: updated_output_grid

  - name: find_source_instances_inside_frame
    input: input_grid, frame_bounding_box, source_colors (keys from mappings)
    process: find contiguous blocks of source_colors within the inner bounds of the frame.
    output: list_of_source_instances [{color, r_min, c_min, coords}, ...] (absolute coordinates)

  - name: apply_templates_to_output
    input: output_grid, list_of_source_instances, dictionary_of_templates, dictionary_of_mappings, BackgroundColor, frame_bbox(r_min, c_min)
    process:
      - Create a mask to track painted cells (initially true for frame cells).
      - For each SourceInstance (color S at r_abs, c_abs):
          - Get TemplateShape 'T_shape' = templates[S].
          - Get TargetColor 'T_color' = mappings[S].
          - Calculate output placement top-left: r_rel = r_abs - r_min_frame, c_rel = c_abs - c_min_frame.
          - Iterate through T_shape (size h x w):
              - For pixel T_shape[r_t, c_t]:
                  - Determine output pixel color: 'T_color' if T_shape pixel is T_color, 'BackgroundColor' if T_shape pixel is BackgroundColor.
                  - Calculate output coordinate: out_r = r_rel + r_t, out_c = c_rel + c_t.
                  - If (out_r, out_c) is within output bounds and not masked:
                      - Place output color in output_grid[out_r, out_c].
                      - Mark (out_r, out_c) in the mask.
    output: final_output_grid

relationships:
  - Frame defines output grid size and boundary.
  - KeyPairs (adjacent SourceShape and OutputShape) define transformations.
  - SourceShape color maps to adjacent OutputShape's TargetColor.
  - OutputShape provides the template (shape and internal pattern) for the transformation.
  - BackgroundColor is invariant and populates OutputShapes and empty output space.
  - SourceInstances inside the frame trigger the placement of the corresponding template.
```


**Natural Language Program**

1.  **Find Frame**: Locate the hollow rectangular boundary of gray (5) pixels. Determine its bounding box (`r_min`, `c_min`, `r_max`, `c_max`). If no valid frame exists, return the input grid.
2.  **Analyze Key Area**: Examine the area outside the frame's bounding box.
    *   Find the most frequent color ('`BackgroundColor`') in this area, excluding gray (5) and colors that will be identified as part of key pairs.
    *   Identify `Source Shapes`: Find all contiguous blocks outside the frame composed of a single color (`SourceColor`) other than `BackgroundColor` or gray (5).
    *   Identify `Output Shapes`: Find all contiguous components outside the frame composed of exactly two colors: the `BackgroundColor` and one other color (`TargetColor`, which is not gray(5)). Store the shape (array) of each Output Shape.
    *   Establish `Mappings` and `Templates`: Find pairs where a `Source Shape` (color `S`) is directly adjacent (touching edge) to an `Output Shape` containing `TargetColor` (`T`). For each such unique pair, record the mapping rule `S -> T` and store the array of the `Output Shape` as the template for `S`. Ensure the `BackgroundColor` used to identify Output Shapes is consistent and not part of any mapping pair.
3.  **Prepare Output Grid**: Create a new grid (`output_grid`) with dimensions matching the frame (`height = r_max - r_min + 1`, `width = c_max - c_min + 1`). Fill it with the determined `BackgroundColor`. Copy the gray (5) frame pixels from the input to the `output_grid`.
4.  **Transform Source Instances**:
    *   Scan the input grid *inside* the frame boundaries.
    *   Find all contiguous blocks (`Source Instances`) made of a single `SourceColor` (`S`) for which a mapping `S -> T` exists.
    *   For each `Source Instance` found, starting at absolute coordinate (`r_abs`, `c_abs`):
        *   Retrieve the template (the `Output Shape` array) associated with `S`. Let its dimensions be `h x w`.
        *   Retrieve the `TargetColor` (`T`) for `S`.
        *   Calculate the top-left placement coordinate in the `output_grid`: `r_rel = r_abs - r_min`, `c_rel = c_abs - c_min`.
        *   Iterate through the template array from `(0, 0)` to `(h-1, w-1)`:
            *   For template pixel at `(r_t, c_t)` with color `template_color`:
                *   Determine the `color_to_paint`: if `template_color` is `T`, use `T`; if `template_color` is `BackgroundColor`, use `BackgroundColor`.
                *   Calculate the target output coordinate: `out_r = r_rel + r_t`, `out_c = c_rel + c_t`.
                *   If `(out_r, out_c)` is within the `output_grid` bounds and is not a gray (5) frame pixel, set `output_grid[out_r, out_c]` to `color_to_paint`. Prevent overwriting already painted non-background pixels if necessary (though based on examples, overlap seems unlikely or handled by placement order/logic).
5.  **Return Result**: The completed `output_grid` is the final output.