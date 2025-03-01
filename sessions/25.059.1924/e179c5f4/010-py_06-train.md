
## example 1
*input:*
```
0 0
0 0
0 0
0 0
0 0
0 0
0 0
0 0
0 0
1 0
```
*expected output:*
```
8 1
1 8
8 1
1 8
8 1
1 8
8 1
1 8
8 1
1 8
```
*transformed output:*
```
8 8
8 8
8 8
8 8
8 8
8 8
8 8
8 8
0 8
1 0
```
size: True
palette: False
color count: False
pixels off: 11
**FAILED!**

## example 2
*input:*
```
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
1 0 0
```
*expected output:*
```
8 1 8
1 8 8
8 1 8
8 8 1
8 1 8
1 8 8
8 1 8
8 8 1
8 1 8
1 8 8
```
*transformed output:*
```
8 8 8
8 8 8
8 8 8
8 8 8
8 8 8
8 8 8
8 8 8
8 8 8
0 8 8
1 0 8
```
size: True
palette: False
color count: False
pixels off: 11
**FAILED!**

## example 3
*input:*
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
1 0 0 0
```
*expected output:*
```
8 8 8 1
8 8 1 8
8 1 8 8
1 8 8 8
8 1 8 8
8 8 1 8
8 8 8 1
8 8 1 8
8 1 8 8
1 8 8 8
```
*transformed output:*
```
8 8 8 8
8 8 8 8
8 8 8 8
8 8 8 8
8 8 8 8
8 8 8 8
8 8 8 8
8 8 8 8
0 8 8 8
1 0 8 8
```
size: True
palette: False
color count: False
pixels off: 11
**FAILED!**
