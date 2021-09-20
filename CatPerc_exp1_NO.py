#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Puzzle of Danish Categorical Perception Experiment 1 Norwegian
# Byurakn Ishkhanyan & Kristian Tylén
# AU 2018

# import modules
from psychopy import visual, core, event, gui, data, sound
import numpy as np
import re
import glob, random, ppc
import time, sys
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf-8')
print u"æåø"


# gui requesting participant info
participant_id = gui.Dlg(title='Categorical Perception') 
participant_id.addText('Subject Info')
participant_id.addField('ID: ')
#participant_id.addField('Age: ')
#participant_id.addField('Gender: ', choices = ['female', 'male', 'other'])
participant_id.show()

#saves data from dialogue box into the variable 'ID'
if participant_id.OK:
    ID = participant_id.data 

# number of repetitions
SESSION = 1

# instructions
intro1 = '''
Velkommen til forsøket.

Du kommer snart til å høre noen varianter av setninger med «Hun har sendt…» eller «Hun har tent…». 

Du skal ta stilling til om du hører «sendt» eller «tent» og klikke på det matchende ordet på skjermen.

Du kan bruke informasjonen i setningene som hjelp. Noen setninger gir mening, andre setninger gjør ikke.

Trykk på mellomromstasten for å begynne.


'''


intro2 = '''
Til å begynne med vil du høre noen setninger som en øvelse.

Husk å klikke i midten av ordet.

Trykk på mellomromstasten for å høre den. 
'''

intro3 = '''
Nå vil du høre flere lignende setninger.

Du skal reagere på den samme måten.

Husk å klikke i midten av ordet.

Trykk på mellomromstasten når du er klar til å begynne.

'''

outro = '''
Forsøket er nå slutt.

Takk for din deltakelse.
'''

pause1 = '''
Blokk 1/4 er ferdig.

Trykk på mellomromstasten når du er klar til å gå videre.
'''
pause2 = '''
Blokk 2/4 er ferdig. 

Trykk på mellomromstasten når du er klar til å gå videre.
'''

pause3 = '''
Blokk 3/4 er ferdig.

Trykk på mellomromstasten når du er klar til å gå videre.

'''

# define window
win = visual.Window(fullscr=True)

# get date for unique logfile id
date = data.getDateStr()


# initiate logfile
subject = '{}_{}'.format(ID[0], date) # ID[0] is the participant id
writer = ppc.csvWriter(subject, 'logfiles_exp1_NO') 
log = pd.DataFrame()

# define mouse
myMouse = event.Mouse(win=win)

# define clock for reaction time
global_time = core.Clock()
stopwatch = core.Clock()                             

# fetch stimuli from folder
path = 'stimuli/'
prac_stim = glob.glob ('practice/*.wav')

# Pseudo-randomize meeting the constraints
path_idx = len(path)

STIM = glob.glob(path + '[nf]*.wav')

context = ['n','f']
item = ['advarsel', 'baal', 'besked', 'blik', 'bordbombe', 'brev', 'flamme', 'gave', 'gloed', 'haab', 'lampe', 'mail', 'paraply', 'pipe', 'svar', 'vokslys']


STIMULI = []

for block in range(5):
    stimuli = []
    for c in context:
        for i in item:
            search_pattern = '{}-{}'.format(c, i) 
            stim = filter(lambda x: search_pattern in x, STIM)
            s = random.choice(stim)
            stimuli +=  [s]
            STIM.remove(s)
    random.shuffle(stimuli)
    
    # check for consecutive elements
    while any(re.search(r"(?<=-).*?(?=-)", i).group(0)==re.search(r"(?<=-).*?(?=-)", j).group(0) for i,j in zip(stimuli, stimuli[1:])):
        random.shuffle(stimuli)

    # make sure that the first 4 four stimuli represent outer steps 
    if block == 0:
        lst = [".*(-01-t).*", ".*(-10-s).*", ".*(-01-s).*", ".*(-10-t).*"]
        random.shuffle(lst)
        
        for p in range(len(lst)):
            regex = re.compile(lst[p])
            s = random.choice([m.group(0) for l in stimuli for m in [regex.search(l)] if m])
            p2 = stimuli.index(s)
            stimuli[p],stimuli[p2] = stimuli[p2],stimuli[p]
    
    STIMULI += stimuli

