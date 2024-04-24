import random
import os
import pygame
import sys

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Inicialização do Pygame
pygame.init()

# Configurações da janela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo da Forca")

# Carregamento de sons
sons = {
    "acerto": pygame.mixer.Sound("audios/acerto.mp3"),
    "erro": pygame.mixer.Sound("audios/erro.mp3"),
    "vitoria": pygame.mixer.Sound("audios/vitoria.mp3"),
    "derrota": pygame.mixer.Sound("audios/derrota.mp3")
}

# Carregamento de pontuações
def carregar_pontuacoes():
    if not os.path.exists("pontuacoes.txt"):
        with open("pontuacoes.txt", "w") as file:
            file.write("0\n0")

    with open("pontuacoes.txt", "r") as file:
        pontuacoes = [int(score) for score in file.readlines()]
    return pontuacoes

# Salvar pontuações
def salvar_pontuacoes(pontuacoes):
    with open("pontuacoes.txt", "w") as file:
        file.write("\n".join(map(str, pontuacoes)))

# Função para desenhar a forca
def desenhar_forca(erros):
    partes_forca = [
        (100, 400, 300, 10),
        (250, 150, 10, 250),
        (250, 150, 150, 10),
        (400, 150, 10, 60),
        (350, 210, 60, 10),
        (350, 240, 20, 40),
        (350, 280, 20, 60),
        (340, 240, 5, 5),
        (365, 240, 5, 5),
        (340, 300, 5, 5),
        (365, 300, 5, 5),
    ]

    for i, parte in enumerate(partes_forca[:erros]):
        pygame.draw.rect(tela, PRETO, parte)

# Função para desenhar as letras da palavra
def desenhar_palavra(palavra, letras_certas):
    fonte = pygame.font.Font(None, 60)
    texto = ""
    for letra, certa in zip(palavra, letras_certas):
        if certa != "_":
            texto += letra.upper() + " "
        else:
            texto += "_ "
    texto_imagem = fonte.render(texto, True, PRETO)
    tela.blit(texto_imagem, (200, 500))

# Função para desenhar as letras erradas
def desenhar_letras_erradas(letras_erradas):
    fonte = pygame.font.Font(None, 30)
    texto = "Letras erradas: " + ", ".join(letras_erradas)
    texto_imagem = fonte.render(texto, True, PRETO)
    tela.blit(texto_imagem, (10, 10))

# Função para desenhar a dica
def desenhar_dica(dica):
    fonte = pygame.font.Font(None, 30)
    texto = "Dica: " + dica
    texto_imagem = fonte.render(texto, True, PRETO)
    tela.blit(texto_imagem, (10, 40))

# Função para desenhar a pontuação
def desenhar_pontuacao(pontuacoes):
    fonte = pygame.font.Font(None, 30)
    texto = "Pontuação: {} Vitórias / {} Derrotas".format(pontuacoes[0], pontuacoes[1])
    texto_imagem = fonte.render(texto, True, PRETO)
    tela.blit(texto_imagem, (10, 70))

# Função para desenhar a tela de game over
def desenhar_game_over(vitoria, palavra):
    fonte = pygame.font.Font(None, 60)
    texto = "Parabéns! Você ganhou!" if vitoria else "Game Over! Você perdeu!"
    texto_imagem = fonte.render(texto, True, VERMELHO)
    tela.blit(texto_imagem, (200, 250))

    fonte_palavra = pygame.font.Font(None, 40)
    texto_palavra = "A palavra era: " + palavra.upper()
    texto_palavra_imagem = fonte_palavra.render(texto_palavra, True, PRETO)
    tela.blit(texto_palavra_imagem, (200, 350))

