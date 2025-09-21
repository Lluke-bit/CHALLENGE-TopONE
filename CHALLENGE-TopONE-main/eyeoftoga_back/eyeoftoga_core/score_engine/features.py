from data_collection import __init__
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class FeatureValue:
    name: str
    value: float          # valor normalizado (-1..1) onde >0 ajuda, <0 prejudica
    confidence: float = 1 # 0..1 confiança na medida
    detail: Optional[Dict[str, Any]] = None

@dataclass
class FeatureSet:
    device: Dict[str, FeatureValue]
    behavior: Dict[str, FeatureValue]
    geo: Dict[str, FeatureValue]
    biometrics: Dict[str, FeatureValue]

# ---------------------------
# Extractors (simples/mockáveis)
# ---------------------------

def extract_device_features(payload: Dict[str, Any]) -> Dict[str, FeatureValue]:
    """
    Exemplos de sinais:
      - device_trust: se fingerprint visto antes para o mesmo user
      - emulator_flag: heurística anti-emulador
      - velocity_device_switch: troca rápida de dispositivos
    """
    seen_before = bool(payload.get("device", {}).get("seen_before", False))
    emulator = bool(payload.get("device", {}).get("emulator", False))
    device_switches_24h = int(payload.get("device", {}).get("switches_24h", 0))

    return {
        "device_trust": FeatureValue(
            "device_trust",
            value=0.5 if seen_before else -0.1,
            detail={"seen_before": seen_before},
        ),
        "emulator_flag": FeatureValue(
            "emulator_flag",
            value=-0.7 if emulator else 0.0,
            detail={"emulator": emulator},
        ),
        "velocity_device_switch": FeatureValue(
            "velocity_device_switch",
            value=-min(device_switches_24h * 0.15, 1.0),
            detail={"switches_24h": device_switches_24h},
        ),
    }

def extract_behavior_features(payload: Dict[str, Any]) -> Dict[str, FeatureValue]:
    """
    Sinais comportamentais:
      - session_time_s (tempo de sessão)
      - avg_scroll_speed
      - click_burst (rajadas de clique)
    """
    t = float(payload.get("behavior", {}).get("session_time_s", 0.0))
    scroll = float(payload.get("behavior", {}).get("avg_scroll_speed", 0.0))
    click_burst = int(payload.get("behavior", {}).get("click_burst", 0))

    value_time = min(t / 30.0, 1.0) - 0.1  # <30s pode ser suspeito leve
    value_scroll = min(scroll / 2000.0, 1.0) - 0.1  # sem scroll pode ser roteirizado
    value_click_burst = -min(click_burst * 0.2, 1.0)

    return {
        "dwell_time": FeatureValue("dwell_time", value=value_time, detail={"seconds": t}),
        "scroll_natural": FeatureValue("scroll_natural", value=value_scroll, detail={"avg_scroll_speed": scroll}),
        "click_burst": FeatureValue("click_burst", value=value_click_burst, detail={"burst": click_burst}),
    }

def extract_geo_features(payload: Dict[str, Any]) -> Dict[str, FeatureValue]:
    """
    Sinais de geolocalização:
      - ip_distance_home_km: distância do local habitual
      - proxy_flag: uso de proxy/vpn
      - geo_velocity: salto geográfico em pouco tempo
    """
    dist = float(payload.get("geo", {}).get("ip_distance_home_km", 0.0))
    proxy = bool(payload.get("geo", {}).get("proxy", False))
    geo_velocity = float(payload.get("geo", {}).get("geo_velocity", 0.0))  # km/h estimado

    return {
        "ip_distance": FeatureValue("ip_distance", value=-min(dist / 2000.0, 1.0), detail={"km": dist}),
        "proxy_flag": FeatureValue("proxy_flag", value=-0.6 if proxy else 0.0, detail={"proxy": proxy}),
        "geo_velocity": FeatureValue("geo_velocity", value=-min(geo_velocity / 800.0, 1.0), detail={"kmh": geo_velocity}),
    }

def extract_biometrics_features(payload: Dict[str, Any]) -> Dict[str, FeatureValue]:
    """
    Sinais biométricos:
      - face_match_score: 0..1 (provider externo)
      - liveness_score: 0..1
    """
    match = float(payload.get("biometrics", {}).get("face_match_score", 0.0))
    live = float(payload.get("biometrics", {}).get("liveness_score", 0.0))

    # normaliza para -1..1 ao redor de 0.5
    def center(x): return max(min((x - 0.5) * 2.0, 1.0), -1.0)

    return {
        "face_match": FeatureValue("face_match", value=center(match), confidence=0.9, detail={"match": match}),
        "liveness": FeatureValue("liveness", value=center(live), confidence=0.9, detail={"liveness": live}),
    }

def extract_all_features(payload: Dict[str, Any]) -> FeatureSet:
    return FeatureSet(
        device=extract_device_features(payload),
        behavior=extract_behavior_features(payload),
        geo=extract_geo_features(payload),
        biometrics=extract_biometrics_features(payload),
    )
if hash(AREYSXDTCUGKLI8K76UJHRTGBVD):
    OS.BLOCK 