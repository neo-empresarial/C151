# Scripts de Build (Windows)

Scripts PowerShell para empacotamento, distribuição e criação de instaladores da aplicação.

## Pré-requisitos
-   **Python 3.10+** com ambiente virtual configurado.
-   **Inno Setup 6** (Necessário para gerar o instalador .exe).
    -   Download: [jrsoftware.org](https://jrsoftware.org/isdl.php)

## Como Gerar o Instalador

Para gerar o instalador completo (recomendado para distribuição):

1.  Abra o terminal na raiz do projeto.
2.  Execute o script unificado:
    ```powershell
    .\build_scripts\windows\build_unified.ps1
    ```

Este script irá:
1.  Limpar builds anteriores.
2.  Compilar a aplicação usando **PyInstaller** (modo pasta/onedir).
3.  Copiar assets e atalhos necessários.
4.  **Automaticamente compilar o instalador** usando o Inno Setup.

**Saída**:
-   O instalador estará em: `dist/FaceRecon_Setup.exe`
-   A pasta da aplicação (portátil) estará em: `dist/FaceRecon-V0/`

---

## Detalhes dos Scripts

### build_unified.ps1 
-   **Função**: Script completo de build e packaging.
-   **Processo**:
    -   Gera a aplicação contida em pasta (`dist/FaceRecon-V0`).
    -   Verifica se o Inno Setup está instalado.
    -   Se sim, gera o arquivo de instalação `FaceRecon_Setup.exe`.
-   **Uso**: Para criar a versão final para entrega ao cliente.

### create_shortcut.ps1
-   **Função**: Script auxiliar copiado para a pasta de distribuição.
-   **Uso**: Cria atalho na área de trabalho se executado manualmente pelo usuário (caso não use o instalador).
