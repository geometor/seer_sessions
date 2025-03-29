Okay, the code execution for metric gathering mostly worked but failed on the YAML import. I can still use the printed output.

**General Assessment:**

The analysis of the failed examples (1 and 3) confirms the hypothesis: the original code incorrectly handles situations where a red pixel has multiple equidistant nearest azure neighbors in cardinal directions.

*   In Example 1, the red pixel at (4, 8) has its nearest cardinal azure neighbor to the left at (4, 3) (distance 5) and another neighbor to the right at (4, 14) (distance 6). The code correctly identifies the left one as the *sole* nearest *cardinal* neighbor and acts only on it. However, the *expected* output shows actions related to *both* the left neighbor (4, 3) and the right neighbor (4, 14). This implies the definition of "nearest" needs adjustment or there's another rule. Re-examining Example 1: The distance to the left azure pixel at (4, 3) is 5. The distance to the right azure pixel at (4, 14) is 6. My previous hypothesis about equidistant neighbors was incorrect for Example 1. Why does the right side get processed? Let's re-check the analysis code... Ah, my analysis code was searching *only* for the *absolute* minimum distance across all directions. Let's re-think Example 1. The code searches Right (no target), Left (target at (4,3), dist 5, `min_dist=5`), Down (no target), Up (no target). It only acts on the left target. The expected output acts on *both* (4,3) and (4,14). This suggests the rule isn't just "nearest overall cardinal", but perhaps "nearest in *each* cardinal direction"? Let's test this revised hypothesis.
    *   Example 1, Red (4,8): Nearest Left: (4,3) dist 5. Nearest Right: (4,14) dist 6. Nearest Up: None. Nearest Down: None. The expected output draws lines and patterns for *both* (4,3) and (4,14). This indicates the rule is likely: **Find the nearest azure pixel in *each* cardinal direction (if one exists) and perform the actions for *all* of them.**
*   In Example 3, the red pixel at (10, 4) has equidistant nearest neighbors *up* at (7, 4) (distance 3) and *down* at (13, 4) (distance 3). The code currently only processes one of them (the one found last, which was (7,4) in the 'up' check, overwriting the 'down' result). The expected output clearly shows lines drawn and patterns placed for *both* targets. This aligns with the revised hypothesis: act on the nearest neighbor found in *each* cardinal direction independently.

**Metrics / Facts:**

(Based on the `code_output`, adjusted for the revised understanding)


```yaml
example_1:
  red_pixel_1:
    location: (4, 8)
    nearest_targets_per_direction:
      left: {target: (4, 3), distance: 5, direction: (0, -1)}
      right: {target: (4, 14), distance: 6, direction: (0, 1)}
      up: null
      down: null
    expected_actions:
      - Draw red line from (4, 8) to (4, 4)
      - Draw 3x3 pattern centered at (4, 3)
      - Draw red line from (4, 8) to (4, 13)
      - Draw 3x3 pattern centered at (4, 14)
    code_error: Did not process the 'right' target (4, 14).
example_3:
  red_pixel_1:
    location: (2, 8)
    nearest_targets_per_direction:
      left: null
      right: null
      up: null
      down: {target: (7, 8), distance: 5, direction: (1, 0)}
    expected_actions:
      - Draw red line from (2, 8) to (6, 8)
      - Draw 3x3 pattern centered at (7, 8)
    code_error: None for this pixel.
  red_pixel_2:
    location: (10, 4)
    nearest_targets_per_direction:
      left: null
      right: null
      up: {target: (7, 4), distance: 3, direction: (-1, 0)}
      down: {target: (13, 4), distance: 3, direction: (1, 0)}
    expected_actions:
      - Draw red line from (10, 4) to (8, 4)
      - Draw 3x3 pattern centered at (7, 4)
      - Draw red line from (10, 4) to (12, 4)
      - Draw 3x3 pattern centered at (13, 4)
    code_error: Did not process the 'down' target (13, 4). Only processed the 'up' target (7, 4).
```


