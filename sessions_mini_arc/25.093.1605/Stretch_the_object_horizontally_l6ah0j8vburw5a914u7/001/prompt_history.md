
## train_1

**input:**
```
0 0 0 0 0
0 3 3 3 0
0 3 3 3 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
3 3 3 3 3
3 3 3 3 3
0 0 0 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0
0 3 0 3 0
0 3 3 3 0
0 3 0 3 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
3 0 0 0 3
3 3 3 3 3
3 0 0 0 3
0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0
0 3 0 0 0
0 3 3 0 0
0 3 3 3 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
3 0 0 0 0
3 3 3 3 0
3 3 3 3 3
0 0 0 0 0
```

Okay, analyzing the provided input-output pairs to understand the transformation logic.

## Perception

1.  **Grid Structure:** The input and output are both 2D grids of the same dimensions (5x5 in the examples).
2.  **Cell Values:** The cells contain integer values, primarily '0' and '3'. The value '3' appears to be the active element being manipulated, while '0' represents the background.
3.  **Transformation Scope:** The transformation operates independently on each row. Rows containing only '0's in the input remain unchanged in the output.
4.  **Row-wise Logic:** For rows containing at least one '3', a specific transformation is applied to generate the corresponding output row.
5.  **Key Features:** The transformation seems dependent on the positions (indices) of the '3's within the input row, specifically the first ('leftmost') and last ('rightmost') occurrences. The *contiguity* of the '3's in the input row also appears crucial.
6.  **Output Pattern:** The output rows generated from active input rows always start with a '3' at index 0. The subsequent '3's in the output row depend on the configuration of '3's in the input row.
    *   If the input row has only one '3', the output row has a '3' only at index 0.
    *   If the input row has multiple, non-contiguous '3's, the output row seems to have a '3' at index 0 and another '3' at an index calculated from the positions of the first and last '3's in the input.
    *   If the input row has multiple, contiguous '3's, the output row appears to be filled with '3's from index 0 up to a calculated index.

## Facts


