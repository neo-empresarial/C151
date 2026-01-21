# DeepFace Recognition Access Control

Sistema visual de controle de acesso baseado em reconhecimento facial utilizando DeepFace, OpenCV e NiceGUI.

## 🚀 Funcionalidades

- **Reconhecimento Facial em Tempo Real**: Identificação de usuários cadastrados via webcam.
- **Painel Administrativo**: Gestão completa de usuários (adicionar, editar, remover) com fotos e níveis de acesso.
- **Configuração Inicial**: Assistente de primeiro uso para criar o usuário Administrador.
- **Controles de Biometria**: Fluxo de captura, visualização e confirmação de fotos para garantir qualidade no reconhecimento.
- **Múltiplas Fotos**: Suporte para múltiplas fotos por usuário para maior precisão.
- **Internacionalização (i18n)**: Suporte completo para múltiplos idiomas (Português, Inglês e Espanhol).
- **Interface Moderna**: Design com Glassmorphism, temas Claro/Escuro e controles de janela integrados.
- **Serviço de Background**: Executável silencioso que monitora o acesso e bloqueia a tela se necessário.

---

## 🛠️ Build e Instalação (Windows)

Para obter a **melhor performance de inicialização** (instantânea), recomendamos o **Modo Pasta**. O Executável Único é portátil, mas demora ~40s para abrir.

### 1. Build Modo Pasta (Recomendado - Rápido)
Gera uma pasta com o aplicativo "instalado". Inicia em 3-5 segundos.

```powershell
.\build_scripts\windows\build_folder.ps1
```
Isso criará a pasta `dist/DeepFaceRec_Unified`.

**Criar Atalho na Área de Trabalho**:
```powershell
.\build_scripts\windows\create_shortcut.ps1
```
Isso cria um ícone "Biometria" no seu Desktop.

### 2. Build Arquivo Único (Modo Portátil - Lento)
Gera `dist/DeepFaceRec_Unified.exe`. Ideal para pen-drives, mas demora cerca de **1 minuto** para extrair e iniciar.

```powershell
.\build_scripts\windows\build_unified.ps1
```

---

## 🚀 Executando a Aplicação (CLI)

O executável unificado (`DeepFaceRec_Unified.exe`) suporta diferentes modos de inicialização via linha de comando:

### Modos de Uso

**1. Modo Padrão (Landing Page)**
Abre a tela inicial com opções de navegação.
```powershell
.\DeepFaceRec_Unified.exe
```

**2. Gestão de Usuários (Dashboard)**
Abre diretamente o painel administrativo.
```powershell
.\DeepFaceRec_Unified.exe --ManageUsers
```

**3. Reconhecimento Facial (Login)**
Abre diretamente a tela de reconhecimento/login.
```powershell
.\DeepFaceRec_Unified.exe --FaceRecognition
```

**4. Serviço Oculto (Hidden Camera)**
Monitoramento silencioso em background. A janela fica **invisível** e só aparece se detectar uma pessoa não autorizada.
```powershell
.\DeepFaceRec_Unified.exe --HiddenCam
```

### Configurações Extras

**Timeout (Auto-Kill)**
Fecha o aplicativo automaticamente após X segundos.
```powershell
.\DeepFaceRec_Unified.exe --HiddenCam --timeout 60
```

**Regra de Segurança (3 Strikes)**
No modo `--HiddenCam`:
- Se uma pessoa **não autorizada** (ou desconhecida) for detectada **3 vezes consecutivas**, a tela de ALERTA VERMELHO ("ACESSO NEGADO") abre em **Tela Cheia**.
- Se um **Administrador** for detectado, o contador zera e a tela se esconde novamente.

---

## 📂 Estrutura de Pastas para Deploy

Para rodar em outro computador **sem internet**:

1. Copie o arquivo `DeepFaceRec_Unified.exe`.
2. (Opcional) Copie o `users.db` se quiser manter os usuários já cadastrados.

O executável já contém:
- Python e bibliotecas.
- Modelos de IA (DeepFace/FaceNet/MiniFASNet).
- Interface Web (NiceGUI).

**Nota**: Na primeira execução, o app pode levar até 1 minuto para extrair os arquivos temporários antes de exibir a **Tela de Carregamento**. Isso é normal para executáveis compactados.

---

## 🛠️ Ambiente de Desenvolvimento (Windows)

### Instalação
1. Clone o repositório.
2. Crie um venv: `python -m venv venv`
3. Ative: `.\venv\Scripts\activate`
4. Instale: `pip install -r requirements.txt`

### Rodando Localmente
```powershell
python main.py
```

---

## 🧠 Configuração do Modelo
O modelo padrão de IA é definido em `src/common/config.py`.
```python
MODEL_NAME = 'ArcFace'
```
