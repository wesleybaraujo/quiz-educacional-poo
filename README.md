# quiz-educacional-poo
## Integrantes da equipe
LUCAS GABRIEL CORREIA GONÇALVES | GITHUB:  -- Responsável pelas classes Pergunta e Usuario  
LUIZ FILIPY SOARES DA SILVA | GITHUB: -- Responsável pela classe Tentativa  
WESLEY BATISTA DE ARAUJO | GITHUB: wesleybaraujo -- Responsável pela classe Quiz  

## Principais classes do projeto (UML Textual)
Class: Pergunta  
Atributos: enunciado, alternativas, resposta_correta, nivel, tema  
Métodos: salvar, mostrar, atualizar, deletar, checar_resposta, mostrar_resposta  

Class: Quiz  
Atributos: titulo, perguntas, pontuacao_max, num_tentativas, tempo_limite  
Métodos: add_pergunta, remover_pergunta, salvar, mostrar, atualizar, deletar, calcular_pontuacao, executar  

Class: Usuario  
Atributos: id, nome, email, tentativas  
Métodos: salvar, mostrar, atualizar, deletar, tentar_quiz  

Class: Tentativa  
Atributos: quiz, respostas, usuario, pontuacao, taxa_acerto, tempo_gasto  
Métodos: salvar, mostrar, atualizar, deletar, registrar_resposta, finalizar, gerar_resultado
