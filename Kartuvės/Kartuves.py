
#i a s t o e n r k u m l p d v g j ė b y š ų ž ą į ū č c ę z f h
import  PySimpleGUI as gui
import os, random
#--------------------------------------------------------užkrauna nuotrauka(karimo eiga)
def LoadPick(Stage):
    pickname = os.getcwd()
    window['STAGE'].update(f'{pickname}\KarimoEiga\{Stage}.png')

#--------------------------------------------------------išrenka atsitiktinį žodį iš žodžių sąrašo
def GetWord():
    with open('Words.txt', 'r', encoding='utf-8') as R:
            zodziai = R.read().splitlines()
            R.close()     
    return str(zodziai[random.randint(0,len(zodziai)-1)]).upper()

#--------------------------------------------------------sudeda tarpelius tarp raidžių ir juos atvaizduoja
def ConvertAndDisplayWord(zodis, key):
    str = ""  
    for raide in zodis: 
        str += f'{raide}  ' 
    window[key].update(str)

#--------------------------------------------------------patikrina, jei žodyje nebėra "_" ženklo parneša, kad žodis atspėtas 
def IsCompleated(zodis):
    for char in zodis:
        if char == '_':
            return False
    return True

#--------------------------------------------------------patikrina ar raidė jau spėta
def ArJauSpetaRaide(Raide):
    for speta in spetos_raides:
        if Raide == speta:
            return True
    spetos_raides.append(Raide)
    ConvertAndDisplayWord(spetos_raides, 'GUESSEDLETTERS')
    return False
#--------------------------------------------------------viską išvalo ir perkrauna iš naujo
def Reset():
    window['SUBMITKEY'].update(disabled=False)
    window['SCREENWORD'].update(text_color='white')
    zodis = GetWord()
    pasleptaszodis = list()
    for num in range(len(zodis)):
        pasleptaszodis.append('_')
    spetos_raides = []
    spejimai = 1
    ConvertAndDisplayWord(pasleptaszodis, 'SCREENWORD')
    ConvertAndDisplayWord(spetos_raides, 'GUESSEDLETTERS')
    return zodis, pasleptaszodis, spetos_raides, spejimai
#--------------------------------------------------------
gui.theme('DarkTeal9')
menu_def=['&Settings', ['Reset', 'Solve']], ['&Kartuves']
layout = [[gui.Menu(menu_def, pad=(10,10), disabled_text_color='red')],
         [gui.Image('', key='STAGE', size=(119, 127))],
         [gui.Text('', justification='center', key='SCREENWORD', size=(25, 1))],
         [gui.Input('', key='INPUT', size=(2,2)), gui.Button('Submit', key='SUBMITKEY', disabled=True)],
         [gui.Text('', justification='center', key='GUESSEDLETTERS', size=(40, 1))],
         [gui.Button('Start/Reset', key='STARTRESET', pad=(3,0))]]
#----Main
window = gui.Window('Kartuves', layout, element_justification='c', grab_anywhere=True)
spetos_raides = []
spejimai = 1

while True:
    event, values = window.read(timeout=1)
    
    if spejimai <= 8:
        LoadPick(spejimai)
    elif spejimai == 99:
        LoadPick('WIN')
    else:
        LoadPick('LOST')
        window['SUBMITKEY'].update(disabled=True)
        ConvertAndDisplayWord(zodis, 'SCREENWORD')
        window['SCREENWORD'].update(text_color='red')
   
    if event == 'SUBMITKEY':
        if str(values['INPUT']).isdigit() == False and str(values['INPUT']).isalpha() == True:
            spejimas = str(values['INPUT']).upper()
            if ArJauSpetaRaide(spejimas) == False: 
                ArYra = False
                for pl in range(len(zodis)):
                    if zodis[pl] == spejimas: 
                        ArYra = True
                        pasleptaszodis[pl] = spejimas
                ConvertAndDisplayWord(pasleptaszodis, 'SCREENWORD')
                if ArYra == False:
                    spejimai += 1
                if IsCompleated(pasleptaszodis) == True:
                    spejimai = 99
                    window['SUBMITKEY'].update(disabled=True)
                    window['SCREENWORD'].update(text_color='green')                  
        window.Element('INPUT').Update('')

    if event == 'STARTRESET':
        zodis, pasleptaszodis, spetos_raides, spejimai = Reset()
        
    if len(values['INPUT']) > 1:
        window.Element('INPUT').Update(values['INPUT'][:-1])

    if event == 'Solve':
        ConvertAndDisplayWord(zodis, 'SCREENWORD')
        window['SCREENWORD'].update(text_color='yellow')
        window['SUBMITKEY'].update(disabled=True)

    if event == 'Reset':
        zodis, pasleptaszodis, spetos_raides, spejimai = Reset()
    if event in (gui.WINDOW_CLOSED, 'Exit'):
        break

window.close()
#--------------------------------------------------------