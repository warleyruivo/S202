from database import Database

class TeacherCRUD:
    def __init__(self, db: Database):
        self.db = db

    def create(self, name, ano_nasc, cpf):
        query = """
        CREATE (:Teacher {name: $name, ano_nasc: $ano_nasc, cpf: $cpf})
        """
        self.db.execute_query(query, {"name": name, "ano_nasc": ano_nasc, "cpf": cpf})

    def read(self, name):
        query = """
        MATCH (t:Teacher {name: $name})
        RETURN t.name AS nome, t.ano_nasc AS nascimento, t.cpf AS cpf
        """
        return self.db.execute_query(query, {"name": name})

    def update(self, name, newCpf):
        query = """
        MATCH (t:Teacher {name: $name})
        SET t.cpf = $newCpf
        RETURN t.name AS name, t.cpf AS cpf
        """
        return self.db.execute_query(query, {"name": name, "newCpf": newCpf})

    def delete(self, name):
        query = """
        MATCH (t:Teacher {name: $name})
        DETACH DELETE t
        """
        self.db.execute_query(query, {"name": name})
