from Pergunta import Pergunta
from typing import List

class Quiz:
    def __init__(self, titulo: str, perguntas: List[Pergunta], num_tentativas: int, tempo_limite: int):
        self.titulo = titulo
        self.perguntas = perguntas
        self.num_tentativas = num_tentativas
        self.tempo_limite = tempo_limite
        self.__pontuacao_max = self.calcular_pontuacao()

    @property
    def titulo(self):
        return self.__titulo
    
    @titulo.setter
    def titulo(self, novo_valor):
        self.__titulo = novo_valor
    
    @property
    def perguntas(self):
        return self.__perguntas
    
    @perguntas.setter
    def perguntas(self, novo_valor: List[Pergunta]):
        self.__perguntas = novo_valor
        self.__pontuacao_max = self.calcular_pontuacao()
    
    @property
    def pontuacao_max(self):
        return self.__pontuacao_max

    @property
    def num_tentativas(self):
        return self.__num_tentativas
    
    @num_tentativas.setter
    def num_tentativas(self, novo_valor):
        self.__num_tentativas = novo_valor
    
    @property
    def tempo_limite(self):
        return self.__tempo_limite
    
    @tempo_limite.setter
    def tempo_limite(self, novo_valor):
        self.__tempo_limite = novo_valor
    
    def calcular_pontuacao(self):
        soma_pontos = 0
        for p in self.perguntas:
            if p.nivel == "FÁCIL":
                soma_pontos += 1
            elif p.nivel == "MÉDIO":
                soma_pontos += 2
            else:
                soma_pontos += 3

        return soma_pontos

    def add_pergunta(self, pergunta: Pergunta):
        self.perguntas.append(pergunta)
    
    def remover_pergunta(self, pos_pergunta: int):
        del self.__perguntas[pos_pergunta]
    
    def salvar()
    
    mostrar
    
    atualizar
    
    deletar

    executar