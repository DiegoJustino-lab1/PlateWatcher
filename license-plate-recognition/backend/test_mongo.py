from pymongo import MongoClient

# URL de conexão com o MongoDB Atlas
mongo_url = 'mongodb+srv://grupoupx:minhasenha123@cluster0.1ezhthk.mongodb.net/?retryWrites=true&w=majority'

try:
    # Conecta ao MongoDB
    client = MongoClient(mongo_url)
    db = client['reconhecimento_placas']  # Nome do banco de dados
    collection = db['placas_detectadas']  # Nome da coleção

    # Insere um documento de teste
    test_data = {"placa": "TESTE-1234", "data_hora": "2025-05-15 12:00:00"}
    collection.insert_one(test_data)

    print("Documento inserido com sucesso!")
    print("Bancos de dados disponíveis:", client.list_database_names())
except Exception as e:
    print("Erro ao conectar ou inserir no MongoDB:", e)