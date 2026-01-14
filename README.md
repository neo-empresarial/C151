# DeepFace Recognition Access Control

Sistema visual de controle de acesso baseado em reconhecimento facial utilizando DeepFace, OpenCV e NiceGUI.

## Funcionalidades

- **Reconhecimento Facial em Tempo Real**: Identificação de usuários cadastrados via webcam.
- **Painel Administrativo**: Gestão completa de usuários (adicionar, editar, remover) com fotos e níveis de acesso.
- **Configuração Inicial**: Assistente de primeiro uso para criar o usuário Administrador.
- **Controles de Biometria**: Fluxo de captura, visualização e confirmação de fotos para garantir qualidade no reconhecimento.
- **Modo Nativo**: Executável desktop (Linux) sem necessidade de navegador externo.

## Como Usar

1. **Configuração**: Na primeira execução, se não houver usuários, você será direcionado para `/setup`. Crie o Admin.
2. **Login/Reconhecimento**: A tela inicial mostra o feed da câmera.
    - Se o rosto for reconhecido, o acesso é liberado (ou admin logado).
    - Se falhar, use o "Entrar com PIN".
3. **Dashboard (Admin)**:
    - **Adicionar Usuário**: Clique em "Adicionar Usuário", preencha os dados e capture a foto. É obrigatório **Confirmar** a foto.
    - **Editar Usuário**: Altere nome/PIN ou clique em "Alterar Foto" para atualizar a biometria.
    - **Remover**: Exclui o usuário permanentemente.

## Instalação e Build

### Dependências
```bash
sudo apt install libgirepository1.0-dev libcairo2-dev python3-dev
pip install -r requirements.txt
```

### Rodar Localmente
```bash
python main.py
```

### Gerar Executável
Execute o script de build:
```bash
./build.sh
```
O executável será gerado em `dist/DeepFaceRec/DeepFaceRec`.

## Estrutura do Projeto

- `src/`: Código fonte da aplicação
- `src/pages/`: Interfaces (Login, Dashboard, Setup)
- `src/common/`: Utilitários (Câmera, Banco de Dados, Config)
- `src/features/`: Lógica de negócios (Auth, Inferência)
