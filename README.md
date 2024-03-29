# 8-Puzzle Solver

This project implements an 8-puzzle solver using the A* algorithm and provides a web-based interface for users to input initial and final puzzle configurations, visualize the solution path, and toggle between light and dark themes.

## Features

- **8-Puzzle Solver**: Solves the 8-puzzle problem using the A* algorithm to find the optimal solution path from the initial configuration to the final configuration.
- **Web Interface**: Provides a user-friendly web interface for inputting puzzle configurations and visualizing the solution path.
- **Light/Dark Theme**: Allows users to toggle between light and dark themes for better readability and user experience.

## Technologies Used

- **Python**: Backend logic for solving the 8-puzzle problem.
- **Flask**: Web framework used to create the web application.
- **HTML/CSS/JavaScript**: Frontend development for the user interface and visualization.
- **Vue.js**: JavaScript framework for reactive UI components.
- **vis.js**: JavaScript library for network visualization.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/whitedevil469/8-puzzle-solver.git
   ```

2. Navigate to the project directory:

   ```bash
   cd 8-puzzle-solver
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:

   ```bash
   python app.py
   ```

2. Open a web browser and go to `http://localhost:5000`.

3. Input the initial and final puzzle configurations in the provided text fields.

4. Click the "Solve" button to initiate the solving process.

5. Visualize the solution path on the network graph displayed on the page.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/improvement`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/improvement`).
6. Create a new Pull Request.


## Acknowledgements

- This project was inspired by the classic 8-puzzle problem and the A* algorithm.
- Special thanks to the contributors of Flask, Vue.js, and vis.js for their excellent libraries and frameworks.

