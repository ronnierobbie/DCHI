# 🏛️ Court Hardware Inventory Dashboard

A comprehensive Streamlit-based dashboard designed to track and manage hardware inventory across various court locations. This tool provides real-time insights into hardware requirements, distribution, and inventory balances, aiding in efficient resource allocation.

## ✨ Features

- **🔐 Secure Access**: Password-protected entry to ensure data privacy (contact administrator for access).
- **📊 Interactive Dashboard**: Visualizes key metrics such as Total Courts, Regular Courts, Family Courts, and TJOs.
- **🌍 State-wise Filtering**: Filter data by specific states to view regional summaries.
- **📍 Location-Specific Views**: Drill down into individual court locations for detailed hardware status.
- **📦 Inventory Tracking**: clear visualization of 'Required', 'Distributed', and 'Balance' quantities for various hardware items.
- **🚦 Status Indicators**: Color-coded badges (Green/Red/Grey) to instantly identify Surplus, Shortfall, or Balanced inventory status.
- **📱 Responsive Design**: Built with Streamlit for a seamless experience on different devices.

## 🛠️ Tech Stack

- **Python**: Core programming language.
- **Streamlit**: Web application framework for the dashboard.
- **Pandas**: Data manipulation and analysis.
- **OpenPyXL**: Excel file reading engine.

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd CourtApp
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Prepare Data:**
    Ensure `data.xlsx` is present in the root directory. This file should contain a sheet named `Tooli` with the relevant hardware data structure.

### Running the Application

Execute the following command in your terminal:

```bash
streamlit run apps.py
```

The application will launch in your default web browser.

## 🔑 Access

On the login screen, enter the following default password to access the dashboard:

**Password**: `[ASK ADMINISTRATOR]`

## 📁 Project Structure

- `apps.py`: The main application script containing the Streamlit logic and UI definitions.
- `data.xlsx`: (Required) Encrypted or local Excel file containing the inventory data.
- `requirements.txt`: List of Python dependencies.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
