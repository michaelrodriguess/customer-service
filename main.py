from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do FastAPI
app = FastAPI()

# Conectar ao MongoDB usando a variável de ambiente MONGO_URI
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)

db = client["users_db"]  # Banco de dados "users_db"
users_collection = db["users"]  # Coleção de "users"

# Definir o modelo Pydantic para os dados de entrada
class User(BaseModel):
    name: str
    email: str

@app.post("/users/")
async def create_user(user: User):
    user_data = user.dict()
    result = users_collection.insert_one(user_data)  # Inserir o usuário no MongoDB
    return {"id": str(result.inserted_id)}  # Retornar o ID do novo usuário

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {"name": user["name"], "email": user["email"]}  # Retornar os dados do usuário
    return {"error": "User not found"}  # Caso não encontre o usuário
