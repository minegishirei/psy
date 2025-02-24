
# python version number:3.9.16
FROM python:3.12

# code ... directory for python codes.
WORKDIR /code

# copy localcode to container image.
COPY ./code /code


# upgrade pip command
RUN pip install --upgrade pip 

# install python lib 
RUN pip install -r requirements.txt

RUN pip install -U groq phidata

ENV MECABRC /opt/homebrew/etc/mecabrc

ENV GROQ_API_KEY=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