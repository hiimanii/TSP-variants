import PySimpleGUI as sg
from aco_ui import tsp
from ParticleSwarmOptimisation import solveTSP
from BlackHoleOptimisation import solveBHO

sg.theme("SandyBeach")
def make_win1():
    layout = [[sg.Text('Select Algorithm:', font='Lucida')],
              [sg.Button("Ant Colony"), sg.Button("Black Hole"), sg.Button("Particle Swarm")],
              [sg.Button("Exit", key="Exit")]]
    # layout = [[sg.Text('This is the FIRST WINDOW'), sg.Text('      ', k='-OUTPUT-')],
    #           [sg.Text('Click Popup anytime to see a modal popup')],
    #           [sg.Button('Launch 2nd Window'), sg.Button('Popup'), sg.Button('Exit')]]
    return sg.Window('Chose Algorithm', layout, location=(800,600), finalize=True)

def make_win2():
    layout = [
            [sg.Text('No. of cities: ',size=(20, 1), justification='left')],
            [sg.Combo(['42'],default_value='48',key='num_ct')],
            [sg.Text("Ants: ")],
            [sg.Slider(range=(1,100), orientation="h", default_value=4, key='Ants')],
            [sg.Text("Iterations: ")],
            [sg.Slider(range=(1,100), orientation="h", default_value=10, key='Iterations')],
            [sg.Button('OK')]
         ]
    return sg.Window('Ant Colony', layout, finalize=True)

def make_win3():
    layout = [
            [sg.Text('No. of cities: ',size=(20, 1), font='Lucida', justification='left')],
            [sg.Combo(['42'],default_value='48',key='m3')],
            [sg.Text('No. of stars: ',size=(20, 1), font='Lucida',justification='left')],
            [sg.Combo(['50','70'],default_value='100',key='n3')],
            [sg.Text("Iterations: ")],
            [sg.Slider(range=(1,1000), orientation="h", default_value=10, key='Iterations3')],
            [sg.Button('OK')]
         ]
    return sg.Window('Black Hole', layout, finalize=True)

def make_win4():
    layout = [
            [sg.Text('No. of cities: ',size=(20, 1), font='Lucida',justification='left')],
            [sg.Combo(['42'],default_value='48',key='m4')],
            [sg.Text('No. of particles: ',size=(20, 1), font='Lucida',justification='left')],
            [sg.Combo(['50','70'],default_value='100',key='n4')],
            [sg.Text("Iterations: ")],
            [sg.Slider(range=(1,1000), orientation="h", default_value=10, key='Iterations4')],
            [sg.Button('OK')]
         ]
    return sg.Window('Particle Swarm', layout, finalize=True)

if __name__ == "__main__":
    window1, window2 = make_win1(), None        # start off with 1 window open

    while True:             # Event Loop
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            if window == window2: # if closing win 2, mark as closed
                window2 = None
            elif window == window1: # if closing win 1, exit program
                break
        elif event == 'Popup':
            sg.popup('This is a BLOCKING popup','all windows remain inactive while popup active')
        elif event == 'Ant Colony' and not window2:
            window2 = make_win2()
            event2, values2 = window2.read()
            window2.close()
            window2 = None
            if event2 == sg.WIN_CLOSED:
                continue

            # print(event2, values2)
            num_cities = (int)(values2.get('num_ct'))
            num_ants = (int)(values2.get('Ants'))
            num_Iterations = (int)(values2.get('Iterations'))
            print(num_cities, num_ants, num_Iterations)
            tsp(num_cities, num_ants, num_Iterations)


        elif event == 'Black Hole' and not window2:
            window2 = make_win3()
            event2, values2 = window2.read()
            window2.close()
            window2 = None
            if event2 == sg.WIN_CLOSED:
                continue
            # print(event2, values2)
            m3 = (int)(values2.get('m3'))
            n3 = (int)(values2.get('n3'))
            num_Iterations3 = (int)(values2.get('Iterations3'))
            print(m3, n3, num_Iterations3)
            solveBHO(m3, n3, num_Iterations3)

        elif event == 'Particle Swarm' and not window2:
            window2 = make_win4()
            event2, values2 = window2.read()
            window2.close()
            window2 = None
            if event2 == sg.WIN_CLOSED:
                continue
            # print(event2, values2)
            m4 = (int)(values2.get('m4'))
            n4 = (int)(values2.get('n4'))
            num_Iterations4 = (int)(values2.get('Iterations4'))
            print(m4, n4, num_Iterations4)
            solveTSP(m4,n4,num_Iterations4)

    window.close()
###################################################
# import PySimpleGUI as sg


# sg.theme("tan")
# def main():
#     layout = [[sg.Button("Ant Colonyac", key="ac")],
#               [sg.Button("Black Hole", key="bh")],
#               [sg.Button("Particle Swarm", key="ps")],
#               [sg.Button("Exit", key="Exit")]]
#     window = sg.Window("Main Window", layout)
#     while True:
#         event, values = window.read()
#         if event == "Exit" or event == sg.WIN_CLOSED:
#             break
#         elif event == "ac":
#             if sg.Window("Other Window", [[sg.Text("Ants: ")], [sg.Slider(range=(1,100), orientation="h", default_value=4, tooltip="ants", key='Ants')],[sg.Text("Iterations: ")],[sg.Slider(range=(1,100), orientation="h", default_value=10, tooltip="intervals", key='Iterations')], [sg.Button('Button')]]).read(close=True)[0] == "Yes":
#                 print("User chose yes!")
#             else:
#                 print("User chose no!")
#         elif event == "bh":
#         elif event == "ps":
        
#     window.close()


# if __name__ == "__main__":
#     main()