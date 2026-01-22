# Assets Publicos (src/public/)

Arquivos estaticos servidos pelo servidor web do NiceGUI.

## Conteudo
-   **images/**: Logotipos, placeholders e backgrounds.
    -   `certi/`: Logotipos especificos da Fundacao Certi.
-   **icons/**: Icones de aplicacao (ex: `.ico` para o executavel Windows).
-   **sounds/**: Efeitos sonoros (sucesso, erro, alerta).

## Uso no Codigo
Para usar uma imagem deste diretorio no codigo Python:
```python
ui.image('/src/public/images/nome_da_imagem.png')
```
Sempre comece com `/src` pois e onde o diretorio estatico e montado em `main.py`.
