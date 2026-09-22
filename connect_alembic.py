"""
ALEMBIC DISTILLATION APPARATUS CIRCUIT CONNECTOR (connect_alembic.py)
Directly connects Voynich token streams to 15th-century distillation stages:
1. Cucurbit / Boiler Body    -> TRANSFORM (C)  [qo-, qok-, qot-, ok-, -edy, -eey]
2. Capitellum / Still-Head   -> CONNECT (L)    [daiin, dain, -aiin, -ain]
3. Rostellum / Delivery Beak -> ROUTE (beta)   [-ol/-al switch vs -or/-ar continue]
4. Pelican / Receiver Flask  -> MAINTAIN (P)   [shed-, y, ol, bath circulation]
5. Purge Valve / Coda Seal   -> RESOLVE (R)    [-m, -am, chdam, shedam]
"""

import re
import pandas as pd

class AlembicCircuitConnector:
    def __init__(self):
        self.stages = {
            "CUCURBIT_BOILER": {
                "macrostate": "C",
                "component": "Cucurbit (Boiler Body)",
                "action": "Thermal decoction & vapor generation",
                "markers": ["qo", "qok", "qot", "ok", "edy", "eey"]
            },
            "CAPITELLUM_HEAD": {
                "macrostate": "L",
                "component": "Alembic Head (Still-Head)",
                "action": "Vapor collection & aqueous menstruum buffer",
                "markers": ["daiin", "dain", "aiin", "ain"]
            },
            "ROSTELLUM_BEAK": {
                "macrostate": "BETA",
                "component": "Rostellum (Delivery Siphon / Beak)",
                "action": "Condensate routing (external receiver vs reflux)",
                "markers": ["ol", "al", "or", "ar"]
            },
            "PELICAN_RECEIVER": {
                "macrostate": "P",
                "component": "Pelican Flask / Receiver",
                "action": "Substrate digestion & liquid bath retention",
                "markers": ["shed", "y"]
            },
            "PURGE_SEAL": {
                "macrostate": "R",
                "component": "Purge Valve / Coda Seal",
                "action": "Line-terminal residue flush & extraction vial seal",
                "markers": ["m", "am", "chdam", "shedam"]
            }
        }

    def classify_token(self, raw_token: str) -> dict:
        t = re.sub(r"[^a-z]", "", str(raw_token).lower().strip())
        if not t:
            return {"token": raw_token, "macrostate": "?", "stage": "IDLE", "component": "Void", "action": "None"}

        # 1. Purge Valve / Terminal Coda Seal (strict line-terminal priority)
        if t.endswith(("m", "am")) or t in ["chdam", "shedam"]:
            return {
                "token": t,
                "macrostate": "R",
                "stage": "PURGE_SEAL",
                "component": self.stages["PURGE_SEAL"]["component"],
                "action": self.stages["PURGE_SEAL"]["action"]
            }

        # 2. Capitellum Menstruum Buffer (daiin / -aiin)
        if t in ["daiin", "dain"] or t.endswith(("aiin", "ain")):
            return {
                "token": t,
                "macrostate": "L",
                "stage": "CAPITELLUM_HEAD",
                "component": self.stages["CAPITELLUM_HEAD"]["component"],
                "action": self.stages["CAPITELLUM_HEAD"]["action"]
            }

        # 3. Pelican Receiver / Bath Retention (shed substrate)
        if "shed" in t:
            return {
                "token": t,
                "macrostate": "P",
                "stage": "PELICAN_RECEIVER",
                "component": self.stages["PELICAN_RECEIVER"]["component"],
                "action": self.stages["PELICAN_RECEIVER"]["action"]
            }

        # 4. Cucurbit Boiler Body (active thermal operators)
        if t.startswith(("qo", "qok", "qot", "ok")) or t.endswith(("edy", "eey")):
            return {
                "token": t,
                "macrostate": "C",
                "stage": "CUCURBIT_BOILER",
                "component": self.stages["CUCURBIT_BOILER"]["component"],
                "action": self.stages["CUCURBIT_BOILER"]["action"]
            }

        # 5. Rostellum Delivery Beak (Routing branch: L-switch vs R-continue)
        if t.endswith(("ol", "al", "or", "ar")):
            routing = "Branch redirect to external receiver" if t.endswith(("ol", "al")) else "Continuous reflux circulation"
            return {
                "token": t,
                "macrostate": "BETA",
                "stage": "ROSTELLUM_BEAK",
                "component": self.stages["ROSTELLUM_BEAK"]["component"],
                "action": routing
            }

        # Default: Ambient matrix substrate
        return {
            "token": t,
            "macrostate": "P",
            "stage": "PELICAN_RECEIVER",
            "component": "Ambient Matrix Vessel",
            "action": "Passive carrier vehicle"
        }

    def trace_line(self, line: str) -> pd.DataFrame:
        tokens = [tok for tok in re.split(r"[.\s]+", str(line).strip()) if tok]
        records = [self.classify_token(tok) for tok in tokens]
        return pd.DataFrame(records)

    def evaluate_circuit_closure(self, line: str) -> dict:
        df_trace = self.trace_line(line)
        stages = set(df_trace["stage"].tolist())

        has_boiler = "CUCURBIT_BOILER" in stages
        has_head = "CAPITELLUM_HEAD" in stages
        has_receiver = "PELICAN_RECEIVER" in stages
        has_seal = "PURGE_SEAL" in stages

        is_closed_loop = has_boiler and (has_head or has_receiver) and (has_seal or df_trace.iloc[-1]["macrostate"] in ["R", "P"])

        return {
            "total_tokens": len(df_trace),
            "boiler_active": has_boiler,
            "menstruum_condensed": has_head,
            "substrate_retained": has_receiver,
            "circuit_purged_sealed": has_seal,
            "is_closed_distillation_loop": is_closed_loop,
            "flow_path": " -> ".join(df_trace["macrostate"].tolist())
        }

if __name__ == "__main__":
    connector = AlembicCircuitConnector()
    benchmark_line = "qokedy qokeey or or chkorol otey qokedy lkedy chdy qokchdy qokal chdam"
    print("--- TRACING BENCHMARK RECIPE LINE THROUGH ALEMBIAPPARATUS ---")
    trace_df = connector.trace_line(benchmark_line)
    print(trace_df[["token", "macrostate", "stage", "component"]].to_string(index=False))

    print("\n--- CIRCUIT CLOSURE EVALUATION ---")
    evaluation = connector.evaluate_circuit_closure(benchmark_line)
    for k, v in evaluation.items():
        print(f"{k}: {v}")
