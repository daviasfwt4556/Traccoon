# O frontend é HTML/CSS/JS puro (sem build step nenhum), então só
# precisa de um servidor de arquivos estáticos na frente. O nginx:alpine
# é a opção mais leve pra isso.
FROM nginx:alpine

# Remove o site padrão do nginx e coloca o frontend no lugar.
RUN rm -rf /usr/share/nginx/html/*
COPY . /usr/share/nginx/html

EXPOSE 80
