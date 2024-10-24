# 3-Tier-Rule-Engine-Application
This project implements a 3-tier rule engine using Abstract Syntax Tree (AST) to determine user eligibility based on attributes such as age, department, income, and spend.

## Table of Contents
1.Features
2.Requirements
3.Setup Instructions
4.Usage
5.Design Choices
6.Project Structure
7.Contributing

## Features
- Implements rule-based logic using AST to dynamically interpret eligibility rules.
- The application consists of three main tiers:
1. Presentation Layer (User Interface)
2. Application Layer (Rule Engine)
3. Data Layer (Data Storage and Retrieval)
- Supports extensible rules that can be easily modified or added.

## Requirements
- Python 3.x
- Docker or Podman (for containerizing the web server and database)

## Dependencies
- Flask (for the webserver) - if a web interface is involved.
- SQLite/MySQL/PostgreSQL (for data storage) - containerized in Docker/Podman.
- Docker or Podman installed on your machine.

Install the dependencies using:
**bash**
pip install -r requirements.txt

You can also use a virtual environment:
**bash**
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Setup Instructions
### Step 1: Clone the Repository
**bash**
https://github.com/Shubhangeeagrawal/3-Tier-Rule-Engine-Application

### Step 2: Build and Run the Application
You can set up the required services using Docker containers. The project includes a Docker Compose file to handle the web server and database.

**1.Build and run the containers:**
**bash**
docker-compose up --build

This command will:
- Build the web server image (Flask server or any other specified web framework).
- Create a database container (MySQL, PostgreSQL, or SQLite).

**2.After running, the application should be accessible on http://localhost:5000.**

### Step 3: Run the Application Manually
If you prefer running it manually (outside of containers):

**1.Start the Flask server:**
**bash**
python app.py
**2.Connect the application to your local database by configuring the connection in config.py or through environment variables.**

## Usage
**1.Submit Rule Engine Input:** Use the interface or API to submit user attributes such as age, department, and income.
**2.Get Eligibility Result:** The application processes the input through the AST-based rule engine and provides a response with eligibility.
You can interact with the application using curl or through the web interface.

## Design Choices
1.AST for Dynamic Rule Processing:
  - The decision to use an Abstract Syntax Tree allows the application to interpret and apply  eligibility rules at runtime, making it flexible and extensible.
2.Three-Tier Architecture:
- Presentation Layer: Handles input from users or API clients.
- Application Layer: Contains the rule engine logic and processes requests.
- Data Layer: Stores the user data and rules for decision-making.
3.Containerization:
  - Using Docker allows easy deployment across environments. The database and web server are isolated in their own containers, making scaling and updates simpler.

## Project Structure
**bash**
3-tier-rule-engine/
│
├── app.py               # Main application file
├── rule_engine.py        # Rule engine logic (AST-based)
├── config.py             # Configuration for database and environment
├── Dockerfile            # Dockerfile for building the web server image
├── docker-compose.yml    # Docker Compose file for managing services
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation (this file)

## Contributing
If you wish to contribute to this project, please follow these steps:
1.Fork the repository.
2.Create a feature branch (git checkout -b feature-branch).
3.Commit your changes (git commit -am 'Add new feature').
4.Push to the branch (git push origin feature-branch).
5.Open a pull request.
