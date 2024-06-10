# Einführung
Alle Dateien im Ordner **./appliance-detection** beziehen sich auf die Verbrauchertypen Detektierung. Eine Einführung in wie der Quellcode zu gebrauchen ist, findet sich **./appliance-detection/README.md**.
Der Trainingsprozess und die genutzten Datenstrukturen sowie Modelle orientieren sich ausschliesslich an folgendem Paper[^1].
Der Code um die Daten vorzuprozessieren ist Unternehmensspezifisch und orientiert sich an den zur Verfügung gestellten .csv Dateien.

# Vorgehen
Die Verbrauchertypen Detektierung kann als ein Supervised Learning[^3] Problem angesehen werden.
Inspiriert vom Paper[^1], ist es das Ziel die Rohdaten so hinzukriegen, dass wir eine Matrix der Form $M^{m \times n}$ hinkriegen, mit $m$ Smartmetern[^2] und $n$ Verbrauchspunkten. Die Matrix $M$ ist hochdimensional, d.h. wir enden mit ca. 200-300 Zeilen (Smartmetern) und ca. 30'000 Spalten, was den Verbrauchspunkten von etwa einem Jahr entspricht.

Wir trainieren $k$ Modelle für $k$ Verbrauchertypen, d.h. jedes Modell wird auf der Matrix $M$ trainiert und soll dann ein binäres Resultat (0 oder 1) liefern, welches anzeigt ob der jeweilige Smartmeter diesen Verbrauchertypen aufweist oder nicht.

Die genutzten Modelle sind Deep Learning[^4] Ansätze und sind heute in diversen Bereichen der neuste Stand der Technik, bezüglich Klassifikationsproblemen.

## Rohdaten
Die Dateien im Rohformat enthalten ungefähr folgende Spalten, welche wichtig sind:
- Smartmeter ID
  - Alphanumerisch, eindeutige Identifikationsnummer.
- Verbrauch in Kw/h
  - Fliesskommazahl oder nicht vorhanden.
- Kanal
  - Es gibt zwei Kanäle, 1.29 gibt den Verbrauch an, der Andere die Einspeisung zurück ins System.
- Timeslot
  - Zeitpunkt der ein Intervall von 15min repräsentiert.
- Verbrauchertypen
  - Freitext.

## Vorprozessierung 
Ziel der Vorprozessierung ist es eine .csv Datei ins gewünschte Matrix Format zu bringen.
- Timeslot
  - Das Intervall wird in folgendes Datumsformat gebracht, z.B. 2023-01-01 00:15:00
- Verbrauchtertypen
  - Der Freitext wird zuerst One-Hot-Encoded[^5] und dann pro Vebrauchertyp eine .csv Datei erstellt, welche als ein Spaltenvektor $y^{s \times 1}$ angesehen werden kann, wobei $s$ die Anzahl an Smartmetern darstellt. Die .csv Dateien pro Verbauchertyp geben an, ob im jeweiligen Smartmeter der Verbrauchertyp vorhanden ist (1 für vorhanden) oder nicht (0 falls nicht vorhanden).

## Training
Das Training erfolgt im besten Fall auf GPUs[^6]. Der Code unterstütz das Rechnen auf einer lokalen Maschine sowie der Cloud, mit entsprechenden Cuda oder M1 (Apple Mac) Geräten.

Folgende Modelle/Architekturen, die im Paper[^1] motiviert werden, wurden verwendet:
- Convolutional Neural Network[^7]
- Residual Neural Network[^8]

Inception[^10] wurde nicht verwendet aufgrund der Komplexität und längeren Rechenzeit.

# Scores
- Confusion Matrix

  Die Confusion Matrix ermöglicht es uns, das Modell aus verschiedenen Blickwinkeln auszuwerten.  
  Im Beispiel unten sehen wir 7 Vorhersagen, bei dem ein Modell sagen würden, ein Verbrauchertyp existiert, jedoch sind nur 6 davon richtig, einer war falsch.
  Desweiteren werden 2 Verbauchertypen die existieren, nicht vorhergesagt.


  |                | Predicted Non-Appliance | Predicted Appliance |
  |----------------|---------------------|-------------------------|
  | Actual Non-Appliance     | 3                   | 1                       |
  | Actual Appliance | 2                   | 6                       |

- Precision (Genauigkeit)

  Die Precision gibt den Anteil der korrekt als positiv klassifizierten Ergebnisse an der Gesamheit der als positiv klassifizierten Ergebnisse an, u.a. welcher Anteil der Verbrauchertypen mit positiven Testergebnis ist auch tatsächlich ein Verbauchertyp.

- Recall (Sensitivität)

  Der Recall gibt die Wahrscheinlichkeit an, mit der ein positives Objekt (Verbrauchertyp) korrekt als positiv klassifiziert wird, z.B. dem Anteil an tatsächlichen Verbrauchertypen, bei denen der Verbrauchertyp auch erkannt wurde.

- F1 Score

  Der F1 Score vereint Precision und Recall und gibt eine einzige Metrik an, mit welcher die Leistung des Modells und der Vergleich zwischen Modellen ermöglicht wird.

# Resultate 
Wir gehen auf die Resultate der zwei wichtigsten Verbrauchtertypen aus Sicht des Unternehmens ein:

