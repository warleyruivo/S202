# query.py
from database import Database

db = Database("bolt://3.91.47.130:7687", "neo4j", "ordnance-manifest-calculations")  # ajuste os dados se necessário

# Questão 1 - Listar professores com mais de 60 anos
def professores_maiores_60():
    query = """
    MATCH (t:Teacher)
    WHERE 2024 - t.ano_nasc > 60
    RETURN t.name AS nome, 2024 - t.ano_nasc AS idade
    """
    return db.execute_query(query)

# Questão 2 - Listar professores e suas escolas
def professores_e_escolas():
    query = """
    MATCH (t:Teacher)-[:WORKS]->(s:School)
    RETURN t.name AS professor, s.name AS escola
    """
    return db.execute_query(query)

# Teste rápido (remova ou comente no uso real)
if __name__ == "__main__":
    print("Professores com mais de 60 anos:")
    for row in professores_maiores_60():
        print(row)

    print("\nProfessores e suas escolas:")
    for row in professores_e_escolas():
        print(row)

db.close()
