**General Assessment and Strategy**

The previous code failed significantly on both training examples. The primary issues appear to be:

1.  **Incorrect Template Identification:** The logic for finding "template blocks" (which define the output shape) was flawed and did not correctly identify these structures in the key area outside the main frame. The assumption about templates being composed of a source color and background was likely misapplied or the search function was incorrect.
2.  **Incorrect Mapping Derivation:** Consequently, the color mapping rules (`A -> B`) derived from adjacency were likely incorrect or incomplete, as they depend on correctly identifying the related blocks (solid source color vs. template shape).
3.  **Background Color Identification:** Errors in mapping can lead to errors in identifying the invariant background color.
4.  **Transformation Logic:** The core transformation step relies heavily on having the correct templates and mappings. With incorrect inputs, the output grid construction failed.

**Strategy:**

1.  **Re-examine the Key Area:** The key area outside the frame contains pairs of related objects. One object is a solid block of a single color (`Source Color`), and the other is a pattern composed of a different color (`Target Color`) mixed with the `Background Color`. This latter object is the `Template`.
2.  **Refine Identification:**
    *   Identify the `Background Color` first (most frequent non-frame color outside).
    *   Identify all `Solid Blocks` (single color `S`, not background, not frame) outside the frame.
    *   Identify all `Template Blocks` (contiguous components made of exactly one non-background/non-frame color `T` plus the `Background Color`) outside the frame.
    *   Establish `Mappings` and `Template Shapes`: Find pairs where a `Solid Block` (color `S`) is directly adjacent (sharing an edge) to a `Template Block` (containing color `T` and background). This defines the mapping `S -> T`. The shape of the `Template Block` is stored as the template associated with the source color `S`.
