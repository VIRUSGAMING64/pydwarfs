FROM python as pydwarf

WORKDIR /pydwarf
COPY . .
RUN ls
RUN pip install -r requirements.txt
RUN python main.py
