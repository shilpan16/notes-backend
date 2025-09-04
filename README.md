
# Notes App Backend

A lightweight RESTful API built with FastAPI to manage notes. This backend supports CRUD operations and serves as the backend for the Notes App frontend.

## Live API

Access the live API here:  
🔗 [https://notes-backend-vug3.onrender.com](https://notes-backend-vug3.onrender.com)

## Frontend

The frontend for this Notes App is built with React and deployed on Vercel:  
🔗 [https://notes-frontend-navy-pi.vercel.app/notes](https://notes-frontend-navy-pi.vercel.app/notes)  
🔗 [Vercel Project Dashboard](https://vercel.com/shilpa-nerallas-projects/notes-frontend)

> The frontend consumes this backend API for creating, reading, updating, deleting, and sharing notes.

## Features

## Features

- **Create Notes**: Add new notes with titles and content.
- **Read Notes**: Retrieve a list of all notes.
- **Update Notes**: Modify existing notes.
- **Delete Notes**: Remove notes from the database.

## Technologies Used

- **Backend Framework**: FastAPI
- **Database**: SQLite
- **Deployment**: Render

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shilpan16/notes-backend.git
   cd notes-backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   * On Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   * On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Documentation

FastAPI provides interactive API documentation:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Contributing

Contributions are welcome! Please fork the repository, create a branch, and submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License.

