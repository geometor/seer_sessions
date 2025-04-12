import numpy as np
from collections import deque

# --- find_objects function (copied from previous response) ---
def find_objects(grid: np.ndarray) -> list[dict]:
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and not visited[r, c]:
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                objects.append({
                    'color': color, 'pixels': obj_pixels, 'height': height, 'width': width,
                    'min_r': min_r, 'max_r': max_r, 'min_c': min_c, 'max_c': max_c
                })
    return objects

# --- Input Grids ---
input_1 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 2, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 0, 0, 1, 1, 1, 1, 0], [0, 3, 3, 0, 0, 1, 0, 0, 1, 0], [0, 3, 3, 0, 0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
input_2 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 4, 4, 4, 0], [0, 0, 0, 0, 0, 4, 4, 4, 4, 0], [0, 7, 7, 7, 0, 4, 4, 4, 4, 0], [0, 7, 0, 7, 0, 4, 4, 4, 4, 0], [0, 7, 0, 7, 0, 0, 0, 0, 0, 0], [0, 7, 0, 7, 0, 8, 8, 8, 0, 0], [0, 7, 0, 7, 0, 8, 0, 8, 0, 0], [0, 7, 7, 7, 0, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
input_3 = np.array([
    [0, 6, 6, 6, 6, 6, 0, 8, 8, 8], [0, 6, 0, 0, 0, 6, 0, 8, 0, 8], [0, 6, 6, 6, 6, 6, 0, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 4, 4, 4, 0], [0, 2, 2, 2, 0, 0, 4, 0, 4, 0], [0, 2, 2, 2, 0, 0, 4, 0, 4, 0], [0, 2, 2, 2, 0, 0, 4, 4, 4, 0], [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 0, 0, 0, 0, 0, 0]
])
# --- Expected Outputs (for dimension check) ---
output_1_expected = [[0, 0], [0, 0], [0, 0]]
output_2_expected = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
output_3_expected = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

inputs = {'train_1': input_1, 'train_2': input_2, 'train_3': input_3}
expected_dims = {'train_1': (len(output_1_expected), len(output_1_expected[0])),
                 'train_2': (len(output_2_expected), len(output_2_expected[0])),
                 'train_3': (len(output_3_expected), len(output_3_expected[0]))}
results_log = {}

print("Detailed Metrics Analysis (Hypothesis 9: Max Area Rule):")
for name, grid in inputs.items():
    objects = find_objects(grid)
    num_objects = len(objects)
    unique_colors = set(obj['color'] for obj in objects)
    num_unique_colors = len(unique_colors)
    max_height = 0
    special_obj_details = "None"
    dims_A = None
    area_A = 0
    dims_B = None
    area_B = 0
    final_dims = None
    rule_explanation = ""

    if objects:
        max_height = max(obj['height'] for obj in objects)

        # Calculate Potential Dims B: MaxH x (C-1)
        h_B = max_height
        w_B = max(0, num_unique_colors - 1)
        dims_B = (h_B, w_B)
        area_B = h_B * w_B

        # Calculate Potential Dims A: From Special Object if N==C
        if num_objects == num_unique_colors:
            found_special = False
            for obj in objects:
                if obj['height'] == obj['color']:
                    h_A = obj['height']
                    w_A = obj['width']
                    dims_A = (h_A, w_A)
                    area_A = h_A * w_A
                    special_obj_details = f"Found: Color={obj['color']}, H={h_A}, W={w_A}"
                    found_special = True
                    break
            if not found_special:
                 special_obj_details = "N==C but no object with H==Color found"
                 # Dims A remains None

        # Selection Rule: Choose Max Area, Tie-break favors A if valid
        if dims_A is not None and area_A >= area_B:
            final_dims = dims_A
            rule_explanation = f"Selected Dims A ({dims_A}, Area={area_A}) because N==C, Special Obj exists, and Area A >= Area B ({area_B})"
        else:
            final_dims = dims_B
            if dims_A is not None: # A was calculated but B won
                 rule_explanation = f"Selected Dims B ({dims_B}, Area={area_B}) because Area B > Area A ({area_A})"
            else: # A was not applicable (N!=C or no special obj)
                 rule_explanation = f"Selected Dims B ({dims_B}, Area={area_B}) because Dims A not applicable (N!=C or no Special Obj)"


    else: # No objects found
        final_dims = (1, 1) # Default or based on task spec for empty
        rule_explanation = "No objects found, defaulting to 1x1"

    # Handle potential zero dimensions (should be covered by max(0, C-1) and default)
    if final_dims[0] <= 0 or final_dims[1] <= 0:
        final_dims = (max(1, final_dims[0]), max(1, final_dims[1]))
        rule_explanation += " (Adjusted to min 1x1)"


    expected_dim = expected_dims[name]
    match_status = "PASS" if final_dims == expected_dim else "FAIL"

    results_log[name] = {
        'N': num_objects, 'C': num_unique_colors, 'MaxH': max_height,
        'Condition': f"N ({num_objects}) {'==' if num_objects == num_unique_colors else '!='} C ({num_unique_colors})",
        'Special Object (H==Color)': special_obj_details,
        'Potential Dims A (SpecObj)': dims_A, 'Area A': area_A,
        'Potential Dims B (MaxHxC-1)': dims_B, 'Area B': area_B,
        'Final Chosen Dims': final_dims,
        'Rule Explanation': rule_explanation,
        'Expected Output Dims': expected_dim,
        'Result': match_status,
        'Objects Found (Color, H, W)': [(obj['color'], obj['height'], obj['width']) for obj in objects]

    }
    print(f"\n--- {name} ---")
    for key, value in results_log[name].items():
            print(f"{key}: {value}")

print("\n--- Final Hypothesis Check ---")
all_pass = all(res['Result'] == 'PASS' for res in results_log.values())
if all_pass:
    print("Conclusion: The 'Max Area' rule (Hypothesis 9) correctly predicts the output dimensions for all training examples.")
else:
    failed_cases = [name for name, res in results_log.items() if res['Result'] == 'FAIL']
    print(f"Conclusion: The 'Max Area' rule (Hypothesis 9) FAILED for examples: {', '.join(failed_cases)}. Logic requires further revision.")
