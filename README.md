# quiz-educacional-poo
## Integrantes da equipe
LUCAS GABRIEL CORREIA GONÇALVES | GITHUB: devlucasgabriel01 -- Responsável pelas classes Pergunta e Usuario  
LUIZ FILIPY SOARES DA SILVA | GITHUB: Filipyd2 -- Responsável pela classe Tentativa  Database
WESLEY BATISTA DE ARAUJO | GITHUB: wesleybaraujo -- Responsável pela classe Quiz  

## Principais classes do projeto (UML Textual)
**Class:** Pergunta  
**Atributos:** uid, enunciado, alternativas, correta_idx, dificuldade, tema  
**Métodos:** verificar_resposta, to_dict  

**Class:** Quiz  
**Atributos:** uid, titulo, perguntas  
**Métodos:** adicionar_pergunta, pontuacao_maxima, to_dict  

**Class:** Usuario  
**Atributos:** uid, nome, email, matricula, tentativas  
**Métodos:** adicionar_tentativa, taxa_acerto_geral, to_dict  

**Class:** Tentativa  
**Atributos:** uid, usuario_id, quiz_id, respostas, pontuacao, data_hora  
**Métodos:** to_dict  

**Class:** Database  
**Atributos:** perguntas, quizzes, usuarios  
**Métodos:** salvar_dados, get_usuario_by_matricula, get_quiz_by_idx  

