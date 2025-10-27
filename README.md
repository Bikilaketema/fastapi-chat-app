# FastAPI Real-Time Chat Application

This project is a real-time, multi-user chat application built with a **FastAPI** backend and a **vanilla JavaScript** frontend. The entire application is fully containerized with Docker, making it easy to run with a single command.

The backend uses **WebSockets** to manage persistent connections and broadcast messages instantly to all connected clients, demonstrating a modern, event-driven architecture.

## ✨ Key Features

* **Real-Time Messaging:** Uses WebSockets for instant, bi-directional communication.
* **Connection Management:** A central `ConnectionManager` on the server tracks all active users.
* **System Broadcasts:** Automatically announces when a user joins or leaves the chat.
* **Chat Broadcasts:** Messages sent by one user are immediately broadcast to all other users.
* **Simple Frontend:** A clean, single-page UI built with HTML, Tailwind CSS, and vanilla JavaScript.
* **Fully Containerized:** One-command setup using `docker compose up --build`.

## 🚀 Tech Stack

* **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
* **Server:** [Uvicorn](https://www.uvicorn.org/)
* **Real-Time:** [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
* **Frontend:** HTML5, [Tailwind CSS](https://tailwindcss.com/) (via CDN), Vanilla JavaScript
* **Containerization:** [Docker](https://www.docker.com/) & Docker Compose
* **Language:** [Python 3.10](https://www.python.org/)

## 🏁 Running the Project Locally

This project is fully containerized. The only prerequisite is having **Docker** and **Docker Compose** installed.

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/bikilaketema/fastapi-chat-app.git](https://github.com/bikilaketema/fastapi-chat-app.git)
    cd fastapi-chat-app
    ```

2.  **Build and Run with Docker Compose:**
    This single command will build the Python image, install dependencies, and start the `uvicorn` server.
    ```sh
    docker compose up --build
    ```

3.  **Open the Chat!**
    Your application is now running. Open **`http://localhost:8000`** in your browser to use the chat.

    To test the real-time functionality, open a second browser window (or tab) and go to the same address. Join with a different username and watch the messages appear in both windows instantly.
