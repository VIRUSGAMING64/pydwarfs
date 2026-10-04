FROM python as pydwarf

WORKDIR /pydwarf

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 1200 9090

CMD ["python", "main.py"]
