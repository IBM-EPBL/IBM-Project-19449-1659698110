FROM python:3.10.6

WORKDIR /Desktop/IBM/InventoryManagement

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./ .

CMD ["python","InventoryManageentSystem.py"]