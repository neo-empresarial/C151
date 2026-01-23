# src/features

Contem a logica central, regras de negocio e features especificas da aplicacao.

## Submodulos

### inferencia/
O motor de Inteligencia Artificial para reconhecimento facial.
-   **engine.py**: `InferenceEngine`. Roda em background, processa frames da camera, detecta rostos, calcula embeddings e compara com o banco de dados.
    -   Gerencia o ciclo de vida do modelo DeepFace.
    -   Implementa cache de embeddings para performance.
-   **liveness/**: Modulo de deteccao de vivacidade (Anti-Spoofing). Verifica se o rosto e real ou uma fraude (foto/tela).

### cadastro/
Logica e UI para o registro de novos usuarios.
-   **ui_cadastro.py**: Interface do wizard de cadastro (Passo 1: Nome/PIN, Passo 2: Fotos).
-   **controller**: Gerencia a captura de frames validos (verificando qualidade, tamanho do rosto, centralizacao).

### auth/
Gerenciamento de autenticacao administrativa.
-   Verifica se o usuario atual possui permissoes de Admin para acessar o Dashboard.
-   Gerencia sessao ou estado de login administrativo (se aplicavel).
