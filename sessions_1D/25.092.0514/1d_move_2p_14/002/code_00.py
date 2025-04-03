import numpy as np

def get_block_info(row):
    """Helper to find block details."""
    start = -1
    end = -1
    color = 0
    length = 0
    in_block = False
    for i, pixel in enumerate(row):
        if pixel != 0:
            if not in_block:
                start = i
                color = pixel
                in_block = True
            if in_block and pixel == color:
                 end = i # Keep updating end index
            else: # Different non-zero color or end of block
                 if in_block:
                      break
        elif in_block: # pixel is 0 and we were in block
            break
    if start != -1:
        length = end - start + 1
    return color, start, end, length

examples = [
    {
        "input": [[0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0]]
    },
    {
        "input": [[0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0]]
    }
]

metrics = []
for i, ex in enumerate(examples):
    input_grid = np.array(ex["input"])
    output_grid = np.array(ex["output"])

    input_row = input_grid[0]
    output_row = output_grid[0]

    in_color, in_start, in_end, in_len = get_block_info(input_row)
    out_color, out_start, out_end, out_len = get_block_info(output_row)

    metrics.append({
        "example": i + 1,
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "input_block": {"color": in_color, "start": in_start, "end": in_end, "length": in_len},
        "output_block": {"color": out_color, "start": out_start, "end": out_end, "length": out_len},
        "shift": out_start - in_start if in_start != -1 and out_start != -1 else "N/A"
    })

print(metrics)