# HerzAktiv

## Beschreibung
HerzAktiv ist ein Projekt zur Auswertung und Darstellung verschiedener Körperdaten wie Leistungsdaten oder EKGs. Die Ergebnisse werden grafisch auf einer Streamlit-Seite präsentiert. Das Projekt wird ständig erweitert, z.B. durch die Implementierung eines BMI-Rechners.

## Installation
Führen Sie die folgenden Schritte aus, um HerzAktiv zu installieren:

1. Laden Sie das Repository herunter:
    ```bash
    git clone https://github.com/Luggy85/HerzAktiv
    cd HerzAktiv
    ```

2. Erstellen Sie eine virtuelle Umgebung:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Auf Windows: venv\Scripts\activate
    ```

3. Installieren Sie die benötigten Module und Bibliotheken:
    ```bash
    pip install streamlit plotly pandas Pillow traceback scipy
    ```

4. Stellen Sie sicher, dass die Module korrekt in das Programm importiert werden und dass die Verknüpfungen zwischen den Programmen richtig sind. Überprüfen und korrigieren Sie gegebenenfalls die Speicherpfade von Bildern.

## Verwendung
Um die Streamlit-Seite zu starten und die Funktionen von HerzAktiv zu nutzen, führen Sie den folgenden Befehl aus:

```bash
streamlit run main.py