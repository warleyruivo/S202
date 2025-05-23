from database import Database

def test_connection():
    db = Database("bolt://3.91.47.130:7687", "neo4j", "ordnance-manifest-calculations")
    result = db.execute_query("RETURN 'Conexão OK!' AS msg")
    print(result[0]['msg'])
    db.close()

if __name__ == "__main__":
    test_connection()
