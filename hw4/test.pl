member(A, [B | C ]) :- \+ (A = B), C = [].
member(A, [B | T]):- \+ (A = B), member(A, T).
