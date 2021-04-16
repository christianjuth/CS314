listMatch([], []).
listMatch([Car1|Cdr1], [Car2|Cdr2]) :- Car1 = Car2, listMatch(Cdr1, Cdr2).

excludeLastItem([_], []).
excludeLastItem([Car1|Cdr1], [Car2|Cdr2]) :- Car1 = Car2, excludeLastItem(Cdr1, Cdr2).

sublistL([A], [A]) :- !.
sublistL(L1, L2) :- ([Car1|Cdr1] = L1, sublistL(Cdr1, L2)); (excludeLastItem(L1, L3), sublistL(L3, L2)); listMatch(L1, L2).
%sublistL(L1, L2) :- (excludeLastItem(L1, L3), sublistL(L3, L2)); listMatch(L1, L2).

