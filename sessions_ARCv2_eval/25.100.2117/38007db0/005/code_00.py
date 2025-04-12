import numpy as np

# --- Data for train_1 ---
input_grid_1 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1],
[1, 6, 4, 6, 6, 6, 1, 6, 4, 6, 6, 6, 1, 6, 4, 6, 4, 6, 1],
[1, 6, 4, 4, 4, 6, 1, 6, 4, 4, 4, 6, 1, 6, 4, 4, 4, 6, 1],
[1, 6, 6, 4, 6, 6, 1, 6, 6, 4, 6, 6, 1, 6, 6, 4, 6, 6, 1],
[1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1],
[1, 6, 4, 6, 6, 6, 1, 6, 4, 6, 6, 6, 1, 6, 4, 6, 6, 6, 1],
[1, 6, 4, 4, 6, 6, 1, 6, 4, 4, 4, 6, 1, 6, 4, 4, 4, 6, 1],
[1, 6, 6, 4, 6, 6, 1, 6, 6, 4, 6, 6, 1, 6, 6, 4, 6, 6, 1],
[1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1],
[1, 6, 4, 6, 6, 6, 1, 6, 4, 6, 6, 6, 1, 6, 4, 6, 6, 6, 1],
[1, 6, 4, 4, 4, 6, 1, 6, 4, 4, 4, 6, 1, 6, 4, 4, 4, 6, 1],
[1, 6, 6, 4, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 4, 6, 6, 1],
[1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
output_grid_1 = [
[1, 1, 1, 1, 1, 1, 1],
[1, 6, 6, 6, 6, 6, 1],
[1, 6, 4, 6, 4, 6, 1],
[1, 6, 4, 4, 4, 6, 1],
[1, 6, 6, 4, 6, 6, 1],
[1, 6, 6, 6, 6, 6, 1],
[1, 1, 1, 1, 1, 1, 1], # Row 6 (overlap row)
[1, 6, 6, 6, 6, 6, 1], # Row 7 (Start of Block2[1:,:])
[1, 6, 4, 6, 6, 6, 1],
[1, 6, 4, 4, 6, 6, 1],
[1, 6, 6, 4, 6, 6, 1],
[1, 6, 6, 6, 6, 6, 1],
[1, 1, 1, 1, 1, 1, 1], # Row 12 (overlap row)
[1, 6, 6, 6, 6, 6, 1], # Row 13 (Start of Block3[1:,:])
[1, 6, 4, 6, 6, 6, 1],
[1, 6, 4, 4, 4, 6, 1],
[1, 6, 6, 6, 6, 6, 1],
[1, 6, 6, 6, 6, 6, 1],
[1, 1, 1, 1, 1, 1, 1]  # Row 18
]

# --- Data for train_2 ---
input_grid_2 = [
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
[3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3],
[3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3],
[3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3],
[3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 4, 4, 3],
[3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3],
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], # Row 6
[3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3],
[3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3],
[3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3],
[3, 4, 4, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3],
[3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3],
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], # Row 12
[3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3],
[3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 1, 4, 3, 4, 1, 1, 4, 4, 3],
[3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 4, 4, 3, 4, 4, 1, 1, 4, 3],
[3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3, 4, 1, 1, 4, 4, 3],
[3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3],
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3] # Row 18
]
output_grid_2 = [
[3, 3, 3, 3, 3, 3, 3],
[3, 4, 4, 4, 4, 4, 3],
[3, 4, 1, 1, 1, 4, 3],
[3, 4, 4, 1, 4, 4, 3],
[3, 4, 1, 1, 1, 4, 3],
[3, 4, 4, 4, 4, 4, 3],
[3, 3, 3, 3, 3, 3, 3], # Row 6 (overlap row)
[3, 4, 4, 4, 4, 4, 3], # Row 7 (Start of Block2[1:,:])
[3, 4, 1, 1, 1, 4, 3],
[3, 4, 4, 1, 4, 4, 3],
[3, 4, 4, 1, 4, 4, 3],
[3, 4, 4, 4, 4, 4, 3],
[3, 3, 3, 3, 3, 3, 3], # Row 12 (overlap row)
[3, 4, 4, 4, 4, 4, 3], # Row 13 (Start of Block3[1:,:])
[3, 4, 1, 1, 4, 4, 3],
[3, 4, 4, 1, 1, 4, 3],
[3, 4, 1, 1, 4, 4, 3],
[3, 4, 4, 4, 4, 4, 3],
[3, 3, 3, 3, 3, 3, 3]  # Row 18
]

