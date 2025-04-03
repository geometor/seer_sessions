import numpy as np
import json

# Updated function to convert numpy types to standard Python types for JSON serialization
def convert_numpy_types(obj):
    if isinstance(obj, (np.intc, np.intp, np.int8,
                        np.int16, np.int32, np.int64, np.uint8,
                        np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float16, np.float32, np.float64)): # Use specific float types
        return float(obj)
    elif isinstance(obj, (np.bool_)):
        return bool(obj)
    elif isinstance(obj, (np.void)):
        return None
    elif isinstance(obj, np.ndarray): # Convert arrays to lists
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        # Special handling for tuples like shape (which contain ints)
        if all(isinstance(i, (int, np.integer)) for i in obj):
             return tuple(int(i) for i in obj)
        # General list conversion
        return [convert_numpy_types(i) for i in obj]
    elif obj is None:
        return None
    # Fallback for types not explicitly handled (like standard Python types)
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
            if in_block and pixel == color:
                 end = i
            elif in_block:
                 break
        elif in_block:
            break
    if start != -1:
        length = end - start + 1
    # Ensure returned values are standard Python types using the converter
    return convert_numpy_types(color), int(start) if start != -1 else -1, int(end) if end != -1 else -1, int(length)

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

    # Store shapes as tuples of standard Python ints
    input_shape_py = tuple(int(dim) for dim in input_grid.shape)
    output_shape_py = tuple(int(dim) for dim in output_grid.shape)


    metrics.append({
        "example": i + 1,
        "input_shape": input_shape_py,
        "output_shape": output_shape_py,
        "input_block": {"color": in_color, "start": in_start, "end": in_end, "length": in_len},
        "output_block": {"color": out_color, "start": out_start, "end": out_end, "length": out_len},
        "shift": out_start - in_start if in_start != -1 and out_start != -1 else "N/A"
    })

# No need to call convert_numpy_types on the final list if individual elements were handled
print(json.dumps(metrics, indent=2))