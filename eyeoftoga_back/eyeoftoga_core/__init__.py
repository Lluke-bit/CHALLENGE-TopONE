import hashlib
import json
import time
import psutil
import device_info
import ip_location
import session_behavior
import storage_adapter

# Relatório completo
if __name__ == "__main__":
    # Inicializa o SDK
    sdk = device_info.DeviceEnvironmentSDK()
    monitor = storage_adapter.RealTimeMonitor()
    
    print("🎯 EyeOfToga - Monitor de Comportamento em Tempo Real")
    print("=" * 60)
    print("Este programa vai capturar suas interações em TODA A TELA:")
    print("• Cliques do mouse em qualquer lugar")
    print("• Movimentos do mouse em qualquer lugar") 
    print("• Teclas pressionadas")
    print("• Scroll")
    print()
    print(f"Tela detectada: {monitor.screen_width}x{monitor.screen_height}")
    print(f"Monitores: {len(monitor.monitors)}")
    for i, m in enumerate(monitor.monitors):
        print(f"  Monitor {i+1}: {m['width']}x{m['height']} at ({m['x']}, {m['y']})")

    # Coleta todos os dados
    print("Coletando dados do dispositivo e ambiente...")
    all_data = sdk.collect_all_data()
    
    # Exibe os dados em formato JSON
    print("\n=== DADOS COLETADOS ===")
    print(json.dumps(all_data, indent=2, ensure_ascii=False))

    ip_teste = "8.8.8.8"  # IP do Google DNS para teste
    session_id = "sess_" + hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    relatorio = ip_location.IPLocationSDK.generate_comprehensive_report(ip_teste, session_id)
    
    print(f"\n=== RELATÓRIO COMPLETO ===")
    print(f"Risco: {relatorio['security_analysis']['risk_level'].upper()}")
    print(f"Duração da sessão: {relatorio['summary']['session_duration_minutes']:.2f} minutos")
    print(f"Tentativas de auth: {relatorio['summary']['total_auth_attempts']}")
    print(f"Localização detectada: {'Sim' if relatorio['summary']['location_detected'] else 'Não'}")# Exporta para diferentes formatos

    # Análise comportamental da sessão
    behavior_analysis = sdk.get_session_behavior_analysis(session_id)
    print(f"   📊 Total de eventos: {behavior_analysis['total_events']}")
    print(f"   ⏱️  Duração da sessão: {behavior_analysis['session_duration_seconds']:.1f}s")
    print(f"   🖱️  Total de cliques: {behavior_analysis['click_patterns']['total_clicks']}")
    print(f"   😴 Tempo total inativo: {behavior_analysis['idle_analysis']['total_idle_time_seconds']:.1f}s")
    print(f"   📈 Req/min da sessão: {behavior_analysis['request_metrics']['requests_per_minute']}")
    
    # Relatório de performance dos endpoints
    performance_report = sdk.get_endpoint_performance_report()
    print(f"\n   🌐 Endpoints monitorados: {performance_report['summary']['total_endpoints']}")
    print(f"   ✅ Taxa de sucesso global: {performance_report['summary']['global_success_rate']:.1f}%")
    print(f"   📊 Total de requisições: {performance_report['summary']['total_requests']}")
    
    # Métricas em tempo real
    real_time = sdk.get_real_time_metrics()
    print(f"\n   🔴 Sessões ativas: {real_time['active_sessions']}")
    print(f"   ⚡ Req/min atual: {real_time['current_requests_per_minute']}")
    print(f"   ⚡ Req/seg atual: {real_time['current_requests_per_second']}")
    
    # 7. Demonstrar análise detalhada
    print("\n7. Análise detalhada dos dados coletados...")
    
    # Top endpoints mais usados
    print("\n   🔝 Top 3 Endpoints Mais Usados:")
    for i, endpoint in enumerate(performance_report['top_endpoints_by_usage'][:3], 1):
        print(f"      {i}. {endpoint['method']} {endpoint['endpoint']} "
              f"({endpoint['total_requests']} req, {endpoint['success_rate']}% sucesso)")
    
    # Sequência de ações do usuário
    print(f"\n   📋 Últimas 5 Ações do Usuário:")
    for i, event in enumerate(behavior_analysis['user_sequence'][-5:], 1):
        timestamp = event['timestamp'].split('T')[1][:8]  # Só o horário
        print(f"      {i}. {timestamp} - {event['event_type'].upper()} "
              f"{'em ' + event['element_id'] if event['element_id'] else ''}")
    
    # Períodos de inatividade
    idle_periods = behavior_analysis['idle_analysis']['idle_periods']
    if idle_periods:
        print(f"\n   😴 Períodos de Inatividade Detectados:")
        for i, period in enumerate(idle_periods, 1):
            print(f"      {i}. {period['duration_seconds']:.1f}s de inatividade")
    
    # 8. Relatório JSON completo
    print("\n8. Gerando relatório completo em JSON...")
    
    complete_report = {
        "session_analysis": behavior_analysis,
        "endpoint_performance": performance_report,
        "real_time_metrics": real_time,
        "analysis_summary": {
            "user_engagement_score": session_behavior.calculate_engagement_score(behavior_analysis),
            "performance_score": session_behavior.calculate_performance_score(performance_report),
            "security_indicators": session_behavior.analyze_security_indicators(session_id, behavior_analysis)
        }
    }
    input("Pressione Enter para iniciar...")
    monitor.start_monitoring()
    input("Pressione ESC para parar...")
    monitor.stop_monitoring()
    print("\n=== EXPORT JSON ===")
    print(sdk.export_data('json'))
    
    print("\n=== EXPORT CSV ===")
    print(sdk.export_data('csv'))