**Natural Language Program (Revised):**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all locations `(r, c)` in the input grid containing a red (2) pixel. These are the source points.
3.  Identify all locations in the input grid containing an azure (8) pixel. Store these potential target points for efficient lookup (e.g., in a set).
4.  For *each* red source point `(r, c)`:
    a.  Search in *each* of the four cardinal directions (e.g., right, left, down, up) independently from `(r, c)`.
    b.  For a given direction, find the *first* azure (8) pixel encountered, let its location be `(target_r, target_c)`. If no azure pixel is found in that direction, do nothing for this direction.
    c.  If an azure target `(target_r, target_c)` was found for the current direction:
        i.  Determine the unit direction vector `(dr, dc)` from the source `(r, c)` towards the target `(target_r, target_c)`.
        ii. Calculate the distance (number of steps) between the source and target along that axis.
        iii. Draw a line of red (2) pixels in the output grid starting from the source point `(r, c)` and moving one step at a time in the direction `(dr, dc)`. The line stops *one pixel before* reaching the target point `(target_r, target_c)`. This line overwrites any existing pixels.
        iv. At the target point's location `(target_r, target_c)`, draw a 3x3 square pattern in the output grid:
            1.  The center pixel `(target_r, target_c)` becomes red (2).
            2.  The 8 surrounding pixels (if they are within the grid boundaries) become azure (8). This pattern overwrites existing pixels in the 3x3 area.
5.  Return the modified output grid.**General Assessment:**

The provided code successfully implemented parts of the transformation rule, specifically identifying red source pixels, finding *a* nearest cardinal azure target, drawing a line towards it, and placing a 3x3 pattern. However, it failed on examples where a red pixel should interact with the nearest azure pixel in *multiple* cardinal directions, not just the single closest one overall or the last one found among equals.

The key errors identified in Examples 1 and 3 stem from this misunderstanding:
1.  **Example 1 Failure:** The code found the nearest cardinal target (left, distance 5) and ignored the nearest target in the other direction (right, distance 6). The expected output shows actions based on *both* the nearest left *and* the nearest right targets.
2.  **Example 3 Failure:** For the second red pixel, the code found two equidistant targets (up and down, distance 3). It correctly identified the minimum distance but only acted upon the last one found during its search (the 'up' target), ignoring the 'down' target. The expected output requires actions for *both* equidistant targets.

The strategy for resolving these errors is to modify the logic to iterate through each cardinal direction *independently* for every red pixel. For each direction where an azure pixel is found, the code must find the *closest* one *in that specific direction* and perform the line-drawing and pattern-placement actions based on that target, regardless of whether closer targets exist in other directions.

**Metrics and Findings:**

