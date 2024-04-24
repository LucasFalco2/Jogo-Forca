import random
import os
import pygame

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

def mostrar_forca(erros):
    forca = [
        """
            ------
            |    |
            |
            |
            |
        ----------
        """,
        """
            ------
            |    |
            |    O
            |
            |
        ----------
        """,
        """
            ------
            |    |
            |    O
            |    |
            |
            |
        ----------
        """,
        """
            ------
            |    |
            |    O
            |   /|
            |
            |
        ----------
        """,
        """
            ------
            |    |
            |    O
            |   /|\\
            |
            |
        ----------
        """,
        """
            ------
            |    |
            |    O
            |   /|\\
            |   /
            |
        ----------
        """,
        """
            ------
            |    |
            |    O
            |   /|\\
            |   / \\
            |
        ----------
        """
    ]
    return forca[erros]


def carregar_sons():
    pygame.mixer.init()
    sons = {
        "acerto": pygame.mixer.Sound("sounds/acerto.wav"),
        "erro": pygame.mixer.Sound("sounds/erro.wav"),
        "vitoria": pygame.mixer.Sound("sounds/vitoria.wav"),
        "derrota": pygame.mixer.Sound("sounds/derrota.wav")
    }
    return sons


def carregar_pontuacoes():
    if not os.path.exists("pontuacoes.txt"):
        with open("pontuacoes.txt", "w") as file:
            file.write("0\n0")

    with open("pontuacoes.txt", "r") as file:
        pontuacoes = [int(score) for score in file.readlines()]
    return pontuacoes


def salvar_pontuacoes(pontuacoes):
    with open("pontuacoes.txt", "w") as file:
        file.write("\n".join(map(str, pontuacoes)))


def main():
    pygame.init()
    sons = carregar_sons()

    print("Bem-vindo ao jogo da forca!")
    modo = input("Escolha o modo de jogo (1 para um jogador, 2 para dois jogadores): ")

    if modo == "2":
        print("\nModo de dois jogadores selecionado.")
        palavra_jogador_1 = input("Jogador 1, por favor, escolha a palavra para o jogador 2 adivinhar: ").lower()
        dica_jogador_1 = input("Jogador 1, por favor, insira uma dica para a palavra escolhida: ")
        palavra = palavra_jogador_1
        dica = dica_jogador_1
    else:
        print("\nModo de um jogador selecionado.")
        tema = input("Escolha um tema para as palavras (animais, países, frutas) ou pressione Enter para palavras aleatórias: ").lower()
        palavra, dica = escolher_palavra(tema)

    max_tentativas = int(input("Escolha o número máximo de tentativas (padrão: 6): ") or 6)

    letras_certas = ['_'] * len(palavra)
    letras_erradas = []
    tentativas_restantes = max_tentativas

    print("\nComeçando o jogo...")
    print("Dica:", dica)

    while True:
        if "_" not in letras_certas:
            print("Parabéns! Você ganhou!")
            pontuacoes = carregar_pontuacoes()
            pontuacoes[0] += 1
            salvar_pontuacoes(pontuacoes)
            print("Pontuação mais alta: {}".format(pontuacoes[0]))
            if pygame.mixer.get_init():
                sons["vitoria"].play()
                pygame.time.wait(5000) #espera 5 segundos
            break

        if tentativas_restantes == 0:
            print("Game over! Você perdeu!")
            print("A palavra era:", palavra)
            if pygame.mixer.get_init():
                sons["derrota"].play()
                pygame.time.wait(3000) #espera 3 segundos
            pontuacoes = carregar_pontuacoes()
            pontuacoes[1] += 1
            salvar_pontuacoes(pontuacoes)
            print("Pontuação mais alta: {}".format(pontuacoes[0]))
            break

        print("\n" + mostrar_forca(len(letras_erradas)))
        print("Palavra:", " ".join(letras_certas))
        print("Letras erradas:", " ".join(letras_erradas))
        print("Dica:", dica)  # Mostrar a dica da palavra
        print("Tentativas restantes:", tentativas_restantes)

        palpite = input("Digite uma letra: ").lower()

        if len(palpite) != 1 or not palpite.isalpha():
            print("Por favor, digite apenas uma letra válida.")
            continue

        if palpite in palavra:
            print("Boa! A letra está na palavra.")
            if pygame.mixer.get_init():
                sons["acerto"].play()
            for i in range(len(palavra)):
                if palavra[i] == palpite:
                    letras_certas[i] = palpite
        else:
            print("Ops! A letra não está na palavra.")
            if pygame.mixer.get_init():
                sons["erro"].play()
            letras_erradas.append(palpite)
            tentativas_restantes -= 1

    if "_" not in letras_certas:
        print("Parabéns! Você adivinhou a palavra:", palavra)
       
    else:
        print("Infelizmente, você não adivinhou a palavra. A palavra era:", palavra)
      


if __name__ == "__main__":
 main()