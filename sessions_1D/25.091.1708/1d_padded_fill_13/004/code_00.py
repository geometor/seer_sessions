import numpy as np

def parse_grid_string(grid_string):
    try:
        return [int(x) for x in grid_string.split()]
    except ValueError:
        return [] 

def analyze_example(example_num, input_str, output_str):
    input_flat = parse_grid_string(input_str)
    output_flat = parse_grid_string(output_str)

    if not input_flat or not output_flat:
        return {f"Example {example_num} Error": "Empty input or output string"}

    input_len = len(input_flat)
    output_len = len(output_flat)

    if input_len != output_len:
        return {f"Example {example_num} Error": f"Length mismatch: input {input_len}, output {output_len}"}
    if input_len == 0:
         return {f"Example {example_num} Error": "Zero length grid"}

    width = input_len
    height = 1
    input_grid = np.array(input_flat).reshape(height, width)
    output_grid = np.array(output_flat).reshape(height, width)

    input_non_white_pixels = np.sum(input_grid != 0)
    output_non_white_pixels = np.sum(output_grid != 0)
    pixels_filled = np.sum((input_grid == 0) & (output_grid != 0))
    
    marker_colors = set(input_grid[input_grid != 0])
    # Fill color is the color that appears in the output where the input was white
    fill_colors = set(output_grid[(input_grid == 0) & (output_grid != 0)])

    row_in = input_grid[0, :] 
    row_out = output_grid[0,:]
    non_white_indices_in = np.where(row_in != 0)[0]
    
    segments_info = []
    
    colors_present = {}
    for idx in non_white_indices_in:
        color = row_in[idx]
        if color not in colors_present:
            colors_present[color] = []
        colors_present[color].append(idx)
    
    # Check specifically for pairs that *caused* filling
    for color, indices in colors_present.items():
        # Check if there are exactly two markers of this color in the input row
        if len(indices) == 2:
             idx1, idx2 = sorted(indices)
             span_len = idx2 - idx1 + 1
             # Check if the segment between idx1 and idx2 in the output is entirely 'color'
             segment_in_output = row_out[idx1:idx2+1]
             if np.all(segment_in_output == color):
                  # Check if any pixel *within* this segment was actually filled (was 0 in input)
                  segment_in_input = row_in[idx1:idx2+1]
                  if np.any(segment_in_input == 0): # Confirms filling happened
                    segments_info.append({
                        "color": int(color),
                        "marker_indices": [int(idx1), int(idx2)],
                        "span_length": int(span_len)
                    })

    return {
        f"Example {example_num} Metrics": {
            "dimensions": f"{height}x{width}",
            "input_non_white_count": int(input_non_white_pixels),
            "output_non_white_count": int(output_non_white_pixels),
            "pixels_changed_to_non_white": int(pixels_filled),
            "input_marker_colors": sorted([int(c) for c in marker_colors]),
            "fill_colors_used_in_output": sorted([int(c) for c in fill_colors]),
            "num_segments_filled": len(segments_info),
            "segment_details": segments_info # Corrected list
        }
    }

# Example 1
input_1 = "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0"
output_1 = "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0"
metrics_1 = analyze_example(1, input_1, output_1)

# Example 2
input_2 = "0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0"
output_2 = "0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0"
metrics_2 = analyze_example(2, input_2, output_2)

# Example 3
input_3 = "8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
output_3 = "8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
metrics_3 = analyze_example(3, input_3, output_3)

print(metrics_1)
print(metrics_2)
print(metrics_3)
