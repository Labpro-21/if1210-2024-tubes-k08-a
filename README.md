# IF1210 - Dasar Pemrograman 2024
**<center><span style="font-size: 1.3em;">Tugas Besar - IF1210 Dasar Pemrograman 2024</span></center>**

# About
Sebagai agen-agen di O.W.C.A (Organisasi Warga Cool Abiez), atas permintaan Purry, kita harus bekerja sama untuk mengalahkan monster-monster terbaru Dr. Asep Spakbor. Untuk mencapai tujuan itu, kita harus merancang rencana yang matang dan mencari serta melatih monster-monster sendiri untuk melawan monster-monster Dr. Asep Spakbor demi keselamatan kota Danville.

# Screenshots
## Main Menu
| | |
|-|-|
| ![](/doc/screenshots/loading-screen.png)<br/><center>Loading Screen</center> | ![](/doc/screenshots/menu-guest.png)<br/><center>Guest Menu</center> |
| ![](/doc/screenshots/menu-admin.png)<br/><center>Admin Menu</center> | ![](/doc/screenshots/menu-agent.png)<br/><center>Agent Menu</center> |
| ![](/doc/screenshots/login-screen.png)<br/><center>Login Screen</center> | ![](/doc/screenshots/transparent.png) |

## Battle
| | |
|-|-|
| ![](/doc/screenshots/battle.png)<br/><center>Battle</center> | ![](/doc/screenshots/transparent.png) |

## Inventory
| | |
|-|-|
| ![](/doc/screenshots/inventory.png)<br/><center>Inventory</center> | ![](/doc/screenshots/transparent.png) |

## Arena
| | |
|-|-|
| ![](/doc/screenshots/arena-choose.png)<br/><center>Arena Choose</center> | ![](/doc/screenshots/arena-battle.png)<br/><center>Arena Battle</center> |
| ![](/doc/screenshots/arena-stats.png)<br/><center>Arena Stats</center> | ![](/doc/screenshots/transparent.png) |

## Shop
| | |
|-|-|
| ![](/doc/screenshots/shop.png)<br/><center>Shop</center> | ![](/doc/screenshots/shop-confirm.png)<br/><center>Shop Confirm</center> |

## Laboratory
| | |
|-|-|
| ![](/doc/screenshots/laboratory.png)<br/><center>Laboratory</center> | ![](/doc/screenshots/laboratory-confirm.png)<br/><center>Laboratory Confirm</center> |

## Shop Management
| | |
|-|-|
| ![](/doc/screenshots/shop-management.png)<br/><center>Shop Management</center> | ![](/doc/screenshots/transparent.png) |

## Monster Management
| | |
|-|-|
| ![](/doc/screenshots/monster-management.png)<br/><center>Monster Management</center> | ![](/doc/screenshots/transparent.png) |

# Contributors
| Name                              |   NIM    |
|-----------------------------------|----------|
| Syifannissa Nafisalia Kuncoro     | 16523048 |
| Julian Benedict                   | 16523178 |
| Jason Samuel                      | 19623118 |
| Nadhif Radityo Nugroho            | 19623178 |
| Aryo Wisanggeni                   | 19623258 |

# Features
| Id  | Feature Name             | Status |
|-----|--------------------------|--------|
| F00 | Random Number Generator  |   ✔   |
| F01 | Register                 |   ✔   |
| F02 | Login                    |   ✔   |
| F03 | Logout                   |   ✔   |
| F04 | Menu & Help              |   ✔   |
| F05 | Monster                  |   ✔   |
| F06 | Potion                   |   ✔   |
| F07 | Inventory                |   ✔   |
| F08 | Battle                   |   ✔   |
| F09 | Arena                    |   ✔   |
| F10 | Shop & Currency          |   ✔   |
| F11 | Laboratory               |   ✔   |
| F12 | Shop Management          |   ✔   |
| F13 | Monster Management       |   ✔   |
| F14 | Load                     |   ✔   |
| F15 | Save                     |   ✔   |
| F16 | Exit                     |   ✔   |

# How to Run
- `python main.py`, will run the program with preloaded default save.
- `python main.py <save-name>`, will run the program with specified game save in `data/saves/<save-name>`

# Developing
1. `python -m venv venv`
2. `venv\Scripts\activate`
3. `pip install requirements.txt`

> Note: This program **does not** use external library. The `requirements.txt` only refers to internal submodule in this project. We decided to use this approach so that the code will be readable and maintainable.
