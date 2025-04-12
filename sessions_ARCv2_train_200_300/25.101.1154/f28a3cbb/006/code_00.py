import numpy as np
from collections import Counter
import json

# Helper to find background color
def find_background_color(grid: np.ndarray) -> int:
    counts = Counter(grid.flatten())
    if not counts: return 0
    return int(counts.most_common(1)[0][0])

# Helper to find solid 3x3 blocks and noise
def find_solid_blocks_and_noise(grid: np.ndarray) -> tuple[int, list[tuple[int, tuple[int, int, int, int], set[tuple[int, int]]]], dict[int, set[tuple[int, int]]]]:
    H, W = grid.shape
    background_color = find_background_color(grid)
    list_of_blocks = []
    all_block_coords = set()
    visited_block_pixels = set()

    for r in range(H - 2):
        for c in range(W - 2):
            if (r, c) in visited_block_pixels: continue
            color = grid[r, c]
            if color == background_color: continue

            is_solid_block = True
            current_block_coords = set()
            for i in range(3):
                for j in range(3):
                    coord = (r + i, c + j)
                    if r+i >= H or c+j >= W or grid[r + i, c + j] != color or coord in visited_block_pixels:
                        is_solid_block = False
                        break
                    current_block_coords.add(coord)
                if not is_solid_block: break

            if is_solid_block:
                bounds = (r, r + 2, c, c + 2)
                list_of_blocks.append((int(color), bounds, current_block_coords))
                all_block_coords.update(current_block_coords)
                visited_block_pixels.update(current_block_coords)

    noise_pixels_by_color = {}
    for r in range(H):
        for c in range(W):
            coord = (r, c)
            color = grid[r, c]
            if color != background_color and coord not in all_block_coords:
                noise_color_key = int(color)
                if noise_color_key not in noise_pixels_by_color:
                    noise_pixels_by_color[noise_color_key] = set()
                noise_pixels_by_color[noise_color_key].add(coord)

    return background_color, list_of_blocks, noise_pixels_by_color

# Helper to get candidate pixels and the side(s) they are adjacent to
def get_edge_adjacent_background_candidates(grid: np.ndarray, background_color: int, block_bounds: tuple[int, int, int, int], block_coords: set[tuple[int, int]]) -> dict[tuple[int, int], set[str]]:
    H, W = grid.shape
    r_min, r_max, c_min, c_max = block_bounds
    candidates = {} # {(r, c): {"Above", "Below", "Left", "Right"}}
    edge_pixels = {(r, c) for r, c in block_coords if r == r_min or r == r_max or c == c_min or c == c_max}

    for r_edge, c_edge in edge_pixels:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r_n, c_n = r_edge + dr, c_edge + dc
            coord_n = (r_n, c_n)

            if 0 <= r_n < H and 0 <= c_n < W and grid[r_n, c_n] == background_color and coord_n not in block_coords:
                if coord_n not in candidates: candidates[coord_n] = set()
                if r_n < r_min: candidates[coord_n].add("Above")
                if r_n > r_max: candidates[coord_n].add("Below")
                if c_n < c_min: candidates[coord_n].add("Left")
                if c_n > c_max: candidates[coord_n].add("Right")

    return {coord: sides for coord, sides in candidates.items() if sides}

# Helper to check Hypothesis 8 condition
def check_h8_condition(candidate_coord: tuple[int, int], candidate_sides: set[str], block_bounds: tuple[int, int, int, int], noise_coords: set[tuple[int, int]]) -> bool:
    """Checks if a candidate should change color based on H8."""
    r_n, c_n = candidate_coord
    r_min, r_max, c_min, c_max = block_bounds

    if not noise_coords: return False

    for side in candidate_sides:
        for r_p, c_p in noise_coords:
            # Condition 1: Noise outside boundary on this side
            # Condition 2: Noise aligned with candidate
            if side == "Above" and r_p < r_min and c_p == c_n: return True
            if side == "Below" and r_p > r_max and c_p == c_n: return True
            if side == "Left"  and c_p < c_min and r_p == r_n: return True
            if side == "Right" and c_p > c_max and r_p == r_n: return True
    return False


# --- Input Data ---
train_1_input = np.array([
    [9, 9, 9, 6, 6, 6, 6, 9, 4], [9, 9, 9, 6, 6, 6, 4, 4, 6], [9, 9, 9, 6, 6, 9, 6, 6, 6],
    [6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 9, 6, 6, 6, 6, 6, 6], [6, 9, 6, 6, 6, 6, 6, 6, 6],
    [9, 6, 6, 6, 6, 6, 4, 4, 4], [6, 6, 4, 6, 6, 6, 4, 4, 4], [6, 6, 6, 4, 6, 6, 4, 4, 4]
], dtype=int)

train_1_output = np.array([
    [9, 9, 9, 9, 6, 6, 6, 6, 6], [9, 9, 9, 6, 6, 6, 6, 6, 6], [9, 9, 9, 9, 6, 6, 6, 6, 6],
    [9, 9, 9, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 4, 4, 4],
    [6, 6, 6, 6, 6, 6, 4, 4, 4], [6, 6, 6, 6, 6, 4, 4, 4, 4], [6, 6, 6, 6, 6, 4, 4, 4, 4]
], dtype=int)

