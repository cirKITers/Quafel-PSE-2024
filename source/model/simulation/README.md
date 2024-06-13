### package model/simulation

- Unterteilung des Models.
- Hier werden die Simulationsdaten als Objekte definiert und gespeichert.
- Des weiteren gibt es hier weitere Klassen, die das Zugreifen auf die Daten erleichtern. (Abstraktion von Querys)

Offene Frage:
- Sollen Simulationsaufträge gespeichert werden?
  - wenn ja:
    - Unterteilung in Input und Output
      - Antowrt: nein

Tabellen:
Quantum Frameworks:
- Name des Simulators

QUAFEL Output: duration_perf_n in zusätzliche Tabelle auslagern, damit keine varibale anzahl an spalten, maybe avg duration hier
- config_id, framework, qubits, depth, shots, avg_duration, expressibility, entangling_capability. evaluationsN

Option 1:
Duration: eine spalte zeigt die ergebnisse einer config_id.
-duration_perf_0, …, duration_perf_N

Option 2:
1 Tabelle für eine config_id
Results von {config_id}:
-duration_perf_0, …, duration_perf_N

Abtrahierte Methoden:
- Laden für Visualisierung(
        min_qubits: int, max_qubits: int, qubits_increment: int, qubits_type: str, 
        min_depth: int, max_depth: int, depth_increment: int, depth_type: str, 
        min_shots: int, max_shots: int, shots_increment: int, shots_type: str,
        quantum_frameworks: QFR[]) -> csv
    oder 
        (qubits: int[][], depths: int[][], shots: int[][], quantum_frameworks: QFR[]) -> csv
- Check welche daten schon vorhanden für datengenerierung(
        min_qubits: int, max_qubits: int, qubits_increment: int, qubits_type: str, 
        min_depth: int, max_depth: int, depth_increment: int, depth_type: str, 
        min_shots: int, max_shots: int, shots_increment: int, shots_type: str,
        quantum_frameworks: QFR[], evaluations: int) 
        ->
        qubits: int[][], depths: int[][], shots: int[][], quantum_frameworks: QFR[]
- Convert QUAFEL results and put into model(csv) -> None