print(STIMULI)
print(len(STIMULI))

prac_stimuli = []
prac_stimuli+=prac_stim


# position order
p_number = range(0, 100, 2)
if int(ID[0][-1]) in p_number:
    target_pos1 = [[-0.8, 0.8],[0.8, 0.8]]
    target_pos2 = [[0.8, 0.8],[-0.8, 0.8]]
else:
    target_pos1 = [[0.8, 0.8],[-0.8, 0.8]]
    target_pos2 = [[-0.8, 0.8],[0.8, 0.8]]

#### functions ####
target_pos = target_pos1
sendt = visual.TextStim(win, text = u'sendt', color = 'white', height = 0.2, pos = target_pos[0])
taendt = visual.TextStim(win, text = u'tent', color = 'white', height = 0.2, pos = target_pos[1])
sendt_box = visual.Rect(win, height = 0.21, width = 0.32, lineColor = 'white', pos = target_pos[0])
taendt_box = visual.Rect(win, height = 0.21, width = 0.32, lineColor = 'white', pos = target_pos[1])
#practice_sound = sound.Sound('stimuli/n-mail-01.wav')

def play_prac(prac_stim):
    stim = sound.Sound(prac_stim)
    stim.play()
    win.flip()
    core.wait(0.25)

def show_txt(txt):
    txt_stim = visual.TextStim(win, text = txt, color = 'white', height = 0.06)
    txt_stim.draw()
    win.flip()
    event.waitKeys(keyList = 'space')

def play_stim(sound_stim):
    stim = sound.Sound(sound_stim)
    stim.play()
    win.flip()
    core.wait(0.25)

#### run experiment ####

# instructions
show_txt(intro1)
show_txt(intro2)
# practice trial
for practice in range(len(prac_stim)):
    myMouse.setPos(newPos=(0,-0.9))
    play_prac(prac_stimuli[practice])
    sendt.draw()
    taendt.draw()
    sendt_box.draw()
    taendt_box.draw()
    win.flip()
    myMouse.setVisible(1)
    endTrial = False
    while not endTrial:
        if myMouse.getPressed()[0]== 1:
            endTrial = True
    win.flip()
    core.wait(1.5)
show_txt(intro3)

#myMouse.setPos(newPos=[0,0])
myMouse.setVisible(0)

# loop through trials
for n in range(len(STIMULI)):
    stopwatch.reset()
    myMouse.setPos(newPos=(0,-0.9))
    if n in [40]:
        show_txt(pause1)
    if n in [80]:
        show_txt(pause2)
#        target_pos = target_pos2
    if n in [120]:
        show_txt(pause3)
    # play stimulus
    play_stim(STIMULI[n])
    
    # show competitor words

    sendt.draw()
    taendt.draw()
    sendt_box.draw()
    taendt_box.draw()
    myMouse.setVisible(1)
    win.flip()
    
    # reset choice to NA
    choice = np.nan
    
    # track the mouse
    endTrial = False
    num = 0
    while not endTrial:
        num = num + 1
        # check for mouse clicks
        if myMouse.getPressed()[0]:
            RT = stopwatch.getTime()
            endTrial = True
            # if clicked in word 'sendt'
            if myMouse.isPressedIn(sendt_box):
                choice = 'sendt'
            # if clicked in word 'tændt'
            elif myMouse.isPressedIn(taendt_box):
                choice = 'taendt'
            myMouse.setVisible(0)
            log = log.append({
            'SubjectID': ID[0],
            'File': STIMULI[n],
            'Response': choice,
            'RT': RT}, ignore_index=True)
            filename = 'logfiles_exp1_NO/{} ({})_summary.csv'.format(subject,date)
            col_order = ['SubjectID', 'File', 'Response', 'RT']
            log[col_order].to_csv(filename)
                #myMouse.setPos(newPos=[0,0])
        else:
            endTrial = False
        if num % 10 == 0:
            trial = {
            'id': ID[0], 
            'File': STIMULI[n],
            'global_time': global_time.getTime(), 
            'mouseX': myMouse.getPos()[0], 
            'mouseY': myMouse.getPos()[1],
            'choice': choice}
            writer.write(trial)
        else:
            pass
    win.flip()
    core.wait(1.5)

show_txt(outro)
core.quit()
