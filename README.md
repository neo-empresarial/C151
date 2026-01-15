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

## 🔒 Serviço Secreto de Biometria (API Local)

O projeto inclui um "Serviço de Background" (`src/background_service.py`) que roda oculto no System Tray e expõe uma API Local para que **outros aplicativos** consultem a identidade do operador atual.

### Como Iniciar
```bash
python src/background_service.py
```
*O app iniciará minimizado. Um ícone aparecerá na bandeja do sistema.*

### 📡 Integração (Como chamar de outro App)
Qualquer linguagem capaz de fazer requisições HTTP pode consultar o serviço.

**Endpoint:** `GET http://localhost:8080/verificar_operador`

#### Exemplo de Resposta (JSON):
```json
{
  "status": "sucesso",
  "usuario": "Bernardo",
  "id": "1234-5678",
  "funcao": "Admin",
  "confianca": 0.98
}
```
*Se ninguém for detectado:* `{"status": "nenhum_usuario", "usuario": null}`

### Exemplos de Código

#### Python (Requests)
```python
import requests

try:
    resp = requests.get("http://localhost:8080/verificar_operador")
    dados = resp.json()
    
    if dados['usuario']:
        print(f"Usuário Identificado: {dados['usuario']} ({dados['funcao']})")
    else:
        print("Nenhum usuário na frente da câmera.")
except:
    print("Erro: O serviço de biometria não está rodando.")
```

#### C# (.NET)
```csharp
using System.Net.Http;
using System.Threading.Tasks;

public async Task VerificarBiometria()
{
    using (HttpClient client = new HttpClient())
    {
        try 
        {
            string resposta = await client.GetStringAsync("http://localhost:8080/verificar_operador");
            // Parse o JSON aqui (ex: Newtonsoft.Json ou System.Text.Json)
            Console.WriteLine(resposta);
        }
        catch 
        {
            Console.WriteLine("Serviço indisponível");
        }
    }
}
```

#### cURL (Terminal)
```bash
curl http://localhost:8080/verificar_operador
```

### 🚨 Recurso "Access Denied"
O serviço possui monitoramento ativo. Se um usuário **NÃO-ADMIN** for detectado, o serviço abre automaticamente uma tela cheia de "ACESSO NEGADO" piscante, bloqueando a visão até que um Administrador seja reconhecido pela câmera.


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
