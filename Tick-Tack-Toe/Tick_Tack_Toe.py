# W-0.1
import PySimpleGUI as gui

#----------------------------------------------------------------------
def buttonPress(player, place, playTable):
    playTable[int(place)] = str(player)
    if player == 'X':
        window[place].update(player, disabled=True, button_color='blue')
        #window[place].update(disabled=True, button_color='blue')
        player = 'O'
    else:
        window[place].update(player, disabled=True, button_color='red')
        #window[place].update(disabled=True, button_color='red')
        player = 'X'
    return playTable, player

#----------------------------------------------------------------------
def winColoring(keya, keyb, keyc):
    window[str(keya)].update(button_color=('black', 'orange'))
    window[str(keyb)].update(button_color=('black', 'orange'))
    window[str(keyc)].update(button_color=('black', 'orange'))
    highlightthickness=5

#----------------------------------------------------------------------
def winConditions(playTable, Select=True):

    if playTable[0] == playTable[1] == playTable[2] and playTable[0] != '':
        if Select == True:
            winColoring(0, 1, 2)
        return playTable[0]
    if playTable[3] == playTable[4] == playTable[5] and playTable[3] != '':
        if Select == True:
            winColoring(3, 4, 5)
        return playTable[3]
    if playTable[6] == playTable[7] == playTable[8] and playTable[6] != '':
        if Select == True:
            winColoring(6, 7, 8)
        return playTable[6]
    if playTable[0] == playTable[3] == playTable[6] and playTable[0] != '':
        if Select == True:
            winColoring(0, 3, 6)
        return playTable[0]
    if playTable[1] == playTable[4] == playTable[7] and playTable[1] != '':
        if Select == True:
            winColoring(1, 4, 7)
        return playTable[1]
    if playTable[2] == playTable[5] == playTable[8] and playTable[2] != '':
        if Select == True:
            winColoring(2, 5, 8)
        return playTable[2]
    if playTable[0] == playTable[4] == playTable[8] and playTable[0] != '':
        if Select == True:
            winColoring(0, 4, 8)
        return playTable[0]
    if playTable[6] == playTable[4] == playTable[2] and playTable[6] != '':
        if Select == True:
            winColoring(6, 4, 2)
        return playTable[6]
    return None
#----------------------------------------------------------------------
def fullTableCheck(playTable):
    for pl in playTable:
        if pl == '':
            return False
    return True

#----------------------------------------------------------------------
def Reset():
    player = 'X'
    playTable = ['', '', '',
                 '', '', '',
                 '', '', '']
    for nr in range(0,9):
        window[str(nr)].update(' ', disabled=False, button_color=gui.theme_input_background_color())
    return player, playTable
#----------------------------------------------------------------------
def checkWiningPos(playTable, player):
    for i in range(0,9):
        tempTable = playTable.copy()
        if tempTable[i] == '':
            tempTable[i] = player
            if winConditions(tempTable, Select=False) == player:
               return i
    return None
        
#----------------------------------------------------------------------
def AiPosition(playTable):

    if checkWiningPos(playTable, 'O') != None:
        return checkWiningPos(playTable, 'O')
    if checkWiningPos(playTable, 'X') != None:
        return checkWiningPos(playTable, 'X') 
    
    if playTable[4] == '':
        return 4
    if playTable[0] == '':
        return 0
    if playTable[8] == '':
        return 8
    if playTable[6] == '':
        return 6
    if playTable[2] == '':
        return 2
    #-
    if playTable[1] == '':
        return 1
    if playTable[5] == '':
        return 5
    if playTable[7] == '':
        return 7
    if playTable[3] == '':
        return 3
#----------------------------------------------------------------------
gui.theme('DarkTeal9')
menu_def=['&Nustatymai', ['Reset']], ['&VS', ['Player VS AI', 'Player VS Player']]
layout = [[gui.Menu(menu_def, pad=(10,10), disabled_text_color='red')],
         [gui.Text('               X', size=(16,1), key='PLAYER')],
         [gui.Button(' ', size=(5,3), key='0'), gui.Button(' ', size=(5,3), key='1'), gui.Button(' ', size=(5,3), key='2')],
         [gui.Button(' ', size=(5,3), key='3'), gui.Button(' ', size=(5,3), key='4'), gui.Button(' ', size=(5,3), key='5')],
         [gui.Button(' ', size=(5,3), key='6'), gui.Button(' ', size=(5,3), key='7'), gui.Button(' ', size=(5,3), key='8')],
         [gui.Text('    Player VS Player', size=(16,1), key='VSWHO')]]

window = gui.Window('Tick-Tack-Toe', layout, element_justification='c')

playTable = ['', '', '',
             '', '', '',
             '', '', '']
player = 'X'
aiplays = False

while True:
    event, values = window.read(timeout=1)
    
    if aiplays == True and player == 'O':     
        playTable, player = buttonPress('O', str(AiPosition(playTable)), playTable)
    if event == '0':
        playTable, player = buttonPress(player, '0', playTable)
    if event == '1':
        playTable, player = buttonPress(player, '1', playTable)
    if event == '2':
        playTable, player = buttonPress(player, '2', playTable)
    if event == '3':
        playTable, player = buttonPress(player, '3', playTable)
    if event == '4':
        playTable, player = buttonPress(player, '4', playTable)
    if event == '5':
        playTable, player = buttonPress(player, '5', playTable)
    if event == '6':
        playTable, player = buttonPress(player, '6', playTable)
    if event == '7':
        playTable, player = buttonPress(player, '7', playTable)
    if event == '8':
        playTable, player = buttonPress(player, '8', playTable)

    if event == 'Reset':
        player, playTable = Reset()
    if event == 'Player VS AI':
        window['VSWHO'].update('      Player VS AI')
        aiplays = True
        player, playTable = Reset()  
    if event == 'Player VS Player':
        window['VSWHO'].update('    Player VS Player')
        aiplays = False
        player, playTable = Reset()
    window['PLAYER'].update(f'               {player}')

    if winConditions(playTable) != None:
       gui.popup(f'{winConditions(playTable)} laimejo!', title='Laimejo', location = (window.CurrentLocation()[0]+200, window.CurrentLocation()[1]+70))
       player, playTable = Reset()
    if fullTableCheck(playTable) == True:
       gui.popup(f'Lygiosios!', title='Laimejo', location = (window.CurrentLocation()[0]+200, window.CurrentLocation()[1]+70))
       player, playTable = Reset()

    if event in (gui.WINDOW_CLOSED, 'Exit'):
        break
    
window.close()
#----------------------------------------------------------------------

