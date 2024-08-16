# 1125-lo-ki-devs

# CareLink - Healthcare Supply Distribution

## Overview

CareLink is a web application designed to streamline the distribution of healthcare supplies to hospitals and pharmacies. With features including inventory management, request handling, and distribution planning, CareLink ensures that essential supplies are delivered efficiently and effectively.

## Features

- **Inventory Management**: Track and manage inventory levels in real-time.
- **Request Management**: Streamline the process of receiving and fulfilling supply requests.
- **Distribution Planning**: Plan and optimize the distribution of supplies.


## Setup Instructions

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/CareLink.git
    cd CareLink
    ```

2. **Set up the virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    Run the scripts to create the necessary tables:

    ```bash
    python create_inventory_table.py
    python create_pharmacy_db.py
    ```

5. **Run the application:**

    ```bash
    python app.py
    ```

    The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Usage

- Navigate to the Home page to explore the available features.
- Use the **Inventory Management** page to track and update supplies.
- **Request Management** allows you to manage incoming requests for supplies.
- The **Distribution Planning** page helps in optimizing delivery routes and schedules.
- Report a shortage or view detailed shortage information on the relevant pages.
