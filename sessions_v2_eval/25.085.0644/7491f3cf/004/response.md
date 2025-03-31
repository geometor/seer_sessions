Okay, let's analyze the results and refine our understanding.

**General Assessment & Strategy**

The core logic seems partially correct: identifying zones, copying from Zone 2 to Zone 4, and conditionally modifying with Zone 3. However, the results indicate significant errors, particularly in how Zone 4 is being populated.

*   **Examples 1, 2, 4 Failure:** Zone 4 is consistently filled with `0` (white) instead of the expected pattern. This strongly suggests an issue with determining the background color for Zone 4 (`bg_z4`) and potentially the clearing step. The function `_get_zone_background` might be incorrectly defaulting to `0` when analyzing Zone 4 in the *input* grid.
*   **Example 3 Failure:** Zone 4 *is* populated, but incorrectly. Some pixels seem to be copied from Zone 2, but others (blue `1`) that are *not* part of the Zone 3 modifier are also appearing. The background color (`9` - maroon) seems correct here. This points towards issues in:
    *   How pattern pixels are identified in Zone 2 and/or Zone 3.
    *   How the Zone 3 modifier condition (`_is_horizontal_line`) is checked or applied. It seems the copy logic might be grabbing non-modifier pixels from Zone 3 in this case.

**Strategy:**

1.  **Re-evaluate Background Color Logic:** The primary hypothesis is that Zone 4 should be cleared using the background color identified in *Zone 2* of the input grid, not a background color derived from Zone 4 itself. Zone 4 in the input often seems empty or irrelevant; its purpose is to be overwritten based on Zones 2 and 3.
2.  **Refine Pattern Identification:** Ensure `_get_pattern_pixels` correctly identifies only the intended pattern elements, distinct from both the border and the determined background color for that specific zone.
3.  **Review Modifier Logic:** Double-check the `_is_horizontal_line` function and how its result is used. Ensure only the green line pixels are overlaid, and only when the condition is strictly met. The error in Example 3 suggests non-modifier pixels might be incorrectly transferred.
4.  **Gather Metrics:** Systematically extract key properties (border, backgrounds, patterns) for each example using the *current* logic and compare them to the expected state to pinpoint discrepancies.

**Metrics Gathering**

