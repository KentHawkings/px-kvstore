FROM gcr.io/distroless/python3-debian11

WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["main.py"] 