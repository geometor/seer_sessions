
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
1 5 5
2 1 5
5 5 1
```
size: False
palette: False
color count: False
pixels off: None
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
5 1 2
1 1 5
2 5 5
```
size: False
palette: False
color count: False
pixels off: None
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
2 1 2
5 2 1
2 1 5
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**