``` python
import numpy as np
from collections import Counter

# Constants (matching the original code)
ZONE_WIDTH = 5
ZONE_SEPARATOR_WIDTH = 1
MODIFIER_COLOR = 3  # green
ZONE_COLUMNS = {
    1: list(range(1, 1 + ZONE_WIDTH)),
    2: list(range(1 + ZONE_WIDTH + ZONE_SEPARATOR_WIDTH, 1 + ZONE_WIDTH + ZONE_SEPARATOR_WIDTH + ZONE_WIDTH)),
    3: list(range(1 + 2 * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH), 1 + 2 * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH) + ZONE_WIDTH)),
    4: list(range(1 + 3 * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH), 1 + 3 * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH) + ZONE_WIDTH)),
}

# Simplified helper functions (based on the original code's logic)
def _get_border_color(grid):
    grid_np = np.array(grid)
    if grid_np.size == 0: return 0
    counts = Counter(grid_np.flatten())
    return counts.most_common(1)[0][0]

def _get_zone_subgrid(grid, zone_index):
    grid_np = np.array(grid)
    rows, cols_total = grid_np.shape
    if rows <= 2: return np.array([[]], dtype=grid_np.dtype)
    cols = ZONE_COLUMNS.get(zone_index)
    if not cols: return np.array([[]], dtype=grid_np.dtype)
    min_col, max_col = min(cols), max(cols)
    if max_col >= cols_total - 1: return np.array([[]], dtype=grid_np.dtype)
    return grid_np[1:rows-1, min_col:max_col+1]

def _get_zone_background(grid, zone_index, border_color):
    zone_subgrid = _get_zone_subgrid(grid, zone_index)
    if zone_subgrid.size == 0: return 0 # Simplified default for analysis
    counts = Counter(zone_subgrid.flatten())
    if border_color in counts: del counts[border_color]
    if not counts: return 0 # Simplified default
    return counts.most_common(1)[0][0]

def _get_pattern_pixels(grid, zone_index, bg_color, border_color):
    pattern_pixels = []
    grid_np = np.array(grid)
    rows, cols_total = grid_np.shape
    zone_cols = ZONE_COLUMNS.get(zone_index)
    if not zone_cols or rows <= 2: return []
    min_col, max_col = min(zone_cols), max(zone_cols)
    if max_col >= cols_total - 1: return []
    for r in range(1, rows - 1):
        for c_abs in range(min_col, max_col + 1):
            color = grid_np[r, c_abs]
            if color != bg_color and color != border_color:
                r_rel = r - 1
                c_rel = c_abs - min_col
                pattern_pixels.append(((r_rel, c_rel), color))
    return pattern_pixels

def _is_horizontal_line(pattern_pixels, zone_index, grid_shape):
    if not pattern_pixels: return False
    inner_height = grid_shape[0] - 2
    inner_width = ZONE_WIDTH
    if inner_height <= 0 or inner_width <= 0: return False
    first_rel_row = pattern_pixels[0][0][0]
    pixel_rel_cols = set()
    for (r_rel, c_rel), color in pattern_pixels:
        if r_rel != first_rel_row: return False
        if color != MODIFIER_COLOR: return False
        if not (0 <= c_rel < inner_width): return False
        pixel_rel_cols.add(c_rel)
    return len(pixel_rel_cols) == inner_width

# --- Input Data ---
inputs = [
    [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 6, 4, 4, 4, 6, 5, 2, 4, 4, 4, 2, 5, 4, 4, 3, 4, 4, 5, 4, 4, 4, 4, 4, 5], [5, 4, 4, 4, 6, 4, 5, 4, 2, 4, 2, 4, 5, 4, 4, 3, 4, 4, 5, 4, 4, 4, 4, 4, 5], [5, 4, 4, 6, 4, 4, 5, 4, 4, 2, 4, 4, 5, 3, 3, 3, 3, 3, 5, 4, 4, 4, 4, 4, 5], [5, 4, 6, 4, 4, 4, 5, 4, 2, 4, 2, 4, 5, 4, 4, 3, 4, 4, 5, 4, 4, 4, 4, 4, 5], [5, 6, 4, 4, 4, 4, 5, 2, 4, 4, 4, 2, 5, 4, 4, 3, 4, 4, 5, 4, 4, 4, 4, 4, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 8, 8, 4, 8, 8, 1, 2, 8, 8, 8, 2, 1, 8, 8, 3, 8, 8, 1, 8, 8, 8, 8, 8, 1], [1, 8, 8, 4, 8, 8, 1, 8, 2, 8, 2, 8, 1, 8, 8, 3, 8, 8, 1, 8, 8, 8, 8, 8, 1], [1, 4, 8, 4, 8, 8, 1, 8, 8, 2, 8, 8, 1, 3, 3, 3, 3, 3, 1, 8, 8, 8, 8, 8, 1], [1, 8, 8, 4, 8, 8, 1, 8, 2, 8, 2, 8, 1, 8, 8, 3, 8, 8, 1, 8, 8, 8, 8, 8, 1], [1, 8, 8, 4, 8, 8, 1, 2, 8, 8, 8, 2, 1, 8, 8, 3, 8, 8, 1, 8, 8, 8, 8, 8, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
    [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 7, 9, 9, 9, 9, 6, 9, 9, 9, 4, 4, 6, 9, 1, 9, 1, 9, 6, 9, 9, 9, 9, 9, 6], [6, 9, 7, 9, 9, 9, 6, 9, 9, 9, 4, 4, 6, 1, 9, 1, 9, 1, 6, 9, 9, 9, 9, 9, 6], [6, 9, 9, 7, 9, 9, 6, 9, 9, 9, 9, 9, 6, 9, 1, 9, 1, 9, 6, 9, 9, 9, 9, 9, 6], [6, 9, 9, 9, 7, 9, 6, 4, 4, 9, 9, 9, 6, 1, 9, 1, 9, 1, 6, 9, 9, 9, 9, 9, 6], [6, 7, 9, 9, 9, 7, 6, 4, 4, 9, 9, 9, 6, 9, 1, 9, 1, 9, 6, 9, 9, 9, 9, 9, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]],
    [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], [4, 0, 0, 1, 0, 0, 4, 2, 0, 0, 0, 2, 4, 0, 0, 3, 0, 0, 4, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 4, 0, 2, 0, 2, 0, 4, 0, 0, 3, 0, 0, 4, 0, 0, 0, 0, 0, 4], [4, 1, 1, 1, 1, 1, 4, 0, 0, 2, 0, 0, 4, 3, 3, 3, 3, 3, 4, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 4, 0, 2, 0, 2, 0, 4, 0, 0, 3, 0, 0, 4, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 4, 2, 0, 0, 0, 2, 4, 0, 0, 3, 0, 0, 4, 0, 0, 0, 0, 0, 4], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]]
]

# Expected background colors for Zone 4 (visually determined from Expected Outputs)
expected_z4_bg = [
    4, # Example 1: yellow
    8, # Example 2: azure
    9, # Example 3: maroon
    0  # Example 4: white
]

results = []
for i, input_grid in enumerate(inputs):
    grid_np = np.array(input_grid)
    border_color = _get_border_color(grid_np)
    bg_z2 = _get_zone_background(grid_np, 2, border_color)
    bg_z3 = _get_zone_background(grid_np, 3, border_color)
    # This is the problematic calculation based on current logic
    bg_z4_calculated = _get_zone_background(grid_np, 4, border_color) 

    z2_pattern = _get_pattern_pixels(grid_np, 2, bg_z2, border_color)
    z3_pattern = _get_pattern_pixels(grid_np, 3, bg_z3, border_color)
    is_modifier = _is_horizontal_line(z3_pattern, 3, grid_np.shape)

    results.append({
        "Example": i + 1,
        "Border Color": border_color,
        "Zone 2 Background (Calculated)": bg_z2,
        "Zone 3 Background (Calculated)": bg_z3,
        "Zone 4 Background (Calculated)": bg_z4_calculated,
        "Zone 4 Background (Expected)": expected_z4_bg[i],
        "Zone 2 Pattern Pixels": len(z2_pattern),
        "Zone 3 Pattern Pixels": len(z3_pattern),
        "Is Zone 3 Modifier? (Calculated)": is_modifier,
    })

# Print results clearly
for res in results:
    print(f"--- Example {res['Example']} ---")
    for key, value in res.items():
        if key != "Example":
            print(f"{key}: {value}")
    print("-" * 15)

# Analyze Zone 3 pattern in Example 3 specifically
input_ex3 = inputs[2]
grid_ex3 = np.array(input_ex3)
border_ex3 = _get_border_color(grid_ex3)
bg_z3_ex3 = _get_zone_background(grid_ex3, 3, border_ex3)
z3_pattern_ex3 = _get_pattern_pixels(grid_ex3, 3, bg_z3_ex3, border_ex3)
print("\n--- Example 3 Zone 3 Pattern Analysis ---")
print(f"Border: {border_ex3}, Zone 3 Background: {bg_z3_ex3}")
print(f"Pattern Pixels Found (RelCoord, Color): {z3_pattern_ex3}")
print(f"Is Modifier according to function: {_is_horizontal_line(z3_pattern_ex3, 3, grid_ex3.shape)}")


# Analyze Zone 4 background calculation for Examples 1, 2, 4
print("\n--- Zone 4 Background Analysis (Examples 1, 2, 4) ---")
for i in [0, 1, 3]: # Indices for examples 1, 2, 4
    grid_np = np.array(inputs[i])
    border_color = _get_border_color(grid_np)
    zone4_subgrid = _get_zone_subgrid(grid_np, 4)
    print(f"\nExample {i+1}:")
    print(f"  Border Color: {border_color}")
    print(f"  Zone 4 Subgrid (Input):\n{zone4_subgrid}")
    counts = Counter(zone4_subgrid.flatten())
    print(f"  Zone 4 Subgrid Counts: {counts}")
    if border_color in counts: del counts[border_color]
    print(f"  Zone 4 Subgrid Counts (after removing border {border_color}): {counts}")
    calculated_bg_z4 = 0 if not counts else counts.most_common(1)[0][0]
    print(f"  Calculated Background for Zone 4: {calculated_bg_z4}")


```
```
--- Example 1 ---
Border Color: 4
Zone 2 Background (Calculated): 2
Zone 3 Background (Calculated): 3
Zone 4 Background (Calculated): 0
Zone 4 Background (Expected): 4
Zone 2 Pattern Pixels: 0
Zone 3 Pattern Pixels: 0
Is Zone 3 Modifier? (Calculated): False
---------------
--- Example 2 ---
Border Color: 8
Zone 2 Background (Calculated): 2
Zone 3 Background (Calculated): 3
Zone 4 Background (Calculated): 0
Zone 4 Background (Expected): 8
Zone 2 Pattern Pixels: 0
Zone 3 Pattern Pixels: 0
Is Zone 3 Modifier? (Calculated): False
---------------
--- Example 3 ---
Border Color: 6
Zone 2 Background (Calculated): 9
Zone 3 Background (Calculated): 9
Zone 4 Background (Calculated): 9
Zone 4 Background (Expected): 9
Zone 2 Pattern Pixels: 8
Zone 3 Pattern Pixels: 12
Is Zone 3 Modifier? (Calculated): False
---------------
--- Example 4 ---
Border Color: 0
Zone 2 Background (Calculated): 2
Zone 3 Background (Calculated): 3
Zone 4 Background (Calculated): 0
Zone 4 Background (Expected): 0
Zone 2 Pattern Pixels: 0
Zone 3 Pattern Pixels: 0
Is Zone 3 Modifier? (Calculated): False
---------------

--- Example 3 Zone 3 Pattern Analysis ---
Border: 6, Zone 3 Background: 9
Pattern Pixels Found (RelCoord, Color): [((0, 1), np.int64(1)), ((0, 3), np.int64(1)), ((1, 0), np.int64(1)), ((1, 2), np.int64(1)), ((1, 4), np.int64(1)), ((2, 1), np.int64(1)), ((2, 3), np.int64(1)), ((3, 0), np.int64(1)), ((3, 2), np.int64(1)), ((3, 4), np.int64(1)), ((4, 1), np.int64(1)), ((4, 3), np.int64(1))]
Is Modifier according to function: False

--- Zone 4 Background Analysis (Examples 1, 2, 4) ---

Example 1:
  Border Color: 4
  Zone 4 Subgrid (Input):
[[4 4 4 4 4]
 [4 4 4 4 4]
 [4 4 4 4 4]
 [4 4 4 4 4]
 [4 4 4 4 4]]
  Zone 4 Subgrid Counts: Counter({np.int64(4): 25})
  Zone 4 Subgrid Counts (after removing border 4): Counter()
  Calculated Background for Zone 4: 0

Example 2:
  Border Color: 8
  Zone 4 Subgrid (Input):
[[8 8 8 8 8]
 [8 8 8 8 8]
 [8 8 8 8 8]
 [8 8 8 8 8]
 [8 8 8 8 8]]
  Zone 4 Subgrid Counts: Counter({np.int64(8): 25})
  Zone 4 Subgrid Counts (after removing border 8): Counter()
  Calculated Background for Zone 4: 0

Example 4:
  Border Color: 0
  Zone 4 Subgrid (Input):
[[0 0 0 0 0]
 [0 0 0 0 0]
 [0 0 0 0 0]
 [0 0 0 0 0]
 [0 0 0 0 0]]
  Zone 4 Subgrid Counts: Counter({np.int64(0): 25})
  Zone 4 Subgrid Counts (after removing border 0): Counter()
  Calculated Background for Zone 4: 0

```
**Analysis of Metrics:**

