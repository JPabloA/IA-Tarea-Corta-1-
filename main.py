from PegSolitaire import PegSolitaire

game = PegSolitaire()

# print(game.GetObjetiveMatrix())
# print(game.GetGameDictionary())
game.PrintGame()

game.MakeMove(3, 1, 3, 3)
game.PrintGame()

game.MakeMove(5, 2, 3, 2)
game.PrintGame()

game.MakeMove(5, 4, 5, 2)
game.PrintGame()

game.MakeMove(2, 6, 3, 1)
game.PrintGame()

print(game.GameDictToMatrix())