# Imagem base com PHP e Apache
FROM php:8.1-apache

# Instalar extensões PHP para PostgreSQL
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Copiar os arquivos do site para o diretório público do Apache
COPY ./public /var/www/html/

# Expor a porta do Apache
EXPOSE 80
