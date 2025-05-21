# pH Calculator Simulation

An educational application that simulates pH measurements and chemical reactions using a virtual pH meter and probe. This interactive tool helps students understand pH concepts, buffer systems, and chemical reactions through a visual and intuitive interface.

Developed at Lewis and Clark College for the Software Development course. Developed for an outside client at the University of South Carolina.

***This repository has been cloned from the original repository, which remains private due to FERPA regulations. Therefore, this repository does not contain any of the original commits.***

## Features

- **Interactive pH Meter**: Simulates a real pH meter with probe insertion/removal
- **Multiple Solution Categories**:
  - Acids and Bases 
  - Salts
  - Buffer Systems
  - Household Items
  - Water
- **Dynamic pH Calculations**:
  - Real-time pH updates based on solution selection
  - Concentration adjustments via sliders
  - Buffer capacity monitoring
  - Titration simulation with acid/base drops
- **Visual Feedback**:
  - pH strip color indicator
  - Solution volume tracking
  - Drop counter for titrations
  - Buffer capacity alerts
- **Educational Features**:
  - Concentration control (0.0001M to 0.1M)
  - Buffer system manipulation
  - Real-time pH calculations using chemical equations
  - Visual representation of chemical reactions

## Technical Details

### Requirements
- Python 3.x
- PySide6 (Qt for Python)
- Modern operating system (Windows, macOS, or Linux)

### Dependencies
- PySide6 for GUI
- Standard Python libraries (math, sys, os)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/gromov1c/ph_simulator.git
cd ph_simulator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

## Usage

1. Launch the application
2. Select a solution category from the left panel
3. Choose a specific solution
4. Adjust concentration using the slider (where applicable)
5. Insert the pH probe to measure pH
6. For buffers and water:
   - Add drops of acid or base
   - Monitor pH changes
   - Observe buffer capacity limits

## Development

The application is built using:
- PySide6 for the GUI framework
- Object-oriented design with clear separation of concerns
- Resource management for efficient memory usage
- Modular code structure for easy maintenance

### Project Structure
```
ph-calculator/
├── src/
│   ├── main.py              # Application entry point
│   ├── pHCalculatorApp.py   # Main application class
│   ├── calculations.py      # Chemical calculations
│   ├── models.py           # Constants and data models
│   ├── resource_manager.py # Resource management
│   └── graphics/          # Application images
├── requirements.txt
└── README.md
```

## Authors

- Ronald Ruszczyk (client)
- Igor Gromovic
- Ryder Selikow
- Nicholas Dill
- Andrew Fletcher

Lewis & Clark College
