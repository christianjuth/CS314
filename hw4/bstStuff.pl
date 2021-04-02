bst(L, V, R).
is_bst(B) :- B = bst(L, V, R), (L = nil; is_bst(L); number(L), L < V), (R = nil; is_bst(R); number(R), R > V).
get_min(B, X) :- B = bst(L, V, R), X = L.
get_max(B, X) :- X = R, B = bst(L, V, R).
