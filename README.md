# 🚀 Trade Bot Project

## 📚 Introduction
This project involves creating a high-frequency trading bot capable of executing thousands of orders per second. The goal is to revolutionize trade markets by utilizing advanced algorithmic trading techniques.

## 🗂️ Project Structure
The project is structured as follows:
- **📜 Source Code**: Contains all the Python scripts used to build the trading bot.
- **📊 Datasets**: Includes three training datasets and a generator provided for evaluation purposes.
- **📄 Documentation**: Contains this README file and any additional documentation.

## 📋 Requirements
The project requires the following software and libraries:
- Python 3.6+
- Libraries: numpy, pandas, sklearn, and matplotlib

## ⚙️ Installation
1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd trade-bot
    ```
2. Install the required libraries:
    ```bash
    pip install numpy pandas sklearn matplotlib
    ```

## 🚀 Usage
To run the trading bot, follow these steps:
1. Navigate to the project directory:
    ```bash
    cd trade-bot
    ```
2. Run the project :
    ```bash
    ./ai-bot-workspace-2.4.3-x86_64.AppImage
    ```

## ✨ Features
- **⚡ High-Frequency Trading**: The bot can compute and execute thousands of orders per second.
- **🤖 Algorithmic Trading**: Utilizes sophisticated techniques to make trading decisions.
- **🔄 Adaptability**: The bot can adapt to new datasets and avoid overfitting.

## 🧪 Evaluation
The performance of the trading bot will be evaluated based on the total amount of money made. The evaluation includes:
- Training on provided datasets.
- Adapting to new datasets during evaluation.
- Comparing total profits with other bots.

## 📡 Updates and Answers
The bot communicates with the server to receive general information about the game and training data. It then makes decisions based on the data and sends orders back to the server. The communication follows a strict grammar:
- **📝 General Information**: `info = 'settings ' variable value (, value)*`
- **📈 Training Data**: `update_c = 'update game next_candles ' rate ';' rate ';' rate`
- **🤔 Decision Making**: `session = update_c eol update_s eol 'action order ' integer`

The bot must respond with valid orders at all times to avoid program collapse.

## 🏗️ Architecture
The architecture of the bot includes:
- **🖥️ Client-Server Interface**: For training purposes, download the client-server interface, specify the location of the bot, and watch it execute trades.
- **🔧 Trading Logic**: The core algorithm that makes trading decisions based on market data.
- **📊 Evaluation Metrics**: To measure the performance and adapt the algorithm.

## 📚 References
- [High-Frequency Trading](https://en.wikipedia.org/wiki/High-frequency_trading)
- [TradingView](https://www.tradingview.com/chart/?symbol=BITSTAMP%3ABTCUSD)
- [Overfitting](https://en.wikipedia.org/wiki/Overfitting)

For more detailed information, please refer to the project documentation and comments within the code.

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for more information.

## 📧 Contact
For any questions or feedback, please contact [damian.gil@epitech.eu] and [guillaume.houriez@epitech.eu].

Made by Guillaume Houriez and Damian Gil.
