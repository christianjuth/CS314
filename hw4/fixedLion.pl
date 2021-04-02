eats(wolf, lamb).
eats(lamb, grass).
eats(lion, X):-plant(Food),eats(X, Food).
plant(grass).
