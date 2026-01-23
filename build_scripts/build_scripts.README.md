# Scripts de Build (Windows)

Scripts PowerShell para empacotamento e distribuicao da aplicacao.

## Scripts Disponiveis

### build_folder.ps1 (Recomendado)
-   **Comando**: PyInstaller com `--onedir`.
-   **Saida**: Pasta `dist/DeepFaceRec_Unified/`.
-   **Vantagem**: Inicializacao instantanea. Arquivos ja descompactados.
-   **Uso**: Desenvolvimento e implantacao fixa.

### build_unified.ps1
-   **Comando**: PyInstaller com `--onefile`.
-   **Saida**: Arquivo `dist/DeepFaceRec_Unified.exe`.
-   **Vantagem**: Portabilidade (um unico arquivo).
-   **Desvantagem**: Lento para iniciar (extrai arquivos para `%TEMP%` a cada execucao).

### build_debug.ps1
-   **Comando**: PyInstaller com `--console`.
-   **Saida**: `dist/DeepFaceRec_Debug.exe`.
-   **Uso**: Debugging. Mantem uma janela de terminal aberta para visualizar erros e prints.

### create_shortcut.ps1
-   Auxiliar para o modo pasta.
-   Cria um atalho na Area de Trabalho apontando para o executavel dentro da pasta `dist`.
