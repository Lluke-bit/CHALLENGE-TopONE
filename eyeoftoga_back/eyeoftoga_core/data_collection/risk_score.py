from ip_location import IPLocationSDK, AuthenticationData, AuthMethod, AuthResult, session_id
from device_info import DeviceEnvironmentSDK

class RiskScorer:
    def __init__(self):
        self.ip_sdk = IPLocationSDK()
        self.device_sdk = DeviceEnvironmentSDK()

    def calcular_score(self, ip: str, session_id: str, monitor_summary: dict, auth_data: AuthenticationData = None):
        score = 0
        risk_factors = []

        # --- Geolocalização ---
        geo = self.ip_sdk.get_ip_location(ip)
        if geo:
            if geo.country_code != "BR":
                score += 50
                risk_factors.append("Acesso de fora do Brasil")
            if geo.is_proxy or geo.is_vpn:
                score += 40
                risk_factors.append("Uso de proxy/VPN detectado")

        # --- Atividade ---
        if monitor_summary:
            nivel = monitor_summary.get("activity_level", "")
            if nivel == "Muito Alta":
                score += 30
                risk_factors.append("Atividade muito alta (cliques/teclas)")
            elif nivel == "Nenhuma" and monitor_summary.get("session_duration_seconds", 0) > 300:
                score += 20
                risk_factors.append("Sessão longa sem atividade")

        # --- Autenticação ---
        if auth_data and auth_data.consecutive_failures > 0:
            score += 10 * auth_data.consecutive_failures
            risk_factors.append(f"{auth_data.consecutive_failures} falhas consecutivas de autenticação")

        # --- Dispositivo ---
        device_type = self.device_sdk.detect_device_type()
        if device_type in ["container", "vm"]:
            score += 25
            risk_factors.append(f"Dispositivo suspeito ({device_type})")

        return {
            "score": score,
            "risk_factors": risk_factors,
            "risk_level": self._nivel_risco(score)
        }

    def _nivel_risco(self, score: int) -> str:
        if score >= 100:
            return "high"
        elif score >= 50:
            return "medium"
        else:
            return "low"
