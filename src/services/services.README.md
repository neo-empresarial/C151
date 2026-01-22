# src/services

Este diretorio contem os "Gerenciadores de Estado" (Singletons) da aplicacao. Eles sao instanciados uma unica vez em `services.py` e importados em varias partes do sistema.

## services.py
Ponto central de instanciacao.
-   Cria `camera_manager`, `db_manager`, e `engine`.
-   Mantem referencias globais para esses objetos.

### Ciclo de Vida
1.  **Startup**: Ao iniciar, `main.py` chama `start_services()`, que inicializa a camera e a thread de IA.
2.  **Runtime**: As paginas acessam os servicos (ex: `camera_manager.get_frame()`).
3.  **Shutdown**: Ao fechar, `stop_services()` libera a camera e encerra threads.

## Por que usar Servicos?
No NiceGUI (e web apps em geral), o estado persistente entre requisicoes ou acessivel por multiplas rotas deve ser gerenciado fora do ciclo de vida da pagina. Os servicos garantem que a camera nao seja reaberta a cada navegacao, e que o modelo de IA permaneca carregado na memoria.
