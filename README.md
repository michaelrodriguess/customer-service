# Todo List para o Projeto

1. **Configurar o Docker**
   - [OK] Escolher a versão correta do Docker.
   - [OK] Configurar o Docker Compose para rodar o FastAPI com o MongoDB.
   - [OK] Verificar as portas expostas e a rede compartilhada.

2. **Configurar o FastAPI + Uvicorn**
   - [OK] Instalar o FastAPI.
   - [OK] Instalar o Uvicorn.
   - [OK] Configurar um ambiente virtual para o projeto.
   - [OK] Criar um script de inicialização para rodar o FastAPI com Uvicorn.

3. **Criar Arquitetura do Projeto**
   - Estrutura de pastas:
     - `app/` para o código da aplicação.
     - `mongodb/` para a configuração do MongoDB.
     - `tests/` para os testes automatizados.
   - Criar um arquivo `main.py` para o FastAPI.
   - Criar um arquivo `mongodb.py` para a configuração do MongoDB.
   - Estruturar os modelos (`User`, `UpdateUser`) usando Pydantic.

4. **Implementação de Endpoints**
   -  **`POST /users/`**: Recebe dados para criar um novo usuário.
     - Validar os dados usando o modelo `User`.
     - Inserir o usuário no MongoDB.
     - Retornar o ID do novo usuário.
   - **`GET /users/{user_id}`**: Retorna os dados de um usuário específico.
     - Encontrar o usuário pelo `ObjectId`.
     - Retornar os dados do usuário.
     - Retornar 404 se o usuário não for encontrado.
   - **`PUT /users/{user_id}`**: Atualiza os dados de um usuário específico.
     - Recebe dados para atualização.
     - Encontra o usuário pelo `ObjectId`.
     - Atualiza os dados no MongoDB.
   - **`DELETE /users/{user_id}`**: Remove um usuário específico.
     - Encontra o usuário pelo `ObjectId`.
     - Remove o usuário do MongoDB.
     - Retorna confirmação da remoção.

5. **Testes**
   - Escrever testes para cada endpoint (criando, lendo, atualizando, deletando).
   - Testar casos de erro (como dados inválidos, usuários não encontrados).
   - Automatizar testes utilizando `pytest` ou outra ferramenta de testes.

6. **Entrega do MVP (Produto Mínimo Viável)**
   - Validar que todos os endpoints estão funcionando conforme esperado.
   - Realizar testes integrados.
   - Documentar a API (usar FastAPI para gerar documentação automaticamente).
   - Verificar a performance e segurança da aplicação.
   - Entregar o projeto para avaliação.