1.  **Background Colors:** The `_get_zone_background` function is failing significantly.
    *   **Zone 4:** As suspected, the calculated `bg_z4` is `0` for Examples 1, 2, and 4 because the input Zone 4 only contains the border color. After removing the border color count, there are no other colors, causing the function to default to `0`. The *expected* background colors for Zone 4 match the background colors calculated for Zone 2 (`bg_z2`). This strongly supports the hypothesis that Zone 4 should inherit Zone 2's background.
    *   **Zone 2 & 3:** The background calculation for Zone 2 and 3 seems incorrect in the metric output (showing 2 and 3 respectively for Ex 1, 2, 4). Let's re-examine the inputs visually:
        *   Ex 1: Z2 bg is yellow (4), Z3 bg is yellow (4).
        *   Ex 2: Z2 bg is azure (8), Z3 bg is azure (8).
        *   Ex 3: Z2 bg is maroon (9), Z3 bg is maroon (9).
        *   Ex 4: Z2 bg is white (0), Z3 bg is white (0).
        The metric code's `_get_zone_background` seems flawed *even for Zones 2 and 3*. It's picking the *pattern* color (blue 2, green 3) as the background, likely because the actual background color (e.g., yellow 4 in Ex 1) is *also* the border color in some examples, causing it to be removed from the counts. This needs correction. The background should be the most common color *excluding the border color*, unless *only* the border color exists, in which case a default like 0 might be needed (or maybe inherit from another zone).
        *Correction:* Looking closer at Ex 1, Border=5 (gray). Z2 bg should be yellow (4). Z3 bg should be yellow (4). `_get_zone_background` returning 2 and 3 is definitely wrong. Ah, the border color is *not* always the most frequent overall. It's the color framing the entire grid. The `_get_border_color` is wrong. It should just be `grid[0][0]`. Let's assume this correction mentally for now.
        *   If Border=5 (Ex1): Z2 subgrid has lots of 4s, some 2s. After removing 5s, 4 is most common -> bg_z2=4. Correct. Z3 subgrid has 4s, some 3s. After removing 5s, 4 is most common -> bg_z3=4. Correct. Z4 subgrid has only 4s. After removing 5s, 4 is most common -> bg_z4=4. Correct.
        *   If Border=1 (Ex2): Z2 subgrid has 8s, some 2s. After removing 1s, 8 is most common -> bg_z2=8. Correct. Z3 subgrid has 8s, some 3s. After removing 1s, 8 is most common -> bg_z3=8. Correct. Z4 subgrid has only 8s. After removing 1s, 8 is most common -> bg_z4=8. Correct.
        *   If Border=6 (Ex3): Z2 subgrid has 9s, some 4s. After removing 6s, 9 is most common -> bg_z2=9. Correct. Z3 subgrid has 9s, some 1s. After removing 6s, 9 is most common -> bg_z3=9. Correct. Z4 subgrid has only 9s. After removing 6s, 9 is most common -> bg_z4=9. Correct.
        *   If Border=4 (Ex4): Z2 subgrid has 0s, some 2s. After removing 4s, 0 is most common -> bg_z2=0. Correct. Z3 subgrid has 0s, some 3s. After removing 4s, 0 is most common -> bg_z3=0. Correct. Z4 subgrid has only 0s. After removing 4s, 0 is most common -> bg_z4=0. Correct.
        *Conclusion:* The *original* background logic was likely flawed by the incorrect border color assumption. Assuming border is `grid[0][0]`, the `_get_zone_background` logic seems mostly okay *except* when the zone only contains the border color (like Z4 often does in the input). The critical insight remains: Zone 4's *target* background should be Zone 2's background.

