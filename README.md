# 📈 **Stocks**

## ✏️ **Project Description**
Stocks is a project designed for monitoring stocks (with plans to add crypto later) through web scraping with various filters, such as:
- Displaying stocks below a specific price
- Showing only favorite or added stocks

The project currently features **authentication and authorization** functionalities, with authorization partially implemented.  
This project is being developed for personal use to streamline stock monitoring.

---

## 📌 **Future Improvements**
- Add a Telegram bot with the described features.
- Introduce several microservices (e.g., notifications) using **RabbitMQ** or **Kafka**.

---

## 🚀 **Getting Started**

### 📔 **Setting up the Project in Your IDE**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GreatTeapot/Stocks.git


``
# Project Setup Instructions

## Setting Up the Virtual Environment

1. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   ```
2. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Environment Files

- Create `.env` and `.env-dev` files based on the provided templates:
  - `.env.example`
  - `.env-dev.example`

## Running the Application

- **Run the application:**
   ```bash
   make run
   ```

## Using Docker

1. **Build the Docker image:**
   ```bash
   make build
   ```
2. **Start the application:**
   ```bash
   make up
   ```
3. **Stop the application:**
   ```bash
   make stop
   ```
4. **Shut down the application:**
   ```bash
   make down
   ```
