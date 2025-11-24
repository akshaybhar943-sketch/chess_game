# ♟️ Professional Python Chess Game

A fully functional, two-player chess game built with **Python**, utilizing **Pygame** for graphical rendering and **Python-Chess** for rigorous game logic and rules enforcement. This project is structured for easy deployment and modification.

## ✨ Features

* **Standard Chess Rules:** Full support for all standard rules, including Castling, En Passant, and Pawn Promotion (defaulting to Queen).
* **Intuitive UX:** Employs a simple two-click system (select piece, select destination).
* **Legal Move Highlighting:** When a piece is selected, all **legal destination squares** are highlighted with semi-transparent indicators (dots for empty squares, rings for captures).
* **Visual Feedback:** Clear highlighting of the currently selected piece and color-coded status messages for Check, Checkmate, and Stalemate.
* **Modular Design:** Easy to swap out piece graphics and customize board colors via constants.

## 🛠️ Prerequisites

Ensure you have **Python 3.x** installed. The required libraries can be installed using `pip` and the included `requirements.txt` file.

```bash
pip install -r requirements.txt
# Alternatively:
# pip install pygame python-chess
