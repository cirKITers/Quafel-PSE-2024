package simulation

- Dieses Package dient als Schnittstelle zwischen Quafel-Web und Quafel.
- Hier kann via der Hardwareprofile auf einem Quafel-Programm eine Simulation gestartet werden.
- Anschließend erhält man Daten, diese müssen dann in die Klassen-Strukturen des Modells umgewandelt werden und via dem
  Controller anschließend in die Datenbank geschrieben werden.

Methoden:

- Submit Simulationsauftrag (min_qubits: int, max_qubits: int, qubits_increment: int, qubits_type: str,
  min_depth: int, max_depth: int, depth_increment: int, depth_type: str,
  min_shots: int, max_shots: int, shots_increment: int, shots_type: str,
  quantum_framework: QFR) -> QUAFLE output als csv

private methoden:

- connect per ssh to correct cluster
- set up quafel
- generate simulations configuration commands für file editing
- download results from bwsyncshare

Wie kann man einem Job auf dem Cluster starten?

- mit ssh verbinden. quafel ansprechen.
  Welche Daten sind nötig um einen Job auf dem KIT-Cluster zu starten?
- Hardwareprofil, Simulationsauftrag.
- Wie erreicht man Quafel?
- SSH
  Wie übergibt man die Parameter an Quafel?
- conf\base\parameters\data_generation.yml & conf\base\parameters\data_science.yml anpassen und hochladen.
  Wie bekommt man die Rückgabe von Quafel?
- bwsyncshare

Fragen an Melvin:
Man wird sich mit SSH verbinden, reicht hierfür die IP und ein Passwort aus, oder gibt es noch weitere
Authentifizierungsschritte?
Reicht für die Auswahl von einem bestimmten Clustern eine bestimmte IP aus oder sind hierfür interne Schritte notwendig?
Wird Quafel bereits installiert sein, oder muss es noch installiert werden, und sind vlt noch weitere
Vorbereitungsschritte notwendig?
Dann würde ich die data_generation.yml & data_science.yml über die console editieren.
Die Ergebnisse werden auf BWSyncShare hochgeladen, richtig? Werden diese öffentlich sein, oder ist hierfür ebenfalls
eine Authentifizierung notwendig?
