bst(L, V, R).
is_bst(B) :- B = bst(L, V, R), (L = nil; is_bst(L); number(L), L < V), (R = nil; is_bst(R); number(R), R > V), !.
get_min(B, X) :- B = bst(L, V, R), ((L = nil, X = V); (number(L), X = L); (get_min(L, X))), !.
get_max(B, X) :- B = bst(L, V, R), ((R = nil, X = V); (number(R), X = R); (get_max(R, X))), !.
