# dsa-wetter
Eine CLI Utility für "schnell mal eben nachm Wetter gucken".
Es richtet sich nach den DSA 4.1 Regeln im WdE, S.156ff.

Wenn ihr Bugs findet, macht gerne nen Issue auf. Ich habe nicht ausgiebig getestet.

## Ausführen
Es ist geschrieben in Python 3, das wird also benötigt.
Ausführen könnt ihr es mit `py -3 dsa-wetter.py [OPTIONS]`, als erste Option empfehle ich `--help`.

## Beispiele
- `py -3 dsa-wetter.py` - Wetter für einen Sommertag im Mittelreich. Die Ausgabe ist direkt und weitestgehend unformatiert.
- `py -3 dsa-wetter.py -n 7 -f csv -o wetter.csv` - Wetter für sieben Sommertage im Mittelreich. Die Ausgabe erfolgt als CSV Tabelle formatiert in die Datei "wetter.csv".
- `py -3 dsa-wetter.py -n 3 -r "Khom" -d -s h -f md` - Wetter für drei Herbsttage in der Khomwüste. Die Ausgabe erfolgt direkt als Stichpunktliste.
- `py -3 dsa-wetter.py -v -n 365 -f csv -o "der-bericht.csv" -x 4711 -d -s w -r "Höhen des Ehernen Schwerts"` - Wetter für ein ganzes Jahr lang windiger Winter auf den wüstenüberzogenen Spitzen des ehernen Schwertes, gespeichert als CSV Tabelle, mit dem Seed 4711 replizierbar und mit Debugausgabe. Kann man machen, muss man nicht.
