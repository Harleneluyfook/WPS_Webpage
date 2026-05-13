"""
utils.py – shared helpers for WPS Streamlit app
"""
from __future__ import annotations
import streamlit as st
from dataclasses import dataclass, field
from typing import List, Optional
import time

# ── Barangay list ─────────────────────────────────────────────────────────────
BAGUIO_BARANGAYS: List[str] = sorted([
    "Abanao-Zandueta-Kayang-Chugum-Otek-Penzola (AZKCO)", "Alfonso Tabora",
    "Ambiong", "Andres Bonifacio", "Apugan-Loakan", "Atab District",
    "Bakakeng Central", "Bakakeng North", "Bal-Marc-Hacienda (Balacbac)",
    "Balsigan", "Bayan Park East", "Bayan Park Village", "Bayan Park West",
    "BGH Compound", "Brookside", "Brookspoint",
    "Cabinet Hill-Teacher's Camp", "Camdas Subdivision", "Camp 7", "Camp 8",
    "Camp Allen", "Campo Filipino", "City Camp Central", "City Camp Lagoon",
    "Country Club Village", "Cresencia Village", "Dagsian (Lower)",
    "Dagsian (Upper)", "Dizon Subdivision", "Dominican Hill-Mirador",
    "Doña Aurora", "Doña Edith Rizal", "Doña Herminia", "East Bayan Park",
    "East Modern site", "Engineers Hill", "Fairview Village",
    "Fort del Pilar", "Gabriela Silang", "General Emilio F. Aguinaldo",
    "General Luna (Lower)", "General Luna (Upper)", "Gibraltar",
    "Greenwater Village", "Guisad Central", "Guisad Sorong",
    "Harrison-Claudio Carantes", "Hillside", "Holy Ghost Extension",
    "Holy Ghost Proper", "Honeymoon-Holy Ghost", "Imelda Village", "Irisan",
    "Jose P. Laurel", "Kabayanihan", "Kagitingan", "Kayang Extension",
    "Kayang-Hilltop", "Kias", "Loakan Liwanag", "Loakan Proper",
    "Lopez Jaena", "Lualhati", "Lucnab", "Magsaysay Central",
    "Magsaysay Lower", "Magsaysay Upper",
    "Malcolm Square-Perfecto (MPS)", "Manuel A. Roxas",
    "Market Subdivision", "Middle Quezon Hill", "Middle Rock Quarry",
    "Military Cut-off", "Mines View Park", "Modern Site (East)",
    "Modern Site (West)", "MRR-Queen of Peace", "North Bayan Park",
    "North Central Aurora Hill", "North Sanctuary", "Outlook Drive",
    "Pacdal", "Padcal Village", "Palo Alto", "Phil-Am", "Pinget",
    "Pinsao Proper", "Pinsao Pilot Project", "Pucsusan",
    "Quezon Hill Proper", "Quezon Hill Upper", "Quirino Hill (Lower)",
    "Quirino Hill (Middle)", "Quirino Hill (Upper)",
    "Quirino-Magsaysay (Upper)", "Rizal Monument Area",
    "Rock Quarry (Lower)", "Rock Quarry (Middle)", "Rock Quarry (Upper)",
    "Saint Joseph Village", "Salud Mitra", "San Antonio Village",
    "San Luis Village", "San Roque Village", "San Vicente",
    "Santa Escolastica", "Santo Niño", "Santo Rosario", "Scout Barrio",
    "Session Road Area", "Slaughter House Area",
    "South Central Aurora Hill", "South Drive", "Sto. Niño Village",
    "Teodora Alonzo", "Trancoville", "Upper Dagsian", "Upper Gen. Luna",
    "Upper Magsaysay", "Upper Market Subdivision", "Upper Quezon Hill",
    "Upper Rock Quarry", "Victoria Village", "West Bayan Park",
    "West Modernsite",
])


