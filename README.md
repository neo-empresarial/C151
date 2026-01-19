# DeepFace Recognition Access Control

Sistema visual de controle de acesso baseado em reconhecimento facial utilizando DeepFace, OpenCV e NiceGUI.

## 🚀 Funcionalidades

- **Reconhecimento Facial em Tempo Real**: Identificação de usuários cadastrados via webcam.
- **Painel Administrativo**: Gestão completa de usuários (adicionar, editar, remover) com fotos e níveis de acesso.
- **Configuração Inicial**: Assistente de primeiro uso para criar o usuário Administrador.
- **Controles de Biometria**: Fluxo de captura, visualização e confirmação de fotos para garantir qualidade no reconhecimento.
- **Múltiplas Fotos**: Suporte para múltiplas fotos por usuário para maior precisão.
- **Serviço de Background**: Executável silencioso que monitora o acesso e bloqueia a tela se necessário.

---

## 💻 Ambiente de Desenvolvimento (Windows)

### Pré-requisitos
- Python 3.10 ou superior.
- Git.
- Webcam conectada.
- [Visual Studio C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (necessário para compilar algumas bibliotecas Python).

### Instalação

1. **Clone o repositório:**
   ```powershell
   git clone <URL_DO_REPOSITORIO>
   cd C151
   ```

2. **Crie e ative o ambiente virtual:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```powershell
   pip install -r requirements.txt
   ```

### Rodando Localmente

**1. Aplicação Principal (Interface de Gestão/Quiosque):**
Esta é a interface onde você cadastra usuários e vê o feedback visual.
```powershell
python main.py
```

**2. Serviço de Background (Proteção):**
Este script roda silenciosamente (ou minimizado) e monitora a câmera.
```powershell
python background_service.py
```

---

## 🛠️ Build (Gerando Executáveis)

O projeto possui scripts PowerShell para gerar os executáveis independentes (`.exe`) para Windows.

**Local dos scripts:** `build_scripts/windows/`

### 1. Construir Aplicação Principal (`DeepFaceRec_Debug.exe`)
Gera o executável com console (para debug) da interface principal.

```powershell
.\build_scripts\windows\build_debug.ps1
```
*Saída gerada em: `dist/DeepFaceRec_Debug.exe`*

### 2. Construir Serviço (`DeepFaceService.exe`)
Gera o executável do serviço de background (sem console).

```powershell
.\build_scripts\windows\build_service.ps1
```
*Saída gerada em: `dist/DeepFaceService.exe`*

---

## Deploy e Distribuição

Para que o sistema funcione corretamente em produção, a estrutura de pastas deve ser mantida.

### Estrutura Recomendada

Crie uma pasta (ex: `C:\DeepFaceAccess`) e coloque os seguintes arquivos:

```text
C:\DeepFaceAccess\
├── DeepFaceRec_Debug.exe   # Aplicação Principal
├── DeepFaceService.exe     # Serviço de Background
└── users.db                # Banco de dados (COMPARTILHADO)
```

> [!IMPORTANT]
> O arquivo `users.db` deve estar na **mesma pasta** dos executáveis. Se o arquivo não existir, o sistema criará um novo automaticamente na primeira execução. Ambos os programas leem e escrevem neste mesmo arquivo.

### Notas sobre o `DeepFaceService`
- Ele roda em **background** e pode adicionar um ícone na bandeja do sistema (Tray Icon).
- Se rodar e fechar imediatamente, verifique se a câmera já não está sendo usada por outro app.
- Para fechar o serviço, procure o ícone na bandeja ou use o Gerenciador de Tarefas.

---

## ⚠️ Solução de Problemas Comuns

### 1. Erro: `can't open camera by index`
Significa que a câmera já está em uso.
- Verifique se você não tem o `main.py` e o `background_service.py` abertos ao mesmo tempo tentando acessar a câmera (o sistema tenta gerenciar isso, mas conflitos podem ocorrer).
- Verifique outros apps (Zoom, Teams).

### 2. Erro de `ModuleNotFoundError` no executável
Geralmente resolvido nos scripts de build. Se persistir, verifique se instalou todas as dependências no `venv` antes de compilar.

### 3. Banco de dados vazio após reiniciar
Certifique-se de que não está rodando o executável de dentro de um arquivo ZIP. Extraia tudo para uma pasta. O banco de dados `users.db` é criado ao lado do executável.

---

## 🧠 Trocando o Modelo de IA

O padrão é configurado no arquivo `src/common/config.py`.
Para trocar (ex: ArcFace, FaceNet, VGG-Face), edite a variável:

```python
MODEL_NAME = 'ArcFace'
```
