from app.database.database import SessionLocal
from app.database.product import CATALOGO_PADRAO
from app.models.models import ItemCardapio


def seed_db():
    with SessionLocal() as db:
        if db.query(ItemCardapio).count() > 0:
            print("CARDÁPIO JÁ EXISTENTE - Nenhuma alteração feita.")
            return

        print("Semeando o cardápio no banco de dados...")
        try:
            for item in CATALOGO_PADRAO:
                novo_item = ItemCardapio(**item)
                db.add(novo_item)
            db.commit()
            print(f"{len(CATALOGO_PADRAO)} itens inseridos com sucesso!")
        except Exception as e:
            db.rollback()
            print(f"Erro ao semear banco: {e}")

if __name__ == "__main__":
    seed_db()