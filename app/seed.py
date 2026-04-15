from app.database import SessionLocal
from app.models.models import ItemCardapio
from app.database.product import CATALOGO_PADRAO

def seed_db():
    db = SessionLocal()
    if db.query(ItemCardapio).count() > 0:
        print("CARDÁPIO JÁ EXISTENTE")
        return

    print(" Semeando o cardápio no banco de dados...")
    for item in CATALOGO_PADRAO:
        novo_item = ItemCardapio(**item) 
        db.add(novo_item)

    db.commit()
    print(f"{len(CATALOGO_PADRAO)} itens inseridos com sucesso!")
    db.close()

if __name__ == "__main__":
    seed_db()