import numpy as np
import math

def analyze_example(input_grid):
    input_array = np.array(input_grid, dtype=int)
    unique_colors, counts = np.unique(input_array, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    if not color_counts: return {"error": "Empty input"}
    if len(color_counts) == 1:
        dominant_color = list(color_counts.keys())[0]
        pixel_color = None
        block_colors = {}
    else:
        dominant_color = max(color_counts, key=color_counts.get)
        pixel_color = None
        pixel_candidates = [c for c, n in color_counts.items() if n == 1]
        if pixel_candidates: pixel_color = pixel_candidates[0]
        block_colors = {c: n for c, n in color_counts.items() if c != dominant_color and c != pixel_color and n > 1}

    output_height = len(block_colors) + (1 if pixel_color is not None else 0) + 1
    block_widths = {c: math.floor(math.sqrt(n)) for c, n in block_colors.items()}

    if pixel_color is not None:
        ordered_elements = [pixel_color] + sorted(block_colors.keys(), reverse=True)
    else:
        ordered_elements = sorted(block_colors.keys())

    element_details = []
    current_col = 0
    final_block_color = None
    final_block_col_start = -1
    final_block_width = 0

    elements_to_place = []
    effective_widths = {}
    for el in ordered_elements:
        w = 0
        if el == pixel_color:
            w = 1
        elif el in block_widths:
            w = block_widths[el]
        if w > 0:
            elements_to_place.append(el)
            effective_widths[el] = w

    output_width = 0
    if elements_to_place:
       output_width = sum(effective_widths[el] for el in elements_to_place) + max(0, len(elements_to_place) - 1)


    last_element = elements_to_place[-1] if elements_to_place else None
    last_block_details = None
    temp_col = 0
    for i, el in enumerate(elements_to_place):
        w = effective_widths[el]
        detail = {
            "element_color": el,
            "type": "pixel" if el == pixel_color else "block",
            "width": w,
            "start_col": temp_col
        }
        element_details.append(detail)
        if el == last_element and el != pixel_color: # Check if last element is a block
            last_block_details = detail

        temp_col += w
        if i < len(elements_to_place) - 1:
            temp_col += 1 # Gap


    return {
        "input_shape": input_array.shape,
        "color_counts": {int(k): int(v) for k, v in color_counts.items()}, # Convert numpy types
        "dominant_color": int(dominant_color) if dominant_color is not None else None,
        "pixel_color": int(pixel_color) if pixel_color is not None else None,
        "block_colors": {int(k): int(v) for k, v in block_colors.items()},
        "calculated_output_height": output_height,
        "block_widths": {int(k): int(v) for k, v in block_widths.items()},
        "element_order_initial": [int(el) for el in ordered_elements],
        "elements_to_place": [int(el) for el in elements_to_place],
        "calculated_output_width": output_width,
        "calculated_output_shape": (output_height, output_width),
        "element_placement_details": element_details,
        "last_block_details_for_top_row": last_block_details
    }

example1_input = [
    [4, 4, 4, 4, 4, 7, 7], [4, 7, 7, 7, 4, 7, 5], [4, 7, 1, 7, 4, 7, 5],
    [4, 7, 7, 7, 4, 7, 7], [4, 4, 4, 4, 4, 7, 5], [7, 7, 7, 7, 7, 7, 5],
    [5, 5, 5, 5, 5, 7, 7]
]
example2_input = [
    [9, 9, 9, 9], [7, 7, 9, 7], [9, 9, 9, 9], [7, 7, 7, 7],
    [7, 6, 7, 6], [7, 6, 7, 6], [7, 7, 7, 7]
]

metrics1 = analyze_example(example1_input)
metrics2 = analyze_example(example2_input)

import json
print("--- Example 1 Metrics ---")
print(json.dumps(metrics1, indent=2))
print("\n--- Example 2 Metrics ---")
print(json.dumps(metrics2, indent=2))