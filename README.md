# DeepFace Recognition Access Control

Sistema visual de controle de acesso baseado em reconhecimento facial utilizando DeepFace, OpenCV e NiceGUI.

## Funcionalidades

- **Reconhecimento Facial em Tempo Real**: Identificação de usuários cadastrados via webcam.
- **Painel Administrativo**: Gestão completa de usuários (adicionar, editar, remover) com fotos e níveis de acesso.
- **Configuração Inicial**: Assistente de primeiro uso para criar o usuário Administrador.
- **Controles de Biometria**: Fluxo de captura, visualização e confirmação de fotos para garantir qualidade no reconhecimento.

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

## 🔒 Serviço de Background (DeepFaceService)

O sistema agora conta com um componente dedicado: **DeepFaceService**. Este é um serviço, execução em System Tray, independente da interface gráfica principal.

### Funcionalidades do Serviço
1.  **Monitoramento Contínuo**: Roda em background, acessando a câmera diretamente.
2.  **API Local (Porta 8080)**: Oferece endpoints para verificação de identidade.
3.  **System Tray**: Ícone na bandeja do sistema para controle básico (Sair).
4.  **Segurança Ativa**:
    - **Bloqueio Visual**: Se um usuário não identificado ou sem permissão for detectado, o serviço pode acionar um bloqueio visual de tela cheia ("ACESSO NEGADO") até que um Administrador seja reconhecido.
    - **Integração**: Outros aplicativos podem simplesmente consultar a API para saber quem está na frente do PC.

### API - Integração
**Endpoint:** `GET http://localhost:8080/verificar_operador`

**Resposta (JSON):**
```json
{
  "status": "sucesso",
  "usuario": "NomeDoUsuario",
  "id": "uuid-do-usuario",
  "funcao": "Admin",
  "confianca": 0.98
}
```

### Como Executar
O serviço pode ser rodado de duas formas:

**1. Via Python (Desenvolvimento):**
```bash
# Requer o ambiente virtual ativado
./venv/bin/python3 src/background_service.py
```

**2. Via Executável Standalone (Produção):**
Após o build, execute o arquivo gerado:
```bash
./dist/DeepFaceService/DeepFaceService
```
*Recomendado configurar este executável para iniciar com o sistema operacional.*

> [!WARNING]
> **Atenção com Caminhos/Diretórios**: 
> Se o executável falhar com erro `ModuleNotFoundError: No module named 'encodings'`, é porque o caminho onde o app está salvo contém caracteres especiais (ex: "Área de trabalho").
> **Solução**: Mova a pasta `dist/DeepFaceService` para um local simples, como `C:\DeepFaceRec` ou `/home/usuario/DeepFaceRec`.

---

## 🔄 Integração com Outros Softwares

O `DeepFaceService` foi desenhado para rodar como um **processo em background**.
Você deve iniciá-lo assim que o computador ligar ou quando seu sistema principal abrir.

**Exemplos de como chamar o executável:**

### Python (subprocess)
```python
import subprocess

# Inicia o serviço sem bloquear o script principal
subprocess.Popen(["C:/DeepFaceRec/DeepFaceService.exe"])
```

### C# (.NET)
```csharp
using System.Diagnostics;

Process.Start("C:\\DeepFaceRec\\DeepFaceService.exe");
```

### Shell / Bash (Linux)
```bash
# O '&' no final libera o terminal
./DeepFaceService &
```

## 🔒 Segurança Ativa
- O sistema bloqueia a tela inteira se uma pessoa não autorizada for detectada por **5 frames seguidos**.
- Para desbloquear:
    1. Um Administrador deve olhar para a câmera.
    2. OU digitar o **PIN de Administrador** na tela de bloqueio.

---

## 🛠️ Build e Distribuição

O projeto possui dois scripts de build separados para gerar executáveis independentes.

### 1. Aplicação Principal (Interface de Gestão)
Gera o `DeepFaceRec`, utilizado para cadastrar usuários e gerenciar o banco de dados.
```bash
./build.sh
# Saída: dist/DeepFaceRec
```

### 2. Serviço de Background (DeepFaceService)
Gera o `DeepFaceService`, o serviço silencioso que deve rodar sempre.
```bash
./build_service.sh
# Saída: dist/DeepFaceService
```

### Notas de Deploy
- O arquivo `users.db` é compartilhado. Se os executáveis estiverem na mesma pasta, eles compartilharão o banco de dados.
- O `DeepFaceService` deve ser iniciado **antes** de qualquer aplicação que dependa da autenticação facial.

## Estrutura do Projeto

- `src/`: Código fonte da aplicação
- `src/pages/`: Interfaces (Login, Dashboard, Setup)
- `src/common/`: Utilitários (Câmera, Banco de Dados, Config)
- `src/features/`: Lógica de negócios (Auth, Inferência)
