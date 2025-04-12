import numpy as np
import collections
import json

# Helper function to convert grids from list of lists to numpy arrays
def to_np(grid):
    return np.array(grid, dtype=int)

# Helper function to convert numpy patterns to hashable tuples
def pattern_to_tuple(pattern_np):
    # Ensure elements are standard Python ints for JSON serialization
    return tuple(tuple(int(x) for x in row) for row in pattern_np)

# Helper function to recursively convert numpy types in dict/list structures
def convert_np_types(obj):
    if isinstance(obj, dict):
        return {k: convert_np_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_np_types(elem) for elem in obj]
    elif isinstance(obj, tuple):
         # Convert tuples containing np types (like positions)
         return tuple(convert_np_types(elem) for elem in obj)
    elif isinstance(obj, (np.integer, np.int64)): # Added np.int64
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return convert_np_types(obj.tolist()) # Convert arrays to lists
    else:
        return obj

# --- Data as provided in the prompt ---
train_examples_data = [
    {'name': 'train_1', 'type': 'input', 'grid': [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1], [1, 6, 4, 6, 6, 6, 1, 6, 4, 6, 6, 6, 1, 6, 4, 6, 4, 6, 1], [1, 6, 4, 4, 4, 6, 1, 6, 4, 4, 4, 6, 1, 6, 4, 4, 4, 6, 1], [1, 6, 6, 4, 6, 6, 1, 6, 6, 4, 6, 6, 1, 6, 6, 4, 6, 6, 1], [1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1], [1, 6, 4, 6, 6, 6, 1, 6, 4, 6, 6, 6, 1, 6, 4, 6, 6, 6, 1], [1, 6, 4, 4, 6, 6, 1, 6, 4, 4, 4, 6, 1, 6, 4, 4, 4, 6, 1], [1, 6, 6, 4, 6, 6, 1, 6, 6, 4, 6, 6, 1, 6, 6, 4, 6, 6, 1], [1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1], [1, 6, 4, 6, 6, 6, 1, 6, 4, 6, 6, 6, 1, 6, 4, 6, 6, 6, 1], [1, 6, 4, 4, 4, 6, 1, 6, 4, 4, 4, 6, 1, 6, 4, 4, 4, 6, 1], [1, 6, 6, 4, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 4, 6, 6, 1], [1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]},
    {'name': 'train_1', 'type': 'output', 'grid': [[1, 1, 1, 1, 1, 1, 1], [1, 6, 6, 6, 6, 6, 1], [1, 6, 4, 6, 4, 6, 1], [1, 6, 4, 4, 4, 6, 1], [1, 6, 6, 4, 6, 6, 1], [1, 6, 6, 6, 6, 6, 1], [1, 1, 1, 1, 1, 1, 1], [1, 6, 6, 6, 6, 6, 1], [1, 6, 4, 6, 6, 6, 1], [1, 6, 4, 4, 6, 6, 1], [1, 6, 6, 4, 6, 6, 1], [1, 6, 6, 6, 6, 6, 1], [1, 1, 1, 1, 1, 1, 1], [1, 6, 6, 6, 6, 6, 1], [1, 6, 4, 6, 6, 6, 1], [1, 6, 4, 4, 4, 6, 1], [1, 6, 6, 6, 6, 6, 1], [1, 6, 6, 6, 6, 6, 1], [1, 1, 1, 1, 1, 1, 1]]}, # Expected output from prompt
    {'name': 'train_1', 'type': 'transformed', 'grid': [[1, 1, 1, 1, 1, 1, 1], [1, 6, 6, 6, 6, 6, 1], [1, 6, 4, 6, 4, 6, 1], [1, 6, 4, 4, 4, 6, 1], [1, 6, 6, 4, 6, 6, 1], [1, 6, 6, 6, 6, 6, 1], [1, 1, 1, 1, 1, 1, 1], [1, 6, 6, 6, 6, 6, 1], [1, 6, 4, 6, 4, 6, 1], [1, 6, 4, 4, 4, 6, 1], [1, 6, 6, 4, 6, 6, 1], [1, 6, 6, 6, 6, 6, 1], [1, 1, 1, 1, 1, 1, 1], [1, 6, 6, 6, 6, 6, 1], [1, 6, 4, 6, 4, 6, 1], [1, 6, 4, 4, 4, 6, 1], [1, 6, 6, 4, 6, 6, 1], [1, 6, 6, 6, 6, 6, 1], [1, 1, 1, 1, 1, 1, 1]]}, # Transformed output from last run
    {'name': 'train_2', 'type': 'input', 'grid': [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3], [3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3], [3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3], [3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 4, 4, 3], [3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3], [3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3], [3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3], [3, 4, 4, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3], [3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3], [3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 4, 4, 3], [3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 1, 4, 3], [3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3], [3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]},
    {'name': 'train_2', 'type': 'output', 'grid': [[3, 3, 3, 3, 3, 3, 3], [3, 4, 4, 4, 4, 4, 3], [3, 4, 1, 1, 1, 4, 3], [3, 4, 4, 1, 4, 4, 3], [3, 4, 1, 1, 1, 4, 3], [3, 4, 4, 4, 4, 4, 3], [3, 3, 3, 3, 3, 3, 3], [3, 4, 4, 4, 4, 4, 3], [3, 4, 1, 1, 1, 4, 3], [3, 4, 4, 1, 4, 4, 3], [3, 4, 4, 1, 4, 4, 3], [3, 4, 4, 4, 4, 4, 3], [3, 3, 3, 3, 3, 3, 3], [3, 4, 4, 4, 4, 4, 3], [3, 4, 1, 1, 4, 4, 3], [3, 4, 4, 1, 1, 4, 3], [3, 4, 1, 1, 4, 4, 3], [3, 4, 4, 4, 4, 4, 3], [3, 3, 3, 3, 3, 3, 3]]}, # Expected output from prompt
    {'name': 'train_2', 'type': 'transformed', 'grid': [[3, 3, 3, 3, 3, 3, 3], [3, 4, 4, 4, 4, 4, 3], [3, 4, 1, 1, 1, 4, 3], [3, 4, 4, 1, 4, 4, 3], [3, 4, 1, 1, 1, 4, 3], [3, 4, 4, 4, 4, 4, 3], [3, 3, 3, 3, 3, 3, 3], [3, 4, 4, 4, 4, 4, 3], [3, 4, 1, 1, 1, 4, 3], [3, 4, 4, 1, 4, 4, 3], [3, 4, 1, 1, 1, 4, 3], [3, 4, 4, 4, 4, 4, 3], [3, 3, 3, 3, 3, 3, 3], [3, 4, 4, 4, 4, 4, 3], [3, 4, 1, 1, 1, 4, 3], [3, 4, 4, 1, 4, 4, 3], [3, 4, 1, 1, 1, 4, 3], [3, 4, 4, 4, 4, 4, 3], [3, 3, 3, 3, 3, 3, 3]]} # Transformed output from last run
]

