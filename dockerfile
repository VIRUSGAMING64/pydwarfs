FROM python as pydwarf

WORKDIR /pydwarf
COPY . .
RUN ls
RUN pip install -r requirements.txt
RUN bash run.sh
