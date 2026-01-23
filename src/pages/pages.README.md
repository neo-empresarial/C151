# src/pages

Contem a definicao das telas da aplicacao usando NiceGUI.

## Estrutura de Telas

### landing/ (Rota /)
-   Tela inicial do modo padrao.
-   Oferece navegacao para Dashboard ou Login Facial.

### login/ (Rota /recognition)
-   Tela de reconhecimento facial.
-   Mostra o feed da camera.
-   Exibe o nome do usuario identificado.
-   Possui fluxo de fallback para entrada via PIN.

### dashboard/ (Rota /dashboard)
-   Painel Administrativo.
-   Listagem de usuarios (Tabela).
-   Adicao/Edicao de usuarios.
-   Visualizacao de fotos cadastradas.
-   Requer autenticacao (simulada por flag de admin) ou acesso direto via flag `--ManageUsers`.

### settings/ (Rota /settings)
-   Configuracoes gerais do sistema.
-   **Database**: Configuracao de conexao e **Secret Key**.
-   **Face Recognition**: Ajuste de limiares (threshold), modelos e liveness.
-   **Camera**: Selecao de dispositivo de entrada.