``` python
import numpy as np

def analyze_example(name, input_grid, expected_output_grid, transformed_output_grid):
    print(f"--- Analyzing {name} ---")
    input_np = np.array(input_grid, dtype=int)
    expected_np = np.array(expected_output_grid, dtype=int)
    transformed_np = np.array(transformed_output_grid, dtype=int)
    height, width = input_np.shape

    red_pixels = np.argwhere(input_np == 2)
    azure_pixels_coords = np.argwhere(input_np == 8)
    azure_set = set(map(tuple, azure_pixels_coords))

    print(f"Input Grid Size: {height}x{width}")
    print(f"Red Pixels (Input): {red_pixels.tolist()}")

    results = {}

    for idx, (r, c) in enumerate(red_pixels):
        print(f"\nProcessing Red Pixel {idx+1} at ({r}, {c}):")
        pixel_results = {
            "location": (r,c),
            "nearest_targets_per_direction": {}
        }
        
        found_targets = [] # Store (target_coord, distance, direction_vector)

        # Check Right (+)
        nearest_right = None
        min_dist_right = float('inf')
        for tc in range(c + 1, width):
            if (r, tc) in azure_set:
                dist = tc - c
                if dist < min_dist_right: # Should always be true first time
                   min_dist_right = dist
                   nearest_right = (r, tc)
                break # Found nearest in this direction
        if nearest_right:
             pixel_results["nearest_targets_per_direction"]["right"] = {"target": nearest_right, "distance": min_dist_right, "direction": (0, 1)}
             found_targets.append((nearest_right, min_dist_right, (0,1)))
             print(f"  Nearest Right Azure: {nearest_right} (Distance: {min_dist_right})")
        else:
             print(f"  Nearest Right Azure: None")
             pixel_results["nearest_targets_per_direction"]["right"] = None


        # Check Left (-)
        nearest_left = None
        min_dist_left = float('inf')
        for tc in range(c - 1, -1, -1):
            if (r, tc) in azure_set:
                dist = c - tc
                if dist < min_dist_left:
                   min_dist_left = dist
                   nearest_left = (r, tc)
                break # Found nearest in this direction
        if nearest_left:
             pixel_results["nearest_targets_per_direction"]["left"] = {"target": nearest_left, "distance": min_dist_left, "direction": (0, -1)}
             found_targets.append((nearest_left, min_dist_left, (0,-1)))
             print(f"  Nearest Left Azure: {nearest_left} (Distance: {min_dist_left})")
        else:
             print(f"  Nearest Left Azure: None")
             pixel_results["nearest_targets_per_direction"]["left"] = None

        # Check Down (+)
        nearest_down = None
        min_dist_down = float('inf')
        for tr in range(r + 1, height):
            if (tr, c) in azure_set:
                dist = tr - r
                if dist < min_dist_down:
                   min_dist_down = dist
                   nearest_down = (tr, c)
                break # Found nearest in this direction
        if nearest_down:
            pixel_results["nearest_targets_per_direction"]["down"] = {"target": nearest_down, "distance": min_dist_down, "direction": (1, 0)}
            found_targets.append((nearest_down, min_dist_down, (1,0)))
            print(f"  Nearest Down Azure: {nearest_down} (Distance: {min_dist_down})")
        else:
             print(f"  Nearest Down Azure: None")
             pixel_results["nearest_targets_per_direction"]["down"] = None

        # Check Up (-)
        nearest_up = None
        min_dist_up = float('inf')
        for tr in range(r - 1, -1, -1):
            if (tr, c) in azure_set:
                dist = r - tr
                if dist < min_dist_up:
                   min_dist_up = dist
                   nearest_up = (tr, c)
                break # Found nearest in this direction
        if nearest_up:
            pixel_results["nearest_targets_per_direction"]["up"] = {"target": nearest_up, "distance": min_dist_up, "direction": (-1, 0)}
            found_targets.append((nearest_up, min_dist_up, (-1,0)))
            print(f"  Nearest Up Azure: {nearest_up} (Distance: {min_dist_up})")
        else:
             print(f"  Nearest Up Azure: None")
             pixel_results["nearest_targets_per_direction"]["up"] = None

        # Compare expected vs transformed actions for *this specific red pixel*
        print("  Comparison (Expected vs Transformed):")
        pixel_results["expected_actions"] = []
        pixel_results["code_errors"] = []

        action_performed_correctly = {} # track which targets the code handled

        for target_coord, dist, direction in found_targets:
            target_r, target_c = target_coord
            dr, dc = direction
            
            # Expected actions for this target
            action_desc = f"Target {target_coord} (Dir: {direction}, Dist: {dist})"
            pixel_results["expected_actions"].append(action_desc)
            
            # Check if the 3x3 pattern is present and correct in the *transformed* output
            pattern_correct_transformed = True
            try:
                if transformed_np[target_r, target_c] != 2: pattern_correct_transformed = False
                for ro in range(-1, 2):
                    for co in range(-1, 2):
                        if ro == 0 and co == 0: continue
                        pr, pc = target_r + ro, target_c + co
                        if 0 <= pr < height and 0 <= pc < width:
                            if transformed_np[pr, pc] != 8:
                                pattern_correct_transformed = False
                                break
                    if not pattern_correct_transformed: break
            except IndexError:
                 pattern_correct_transformed = False # Pattern check went out of bounds

            action_performed_correctly[target_coord] = pattern_correct_transformed

            print(f"    {action_desc}: Pattern in Transformed Output Correct: {pattern_correct_transformed}")

            # Check if pattern exists in expected output around target (for verification)
            pattern_correct_expected = True
            try:
                if expected_np[target_r, target_c] != 2: pattern_correct_expected = False
                for ro in range(-1, 2):
                    for co in range(-1, 2):
                         if ro == 0 and co == 0: continue
                         pr, pc = target_r + ro, target_c + co
                         if 0 <= pr < height and 0 <= pc < width:
                            if expected_np[pr, pc] != 8:
                                pattern_correct_expected = False
                                break
                    if not pattern_correct_expected: break
            except IndexError:
                pattern_correct_expected = False
            
            print(f"      (Verification) Pattern in Expected Output Correct: {pattern_correct_expected}")


        # Identify errors based on which targets were not handled correctly by the code
        for target_coord, _, _ in found_targets:
             if not action_performed_correctly.get(target_coord, False):
                 error_msg = f"Code failed to correctly place pattern for target {target_coord}."
                 pixel_results["code_errors"].append(error_msg)
                 print(f"    ERROR: {error_msg}")


        results[f"red_pixel_{idx+1}"] = pixel_results

    # Overall comparison
    match = np.array_equal(expected_np, transformed_np)
    pixels_off = np.sum(expected_np != transformed_np)
    print(f"\nOverall Match: {match}")
    print(f"Overall Pixels Off: {pixels_off}")

    return results


# Example 1 Data
input_grid_1 = [[0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,2,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0]]
expected_output_1 = [[0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,8,8,8,0,0,0,0,0,0,0,0,8,8,8,0,0], [0,0,8,2,8,2,2,2,2,2,2,2,2,8,2,8,0,0], [0,0,8,8,8,0,0,0,0,0,0,0,0,8,8,8,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0]]
transformed_output_1 = [[0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,8,8,8,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,8,2,8,2,2,2,2,0,0,0,0,0,8,0,0,0], [0,0,8,8,8,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0], [0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0]]

# Example 3 Data
input_grid_3 = [[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,2,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [8,8,8,8,8,8,8,8,8,8,8,8], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,2,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [8,8,8,8,8,8,8,8,8,8,8,8], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]
expected_output_3 = [[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,2,0,0,0], [0,0,0,0,0,0,0,0,2,0,0,0], [0,0,0,0,0,0,0,0,2,0,0,0], [0,0,0,0,0,0,0,0,2,0,0,0], [0,0,0,8,8,8,0,8,8,8,0,0], [8,8,8,8,2,8,8,8,2,8,8,8], [0,0,0,8,8,8,0,8,8,8,0,0], [0,0,0,0,2,0,0,0,0,0,0,0], [0,0,0,0,2,0,0,0,0,0,0,0], [0,0,0,0,2,0,0,0,0,0,0,0], [0,0,0,8,8,8,0,0,0,0,0,0], [8,8,8,8,2,8,8,8,8,8,8,8], [0,0,0,8,8,8,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]
transformed_output_3 = [[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,2,0,0,0], [0,0,0,0,0,0,0,0,2,0,0,0], [0,0,0,0,0,0,0,0,2,0,0,0], [0,0,0,0,0,0,0,0,2,0,0,0], [0,0,0,0,0,0,0,8,8,8,0,0], [8,8,8,8,8,8,8,8,2,8,8,8], [0,0,0,0,0,0,0,8,8,8,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,2,0,0,0,0,0,0,0], [0,0,0,0,2,0,0,0,0,0,0,0], [0,0,0,8,8,8,0,0,0,0,0,0], [8,8,8,8,2,8,8,8,8,8,8,8], [0,0,0,8,8,8,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]

metrics_1 = analyze_example("Example 1", input_grid_1, expected_output_1, transformed_output_1)
metrics_3 = analyze_example("Example 3", input_grid_3, expected_output_3, transformed_output_3)

# Combine metrics
all_metrics = {"example_1": metrics_1, "example_3": metrics_3}

# Convert tuple keys and values to strings for YAML compatibility
import json
def convert_keys_to_str(obj):
    if isinstance(obj, dict):
        # Convert tuple keys like (4, 3) to string 'target_(4, 3)'
        # Convert other keys normally
        new_dict = {}
        for k, v in obj.items():
             key_str = str(k)
             # Specific handling for target tuples if needed, otherwise default str() is fine
             # if isinstance(k, tuple) and len(k) == 2:
             #    key_str = f"target_{k}" 
             new_dict[key_str] = convert_keys_to_str(v)
        return new_dict
    elif isinstance(obj, list):
        return [convert_keys_to_str(elem) for elem in obj]
    elif isinstance(obj, tuple) and len(obj) == 2:
         # Represent coordinate tuples as strings '(r, c)' for clarity in YAML
        return f"({obj[0]}, {obj[1]})" 
    elif isinstance(obj, np.int64): # Handle numpy int types
        return int(obj)
    else:
        # Convert other types (like np scalars) to standard python types if possible
        try:
             return json.loads(json.dumps(obj)) # Basic attempt to json-serialize/deserialize
        except TypeError:
             return str(obj) # Fallback to string representation

all_metrics_str_keys = convert_keys_to_str(all_metrics)

# Generate YAML output
import yaml
yaml_output = yaml.dump(all_metrics_str_keys, indent=2, sort_keys=False, default_flow_style=False)

print("\n--- YAML Facts ---")
print(yaml_output)


```
```
--- Analyzing Example 1 ---
Input Grid Size: 13x18
Red Pixels (Input): [[4, 8]]

Processing Red Pixel 1 at (4, 8):
  Nearest Right Azure: (np.int64(4), 14) (Distance: 6)
  Nearest Left Azure: (np.int64(4), 3) (Distance: 5)
  Nearest Down Azure: None
  Nearest Up Azure: None
  Comparison (Expected vs Transformed):
    Target (np.int64(4), 14) (Dir: (0, 1), Dist: 6): Pattern in Transformed Output Correct: False
      (Verification) Pattern in Expected Output Correct: True
    Target (np.int64(4), 3) (Dir: (0, -1), Dist: 5): Pattern in Transformed Output Correct: True
      (Verification) Pattern in Expected Output Correct: True
    ERROR: Code failed to correctly place pattern for target (np.int64(4), 14).

Overall Match: False
Overall Pixels Off: 11
--- Analyzing Example 3 ---
Input Grid Size: 17x12
Red Pixels (Input): [[2, 8], [10, 4]]

Processing Red Pixel 1 at (2, 8):
  Nearest Right Azure: None
  Nearest Left Azure: None
  Nearest Down Azure: (7, np.int64(8)) (Distance: 5)
  Nearest Up Azure: None
  Comparison (Expected vs Transformed):
    Target (7, np.int64(8)) (Dir: (1, 0), Dist: 5): Pattern in Transformed Output Correct: True
      (Verification) Pattern in Expected Output Correct: True

Processing Red Pixel 2 at (10, 4):
  Nearest Right Azure: None
  Nearest Left Azure: None
  Nearest Down Azure: (13, np.int64(4)) (Distance: 3)
  Nearest Up Azure: (7, np.int64(4)) (Distance: 3)
  Comparison (Expected vs Transformed):
    Target (13, np.int64(4)) (Dir: (1, 0), Dist: 3): Pattern in Transformed Output Correct: True
      (Verification) Pattern in Expected Output Correct: True
    Target (7, np.int64(4)) (Dir: (-1, 0), Dist: 3): Pattern in Transformed Output Correct: False
      (Verification) Pattern in Expected Output Correct: True
    ERROR: Code failed to correctly place pattern for target (7, np.int64(4)).

Overall Match: False
Overall Pixels Off: 8

```
``` failed
Traceback (most recent call last):
  File "<string>", line 221, in <module>
ModuleNotFoundError: No module named 'yaml'

```
**YAML Facts:**


