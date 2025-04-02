# Prepare data in list format for analysis
train_data = [
    {
        "input": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 6, 0, 0, 0],
        "output": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 6, 0, 0, 0]
    },
    {
        "input": [0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 6, 0, 0, 0],
        "output": [0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 0, 0, 0]
    },
    {
        "input": [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 6, 0, 0],
        "output": [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 0, 0]
    }
]

results = []
for i, example in enumerate(train_data):
    inp = example["input"]
    outp = example["output"]
    marker_idx = -1
    try:
        marker_idx = inp.index(6)
    except ValueError:
        pass

    block_end_idx = -1
    fill_color = -1
    for j in range(marker_idx - 1, -1, -1):
        if inp[j] != 0:
            block_end_idx = j
            fill_color = inp[j]
            break
            
    gap_start_idx = block_end_idx + 1 if block_end_idx != -1 else -1
    gap_end_idx = marker_idx
    gap_len = max(0, gap_end_idx - gap_start_idx) if marker_idx != -1 and block_end_idx != -1 else 0
    
    num_filled = 0
    if gap_len > 0:
        for k in range(gap_start_idx, gap_end_idx):
            if inp[k] == 0 and outp[k] == fill_color:
                 num_filled += 1


    results.append({
        "example": i + 1,
        "input_len": len(inp),
        "output_len": len(outp),
        "marker_index": marker_idx,
        "fill_color": fill_color,
        "block_end_index": block_end_idx,
        "gap_start_index": gap_start_idx,
        "gap_end_index": gap_end_idx,
        "gap_length": gap_len,
        "white_pixels_in_gap": sum(1 for k in range(gap_start_idx, gap_end_idx) if inp[k] == 0) if gap_len > 0 else 0,
        "num_pixels_filled": num_filled
    })

print(results)