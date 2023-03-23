FROM python:3.8-slim as base

FROM base as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    curl \
    unzip

WORKDIR /install

COPY requirements.txt ./
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# 日本語評価極性辞書をダウンロードして展開
RUN curl -LO https://www.cl.ecei.tohoku.ac.jp/resources/sent_lex/pn.csv.m3.120408.trim.zip \
    && unzip pn.csv.m3.120408.trim.zip \
    && rm pn.csv.m3.120408.trim.zip

FROM base

COPY --from=builder /install /usr/local
COPY --from=builder /usr/lib/x86_64-linux-gnu/mecab /usr/lib/x86_64-linux-gnu/mecab
COPY --from=builder /var/lib/mecab/dic/ipadic-utf8 /var/lib/mecab/dic/ipadic-utf8
COPY --from=builder /install/pn.csv.m3.120408.trim /app/pn.csv.m3.120408.trim

WORKDIR /app

COPY . .

EXPOSE 8000


CMD ["python", "main.py"]

