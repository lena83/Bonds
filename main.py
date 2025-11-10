from __future__ import annotations

from data_loader import load_bonds


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bonds = load_bonds("bonds.csv")
    print(f'Hi')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
