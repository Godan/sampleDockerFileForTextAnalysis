FROM python:3.5.2-alpine

ADD . /code
ENV IPADIC_VERSION 2.7.0-20070801
ENV ipadic_url https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM

RUN mkdir local
WORKDIR local
RUN apk update
RUN apk --no-cache add git mariadb-client gcc curl bash file sudo openssh build-base openssl

RUN mkdir crf
RUN cd crf
RUN curl -L -o CRF++-0.58.tar.gz 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7QVR6VXJ5dWExSTQ'
RUN tar -zxf CRF++-0.58.tar.gz
WORKDIR CRF++-0.58
RUN ./configure
RUN make
RUN make install

WORKDIR /local
RUN curl -L -o mecab-0.996.tar.gz 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE'
RUN tar -zxf mecab-0.996.tar.gz
WORKDIR mecab-0.996
RUN  ./configure --enable-utf8-only --with-charset=utf8
RUN make
RUN make check
RUN make install

# Install IPA dic
WORKDIR /local
RUN  curl -SL -o mecab-ipadic-${IPADIC_VERSION}.tar.gz ${ipadic_url} \
&& tar zxf mecab-ipadic-${IPADIC_VERSION}.tar.gz \
&& cd mecab-ipadic-${IPADIC_VERSION} \
&& ./configure --with-charset=utf8 \
&& make \
&& make install

# Install Neologd
WORKDIR /local
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
&& mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y


WORKDIR /local
ENV CPPFLAGS -I/usr/local/include
RUN curl -c  cabocha-0.69.tar.bz2 -s -L "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU" |grep confirm |  sed -e "s/^.*confirm=\(.*\)&amp;id=.*$/\1/" | xargs -I{} \
    curl -b  cabocha-0.69.tar.bz2 -L -o cabocha-0.69.tar.bz2 "https://drive.google.com/uc?confirm={}&export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU"
RUN tar -jxf cabocha-0.69.tar.bz2
WORKDIR cabocha-0.69
RUN ./configure --prefix=/usr/local --with-charset=utf8
RUN make
RUN make install

WORKDIR python
RUN python setup.py install

RUN pip3 install PyMySQL3 mecab-python3 beautifulsoup4 pandas urllib3
WORKDIR /code
RUN pip install -r requirements.txt

CMD python app.py