# Função principal do jogo
def jogo_da_forca(modo, palavra_jogador_1="", dica_jogador_1=""):
    # Inicialização de variáveis
    if modo == 2:
        palavra = palavra_jogador_1.lower()
        dica = dica_jogador_1
    else:
        tema = random.choice(["animais", "países", "frutas"])
        palavra, dica = escolher_palavra(tema)

    max_tentativas = 6
    letras_certas = ['_'] * len(palavra)
    letras_erradas = []
    tentativas_restantes = max_tentativas
    vitoria = False

    # Loop do jogo
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Verifica se o jogador ganhou
        if "_" not in letras_certas:
            vitoria = True
            break

        # Verifica se o jogador perdeu
        if tentativas_restantes == 0:
            break

        # Desenhar tela do jogo
        tela.fill(BRANCO)
        desenhar_forca(len(letras_erradas))
        desenhar_palavra(palavra, letras_certas)
        desenhar_letras_erradas(letras_erradas)
        desenhar_dica(dica)
        desenhar_pontuacao(pontuacoes)

        # Atualizar tela
        pygame.display.update()

        # Captura de entrada do usuário
        palpite = input("Digite uma letra: ").lower()

        # Processamento do palpite
        if len(palpite) != 1 or not palpite.isalpha():
            print("Por favor, digite apenas uma letra válida.")
            continue

        if palpite in palavra:
            sons["acerto"].play()
            for i in range(len(palavra)):
                if palavra[i] == palpite:
                    letras_certas[i] = palpite
        else:
            sons["erro"].play()
            letras_erradas.append(palpite)
            tentativas_restantes -= 1

    # Desenhar tela de game over
    tela.fill(BRANCO)
    desenhar_game_over(vitoria, palavra)
    desenhar_pontuacao(pontuacoes)

    # Atualizar tela
    pygame.display.update()

    # Aguardar antes de fechar
    pygame.time.wait(5000)

# Função para escolher a palavra
def escolher_palavra(tema):
    palavras_e_dicas = {
        "animais": [("gato", "Um animal doméstico com bigodes e cauda peluda."),
                    ("cachorro", "Melhor amigo do homem."),
                    ("elefante", "Um mamífero terrestre enorme com tromba."),
                    ("leão", "O rei da selva."),
                    ("tigre", "Um grande felino laranja com listras pretas."),
                    ("girafa", "Um animal com um longo pescoço e pernas."),
                   ],
        "países": [("brasil", "O maior país da América do Sul."),
                   ("estados unidos", "Uma superpotência mundial na América do Norte."),
                   ("canadá", "Famoso por suas vastas paisagens e frio intenso."),
                   ("alemanha", "Conhecida por sua eficiência e cervejas."),
                   ("japão", "Tecnologia avançada e cultura rica."),
                   ("austrália", "Lar de coalas, cangurus e o Outback."),
                  ],
        "frutas": [("banana", "Amarela e pode ser encontrada em cachos."),
                   ("maçã", "Uma fruta crocante e vermelha ou verde."),
                   ("laranja", "Uma fruta cítrica suculenta."),
                   ("abacaxi", "Tem uma casca espinhosa e é tropical."),
                   ("uva", "Pode ser verde ou roxa e é usada para fazer vinho."),
                   ("morango", "Pequena fruta vermelha com sementes."),
                  ],
    }

    if tema in palavras_e_dicas:
        palavras, dicas = zip(*palavras_e_dicas[tema])
    else:
        palavras = ["python", "programacao", "computador", "inteligencia", "dados", "algoritmo"]
        dicas = ["Linguagem de programação",
                 "Processo de escrever código",
                 "Máquina que processa dados",
                 "Capacidade de aprender e adaptar",
                 "Informação processada",
                 "Sequência de instruções"]

    palavra = random.choice(palavras)
    dica = dicas[palavras.index(palavra)]
    return palavra, dica

# Função principal do jogo
def main():
    global pontuacoes
    pontuacoes = carregar_pontuacoes()

    print("Bem-vindo ao jogo!")
    print("Escolha o modo de jogo:")
    print("1. Jogar contra o computador")
    print("2. Jogar contra outro jogador")

    while True:
        try:
            modo = int(input("Digite 1 ou 2 para escolher o modo: "))
            if modo in [1, 2]:
                break
            else:
                print("Por favor, digite 1 ou 2.")
        except ValueError:
            print("Por favor, digite apenas números.")

    if modo == 2:
        print("\nModo de dois jogadores selecionado.")
        palavra_jogador_1 = input("Jogador 1, por favor, escolha a palavra para o jogador 2 adivinhar: ")
        dica_jogador_1 = input("Jogador 1, por favor, insira uma dica para a palavra escolhida: ")
        jogo_da_forca(modo, palavra_jogador_1, dica_jogador_1)
    else:
        print("\nModo de um jogador selecionado.")
        tema = input("Escolha um tema para as palavras (animais, países, frutas) ou pressione Enter para palavras aleatórias: ")
        jogo_da_forca(modo, tema)

if __name__ == "__main__":
    main()