2.  **Pattern Pixels:** The metric code shows 0 pattern pixels for Zones 2 and 3 in Examples 1, 2, 4. This is also likely due to the faulty background color calculation used *within* the metric code run. If `bg_z2` was calculated as 2 (the pattern color), then `_get_pattern_pixels` would correctly find no pixels different from the background (2) and the border. This confirms the background calculation is the root cause. Example 3 correctly identifies pattern pixels because the calculated background (`9`) was correct by chance.
3.  **Modifier Check:** The `is_modifier` check correctly returns `False` for Example 3, as the pattern pixels are blue (`1`), not green (`3`), and don't form a single horizontal line. It returns `False` for the others, which needs re-evaluation once pattern pixels are correctly identified. Visually, Examples 1, 2, and 4 *do* have the green horizontal line modifier in Zone 3.

**YAML Facts**


```yaml
Grid Structure:
  - Type: Global Border
    Properties: Surrounds the entire grid. Color determined by grid[0][0].
  - Type: Vertical Separators
    Properties: Single column wide, same color as the Global Border.
    Location: Between Zones 1&2, 2&3, 3&4.
  - Type: Zones (1, 2, 3, 4)
    Properties: Contiguous rectangular areas between borders/separators. Assumed fixed width (5 columns inner content).
    Location: Sequentially from left to right.

Objects & Properties:
  - Object: Zone Background
    Applies To: Zones 2, 3, 4 (inner area, excluding global border)
    Property: Color - Most frequent color in the zone's inner area, excluding the global border color.
  - Object: Zone 2 Pattern
    Applies To: Zone 2 (inner area)
    Property: Pixels whose color is neither the Zone 2 Background nor the Global Border color.
    Structure: Can be any shape.
  - Object: Zone 3 Pattern
    Applies To: Zone 3 (inner area)
    Property: Pixels whose color is neither the Zone 3 Background nor the Global Border color.
    Structure: Can be any shape.
  - Object: Zone 3 Modifier (Conditional)
    Derived From: Zone 3 Pattern
    Condition: Zone 3 Pattern consists *only* of green (3) pixels forming a *single, continuous horizontal line* spanning the full width of Zone 3's inner area.
    Property: The specific green pixels forming the line.

Actions & Transformations:
  - Action: Define Target State for Zone 4
    Input: Zone 2 Background Color, Zone 2 Pattern Pixels
    Output: A temporary representation of Zone 4 filled with Zone 2's Background Color, with Zone 2's Pattern Pixels overlaid at corresponding relative positions.
  - Action: Check for Modification
    Input: Zone 3 Pattern Pixels, Zone 3 Inner Area Dimensions
    Output: Boolean (True if Zone 3 Modifier condition is met).
  - Action: Apply Modification (Conditional)
    Condition: Check for Modification is True.
    Input: Target State for Zone 4, Zone 3 Modifier Pixels
    Process: Overwrite pixels in the Target State for Zone 4 at locations corresponding to the relative positions of the Zone 3 Modifier Pixels, using the modifier color (green).
  - Action: Finalize Output Grid
    Input: Input Grid, Final State for Zone 4
    Process: Replace the inner area of Zone 4 in a copy of the Input Grid with the Final State for Zone 4.
```


