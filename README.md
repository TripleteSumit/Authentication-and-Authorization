# Authentication Backend Project

## Table of Contents

- [Project Overview](#project-overview)
- [Setup and Installation](#setup-and-installation)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Postman Setup](#postman-setup)

## Project Overview

This is a authentication backend project that provides a basic user authentication system with role-based access control (RBAC).

## Setup and Installation

### Prerequisites

- Python 3.10+
- Django 5.1.3+
- Required packages listed in `requirements.txt`

### Installation

1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd authenticationbackend`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
5. Install required packages: `pip install -r requirements.txt`
6. Set up the database: `python manage.py migrate`

## Running the Project

1. Run the development server: `python manage.py runserver`
2. Access the API endpoints: `http://localhost:8000/api/`

## API Endpoints

- `POST /api/signup/`: Create a new user account
- `POST /api/signin/`: Login to an existing user account
- `POST /api/refresh/`: Refresh an existing access token
- `POST /api/logout/`: Logout from the current session
- `GET /api/comment/`: Retrieve a list of comments (requires authentication)

Note: This is not an exhaustive list of API endpoints. You can explore the [core/urls.py](cci:7://file:///home/sumit9090/All-Projects/Authentication/core/urls.py:0:0-0:0) and [message/urls.py](cci:7://file:///home/sumit9090/All-Projects/Authentication/message/urls.py:0:0-0:0) files for more information otherwise you can directly test the things with stored postman collection.

## POSTMAN SETUP

### Step 1: Import the Collection

- Import the collection to your Postman by clicking on the `Import` button on the top left corner of the screen
- Select the `Authentication Backend.postman_collection.json` file from the repository

### Step 2: Create an Account

- Run the `POST /api/signup/` request to create a new user account
- Make sure the server is up and running

### Step 3: Login and Set Environment

- Run the `POST /api/signin/` request to login to the newly created account
- Make sure to set the environment file of Postman which is located at the top right corner of the screen
- Select the `Authentication Backend.postman_environment.json` file from the repository

### You are all set!

- You can now explore the API endpoints and test them with the stored Postman collection.

### Created by: Sumit dey

### Submitted to <span style="color: #34A85A; animation: blink 1s ease-in-out infinite;">V</span><span style="color: #4B5154; animation: blink 1s ease-in-out infinite alternate;">R</span><span style="color: #50B83C; animation: blink 1s ease-in-out infinite;">V</span> <span style="color: #64C7B8; animation: blink 1s ease-in-out infinite alternate;">S</span><span style="color: #73D0C8; animation: blink 1s ease-in-out infinite;">e</span><span style="color: #34A85A; animation: blink 1s ease-in-out infinite alternate;">c</span><span style="color: #4B5154; animation: blink 1s ease-in-out infinite;">u</span><span style="color: #50B83C; animation: blink 1s ease-in-out infinite alternate;">r</span><span style="color: #64C7B8; animation: blink 1s ease-in-out infinite;">i</span><span style="color: #73D0C8; animation: blink 1s ease-in-out infinite alternate;">t</span><span style="color: #34A85A; animation: blink 1s ease-in-out infinite;">y</span>