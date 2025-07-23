FROM python:3.11-slim as builder

RUN mkdir /data && chown 65532:65532 /data

FROM gcr.io/distroless/python3-debian11

WORKDIR /app

COPY --chown=nonroot:nonroot . .

COPY --from=builder /data /data

EXPOSE 8000

CMD ["main.py"] 