import numpy as np

train_examples = [
    {
        "input": np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 9, 0, 0, 0, 0, 0, 0, 0]),
        "output": np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 1, 1, 1, 1, 0, 0]),
    },
    {
        "input": np.array([0, 0, 0, 4, 4, 4, 4, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0]),
        "output": np.array([0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 4, 4, 4, 4, 0, 0, 0]),
    },
    {
        "input": np.array([2, 2, 2, 2, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        "output": np.array([0, 0, 0, 0, 0, 0, 9, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0]),
    },
]

results = []
for i, example in enumerate(train_examples):
    inp = example["input"]
    outp = example["output"]
    
    n = len(inp)
    pivot_indices = np.where(inp == 9)[0]
    pivot_index = pivot_indices[0] if len(pivot_indices) == 1 else -1

    segment_indices = np.where((inp != 0) & (inp != 9))[0]
    segment_color = -1
    segment_start = -1
    segment_length = 0
    distance = -1
    new_segment_start = -1

    if len(segment_indices) > 0:
        segment_color = inp[segment_indices[0]]
        # Check for contiguity
        if np.all(np.diff(segment_indices) == 1):
            segment_start = segment_indices[0]
            segment_length = len(segment_indices)
            segment_end = segment_start + segment_length - 1

            # Calculate distance
            if segment_end < pivot_index: # Left
                distance = np.sum(inp[segment_end + 1 : pivot_index] == 0)
                new_segment_start = pivot_index + distance + 1
            elif segment_start > pivot_index: # Right
                distance = np.sum(inp[pivot_index + 1 : segment_start] == 0)
                new_segment_start = pivot_index - distance - segment_length
            else: # Should not happen in examples
                 distance = 0 

    results.append({
        "example": i + 1,
        "length": n,
        "pivot_index": pivot_index,
        "segment_color": segment_color,
        "segment_start": segment_start,
        "segment_length": segment_length,
        "distance_from_pivot": distance,
        "original_side": "left" if segment_start < pivot_index else ("right" if segment_start > pivot_index else "N/A"),
        "calculated_new_start": new_segment_start,
        "expected_output_segment_start": np.where((outp != 0) & (outp != 9))[0][0] if len(np.where((outp != 0) & (outp != 9))[0]) > 0 else -1
    })

print(results)