# --- Analysis Functions ---
def find_grid_parameters(np_grid: np.ndarray) -> tuple[int, int, int, int, int]:
    # (Using the same robust find_grid_parameters from the previous Python code block)
    input_height, input_width = np_grid.shape
    separator_color = int(np_grid[0, 0])
    h = -1
    for r in range(1, input_height):
        if np.all(np_grid[r, :] == separator_color):
            h = r - 1; break
    if h == -1: h = input_height - 2 if input_height > 1 else 0
    w = -1
    for c in range(1, input_width):
         if np.all(np_grid[:, c] == separator_color):
            w = c - 1; break
    if w == -1: w = input_width - 2 if input_width > 1 else 0
    if h <= 0 or w <= 0: raise ValueError(f"Invalid block dims H={h}, W={w}")
    r_blocks = (input_height - 1) // (h + 1) if (input_height - 1) % (h + 1) == 0 else (1 if input_height == h + 2 else 0)
    c_blocks = (input_width - 1) // (w + 1) if (input_width - 1) % (w + 1) == 0 else (1 if input_width == w + 2 else 0)
    if r_blocks <= 0 or c_blocks <= 0: raise ValueError(f"Invalid block counts R={r_blocks}, C={c_blocks}")
    if input_height != r_blocks * h + (r_blocks + 1) or input_width != c_blocks * w + (c_blocks + 1):
         raise ValueError(f"Grid dim mismatch Ht={input_height}, Wd={input_width} vs R={r_blocks},C={c_blocks},H={h},W={w}")
    return separator_color, h, w, r_blocks, c_blocks

