
## example 1
*input:*
```
1 0 0
2 1 0
0 0 1
```
*expected output:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0
2 1 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
8 8 8 8 8 8 8 8 8
8 8 8 8 0 8 8 0 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 0 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 0 8 8 0 8 8 8 8
8 8 8 8 8 8 8 8 8
```
size: True
palette: False
color count: False
pixels off: 76
**FAILED!**

## example 2
*input:*
```
0 1 2
1 1 0
2 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 1 2
0 0 0 0 0 0 1 1 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 1 2 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
```
*transformed output:*
```
8 8 8 8 8 8 8 8 8
8 0 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 0 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 8 8 8 0 8 8 0 8
8 8 8 8 8 8 8 8 8
```
size: True
palette: False
color count: False
pixels off: 77
**FAILED!**

## example 3
*input:*
```
2 1 2
0 2 1
2 1 0
```
*expected output:*
```
2 1 2 0 0 0 2 1 2
0 2 1 0 0 0 0 2 1
2 1 0 0 0 0 2 1 0
0 0 0 2 1 2 0 0 0
0 0 0 0 2 1 0 0 0
0 0 0 2 1 0 0 0 0
2 1 2 0 0 0 0 0 0
0 2 1 0 0 0 0 0 0
2 1 0 0 0 0 0 0 0
```
*transformed output:*
```
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 0 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 0 8
8 8 8 8 8 8 8 8 8
```
size: True
palette: False
color count: False
pixels off: 79
**FAILED!**
