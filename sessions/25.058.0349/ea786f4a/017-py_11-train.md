
## example 1
*input:*
```
1 1 1
1 0 1
1 1 1
```
*expected output:*
```
0 1 0
1 0 1
0 1 0
```
*transformed output:*
```
5 0 5
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
2 2 2 2 2
2 2 2 2 2
2 2 0 2 2
2 2 2 2 2
2 2 2 2 2
```
*expected output:*
```
0 2 2 2 0
2 0 2 0 2
2 2 0 2 2
2 0 2 0 2
0 2 2 2 0
```
*transformed output:*
```
5 5 0 5 5
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 0 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
```
*expected output:*
```
0 3 3 3 3 3 0
3 0 3 3 3 0 3
3 3 0 3 0 3 3
3 3 3 0 3 3 3
3 3 0 3 0 3 3
3 0 3 3 3 0 3
0 3 3 3 3 3 0
```
*transformed output:*
```
5 5 5 0 5 5 5
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**
