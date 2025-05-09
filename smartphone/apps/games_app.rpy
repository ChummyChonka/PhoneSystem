
screen tictactoe():
    style_prefix "smartphone"
    text "TicTacToe" at phone_title
    vbox:
        xalign 0.5
        yalign 0.2
        hbox:
            spacing 20
            text "Winner:"
            if(tictactoe.winner == 1):
                text "X"
            elif(tictactoe.winner == 2):
                text "O"
            else:
                text "-"

    grid 3 3:
        xalign 0.5
        yalign 0.4
        spacing 20
        $ counter = 0
        for field in tictactoe.game:
            if(field == 0):
                if(tictactoe.winner == 0):
                    imagebutton:
                        auto "images/smartphone/games/tictactoe_empty_%s.webp" at iconzoom
                        #action [Function(set_tictactoe, counter), Function(check_tictactoe_winner_no_return), Function(tictactoe_ai)]
                        action [Function(set_tictactoe, counter), Function(tictactoe_ai)]
                else:
                    imagebutton:
                        idle "images/smartphone/games/tictactoe_empty_idle.webp" at iconzoom
                        action NullAction()
            elif(field == 1):
                imagebutton:
                    auto "images/smartphone/games/tictactoe_cross_%s.webp" at iconzoom
                    action NullAction()
            elif(field == 2):
                imagebutton:
                    auto "images/smartphone/games/tictactoe_circle_%s.webp" at iconzoom
                    action NullAction()
            $ counter += 1
    text "[tictactoe.game]"
    textbutton("Reset"):
        xalign 0.5
        yalign 0.8
        action Function(reset_tictactoe)


screen games():
    style_prefix "smartphone"
    text "Games" at phone_title
    vbox at phone_content:
        hbox:
            textbutton("TicTacToe") action Function(smartphone_screen_push, "tictactoe") #action [Hide("games"), Show("tictactoe")]

