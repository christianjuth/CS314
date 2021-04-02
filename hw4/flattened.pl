flattened(List) :- List = [].
flattened([Car | Cdr]) :- \+is_list(Car), flattened(Cdr).