**Natural Language Program (Revised)**

1.  **Initialization:** Create a copy of the input grid to serve as the output grid.
2.  **Identify Borders and Backgrounds:**
    *   Determine the `border_color` from the top-left pixel (`input_grid[0][0]`).
    *   Determine the `background_color_z2` by finding the most frequent color within the inner area of Zone 2 (rows 1 to H-2, relevant columns), excluding the `border_color`.
    *   Determine the `background_color_z3` similarly for Zone 3.
3.  **Identify Patterns:**
    *   Identify `pattern_pixels_z2` within the inner area of Zone 2: find all pixels whose color is neither `background_color_z2` nor `border_color`. Record their relative coordinates (row, col within the zone's inner area) and colors.
    *   Identify `pattern_pixels_z3` similarly for Zone 3, using `background_color_z3`.
4.  **Prepare Zone 4 Canvas:**
    *   Determine the start column (`min_col4`) and end column (`max_col4`) for the inner area of Zone 4.
    *   Fill the inner area of Zone 4 (rows 1 to H-2, columns `min_col4` to `max_col4`) in the `output_grid` with `background_color_z2`.
5.  **Copy Zone 2 Pattern to Zone 4:**
    *   For each pixel `(rel_coord, color)` in `pattern_pixels_z2`:
        *   Calculate the corresponding absolute target coordinates `(r_abs, c_abs)` in Zone 4 (using `r_abs = rel_coord[0] + 1`, `c_abs = rel_coord[1] + min_col4`).
        *   Set the pixel at `(r_abs, c_abs)` in the `output_grid` to `color`.
6.  **Check for Zone 3 Modifier:**
    *   Evaluate if `pattern_pixels_z3` meets the modifier criteria:
        *   All pixels in `pattern_pixels_z3` must have the color green (3).
        *   The relative coordinates of these green pixels must form a single, continuous horizontal line across the full width (ZONE_WIDTH) of Zone 3's inner area (i.e., all on the same relative row, and covering all relative columns from 0 to ZONE_WIDTH-1).
    *   Set `is_modifier` to True if criteria are met, False otherwise.
7.  **Apply Zone 3 Modifier (if applicable):**
    *   If `is_modifier` is True:
        *   For each pixel `(rel_coord, color)` in `pattern_pixels_z3` (which must be green):
            *   Calculate the corresponding absolute target coordinates `(r_abs, c_abs)` in Zone 4 (using `r_abs = rel_coord[0] + 1`, `c_abs = rel_coord[1] + min_col4`).
            *   Set the pixel at `(r_abs, c_abs)` in the `output_grid` to green (3), overwriting any pixel previously copied from Zone 2.
8.  **Output:** Return the modified `output_grid`.