def extract_patterns_and_details(np_grid: np.ndarray, h: int, w: int, r_blocks: int, c_blocks: int) -> list[dict]:
    # (Using the same extract_patterns_and_details from the previous Python code block)
    patterns_data = {}
    for r in range(r_blocks):
        for c in range(c_blocks):
            start_row = r * (h + 1) + 1; start_col = c * (w + 1) + 1
            pattern_np = np_grid[start_row : start_row + h, start_col : start_col + w]
            pattern_tuple = pattern_to_tuple(pattern_np)
            current_pos = (r, c)
            if pattern_tuple not in patterns_data:
                patterns_data[pattern_tuple] = {'pattern': pattern_tuple,'count': 0,'positions': [],'first_pos': current_pos}
            patterns_data[pattern_tuple]['count'] += 1
            patterns_data[pattern_tuple]['positions'].append(current_pos)
    return list(patterns_data.values())

def select_target_pattern(patterns_details: list[dict]) -> tuple[tuple[int]]:
     # (Using the same select_target_pattern from the previous Python code block)
    unique_patterns = [p for p in patterns_details if p['count'] == 1]
    if unique_patterns:
        unique_patterns.sort(key=lambda p: p['first_pos'])
        return unique_patterns[0]['pattern']
    else:
        if not patterns_details: raise ValueError("No patterns found.")
        max_count = max(p['count'] for p in patterns_details)
        most_common_patterns = [p for p in patterns_details if p['count'] == max_count]
        most_common_patterns.sort(key=lambda p: p['first_pos'])
        return most_common_patterns[0]['pattern']

# --- Run Analysis ---
analysis_results = []

for example_name in ['train_1', 'train_2']:
    input_data = next(item for item in train_examples_data if item['name'] == example_name and item['type'] == 'input')
    output_data = next(item for item in train_examples_data if item['name'] == example_name and item['type'] == 'output')
    transformed_data = next(item for item in train_examples_data if item['name'] == example_name and item['type'] == 'transformed')

    input_grid = input_data['grid']
    expected_output_grid = output_data['grid']
    transformed_output_grid = transformed_data['grid']

    input_np = to_np(input_grid)
    expected_np = to_np(expected_output_grid)
    transformed_np = to_np(transformed_output_grid)

    # Basic Metrics
    example_analysis = {
        'name': example_name,
        'transform_matches_expected': np.array_equal(expected_np, transformed_np),
    }

    # Pattern Analysis
    try:
        sep, h, w, r, c = find_grid_parameters(input_np)
        example_analysis['grid_params'] = {'H': h, 'W': w, 'R': r, 'C': c, 'sep': sep}
        patterns_details = extract_patterns_and_details(input_np, h, w, r, c)

        # Summarize pattern counts
        counts_summary = collections.Counter(p['count'] for p in patterns_details)
        example_analysis['pattern_counts_summary'] = dict(counts_summary)
        example_analysis['unique_patterns_count'] = counts_summary.get(1, 0)

        # Identify unique patterns and their first positions
        unique_patterns_info = sorted(
            [{'pattern': p['pattern'], 'first_pos': p['first_pos']} for p in patterns_details if p['count'] == 1],
            key=lambda x: x['first_pos']
        )
        example_analysis['unique_patterns_info'] = unique_patterns_info

        # Identify most common patterns and their first positions
        if patterns_details:
            max_count = max(p['count'] for p in patterns_details)
            most_common_info = sorted(
                [{'pattern': p['pattern'], 'first_pos': p['first_pos'], 'count':p['count']} for p in patterns_details if p['count'] == max_count],
                key=lambda x: x['first_pos']
            )
            example_analysis['most_common_patterns_info'] = most_common_info
        else:
             example_analysis['most_common_patterns_info'] = []


        # Determine the pattern selected by the code's logic
        selected_pattern_by_code = select_target_pattern(patterns_details)
        example_analysis['pattern_selected_by_code'] = selected_pattern_by_code
        # Find info about the selected pattern
        selected_pattern_details = next((p for p in patterns_details if p['pattern'] == selected_pattern_by_code), None)
        example_analysis['code_selected_pattern_details'] = selected_pattern_details


        # Determine the pattern used in the *first block* of the expected output
        expected_output_pattern_np = expected_np[1:1+h, 1:1+w]
        expected_pattern_tuple = pattern_to_tuple(expected_output_pattern_np)
        example_analysis['expected_output_first_pattern'] = expected_pattern_tuple
         # Find info about this expected pattern in the input
        expected_pattern_details = next((p for p in patterns_details if p['pattern'] == expected_pattern_tuple), None)
        example_analysis['expected_pattern_details_in_input'] = expected_pattern_details


    except Exception as e:
        example_analysis['error'] = str(e)

    # Convert numpy types before storing
    analysis_results.append(convert_np_types(example_analysis))

# Print Analysis
print(json.dumps(analysis_results, indent=2))