- Autoladestation
  - Convolutional und Residual Neural Network liefern hier diesselben Ergebnisse.
  - Confusion Matrix: 
  - [26  0]
  - [ 1  0]
  - PRECISION: 0.0
  - RECALL: 0.0
  - F1_SCORE: 0.0
  
  Von 27 Smartmetern im Testdatensatz, gibt es nur einen einzigen der eine Autoladestation enthält. Somit könnte das Modell genau einen richtigen vorhersagen, hat es aber nicht getan. Mit einem solchen Setting kann das Modell gar keine guten Ergebnisse liefern. Es braucht viel mehr Smartmeter die eine Autoladestation aufweisen, damit die Metriken Sinn ergeben.

- Wärmepumpe
  - Hier betrachten wir das Residual Modell, das Convolutional liefert keine guten Ergebnisse.
  - CONFUSION_MATRIX:
  - [14  8]
  - [ 0  5]
  - PRECISION: 0.4
  - RECALL: 1.0
  - F1_SCORE: 0.55

  Von gesamthaft 27 Smartmetern im Testdatensatz, gibt es 5 die eine Wärmepumpe enthalten, 22 davon haben keine Wärmepumpe.
  Die Genauigkeit des Modells ist 40%, d.h. von den Smartmetern die den Verbrauchertyp Wärmepumpe haben, hat das Modell 5 richtig vorhergesagt und bei 8 hat es den Verbrauchertyp vorhergesagt obwohl keiner vorhanden war. Die Sensitivität mit 100% besagt, dass 5 von 5 richtig vorhergesagt wurden und keiner vergessen wurde.

# Schlussfolgerungen
- Die Anzahl der Smartmeter ist zu gering, als dass das Model eine vernünftige Funktion aus den Daten lernen kann.
- Die kleinen Testdatensätze ermöglichen es auch nicht, eine vernünftige Abschätzung des Fehlers vorherzusagen. Im Beispiel der Autoladestation, gab es genau einen Smartmeter, bei dem das Modell eine korrekte Vorhersage machen könnte. Hätte es diesen zufällig getroffen, wäre die Sensitivität sowie die Genauigkeit 100% gewesen. Man könnte keine Schlüsse ziehen, wie sich das Modell auf ungesehen Daten verhalten würde.

# Nächsten Schritte
Durch die Hochdimensionalität des Ansatzes, kann mit der jetzigen Menge an Daten, nicht viel erreicht werden. Möchte man die Deep Learning Methoden weiterführen, könnte man folgende Punkte ausprobieren:
1. Klassenungleichgewicht durch mehr Smartmeter Daten ausbalancieren.
2. Künstlich Smartmeter Daten generieren.
   Die künstliche Generation von Smartmeter Daten könnte mit GANs[^9] erfolgen.
3. Kreuzvalidierung könnte helfen, die Fehlerabschätzung auf diversen Teilen der Daten durchzuführen.
4. Dimensionalität runterbrechen auf Monate, Wochen, Tage.
5. Öffentliche Datensätze miteinbeziehen, siehe Paper[^1].

[^1]: Appliance Detection Using Very Low-Frequency Smart Meter Time Series https://arxiv.org/pdf/2305.10352.pdf

[^2]: Ein Smartmeter ist ein moderner Zähler der in Häusern, Schulen und diversen anderen Einrichtungen anzutreffen ist. Er misst den Kilowatt Vebrauch pro Stunde sowie die Einspeisung von Strom ins Netz, z.B. falls das Gebäude eine Photovoltaik Anlage besitzt.

[^3]: Supervised Learning ist eine Methode des maschinellen Lernens, bei der die Zielvariable vorhanden ist, und das Modell so die Repräsentation versucht zu erlernen.

[^4]: Deep Learning (tiefes Lernen) ist ein Teilbereich des maschinellen Lernens, bei dem künstliche neuronale Netze (ANN) zur Lösung komplexer Aufgaben eingesetzt werden.

[^5]: One-Hot-Encoding (One-Hot-Encoding) ist eine Technik, mit der kategorische Daten in numerische Daten umgewandelt werden. Bei der One-Hot-Kodierung wird jeder Kategorie ein eindeutiger Wert zugewiesen, und jeder Datenpunkt wird als Vektor kodiert, wobei nur eine Eins der Kategorie entspricht, zu der er gehört.

[^6]: Grafikprozessor (GPU) (Graphics Processing Unit) ist ein spezieller Prozessor für die Verarbeitung von Grafikdaten. GPUs sind in der Lage, viele Berechnungen gleichzeitig durchzuführen, was sie ideal für den Einsatz in Algorithmen des maschinellen Lernens macht, da diese oft sehr komplexe Berechnungen erfordern.

[^7]: Convolutional Neural Network (CNN) ist ein architektonischer Typ eines künstlichen neuronalen Netzwerks, das ursprünglich für die Verarbeitung von Bildern entwickelt wurde. CNNs verwenden Filter, um Muster zu erkennen.

[^8]: Residuales neuronales Netz (ResNet) ist ein architektonischer Typ eines künstlichen neuronalen Netzes, der speziell für die Lösung von Overfitting-Problemen entwickelt wurde. ResNets verwenden zusätzliche Verbindungen, um den Informationsverlust zwischen Layers entgegenzuwirken.

[^9]: Generative Adverserial Network ist ein Machine Learning Framework, bei dem zwei Neuronale Netzwerke, ein Generator und ein Diskriminator, gegeneinander antreten.

[^10]: Inception ist ein Convolutional Neural Network. Es hat mehr tiefe und breite als ein herkömmliches durch die Verwendungen von Blöcken, die aneinandergereiht das Netzwerk ergeben. 