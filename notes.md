board = board_rsconnect()
board.pin("hadley/sales").write(my_object)
# shortcut?
board["hadley/sales"]
pin = board.pin("hadley/sales")
pin.read()
pin.meta()
board.search("sales")[0].read()
