notmember(A, [B | C ]) :- \+ (A = B), C = [], !.
notmember(A, [B | T]):- \+ (A = B), notmember(A, T), !.
