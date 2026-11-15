from pathlib import Path
from tinydb import TinyDB


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / 'data'
DB_FILE = DATA_DIR / 'products.json'

DATA_DIR.mkdir(exist_ok=True)

db = TinyDB(DB_FILE, encoding='utf-8')
products_table = db.table('products')


if len(products_table) == 0:
    products_table.insert_multiple([
        {
            "id": 1,
            "name": "Laptop",
            "price": 1200.00,
            "content": "Потужний ноутбук з процесором Intel Core i7, 16 ГБ оперативної пам'яті та SSD на 512 ГБ.",
            "category": "Електроніка",
            "quantity": 5,
            "image": "",
            "created_at": "2026-11-15"
        },
        {
            "id": 2,
            "name": "Phone",
            "price": 800.00,
            "content": "Смартфон із 6.5-дюймовим OLED-дисплеєм, подвійною камерою та акумулятором на 5000 мА·год.",
            "category": "Електроніка",
            "quantity": 10,
            "image": "",
            "created_at": "2026-11-15"
        },
        {
            "id": 3,
            "name": "PC",
            "price": 1800.00,
            "content": "Настільний комп'ютер для ігор або роботи з графікою: RTX 4070, 32 ГБ RAM, 1 ТБ SSD.",
            "category": "Електроніка",
            "quantity": 3,
            "image": "",
            "created_at": "2026-11-15"
        }
    ])