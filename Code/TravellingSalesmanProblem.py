from ParticleSwarmOptimisation import ParticleSwarmOptimisation
from BlackHoleOptimisation import BlackHoleOptimisation
import PySimpleGUI as sg
class TravellingSalesMan:
    def __init__(self):
        self.curr_step = 0
        self.optimisation_technique = 'Particle Swarm Optimisation'
        self.num_iterations = 1000
        self.alpha = 0.6
        self.beta = 0.4
        self.cities = 48
        self.sample_dataset = {'48': 'att48_d.txt'}
    def get_layout(self):

if __name__ == '__main__':
    ### Step - 1 : Get the optimisation method
    ### Step - 1 : Get the Dataset (Two Options: Sample Dataset or Own Dataset)
    ### Case -1 Sample Dataset
    ### Step 2.1: Number of cities to choose from
    ### Case -2: Get Your Own Dataset
    ### Step-2.1: Get the number of cities
    ### Step-2.2: Enter the distance between each cities to form the dataset
    ### Step-2.3: Ask to store the dataset in the current directory If Yes-Store the dataset or if No, do not store the dataset
    ### Step - 3: Choose the optimisation technique
    ### Case 3.1 - Clicked on Swarm Particle Optimisation
    ### Case 3.2 - Clicked on Black Hole Optimisation
    ### Enter number of iterations
    ### Enter number of particles / stars
    ### For Particles swarm optimisation (Enter the value of alpha and beta)
    ### For Black Hole Optimisation (Enter the value of alpha)
    sg.theme('BluePurple')
    layout1 = [
                    [sg.Text('Select the Optimisation Technique:', key='-input_text-')],
                    [sg.Button('Particle Swarm Optimisation')],
                    [sg.Button('Black Hole Optimisation')],
                    [sg.Button('Ant Colony Optimisation')],
                    [sg.Button('Exit')]
              ]
    layout2 = [
        [sg.Text('Do you want to create your own DataSet or try one of the Sample Dataset: ')],
        [sg.Button('Create a New Dataset')],
        [sg.Button('Open an Existing Dataset')],
        [sg.Button('Try one of the Sample Dataset')],
        [sg.Button('Exit')]
    ]
    layout3 = [
        ##### If clicked on Try One of the Sample Dataset
        [sg.Text('Choose the number of cities')],
        [sg.Button('48')],
        [sg.Button('Exit')]
    ]
    layout4 = [
        ##### If clicked on Try One of the Sample Dataset (Particle Swarm Optimisation)
        [sg.Text('Enter the number of Iterations')],
        [sg.Input(key = '-iterations-')],
        [sg.Text('Enter the value of alpha (denotes the importance given to the local maxima)')],
        [sg.Input(key = '-alpha-')],
        [sg.Text('Enter the value of beta (denotes the importance given to the global maxima)')],
        [sg.Input(key = '-beta-')],
        [sg.Button('Okay')],
        [sg.Button('Exit')]
    ]
    window = sg.Window('Travelling Salesman Problem', layout)
    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Show':
            # Update the "output" text element to be the value of "input" element
            window['-OUTPUT-'].update(values['-IN-'])
            window['-input_text-'].update('My name is Karan.....')
    window.close()
        
