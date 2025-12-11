# quiz-educacional-poo
## Integrantes da equipe
LUCAS GABRIEL CORREIA GONÇALVES | GITHUB: -- 
LUIZ FILIPY SOARES DA SILVA | GITHUB: -- 
WESLEY BATISTA DE ARAUJO | GITHUB: wesleybaraujo -- 

## Principais classes do projeto (UML Textual)
Class: Pergunta
Atributos: enunciado, alternativas, resposta_correta, nivel, tema
Métodos: salvar, mostrar, atualizar, deletar, checar_resposta, mostrar_resposta

Class: Quiz
Atributos: titulo, perguntas, pontuacao_max, num_tentativas, tempo_limite
Métodos: salvar, mostrar, atualizar, deletar, calcular_pontuacao

Class: Usuario
Atributos: id, nome, email, tentativas
Métodos: salvar, mostrar, atualizar, deletar, tentar_quiz

Class: Tentativa
Atributos: quiz, respostas
Métodos: salvar, mostrar, atualizar, deletar

Class: Estatisticas
Atributos: 
Métodos: 
