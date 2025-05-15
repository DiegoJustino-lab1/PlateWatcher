# License Plate Recognition Project

Este projeto implementa um sistema de reconhecimento automatizado de placas de veículos utilizando Python, OpenCV e Tesseract. O sistema é dividido em duas partes principais: o backend, que lida com a lógica de reconhecimento e a comunicação com o frontend, e o frontend, que fornece a interface do usuário.

## Estrutura do Projeto

```
license-plate-recognition
├── backend
│   ├── app.py               # Ponto de entrada da aplicação backend
│   ├── CV3T.py              # Lógica de reconhecimento de placas
│   └── requirements.txt      # Dependências do backend
├── frontend
│   ├── index.html           # Página principal do frontend
│   ├── styles
│   │   └── style.css        # Estilos CSS para a interface
│   └── scripts
│       └── main.js          # Lógica JavaScript para interação com a interface
└── README.md                # Documentação do projeto
```

## Requisitos

### Backend

Para executar o backend, você precisará instalar as dependências listadas no arquivo `requirements.txt`. Você pode fazer isso utilizando o seguinte comando:

```
pip install -r requirements.txt
```

### Frontend

O frontend é uma aplicação web simples que pode ser aberta diretamente em um navegador. Não são necessárias dependências adicionais para o frontend.

## Como Executar

1. **Inicie o Backend:**
   - Navegue até o diretório `backend` e execute o arquivo `app.py` para iniciar o servidor.
   - Exemplo: `python app.py`

2. **Abra o Frontend:**
   - Navegue até o diretório `frontend` e abra o arquivo `index.html` em um navegador web.

3. **Utilização:**
   - Acesse a interface do usuário no navegador, onde você poderá capturar vídeo e visualizar os resultados do reconhecimento de placas.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias e correções.

## Licença

Este projeto é licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.