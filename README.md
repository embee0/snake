# Snake-Spiel: Von einer simplen Textversion zu Pygame und Kivy
Basierend auf einem minimalen, text-basierten Snake-Spiel (`snake0.py`), das nur rein prozedural programmiert und nur schwer erweiterbar ist, führen wir mehrere Refactorings durch, bis wir bei einer Version sind, die sich leicht an andere Darstellungsformen (zB pygame oder Kivy) anpassen lässt.

## Curses installieren (nur unter Windows nötig)
Wir verwenden die für das textbasierte User-Interface die curses-Bibliothek. Unter Linux und MacOS ist sie wohl schon in der Standardinstallation dabei - unter Windows aber nicht. Dort müssen wir sie zusätzlich installieren (s. [Curses-Tutorial hier](https://www.devdungeon.com/content/curses-programming-python#toc-2)). Im Anaconda Prompt also bitte eingeben:  

`conda install -c labscript-suite windows-curses`

Um zu testen, ob das geklappt hat, kannst du die Originalversion des Spiels in der Konsole (Anaconda Prompt) ausprobieren:

`python .\snake0.py`

## Pygame

`conda install -c conda-forge pygame`  oder `pip install pygame`

## Ziel
Verbessere das Spiel weiter, so dass es schick wird wie [diese Version](https://g.co/kgs/YATqFtm) oder [diese](https://snake.io/) ;-)


