# Vorbereitung
1. Installiere den Paketmanager Conda und führe im Terminal `conda env create -f requirements.yaml` aus.
2. Falls kein Ordner "data" existiert, muss einer erstellt werden.
3. Im Ordner "data" braucht es einen Unterordner "raw".
4. Im Unterordner "raw" werden die .csv Dateien abgelegt.
   Wenn mehrere .csv Dateien abgelegt werden, wird versucht sie miteinander zu konkatenieren, um die Datenmatrix zu bilden.

# Vorprozessierung
Gebe `python preprocess.py` im Terminal ein und drücke Eingabe.
Es werden folgende Schritte ausgeführt:
1. preprocess_data:
   Iteriert durch alle .csv Dateien.
   Erstellt die Spalte "Timestamp" als Datumsformat.
   Filtert nur Kanal == 1.29.
   Der Freitext "Strom_Bezeichnung" wird One-Hot-Encoded.
   Das prozessierte .csv wird unter './data/processed' geschrieben.
2. concatenate:
   Versucht die Dateien unter './data/processed' miteinander zu konkatenieren.
3. preprocess_labels:
   Unter dem Ordner "labels" wird pro Verbrauchertyp eine .csv Datei erstellt.
   Diese beinhaltet pro Zeile einen Smartmeter und als Label 0 oder 1, ob dieser Verbrauchertyp vorhanden ist oder nicht.
4. get_final_data:
   Bringt das .csv unter "data/concatenated/concatenated.csv" ins Format $M^{m \times n}$, wobei $m$ die Anzahl Smartmeter und $n$ die Anzahl Verbrauchspunkte darstellt.

# Training
Man kann `python train.py` im Terminal eingeben und ausführen, und es wird standardmässiger nur ein Verbrauchertyp ausgeführt und ein bestimmtes Modell, siehe `case = "x"` und `classifier = "y"`.
Man kann aber auch Kommandozeilenparameter übergeben und einen oder mehrere Verbrauchertypen ausführen und das Modell bestimmen:
`python train.py ConvNet boiler,wärmepumpe,ladestation_pw`.
Die zur Verfügung gestellten Modelle sind im entry point ersichtlich unter `classifiers = {...}`.
Die entsprechenden Verbrauchertypen entimmt man aus den Dateinamen unter dem Ordner "./labels".

# Potenzielle Bugs
Der Freitext für die Verbrauchertypen wird zu Fehlern führen, da diese nicht eindeutig sind, z.b. gibt es "Autoladestation" und "Ladestation PW" die für dasselbe stehen, und noch weitere solcher Fälle. Unter "./process/mapping.py" sieht man die derzeitigen Mappings von Verbrauchertyp zu Index.