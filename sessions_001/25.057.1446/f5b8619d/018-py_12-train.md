
## example 1
*input:*
```
2 0 0
0 0 0
0 0 2
```
*expected output:*
```
2 0 8 2 0 8
8 0 8 8 0 8
8 0 2 8 0 2
2 0 8 2 0 8
8 0 8 8 0 8
8 0 2 8 0 2
```
*transformed output:*
```
2 0 0 0 0 0
0 2 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 2 0
0 0 0 0 0 2
```
size: True
palette: True
color count: False
pixels off: 24
**FAILED!**

## example 2
*input:*
```
0 5 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
5 0 0 0 0 5
0 0 0 0 0 0
```
*expected output:*
```
8 5 0 0 0 8 8 5 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
5 8 0 0 0 5 5 8 0 0 0 5
8 8 0 0 0 8 8 8 0 0 0 8
8 5 0 0 0 8 8 5 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
5 8 0 0 0 5 5 8 0 0 0 5
8 8 0 0 0 8 8 8 0 0 0 8
```
*transformed output:*
```
0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 75
**FAILED!**

## example 3
*input:*
```
0 4
0 0
```
*expected output:*
```
0 4 0 4
0 8 0 8
0 4 0 4
0 8 0 8
```
*transformed output:*
```
0 0 4 0
0 0 0 4
0 0 0 0
0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 9
**FAILED!**
