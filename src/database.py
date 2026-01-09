import json
import os
from typing import List, Dict
from models import Pergunta, Quiz, Usuario, Tentativa

DB_FILE = "data.json"

class Database:
    def __init__(self):
        self.perguntas: List[Pergunta] = []
        self.quizzes: List[Quiz] = []
        self.usuarios: List[Usuario] = []
        self.carregar_dados()

    def _inicializar_db(self):
        return {"perguntas": [], "quizzes": [], "usuarios": []}

    def salvar_dados(self):
        data = {
            "perguntas": [p.to_dict() for p in self.perguntas],
            "quizzes": [q.to_dict() for q in self.quizzes],
            "usuarios": [u.to_dict() for u in self.usuarios]
        }
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def carregar_dados(self):
        if not os.path.exists(DB_FILE):
            data = self._inicializar_db()
        else:
            with open(DB_FILE, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = self._inicializar_db()

        def clean_keys(d):
            return {k.lstrip('_'): v for k, v in d.items()}

        self.perguntas = [Pergunta(**clean_keys(p)) for p in data.get("perguntas", [])]
        
        self.quizzes = []
        for q_data in data.get("quizzes", []):
            perguntas_obj = [Pergunta(**clean_keys(p)) for p in q_data.pop('_perguntas', [])]
            self.quizzes.append(Quiz(perguntas=perguntas_obj, **clean_keys(q_data)))

        self.usuarios = []
        for u_data in data.get("usuarios", []):
            tentativas_data = u_data.pop('tentativas', [])
            tentativas_obj = [Tentativa(**clean_keys(t)) for t in tentativas_data]
            self.usuarios.append(Usuario(tentativas=tentativas_obj, **clean_keys(u_data)))

    def get_usuario_by_matricula(self, matricula: str):
        return next((u for u in self.usuarios if u.matricula == matricula), None)

    def get_quiz_by_idx(self, idx: int):
        if 0 <= idx < len(self.quizzes):
            return self.quizzes[idx]
        return None
