# Vinyl Simulator

This project is a digital simulation of the classic vinyl record player experience. It aims to recreate the subtle nuances and warm sound signatures that are traditionally associated with playing music on vinyl. Our simulator provides users with a nostalgic auditory journey through the use of modern digital signal processing techniques. You can get more information of code in this site:

```bash
https://github.com/duckduckxuan/Projet_SON
```

## How to Use?

Although our machine can directly simulate the sound effect of vinyl records, for better visual effects, we recommend that you do some preparation work on your computer.

### Installation

Before running the simulator, ensure that you have Python and pip (Python’s package installer) installed on your system. Follow the instructions below to set up the environment and the necessary libraries:

```bash
# Install the required Python libraries
pip install tkinter math serial threading
```

**Note:** The `tkinter` and `threading` library is typically included with Python, so you may not need to install it separately. However, the `serial` library refers to `pyserial`, which you will need to install using pip if it's not already present.

Load your favorite music into the SD card (WAV format is recommended), and insert the SD card into the teensy module.

Connect the teensy module to the headphones and computer respectively, and make sure the teensy module has been started and the computer port is set.

### Running the Project

Once the installation our program is complete, you can run the simulator using the following command:

```bash
# Start the simulator from the command line
python GUI.py
```

If you have special program to run the python, such as VSCODE, you can open the GUI.py and run the simulator directly.

**Note:** The C++ and Arduino code has been preloaded onto the hardware and does not require additional user intervention.

### Play the music

Buttons and knobs on the breadboard allow you to set the start and pause of the music, as well as varying degrees of vinyl effects. Enjoy!