FROM python:3-onbuild

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 -m nltk.downloader -d /usr/share/nltk_data punkt stopwords wordnet

COPY . .

CMD [ "python",  "-u", "./app.py" ]