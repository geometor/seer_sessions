
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
0 1 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 2 0 0 1 0 0 0 0
2 2 2 1 1 1 0 0 0
0 2 0 0 1 0 0 0 0
0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 1 0
```
size: True
palette: True
color count: False
pixels off: 21
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
0 0 0 0 1 0 0 2 0
0 0 0 1 1 1 2 2 2
0 0 0 0 1 0 0 2 0
0 1 0 0 1 0 0 0 0
1 1 1 1 1 1 0 0 0
0 1 0 0 1 0 0 0 0
0 2 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 29
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
0 2 0 0 1 0 0 2 0
2 2 2 1 1 1 2 2 2
0 2 0 0 1 0 0 2 0
0 0 0 0 2 0 0 1 0
0 0 0 2 2 2 1 1 1
0 0 0 0 2 0 0 1 0
0 2 0 0 1 0 0 0 0
2 2 2 1 1 1 0 0 0
0 2 0 0 1 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 43
**FAILED!**
