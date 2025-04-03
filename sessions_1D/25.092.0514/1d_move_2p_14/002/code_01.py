import numpy as np
import json

# Function to convert numpy types to standard Python types for JSON serialization
def convert_numpy_types(obj):
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                        np.int16, np.int32, np.int64, np.uint8,
                        np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float_, np.float16, np.float32,
                          np.float64)):
        return float(obj)
    elif isinstance(obj, (np.ndarray,)): # arrays get converted to lists
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(i) for i in obj]
    return obj


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
            # Ensure we only extend if it's the *same* non-zero color
            if in_block and pixel == color:
                 end = i # Keep updating end index
            elif in_block: # Different non-zero color or zero after block
                 break # Block ends if color changes or hits zero
        elif in_block: # pixel is 0 and we were in block
            break
    if start != -1:
        length = end - start + 1
    # Ensure returned values are standard Python types
    return int(color), int(start) if start != -1 else -1, int(end) if end != -1 else -1, int(length)

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
    # Use np.array to simulate the potential environment behavior
    input_grid = np.array(ex["input"])
    output_grid = np.array(ex["output"])

    # Assuming single row inputs based on observation
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

# Convert numpy types before printing
metrics_serializable = convert_numpy_types(metrics)
print(json.dumps(metrics_serializable, indent=2))