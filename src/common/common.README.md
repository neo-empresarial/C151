# src/common

Utilitarios, configuracoes e classes compartilhadas por toda a aplicacao.

## Arquivos e Modulos

### config.py
Carrega e gerencia as configuracoes globais (do arquivo `db_config.json` e variaveis de ambiente). Contem constantes como dimensoes da janela, modelos de IA padrao, etc.

### database.py
Gerenciador de Banco de Dados (DatabaseManager).
-   Abstrai o acesso SQL (SQLAlchemy).
-   Gerencia conexoes SQLite e PostgreSQL.
-   Implementa migracoes de schema automaticas.
-   Criptografa/Descriptografa dados sensiveis automaticamente.

### security.py
Criptografia e Seguranca.
-   Wrapper para `cryptography.fernet`.
-   Gerencia a `SECRET_KEY` (carregamento, salvamento, validacao).
-   Criptografia de PINs e Embeddings faciais.

### theme.py
Gerenciamento de Tema e UI Global.
-   Controle Dark/Light mode.
-   **Loading Overlay**: A tela de carregamento que aparece durante operacoes pesadas ou inicializacao.

### styles.py
Definicoes de estilos CSS, cores e classes utilitarias usadas pelo NiceGUI para manter a identidade visual (Glassmorphism, paleta de cores).

### camera.py
Gerenciador de Camera (CameraManager).
-   Acessa a webcam (OpenCV `cv2.VideoCapture`).
-   Fornece frames para a UI (MJPEG stream) e para o `InferenceEngine`.
-   Trata reconexao automatica e erros de dispositivo.

### models.py
Definicoes das tabelas do Banco de Dados (SQLAlchemy Models).
-   `User`: Dados do usuario (Nome, PIN criptografado, Nivel de Acesso).
-   `FaceEmbedding`: Vetores faciais (embeddings) e fotos originais (blobs) criptografados.

### loading_screen.py
(Legado ou Auxiliar) Utilitarios para telas de espera especificas ou componentes de loading localizados.

### logger.py
Configuracao do sistema de logs (logging). Formata a saida do console para facilitar debugging.

### state.py
Gerenciamento de estado simples ou variaveis globais de sessao (se usado).

### utils.py
Pequenas funcoes auxiliares de uso geral.