def get_metrics_and_verify(input_grid, output_grid, example_name):
    print(f"--- Metrics for {example_name} ---")
    input_array = np.array(input_grid, dtype=int)
    output_array = np.array(output_grid, dtype=int)
    height, width = input_array.shape
    output_height, output_width = output_array.shape

    if height == 0 or width == 0:
        print("Empty input grid.")
        return None

    sep_value = input_array[0, 0]
    sep_rows = [i for i in range(height) if np.all(input_array[i, :] == sep_value)]
    sep_cols = [j for j in range(width) if np.all(input_array[:, j] == sep_value)]

    if len(sep_rows) < 2 or len(sep_cols) < 2:
        print("Insufficient separators found.")
        return None

    num_block_rows = len(sep_rows) - 1
    num_block_cols = len(sep_cols) - 1
    N = num_block_cols

    if num_block_rows < 3:
        print(f"Requires M>=3, found M={num_block_rows}")
        return None

    # Calculate C3
    if N % 2 == 0: C3 = N - 1
    else: C3 = N - 2

    # Indices to select
    indices = [(0, 2), (1, 0), (2, C3)]
    r1, c1 = indices[0]
    r2, c2 = indices[1]
    r3, c3 = indices[2] # Renamed local var to c3_val to avoid confusion

    # Validate indices
    valid_indices = (0 <= c1 < N and 0 <= c2 < N and 0 <= c3 < N)
    if not valid_indices:
        print(f"Invalid calculated column index: N={N}, c1={c1}, c2={c2}, c3={c3}")
        return None

    metrics = {
        "input_shape": (height, width),
        "output_shape": (output_height, output_width),
        "separator_value": int(sep_value),
        "separator_rows": sep_rows,
        "separator_cols": sep_cols,
        "num_block_rows (M)": num_block_rows,
        "num_block_cols (N)": N,
        "calculated_C3": c3,
        "selected_block_indices": indices,
    }
    for k, v in metrics.items():
        print(f"{k}: {v}")

    # Extract blocks
    try:
        block1 = input_array[sep_rows[r1]:sep_rows[r1+1]+1, sep_cols[c1]:sep_cols[c1+1]+1]
        block2 = input_array[sep_rows[r2]:sep_rows[r2+1]+1, sep_cols[c2]:sep_cols[c2+1]+1]
        block3 = input_array[sep_rows[r3]:sep_rows[r3+1]+1, sep_cols[c3]:sep_cols[c3+1]+1]
        print(f"Extracted block shapes: {block1.shape}, {block2.shape}, {block3.shape}")
    except IndexError:
        print("Error extracting blocks due to index issues.")
        return metrics # Return collected metrics even if extraction fails

    # Verify overlap hypothesis
    if block1.shape[0] == 0 or block2.shape[0] == 0 or block3.shape[0] == 0:
         print("One or more extracted blocks are empty. Cannot verify overlap.")
         return metrics
         
    block_h = block1.shape[0]
    if block_h <= 1:
        print(f"Block height ({block_h}) is too small for overlap logic.")
        return metrics

    overlap_match_1_2 = np.array_equal(block1[-1,:], block2[0,:])
    overlap_match_2_3 = np.array_equal(block2[-1,:], block3[0,:]) # Not directly used, but check consistency
    
    # Verify output construction
    output_match = True
    expected_rows_b1 = block_h
    expected_rows_b2 = block_h - 1
    expected_rows_b3 = block_h - 1
    
    if output_height != expected_rows_b1 + expected_rows_b2 + expected_rows_b3:
        output_match = False
        print(f"Output height mismatch: Expected {expected_rows_b1 + expected_rows_b2 + expected_rows_b3}, Got {output_height}")
    else:
        # Check content segments
        match_b1 = np.array_equal(output_array[0:expected_rows_b1, :], block1)
        match_b2 = np.array_equal(output_array[expected_rows_b1 : expected_rows_b1+expected_rows_b2, :], block2[1:, :])
        match_b3 = np.array_equal(output_array[expected_rows_b1+expected_rows_b2 : , :], block3[1:, :])
        if not (match_b1 and match_b2 and match_b3):
            output_match = False
            print(f"Content mismatch: B1 OK={match_b1}, B2[1:] OK={match_b2}, B3[1:] OK={match_b3}")

    print(f"Overlap Check (Block1[-1] == Block2[0]): {overlap_match_1_2}")
    print(f"Overlap Check (Block2[-1] == Block3[0]): {overlap_match_2_3}") # Note: This overlap isn't used in construction but might be true
    print(f"Output Construction Verification (Size and Content): {output_match}")

    return metrics


metrics_1 = get_metrics_and_verify(input_grid_1, output_grid_1, "train_1")
print("\n")
metrics_2 = get_metrics_and_verify(input_grid_2, output_grid_2, "train_2")