```yaml
example_1:
  red_pixel_1:
    location: (4, 8)
    nearest_targets_per_direction:
      right:
        target: (4, 14)
        distance: 6
        direction: (0, 1)
      left:
        target: (4, 3)
        distance: 5
        direction: (0, -1)
      down: null
      up: null
    expected_actions:
    - Target (4, 14) (Dir: (0, 1), Dist: 6)
    - Target (4, 3) (Dir: (0, -1), Dist: 5)
    code_errors:
    - Code failed to correctly place pattern for target (4, 14).
example_3:
  red_pixel_1:
    location: (2, 8)
    nearest_targets_per_direction:
      right: null
      left: null
      down:
        target: (7, 8)
        distance: 5
        direction: (1, 0)
      up: null
    expected_actions:
    - Target (7, 8) (Dir: (1, 0), Dist: 5)
    code_errors: []
  red_pixel_2:
    location: (10, 4)
    nearest_targets_per_direction:
      right: null
      left: null
      down:
        target: (13, 4)
        distance: 3
        direction: (1, 0)
      up:
        target: (7, 4)
        distance: 3
        direction: (-1, 0)
    expected_actions:
    - Target (13, 4) (Dir: (1, 0), Dist: 3)
    - Target (7, 4) (Dir: (-1, 0), Dist: 3)
    code_errors:
    - Code failed to correctly place pattern for target (7, 4).

```


