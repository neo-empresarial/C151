# Common (Comum)

Utilitários e configurações transversais da aplicação.

- `camera.py`: Gerenciamento de thread de captura de vídeo (OpenCV) para garantir performance sem bloquear a UI.
- `database.py`: Gerenciador SQLite. Lida com persistência de usuários, embeddings e imagens.
- `config.py`: Constantes globais (índice da câmera, caminhos).
- `state.py`: Estado global mutável da aplicação (usuário atual, flag de admin).
- `theme.py`: Definições de tema e cores.