# ── Data model ────────────────────────────────────────────────────────────────
@dataclass
class BarangayData:
    id: str
    name: str
    casualties: int = 0
    affected_families: int = 0
    damaged_houses: int = 0
    priority_score: float = 0.0
    normalized_casualties: float = 0.0
    normalized_families: float = 0.0
    normalized_houses: float = 0.0
    rank: int = 0
    disaster: str = "Default"
    last_updated: Optional[float] = None


# ── WSM core ─────────────────────────────────────────────────────────────────
def calculate_wsm(data: List[BarangayData]) -> List[BarangayData]:
    if not data:
        return []

    # Group by disaster
    groups: dict[str, List[BarangayData]] = {}
    for item in data:
        d = item.disaster or "Default"
        groups.setdefault(d, []).append(item)

    results: List[BarangayData] = []

    for group_data in groups.values():
        casualties_vals = [d.casualties for d in group_data]
        families_vals   = [d.affected_families for d in group_data]
        houses_vals     = [d.damaged_houses for d in group_data]

        max_c, min_c = max(casualties_vals, default=0), min(casualties_vals, default=0)
        max_f, min_f = max(families_vals,   default=0), min(families_vals,   default=0)
        max_h, min_h = max(houses_vals,     default=0), min(houses_vals,     default=0)
        range_c = max_c - min_c if max_c != min_c else 0
        range_f = max_f - min_f if max_f != min_f else 0
        range_h = max_h - min_h if max_h != min_h else 0

        processed = []
        for item in group_data:
            if not item.last_updated:
                item.normalized_casualties = 0
                item.normalized_families   = 0
                item.normalized_houses     = 0
                item.priority_score        = 0
                processed.append(item)
                continue

            nc = 0.5 if range_c == 0 else (item.casualties       - min_c) / range_c
            nf = 0.5 if range_f == 0 else (item.affected_families - min_f) / range_f
            nh = 0.5 if range_h == 0 else (item.damaged_houses    - min_h) / range_h
            score = (nc + nf + nh) / 3

            item.normalized_casualties = nc
            item.normalized_families   = nf
            item.normalized_houses     = nh
            item.priority_score        = score
            processed.append(item)

        ranked = sorted(
            processed,
            key=lambda x: (x.priority_score, x.casualties),
            reverse=True,
        )
        for i, item in enumerate(ranked):
            item.rank = i + 1
        results.extend(ranked)

    return results


# ── Urgency helpers ───────────────────────────────────────────────────────────
def get_urgency(score: float) -> dict:
    if score >= 0.7:
        return {"label": "Highest",  "badge": "badge-highest", "emoji": "🔴"}
    if score >= 0.4:
        return {"label": "Urgent",   "badge": "badge-urgent",  "emoji": "🟠"}
    if score >= 0.1:
        return {"label": "Moderate", "badge": "badge-moderate","emoji": "🔵"}
    return     {"label": "Low",      "badge": "badge-low",     "emoji": "⚪"}


def get_recommendation(score: float) -> str:
    if score >= 0.7: return "Immediate response (within 24 hours)"
    if score >= 0.4: return "Urgent (24–48 hours)"
    if score >= 0.1: return "Scheduled (2–3 days)"
    return "Monitoring / delayed response"


# ── Session state initializer ─────────────────────────────────────────────────
def init_session_state():
    if "barangay_list" not in st.session_state:
        st.session_state.barangay_list = [
            BarangayData(id=f"brgy-{i}", name=name, rank=i + 1)
            for i, name in enumerate(BAGUIO_BARANGAYS)
        ]
    if "ranked_data" not in st.session_state:
        st.session_state.ranked_data = calculate_wsm(st.session_state.barangay_list)


def refresh_rankings():
    st.session_state.ranked_data = calculate_wsm(st.session_state.barangay_list)


def get_assessed():
    return [b for b in st.session_state.ranked_data if b.last_updated]


def get_stats():
    assessed = get_assessed()
    return {
        "total_families":       sum(b.affected_families for b in assessed),
        "total_casualties":     sum(b.casualties        for b in assessed),
        "total_damaged_houses": sum(b.damaged_houses    for b in assessed),
        "total_assessed":       len(assessed),
        "highest_priority_name": assessed[0].name if assessed else "None",
    }
