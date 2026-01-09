import json
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List



class SerializableMixin:
    """Mixin para facilitar a conversão para dicionário (JSON)."""
    def to_dict(self):
        data = self.__dict__.copy()
        for key, value in data.items():
            if isinstance(value, Enum):
                data[key] = value.name
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, list):
                data[key] = [item.to_dict() if hasattr(item, 'to_dict') else item for item in value]
        return data

class Entidade(SerializableMixin):
    """Classe base para entidades com ID único."""
    def __init__(self, uid: str = None):
        self.uid = uid if uid else str(uuid.uuid4())

class Dificuldade(Enum):
    FACIL = "FACIL"
    MEDIO = "MEDIO"
    DIFICIL = "DIFICIL"

def carregar_settings():
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"pesos_dificuldade": {"FACIL": 1, "MEDIO": 2, "DIFICIL": 3}, "max_tentativas_usuario": 3}

SETTINGS = carregar_settings()

class Pergunta(Entidade):
    def __init__(self, enunciado: str, alternativas: List[str], correta_idx: int, dificuldade: str, tema: str, uid: str = None):
        super().__init__(uid)
        self._enunciado = enunciado
        self._alternativas = alternativas
        self._correta_idx = correta_idx
        self._dificuldade = Dificuldade(dificuldade)
        self._tema = tema
        self._validar()

    def _validar(self):
        """Validações de negócio."""
        if not (3 <= len(self._alternativas) <= 5):
            raise ValueError("A pergunta deve ter entre 3 e 5 alternativas.")
        if not (0 <= self._correta_idx < len(self._alternativas)):
            raise ValueError("Índice da resposta correta inválido.")

    @property
    def enunciado(self):
        return self._enunciado

    @property
    def alternativas(self):
        return self._alternativas

    @property
    def peso(self) -> int:
        return SETTINGS['pesos_dificuldade'].get(self._dificuldade.name, 1)
    
    @property
    def tema(self):
        return self._tema
    
    @property
    def correta_idx(self):
        return self._correta_idx

    def verificar_resposta(self, idx: int) -> bool:
        return idx == self._correta_idx

    def __str__(self):
        return f"[{self._dificuldade.name}] {self._enunciado} ({len(self._alternativas)} alts)"

    def __eq__(self, other):
        if not isinstance(other, Pergunta):
            return False
        return self._enunciado == other._enunciado and self._tema == other._tema

class Quiz(Entidade):
    def __init__(self, titulo: str, perguntas: List[Pergunta], uid: str = None):
        super().__init__(uid)
        self.titulo = titulo
        self._perguntas = perguntas

    @property
    def pontuacao_maxima(self) -> int:
        return sum(p.peso for p in self._perguntas)

    def adicionar_pergunta(self, pergunta: Pergunta):
        self._perguntas.append(pergunta)

    def __len__(self):
        return len(self._perguntas)

    def __iter__(self):
        return iter(self._perguntas)

    def __str__(self):
        return f"Quiz: {self.titulo} | Perguntas: {len(self)} | Max Pontos: {self.pontuacao_maxima}"

class Tentativa(Entidade):
    def __init__(self, usuario_id: str, quiz_id: str, respostas: List[int], pontuacao: int, data_hora: str = None, uid: str = None):
        super().__init__(uid)
        self.usuario_id = usuario_id
        self.quiz_id = quiz_id
        self.respostas = respostas 
        self.pontuacao = pontuacao
        self.data_hora = data_hora if data_hora else datetime.now().isoformat()

class Usuario(Entidade):
    def __init__(self, nome: str, email: str, matricula: str, tentativas: List[Tentativa] = None, uid: str = None):
        super().__init__(uid)
        self.nome = nome
        self.email = email
        self.matricula = matricula
        self.tentativas = tentativas if tentativas else []

    def adicionar_tentativa(self, tentativa: Tentativa):
        tentativas_quiz = [t for t in self.tentativas if t.quiz_id == tentativa.quiz_id]
        if len(tentativas_quiz) >= SETTINGS['max_tentativas_usuario']:
            raise PermissionError(f"Limite de tentativas ({SETTINGS['max_tentativas_usuario']}) excedido para este quiz.")
        self.tentativas.append(tentativa)

    @property
    def taxa_acerto_geral(self) -> float:
        if not self.tentativas:
            return 0.0
        return sum(t.pontuacao for t in self.tentativas) / len(self.tentativas)

    def __str__(self):
        return f"{self.nome} ({self.matricula}) - Tentativas: {len(self.tentativas)}"
