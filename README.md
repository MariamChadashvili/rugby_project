# rugby_project
## Description:

Welcome to the Rugby Project, a web application designed to connect rugby enthusiasts and facilitate seamless team formation! This Flask-based application empowers users to:

Register and Login: Create an account for secure access and team management.
Discover Teams: Browse through available rugby teams seeking players. Gain insights into each team's details, including:
Required player count
Location (where the game will be played)
Team strength (represented by a ranking system)
Current team size (players already signed up)
Maximum capacity (indicating available slots)
Join Teams: If a team has open spots, users can effortlessly join the team.
View Team Members: Once joined, users can access a list of teammates, enabling communication and coordination.
This list may optionally include phone numbers (subject to privacy considerations and user consent).
Exit Teams: Users can easily leave a team if their plans change.
Team Management (for Team Creators): Users who create teams have exclusive privileges to:
Update team information (location, ranking, etc.)
Delete teams they have created


## Technologies:

Backend: Flask (Python microframework)
Database: SQLite (lightweight relational database)
User Sessions: Flask-Session or similar library for user authentication
Templating: Jinja2 for dynamic HTML generation
Frontend: Bootstrap (CSS framework) for responsive design


## Installation:

Clone or Download: Obtain the source code by cloning the repository or downloading the zipped files.

Set Up Environment: Ensure Python 3 and pip (package manager) are installed on your system.

Install Dependencies: Navigate to your project's root directory and run the following command in your terminal:

Bash
pip install Flask Flask-Session db-sqlite3 Jinja2 Werkzeug Bootstrap


## Running the Application:

Start Development Server: Launch the development server using the following command:

```Bash
flask run
Access Application: Your application will typically be accessible at http://127.0.0.1:5000/ in your web browser.
