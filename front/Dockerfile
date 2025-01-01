# Используем образ Node.js 18
FROM node:18

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь код проекта в контейнер
COPY . .

# Собираем Angular проект
RUN npm run build --prod

# Указываем порт, на котором будет работать приложение
EXPOSE 80

# Команда запуска на порту 80
CMD ["npm", "start", "--", "--host", "0.0.0.0", "--port", "80"]
