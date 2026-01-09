import sys
import time
from models import Pergunta, Quiz, Usuario, Tentativa, SETTINGS
from database import Database

db = Database()

def menu_principal():
    while True:
        print("\n=== SISTEMA DE QUIZ ===")
        print("1. Admin: Criar Pergunta")
        print("2. Admin: Criar Quiz")
        print("3. Admin: Cadastrar Usuário")
        print("4. Usuário: Responder Quiz")
        print("5. Relatórios")
        print("0. Sair")
        opcao = input("Escolha: ")

        if opcao == '1': criar_pergunta()
        elif opcao == '2': criar_quiz()
        elif opcao == '3': cadastrar_usuario()
        elif opcao == '4': responder_quiz()
        elif opcao == '5': relatorios()
        elif opcao == '0': sys.exit()
        else: print("Opção inválida.")

def criar_pergunta():
    print("\n--- Nova Pergunta ---")
    tema = input("Tema: ")
    enunciado = input("Enunciado: ")
    
    for p in db.perguntas:
        if p.enunciado == enunciado and p.tema == tema: 
            print("Erro: Pergunta já existe neste tema.")
            return

    alternativas = []
    print("Digite as alternativas (digite 'FIM' para parar, min 3, max 5):")
    while len(alternativas) < 5:
        alt = input(f"Alternativa {len(alternativas)+1}: ")
        if alt.upper() == 'FIM':
            if len(alternativas) < 3:
                print("Mínimo de 3 alternativas necessário.")
                continue
            break
        alternativas.append(alt)
    
    try:
        correta = int(input(f"Índice da correta (0 a {len(alternativas)-1}): "))
        dificuldade = input("Dificuldade (FACIL, MEDIO, DIFICIL): ").upper()
        
        nova_p = Pergunta(enunciado, alternativas, correta, dificuldade, tema)
        db.perguntas.append(nova_p)
        db.salvar_dados()
        print("Pergunta salva!")
    except ValueError as e:
        print(f"Erro de validação: {e}")

def criar_quiz():
    print("\n--- Novo Quiz ---")
    if not db.perguntas:
        print("Nenhuma pergunta cadastrada.")
        return
    
    titulo = input("Título do Quiz: ")
    print("Selecione as perguntas pelo ID (índice) separadas por vírgula:")
    for i, p in enumerate(db.perguntas):
        print(f"{i}: {p}")
    
    idxs = input("IDs: ").split(',')
    perguntas_selecionadas = []
    try:
        for idx in idxs:
            perguntas_selecionadas.append(db.perguntas[int(idx.strip())])
        
        novo_quiz = Quiz(titulo, perguntas_selecionadas)
        db.quizzes.append(novo_quiz)
        db.salvar_dados()
        print(f"Quiz criado com {len(novo_quiz)} perguntas.")
    except (ValueError, IndexError):
        print("Índices inválidos.")

def cadastrar_usuario():
    nome = input("Nome: ")
    email = input("Email: ")
    matricula = input("Matrícula/ID: ")
    if db.get_usuario_by_matricula(matricula):
        print("Usuário já existe.")
        return
    
    user = Usuario(nome, email, matricula)
    db.usuarios.append(user)
    db.salvar_dados()
    print("Usuário cadastrado.")

def responder_quiz():
    matricula = input("Sua matrícula: ")
    user = db.get_usuario_by_matricula(matricula)
    if not user:
        print("Usuário não encontrado.")
        return

    print("\nQuizzes Disponíveis:")
    for i, q in enumerate(db.quizzes):
        print(f"{i}: {q.titulo} (Max Pontos: {q.pontuacao_maxima})")
    
    try:
        q_idx = int(input("Escolha o Quiz: "))
        quiz = db.get_quiz_by_idx(q_idx)
        if not quiz: raise ValueError
    except ValueError:
        print("Quiz inválido.")
        return

    try:
        tentativas_anteriores = [t for t in user.tentativas if t.quiz_id == quiz.uid]
        if len(tentativas_anteriores) >= SETTINGS['max_tentativas_usuario']:
            print("Você atingiu o limite de tentativas para este quiz.")
            return
    except Exception as e:
        print(e)
        return

    print(f"\nIniciando Quiz: {quiz.titulo}")
    print(f"Tempo limite sugerido: {SETTINGS.get('duracao_padrao_minutos', 10)} min (não forçado no CLI)")
    
    respostas_usuario = []
    pontuacao_atual = 0
    inicio = time.time()

    for i, pergunta in enumerate(quiz):
        print(f"\nQ{i+1}: {pergunta.enunciado} [{pergunta._dificuldade.name}]")
        for idx, alt in enumerate(pergunta.alternativas):
            print(f"   {idx}) {alt}")
        
        try:
            resp = int(input("Sua resposta: "))
            respostas_usuario.append(resp)
            if pergunta.verificar_resposta(resp):
                pontuacao_atual += pergunta.peso
        except ValueError:
            respostas_usuario.append(-1) 

    fim = time.time()
    tempo_total = fim - inicio
    
    tempo_limite_sec = SETTINGS.get('duracao_padrao_minutos', 10) * 60
    if tempo_total > tempo_limite_sec:
        print("\nTEMPO ESGOTADO! Tentativa anulada ou pontuação zerada.")
        pontuacao_atual = 0
    
    nova_tentativa = Tentativa(user.uid, quiz.uid, respostas_usuario, pontuacao_atual)
    
    try:
        user.adicionar_tentativa(nova_tentativa)
        db.salvar_dados()
        print(f"\nQuiz finalizado! Pontuação: {pontuacao_atual}/{quiz.pontuacao_maxima}")
        
        print("\n--- Gabarito ---")
        for i, pergunta in enumerate(quiz):
            resp_user = respostas_usuario[i]
            status = "ACERTOU" if pergunta.verificar_resposta(resp_user) else f"ERROU (Correta: {pergunta.correta_idx})"
            print(f"Q{i+1}: {status}")

    except PermissionError as e:
        print(f"Erro ao salvar tentativa: {e}")

def relatorios():
    print("\n--- Ranking de Usuários (Média de Pontos) ---")
    ranking = sorted(db.usuarios, key=lambda u: u.taxa_acerto_geral, reverse=True)
    for i, u in enumerate(ranking):
        print(f"{i+1}. {u.nome}: Média {u.taxa_acerto_geral:.2f} pts")

if __name__ == "__main__":
    menu_principal()
