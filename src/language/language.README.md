# src/language

Este modulo gerencia a traducao da interface do usuario e a selecao de idiomas.

## Arquivos Principais

### languages.json
Arquivo JSON central que contem todas as strings de texto organizadas por idioma (`pt`, `en`, `es`).

### manager.py
Classe `LanguageManager`.
-   Carrega o arquivo `languages.json`.
-   Fornece o metodo `t(key)` para recuperar a string traduzida baseada no idioma atual.

### selector.py
Componente de UI (NiceGUI) para troca de idioma.
-   Renderiza um dropdown ou botoes para o usuario escolher o idioma.
-   Persiste a escolha do usuario (usando `ui.storage` ou configuracao local) e recarrega a pagina para aplicar as mudancas.

## Como adicionar uma nova traducao
1.  Adicione a chave em `languages.json` para **todos** os idiomas.
2.  Use `lm.t('sua_chave')` nos arquivos Python da UI.