train_2_input = np.array([
    [2, 2, 2, 6, 6, 6, 6, 6, 2], [2, 2, 2, 6, 6, 6, 6, 6, 2], [2, 2, 2, 6, 6, 6, 6, 6, 6],
    [6, 6, 6, 6, 2, 6, 6, 6, 6], [6, 2, 6, 6, 6, 6, 6, 5, 6], [6, 6, 6, 6, 5, 6, 6, 6, 6],
    [6, 6, 6, 6, 6, 6, 5, 5, 5], [5, 6, 6, 6, 6, 6, 5, 5, 5], [6, 6, 2, 6, 6, 6, 5, 5, 5]
], dtype=int)

train_2_output = np.array([
    [2, 2, 2, 2, 6, 6, 6, 6, 6], [2, 2, 2, 2, 6, 6, 6, 6, 6], [2, 2, 2, 2, 6, 6, 6, 6, 6],
    [6, 2, 2, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 5, 6],
    [6, 6, 6, 6, 6, 5, 5, 5, 5], [6, 6, 6, 6, 6, 5, 5, 5, 5], [6, 6, 6, 6, 6, 6, 5, 5, 5]
], dtype=int)

# --- Analysis ---
results = {}
for i, (input_grid, output_grid) in enumerate([(train_1_input, train_1_output), (train_2_input, train_2_output)]):
    example_key = f"train_{i+1}"
    results[example_key] = {}

    bg, blocks, noise = find_solid_blocks_and_noise(input_grid)
    results[example_key]['background_color'] = bg
    results[example_key]['noise'] = {int(color): [f"{r},{c}" for r,c in sorted(list(coords))] for color, coords in noise.items()} # Sorted list

    expected_changes = {}
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
             if input_grid[r,c] == bg and output_grid[r,c] != bg:
                 expected_changes[f"{r},{c}"] = int(output_grid[r,c])
    results[example_key]['expected_changes'] = dict(sorted(expected_changes.items())) # Sorted dict

    results[example_key]['blocks_analysis'] = {}
    h8_predictions = {} # {(r,c): color}

    for color, bounds, coords in blocks:
        block_color_int = int(color)
        block_key = f"block_{block_color_int}_at_{bounds[0]}_{bounds[2]}"
        block_noise_coords = noise.get(block_color_int, set())
        candidates = get_edge_adjacent_background_candidates(input_grid, bg, bounds, coords)

        block_analysis = {
            'noise_coords': [f"{r},{c}" for r,c in sorted(list(block_noise_coords))], # Sorted list
            'candidates': {}
        }

        # Sort candidate keys for consistent output
        sorted_candidate_coords = sorted(list(candidates.keys()))

        for coord_n in sorted_candidate_coords:
            sides = candidates[coord_n]
            coord_n_str = f"{coord_n[0]},{coord_n[1]}"
            should_change = check_h8_condition(coord_n, sides, bounds, block_noise_coords)
            block_analysis['candidates'][coord_n_str] = {
                'adjacent_sides': sorted(list(sides)), # Sorted list
                'h8_predicts_change': should_change
            }
            if should_change:
                h8_predictions[coord_n_str] = block_color_int
        
        results[example_key]['blocks_analysis'][block_key] = block_analysis


    results[example_key]['h8_predictions'] = dict(sorted(h8_predictions.items())) # Sorted dict
    # Compare predictions with expected
    h8_correct = {}
    h8_errors_fp = {} # False Positives (Predicted change, but shouldn't have)
    h8_errors_fn = {} # False Negatives (Should have changed, but wasn't predicted)

    all_prediction_coords = set(h8_predictions.keys())
    all_expected_coords = set(expected_changes.keys())

    # Sort combined keys for consistent output
    sorted_all_coords = sorted(list(all_prediction_coords.union(all_expected_coords)))

    for coord_str in sorted_all_coords:
        predicted = coord_str in h8_predictions
        expected = coord_str in expected_changes

        if predicted and expected and h8_predictions[coord_str] == expected_changes[coord_str]:
            h8_correct[coord_str] = True
        elif predicted and not expected:
             h8_errors_fp[coord_str] = {'predicted': h8_predictions[coord_str], 'expected': bg}
             h8_correct[coord_str] = False
        elif not predicted and expected:
             h8_errors_fn[coord_str] = {'predicted': bg, 'expected': expected_changes[coord_str]}
             h8_correct[coord_str] = False
        elif predicted and expected and h8_predictions[coord_str] != expected_changes[coord_str]:
             # This case indicates a wrong color prediction, treat as FP
             h8_errors_fp[coord_str] = {'predicted': h8_predictions[coord_str], 'expected': expected_changes[coord_str]}
             h8_correct[coord_str] = False

    results[example_key]['h8_summary'] = {
        'correct': h8_correct,
        'false_positives': h8_errors_fp,
        'false_negatives': h8_errors_fn
    }


# Custom JSON encoder for sets and numpy types
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set): return sorted(list(obj))
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)): return int(obj)
        if isinstance(obj, (np.float_, np.float16, np.float32, np.float64)): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return json.JSONEncoder.default(self, obj)

# Print results as JSON
print(json.dumps(results, indent=2, cls=NpEncoder))