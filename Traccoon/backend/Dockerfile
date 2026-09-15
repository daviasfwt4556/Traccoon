# Imagem enxuta com Python 3.12 (slim = sem as ferramentas de build que
# a gente não precisa, imagem final bem menor).
FROM python:3.12-slim

WORKDIR /app

# Copia só o requirements.txt primeiro: se o código mudar mas as
# dependências não, o Docker reaproveita essa camada em cache e o build
# fica bem mais rápido.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Agora copia o resto do código do backend.
COPY . .

EXPOSE 5000

# app.py já sobe com host="0.0.0.0" (necessário pra ser acessível de
# fora do container) e porta 5000, então basta rodar direto.
CMD ["python", "app.py"]
