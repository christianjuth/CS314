indexList(A, B, [ Car | Cdr ]) :- I is B - 1, indexList(A, I, Cdr), !.
indexList(A, 0, [ A | _ ]):- !.
