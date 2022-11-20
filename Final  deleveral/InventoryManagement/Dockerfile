FROM python:3.10.6

WORKDIR /home/balag/Desktop/IBM/InventoryManagement

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./inventoryapp

CMD ["python","app/InventoryMangementSystem.py"]