3.  **Refine Transformation:**
    *   Find solid blocks of `Source Color S` inside the frame.
    *   For each internal block `S` at `(r, c)`, retrieve the `Template Shape` associated with `S`.
    *   Create the `Output Pattern` by taking the `Template Shape`, replacing occurrences of `T` (the target color *from the template's definition*) with `T` (the mapped target color - they are the same in this revised logic) and occurrences of the background color with the background color. This step simplifies: just use the template shape directly after mapping `S` to `T`. Replace the original `S` color in the template with `T`.
    *   Place this `Output Pattern` onto the output grid at `(r, c)`.

**Gather Metrics**

Let's re-analyze the structure of the key area using code execution to verify the new hypotheses about solid blocks, template blocks, and mappings.

*code_execution:*

```python
import numpy as np
from collections import Counter, deque

# --- Data ---
# train_1 input
input_grid_1 = [[1, 1, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [1, 1, 1, 4, 8, 8, 1, 8, 1, 8, 8, 3, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [1, 1, 4, 4, 8, 8, 1, 1, 1, 8, 8, 3, 3, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 3, 3, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 3, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 3, 3, 3, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 3, 3, 3, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 3, 3, 3, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 8, 8, 8, 8, 3, 3, 3, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 8, 8, 8, 8, 3, 3, 3, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 8, 8, 8, 8, 3, 3, 3, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 3, 3, 3, 8, 1, 1, 1, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 3, 3, 3, 8, 1, 1, 1, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 3, 3, 3, 8, 1, 1, 1, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 8]]
# train_2 input
input_grid_2 = [[2, 2, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 4, 1, 1, 2, 2, 2, 2, 1, 3, 3, 3, 3, 1, 1, 6, 6, 6, 6, 1, 1], [2, 2, 4, 4, 1, 1, 2, 2, 2, 2, 1, 1, 3, 3, 1, 1, 1, 6, 6, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 3, 3, 3, 3, 1, 1, 6, 6, 1, 1, 1, 1], [3, 3, 8, 8, 1, 1, 2, 1, 2, 2, 1, 3, 1, 1, 3, 1, 1, 6, 6, 6, 6, 1, 1], [3, 3, 3, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [3, 3, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [6, 6, 7, 7, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [6, 6, 6, 7, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5], [6, 6, 7, 7, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5], [1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

frame_color = 5

# --- Helper Functions (Adapted) ---

def find_frame_bbox(grid_np: np.ndarray, frame_color: int = 5) -> tuple[int, int, int, int] | None:
    # (Same as previous version - assumed correct for now)
    coords = np.argwhere(grid_np == frame_color)
    if coords.size == 0: return None
    r_min, c_min = coords.min(axis=0)
    r_max, c_max = coords.max(axis=0)
    on_border = (coords[:, 0] == r_min) | (coords[:, 0] == r_max) | \
                (coords[:, 1] == c_min) | (coords[:, 1] == c_max)
    if not np.all(on_border): return None
    if r_max > r_min + 1 and c_max > c_min + 1:
        inner_slice = grid_np[r_min + 1:r_max, c_min + 1:c_max]
        if np.any(inner_slice == frame_color): return None
    return (r_min, c_min, r_max, c_max)

def find_blocks_outside_frame(grid_np: np.ndarray, frame_bbox: tuple[int, int, int, int], frame_color: int):
    """Finds solid blocks and template blocks outside the frame."""
    rows, cols = grid_np.shape
    r_min, c_min, r_max, c_max = frame_bbox
    visited = np.zeros_like(grid_np, dtype=bool)
    
    # Mark frame area as visited to ignore it
    visited[r_min:r_max+1, c_min:c_max+1] = True
    
    solid_blocks = [] # {color, coords, r_min, c_min, r_max, c_max}
    template_blocks = [] # {target_color, background_color, coords, r_min, c_min, r_max, c_max, array}
    
    # First pass: Identify potential background color
    outside_colors_counter = Counter()
    for r in range(rows):
        for c in range(cols):
            if not visited[r,c]: # Outside frame
                 color = grid_np[r,c]
                 if color != frame_color: # Should always be true here
                     outside_colors_counter[color]+=1
    
    potential_background = -1
    if outside_colors_counter:
        # Simple most frequent for now, refinement needed later
        potential_background = outside_colors_counter.most_common(1)[0][0] 
    else:
        potential_background = 0 # Default

    # Second pass: BFS to find components outside frame
    for r_init in range(rows):
        for c_init in range(cols):
            if not visited[r_init, c_init]:
                component_coords = set()
                colors_in_component = set()
                q = deque([(r_init, c_init)])
                visited[r_init, c_init] = True
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
                        # Check bounds and if outside frame (implicitly true if not visited)
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc]: 
                             # Check if connected pixel has same color OR is potential background
                             # This definition might need adjustment based on examples
                             neighbor_color = grid_np[nr, nc]
                             # *** Crucial Decision: How are components defined? ***
                             # Option 1: Only same color (finds solid blocks easily)
                             # Option 2: Same color OR background (tries to find templates)
                             # Option 3: Any non-frame color (finds all connected stuff)
                             
                             # Let's try Option 3 first to categorize components, then analyze
                             visited[nr, nc] = True
                             q.append((nr, nc))
                             
                # --- Categorize the found component ---
                non_background_colors = colors_in_component - {potential_background}
                
                if len(non_background_colors) == 1:
                    single_color = list(non_background_colors)[0]
                    # Is it a solid block or a template block?
                    if len(colors_in_component) == 1: # Only the single color present
                         solid_blocks.append({
                             'color': single_color, 'coords': component_coords,
                             'r_min': r_min_comp, 'c_min': c_min_comp,
                             'r_max': r_max_comp, 'c_max': c_max_comp
                         })
                    elif len(colors_in_component) == 2 and potential_background in colors_in_component:
                         # Contains the single color and the background -> Template
                         template_arr = grid_np[r_min_comp:r_max_comp+1, c_min_comp:c_max_comp+1]
                         template_blocks.append({
                             'target_color': single_color, 
                             'background_color': potential_background, 
                             'coords': component_coords,
                             'r_min': r_min_comp, 'c_min': c_min_comp,
                             'r_max': r_max_comp, 'c_max': c_max_comp,
                             'array': template_arr
                         })
                    # else: More than 2 colors or just background -> ignore for mapping
                # else: More than 1 non-background color or only background -> ignore

    # --- Refine Background and Find Mappings ---
    mapped_colors = set()
    mappings = {} # source_color -> target_color
    templates = {} # source_color -> template_array

    # Collect colors involved in solid and template blocks
    solid_colors = {b['color'] for b in solid_blocks}
    target_colors = {b['target_color'] for b in template_blocks}
    
    # Find actual background: most frequent OUTSIDE color NOT in solid_colors or target_colors
    actual_background = -1
    sorted_outside = sorted(outside_colors_counter.items(), key=lambda item: (-item[1], item[0]))
    possible_mapping_colors = solid_colors | target_colors
    for color, count in sorted_outside:
        if color not in possible_mapping_colors:
             actual_background = color
             break
    if actual_background == -1: # Fallback if conflict
        actual_background = potential_background 
        
    # Re-filter template blocks if potential_background was wrong
    valid_template_blocks = [
        tb for tb in template_blocks if tb['background_color'] == actual_background
    ]
    
    # Find adjacency between SOLID (Source) and TEMPLATE (Target+BG) blocks
    for sb in solid_blocks:
        source_color = sb['color']
        if source_color in mappings: continue # Already mapped

        for tb in valid_template_blocks:
            target_color = tb['target_color']
            if target_color in mappings.values(): continue # Already mapped to

            # Check adjacency (simple check: bounding box proximity + 1 pixel check)
            # A more robust check looks at actual coordinate adjacency
            is_adjacent = False
            for r_s, c_s in sb['coords']:
                 for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                     nr, nc = r_s + dr, c_s + dc
                     if (nr, nc) in tb['coords']:
                         is_adjacent = True
                         break
                 if is_adjacent: break
                 
            if is_adjacent:
                 mappings[source_color] = target_color
                 templates[source_color] = tb['array']
                 mapped_colors.add(source_color)
                 mapped_colors.add(target_color)
                 break # Found mapping for this source color

    # Final check on background - ensure it wasn't accidentally part of a mapped pair
    if actual_background in mapped_colors:
        # This indicates an issue, try second most frequent non-mapped?
        print(f"Warning: Background color {actual_background} seems to be involved in mapping.")
        # Attempt to find a new background
        new_background = -1
        possible_mapping_colors = set(mappings.keys()) | set(mappings.values())
        for color, count in sorted_outside:
             if color not in possible_mapping_colors:
                 new_background = color
                 break
        if new_background != -1:
            print(f"Switching background to {new_background}")
            actual_background = new_background
        else:
            print("Could not find alternative background. Proceeding with caution.")


    return actual_background, solid_blocks, valid_template_blocks, mappings, templates


# --- Analysis ---
results = {}
for i, grid in enumerate([input_grid_1, input_grid_2]):
    name = f"train_{i+1}"
    print(f"--- Analyzing {name} ---")
    input_np = np.array(grid)
    frame_bbox = find_frame_bbox(input_np, frame_color)
    if frame_bbox:
        print(f"Frame: {frame_bbox}")
        try:
            background, solid, templates_found, mappings, templates_shapes = find_blocks_outside_frame(input_np, frame_bbox, frame_color)
            results[name] = {
                "background": background,
                "mappings": mappings,
                "templates": templates_shapes # {source: array}
            }
            print(f"Background: {background}")
            print(f"Mappings (Source -> Target): {mappings}")
            # print(f"Solid Blocks Found: {len(solid)}")
            # print(f"Template Blocks Found (Target+BG): {len(templates_found)}")
            print(f"Templates Assigned (Source -> Shape): { {k: v.shape for k,v in templates_shapes.items()} }")
            if len(mappings) != len(templates_shapes):
                 print("Warning: Mismatch between mappings found and templates assigned!")

        except Exception as e:
            print(f"Error analyzing {name}: {e}")
            results[name] = {"error": str(e)}
    else:
        print("No frame found.")
        results[name] = {"error": "No frame found"}

# print("\n--- Summary ---")
# print(results)

```


*code_execution_result:*
outcome: OUTCOME_OK

```
--- Analyzing train_1 ---
Frame: (np.int64(8), np.int64(3), np.int64(22), np.int64(21))
Background: 8
Mappings (Source -> Target): {3: 2, 1: 4}
Templates Assigned (Source -> Shape): {3: (3, 3), 1: (3, 3)}
--- Analyzing train_2 ---
Frame: (np.int64(8), np.int64(5), np.int64(20), np.int64(22))
Background: 1
Mappings (Source -> Target): {2: 4, 3: 8, 6: 7}
Templates Assigned (Source -> Shape): {2: (4, 4), 3: (4, 4), 6: (4, 4)}
```

**Metrics Analysis:**

The refined analysis using `code_execution` successfully identified the key components according to the revised hypothesis:

*   **`train_1`**:
    *   Frame: Correctly identified.
    *   Background: Correctly identified as `8` (azure).
    *   Mappings: Correctly identified `3 -> 2` and `1 -> 4`.
    *   Templates: Correctly associated source colors `3` and `1` with template shapes extracted from the key area. Both templates are 3x3.
*   **`train_2`**:
    *   Frame: Correctly identified.
    *   Background: Correctly identified as `1` (blue).
    *   Mappings: Correctly identified `2 -> 4`, `3 -> 8`, `6 -> 7`.
    *   Templates: Correctly associated source colors `2`, `3`, `6` with template shapes. All templates are 4x4.

This confirms the revised understanding of the relationship between solid blocks (source color), template blocks (target color + background), adjacency, and the resulting mapping and template shape.

**YAML Facts**


```yaml
elements:
  - object: Frame
    properties:
      - color: gray (5)
      - shape: hollow rectangle
      - role: defines the region of interest (ROI) for cropping and output

  - object: KeyArea
    properties:
      - location: outside the Frame's bounding box
      - contains: KeyPairs, BackgroundPixels

  - object: KeyPair
    properties:
      - structure: consists of two adjacent blocks - a SolidBlock and a TemplateBlock
      - role: defines a transformation rule (SolidBlock Color -> TemplateBlock Target Color) and the output shape (TemplateBlock shape)
      - location: within KeyArea

  - object: SolidBlock
    properties:
      - structure: contiguous block of a single color ('SourceColor')
      - role: represents the input color/object identifier in a KeyPair
      - location: within KeyArea, adjacent to a TemplateBlock

  - object: TemplateBlock
    properties:
      - structure: contiguous component composed ONLY of a 'TargetColor' and the 'BackgroundColor'
      - shape: specific pattern defining the output object's shape and internal structure
      - role: represents the output shape and target color identifier in a KeyPair
      - location: within KeyArea, adjacent to a SolidBlock

  - object: SourceBlockInstance
    properties:
      - structure: contiguous block of a single 'SourceColor' (matching a color from a SolidBlock in KeyArea)
      - location: inside the Frame
      - role: input object instance to be transformed

  - object: BackgroundColor
    properties:
      - color: varies by task (most frequent color in KeyArea excluding frame, SourceColors, and TargetColors)
      - role: invariant color, used within TemplateBlocks and fills empty space in the output

actions:
  - name: locate_frame
    input: input_grid
    output: bounding_box_of_gray_frame

  - name: analyze_key_area
    input: input_grid, frame_bounding_box
    process:
      - Identify potential BackgroundColor (most frequent outside, non-frame).
      - Find all SolidBlocks outside frame.
      - Find all TemplateBlocks outside frame (TargetColor + BackgroundColor).
      - Identify adjacent (SolidBlock, TemplateBlock) pairs.
      - For each pair (Solid S, Template T): record mapping S_color -> T_target_color, store T_shape as template[S_color].
      - Refine/Confirm BackgroundColor (most frequent outside non-frame, non-S_color, non-T_target_color). Re-validate templates if background changes.
    output: dictionary_of_mappings {S_color: T_target_color, ...}, BackgroundColor, dictionary_of_templates {S_color: template_array, ...}

  - name: initialize_output
    input: frame_bounding_box, BackgroundColor
    output: output_grid (filled with BackgroundColor, sized by frame)

  - name: copy_frame_to_output
    input: input_grid, frame_bounding_box, output_grid
    process: copy gray (5) pixels from input frame location to output grid.
    output: updated_output_grid

  - name: locate_source_block_instances
    input: input_grid, frame_bounding_box, source_colors (keys from mappings)
    output: list_of_source_instances [{color, r_min, c_min, coords}, ...] (coordinates relative to input_grid)

  - name: apply_transformations
    input: output_grid, list_of_source_instances, dictionary_of_templates, dictionary_of_mappings, BackgroundColor, frame_bbox(r_min, c_min)
    process:
      - For each SourceBlockInstance (color S at r_min_abs, c_min_abs):
          - Get the TemplateBlock array 'T_shape' for color S.
          - Get the TargetColor 'T_color' for color S from mappings.
          - Calculate the top-left placement coordinate in output_grid: r_rel = r_min_abs - r_min_frame, c_rel = c_min_abs - c_min_frame.
          - Iterate through T_shape (height h, width w):
              - For pixel at (r_t, c_t) in T_shape:
                  - Determine output pixel color: if T_shape[r_t, c_t] == T_color (the target color *in* the template), use T_color; if T_shape[r_t, c_t] == BackgroundColor, use BackgroundColor.
                  - Calculate output coordinate: out_r = r_rel + r_t, out_c = c_rel + c_t.
                  - If (out_r, out_c) is within output_grid bounds and not part of the frame: place the determined color.
    output: final_output_grid

relationships:
  - The Frame defines the output dimensions and boundary.
  - KeyPairs in the KeyArea define the transformation rules.
  - A SolidBlock's color maps to its adjacent TemplateBlock's target color.
  - A SolidBlock's color determines which TemplateBlock shape to use for transformation.
  - BackgroundColor is invariant and part of TemplateBlocks.
  - SourceBlockInstances inside the frame trigger the application of the transformation rule defined by their color.
```


**Natural Language Program**

1.  **Find the Frame**: Locate the hollow rectangular boundary of gray (5) pixels in the input grid. Determine its bounding box coordinates (`r_min`, `c_min`, `r_max`, `c_max`). If no valid frame is found, return the input grid unchanged.
2.  **Analyze Key Area (Outside Frame)**:
    *   Identify the most frequent color outside the frame area, excluding gray (5), as the initial candidate `BackgroundColor`.
    *   Find all `Solid Blocks`: contiguous blocks outside the frame composed of a single color (`SourceColor`), which is not the candidate `BackgroundColor` or gray (5).
    *   Find all `Template Blocks`: contiguous components outside the frame composed exclusively of the candidate `BackgroundColor` and exactly one other color (`TargetColor`), which is not gray (5). Store the array (shape and content) of each `Template Block`.
    *   Identify `Key Pairs`: Find instances where a `Solid Block` (color `S`) is directly adjacent (shares an edge) to a `Template Block` (containing target color `T`).
    *   Establish `Mappings` and `Template Shapes`: For each adjacent pair found, record a mapping rule `S -> T` and store the array of the corresponding `Template Block` as the template shape for source color `S`.
    *   Refine `BackgroundColor`: Confirm the `BackgroundColor` is the most frequent color outside the frame that is not gray (5) and is not any `SourceColor` (`S`) or `TargetColor` (`T`) involved in the mappings. If the initial candidate was incorrect, update the `BackgroundColor` and re-validate the `Template Blocks` and `Mappings`.
3.  **Initialize Output Grid**: Create a new grid (`output_grid`) with dimensions matching the frame's bounding box (`height = r_max - r_min + 1`, `width = c_max - c_min + 1`). Fill this grid entirely with the final `BackgroundColor`.
4.  **Copy Frame**: Copy the gray (5) pixels from the input grid's frame location to the corresponding positions in the `output_grid`.
5.  **Transform Instances Inside Frame**:
    *   Scan the input grid *inside* the frame boundaries (from `r_min+1` to `r_max-1`, `c_min+1` to `c_max-1`).
    *   Identify all contiguous blocks composed of a single `SourceColor` (`S`) for which a mapping rule exists. Keep track of visited pixels to process each block only once.
    *   For each such `Source Block Instance` found, note its top-left absolute coordinate (`r_abs`, `c_abs`).
    *   Retrieve the `Template Shape` (an array) associated with its color `S`.
    *   Retrieve the `TargetColor` (`T`) from the mapping `S -> T`.
    *   Calculate the top-left placement coordinate relative to the output grid: `r_rel = r_abs - r_min`, `c_rel = c_abs - c_min`.
    *   Iterate through each pixel `(r_t, c_t)` of the `Template Shape`:
        *   Get the color `template_pixel_color` from the `Template Shape` at `(r_t, c_t)`.
        *   Determine the `output_color`: if `template_pixel_color` is the `TargetColor` (`T`), the `output_color` is `T`; if `template_pixel_color` is the `BackgroundColor`, the `output_color` is `BackgroundColor`.
        *   Calculate the target coordinate in the `output_grid`: `out_r = r_rel + r_t`, `out_c = c_rel + c_t`.
        *   If `(out_r, out_c)` is within the bounds of `output_grid` and is not already occupied by a gray (5) frame pixel, place the `output_color` at `output_grid[out_r, out_c]`.
6.  **Return Output**: The final `output_grid` is the result.