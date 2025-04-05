
## train_1

**input:**
```
0 1 1 0 0 2 0 0 1 1 2 0
```


**output:**
```
0 0 0 0 0 0 1 1 1 1 2 2
```


## train_2

**input:**
```
1 0 0 0 0 0 0 2 1 1 1 2
```


**output:**
```
0 0 0 0 0 0 1 1 1 1 2 2
```


## train_3

**input:**
```
0 2 0 1 0 2 0 2 0 1 1 1
```


**output:**
```
0 0 0 0 0 1 1 1 1 2 2 2
```


## train_4

**input:**
```
2 0 1 1 0 1 1 1 2 0 0 0
```


**output:**
```
0 0 0 0 0 1 1 1 1 1 2 2
```


## train_5

**input:**
```
2 0 0 1 0 0 0 2 0 2 0 2
```


**output:**
```
0 0 0 0 0 0 0 1 2 2 2 2
```


## train_6

**input:**
```
1 0 0 2 1 0 0 0 1 1 0 1
```


**output:**
```
0 0 0 0 0 0 1 1 1 1 1 2
```


## train_7

**input:**
```
0 2 0 1 2 1 0 2 0 2 2 0
```


**output:**
```
0 0 0 0 0 1 1 2 2 2 2 2
```

## Perception of Task Elements

The input consists of a sequence of single-digit integers (specifically, 0, 1, and 2). The output is also a sequence of single-digit integers of the same length as the input. Comparing the input and output sequences across multiple examples reveals that the output sequence contains the exact same digits as the input sequence, but they are arranged in non-decreasing (ascending) order. The number of occurrences of each digit (0, 1, 2) is preserved between the input and the output.

## Factual Documentation


```yaml
Observations:
  Input:
    Type: Sequence
    Elements:
      Type: Integer
      Values: [0, 1, 2]
    Structure: Linear array/list
    Length: Constant (12 in examples)
  Output:
    Type: Sequence
    Elements:
      Type: Integer
      Values: [0, 1, 2]
    Structure: Linear array/list
    Length: Same as input
  Relationship:
    - The output sequence contains the same multiset of integers as the input sequence.
    - The output sequence is a sorted version of the input sequence.
    - Sorting order: Ascending (non-decreasing).
Action:
  Name: Sort
  Target: Input sequence
  Order: Ascending (0s first, then 1s, then 2s)
  Result: Output sequence
```


## Natural Language Program

1.  Accept the input sequence of integers.
2.  Sort the elements of the input sequence in ascending numerical order.
3.  Return the sorted sequence as the output.
