from __future__ import annotations
from typing import Dict, Tuple
from .features import FeatureSet, FeatureValue

# Pesos padrão (podem vir de config externa)
DEFAULT_WEIGHTS: Dict[str, float] = {
    # device
    "device_trust": 0.35,
    "emulator_flag": 0.50,
    "velocity_device_switch": 0.25,
    # behavior
    "dwell_time": 0.25,
    "scroll_natural": 0.20,
    "click_burst": 0.35,
    # geo
    "ip_distance": 0.30,
    "proxy_flag": 0.45,
    "geo_velocity": 0.25,
    # biometrics
    "face_match": 0.60,
    "liveness": 0.55,
}

# Regras duras (hard rules) que podem “forçar” decisão
def hard_rules(feature_set: FeatureSet) -> Tuple[bool, str]:
    # Ex.: emulador + proxy forte => block imediato
    emulator = feature_set.device.get("emulator_flag")
    proxy = feature_set.geo.get("proxy_flag")
    if emulator and emulator.value < -0.5 and proxy and proxy.value < -0.5:
        return True, "HARD_BLOCK_EMULATOR_PROXY"
    return False, ""

def weighted_sum(feature_set: FeatureSet, weights: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
    """
    Combina atributos por soma ponderada (valor -1..1) * peso.
    Retorna score_raw e contribuição por feature.
    """
    contributions: Dict[str, float] = {}

    def acc(group: Dict[str, FeatureValue]):
        for k, f in group.items():
            w = weights.get(k, 0.0)
            contributions[k] = f.value * w * max(f.confidence, 0.1)

    acc(feature_set.device)
    acc(feature_set.behavior)
    acc(feature_set.geo)
    acc(feature_set.biometrics)

    score_raw = sum(contributions.values())  # tipicamente na faixa [-Σw, +Σw]
    return score_raw, contributions
