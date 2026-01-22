# Codigo Fonte (src/)

Este diretorio contem todo o codigo fonte da aplicacao DeepFace Access Control. A aplicacao e construida utilizando Python 3.10+ e NiceGUI.

## Estrutura

-   **main.py** (na raiz, mas importa daqui): Ponto de entrada da aplicacao. Inicializa a UI e os servicos.
-   **common/**: Modulos compartilhados e utilitarios (Banco de Dados, Configuracao, Seguranca, Logs).
-   **features/**: Logica de negocios central (Motor de Inferencia, Cadastro de Usuarios).
-   **language/**: Arquivos de traducao (i18n).
-   **pages/**: Definicao das interfaces (UI) e rotas.
-   **public/**: Assets estaticos (imagens, icones, sons).
-   **services/**: Servicos singleton que mantem o estado da aplicacao em tempo de execucao.

## Convencoes
-   **Imports**: Sempre use caminhos absolutos a partir da raiz (ex: `from src.common.database import ...`).
-   **Async**: A UI do NiceGUI roda em um loop de eventos. Operacoes pesadas (como reconhecimento facial) devem rodar em threads separadas para nao bloquear a interface.