**Natural Language Program (Revised):**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all locations `(r, c)` in the input grid containing a red (2) pixel. These are the source points.
3.  Identify all locations in the input grid containing an azure (8) pixel. Store these potential target points for efficient lookup (e.g., in a set).
4.  For *each* red source point `(r, c)`:
    a.  **Independently** search in *each* of the four cardinal directions (right, left, down, up) starting from `(r, c)`.
    b.  For a given direction, find the location `(target_r, target_c)` of the *first* azure (8) pixel encountered along that path.
    c.  If an azure target `(target_r, target_c)` is found for that specific direction:
        i.  Calculate the distance (number of steps) from `(r, c)` to `(target_r, target_c)`.
        ii. Determine the unit direction vector `(dr, dc)` from the source `(r, c)` towards the target `(target_r, target_c)`.
        iii. Draw a line of red (2) pixels in the output grid starting *at* the source point `(r, c)` and moving `distance - 1` steps in the direction `(dr, dc)`. Each pixel on this path (including the start, excluding the target) overwrites the existing pixel with red (2).
        iv. At the target point's location `(target_r, target_c)`, draw a 3x3 square pattern in the output grid:
            1.  The center pixel `(target_r, target_c)` becomes red (2).
            2.  The 8 surrounding pixels (within grid bounds) become azure (8). This pattern overwrites existing pixels in the 3x3 area centered on the target.
    d. Repeat steps 4b and 4c for all four cardinal directions for the current red source point `(r,c)`.
5.  Return the modified output grid.