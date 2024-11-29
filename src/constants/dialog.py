from src.datatypes.dialog import Dialog
import os

DIALOG_START_GAME = [
    Dialog(
        Text="Olá, eu sou o Lipe, o robô do Laboratório Inteligente voltado para Educação",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
    ),
    Dialog(
        Text="O Lipe, como todos os outros robôs, não sabe o que fazer sozinho. Para que ele consiga realizar tarefas, os programadores precisam ensiná-lo usando algo chamado algoritmo.",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
        Italic=True,
    ),
    Dialog(
        Text="Um algoritmo é escrito através de uma linguagem especial que o computador do robô consegue entender. Essa linguagem é chamada de código. O computador lê o código e segue os passos do algoritmo.",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
        Italic=True,
    ),
    Dialog(
        Text="Mas temos um problema, o Lipe bateu a cabeça, o que prejudicou sua memória. Ele não lembra como seguir os passos de um algoritmo. Para ajudá-lo vocês deverão executar os passos de alguns algoritmos. Vamos lá? ",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe_confuso.png",
        Italic=True,
    ),
]

DIALOG_SEQUENCE = [
    Dialog(
        Text="Sequência é tipo uma receita! Primeiro faz isso, depois aquilo... sempre na ordem certinha!",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
    ),
    Dialog(
        Text="Imagine que você tem uma missão: ajudar o robô a descer o escorregador!",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
    ),
    Dialog(
        Text="Você seguirá a seguinte ordem:",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
    ),
    Dialog(
        Text="1 - Ande até o escorregador.",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
    ),
    Dialog(
        Text="2 - Suba as escadinhas.",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
    ),
    Dialog(
        Text="3 - Sente no topo.",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
    ),
    Dialog(
        Text="4 - ESCORREGA!!!",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
    ),
    Dialog(
        Text="Se você fizer fora da ordem, dá erro",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
    ),
    Dialog(
        Text="Pronto pra praticar? Monte seu plano e faça o robô completar a missão!",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
    ),
]

DIALOG_CONDITION = [
    Dialog(
        Text="TEXTO DA CONDIÇÃO!",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
    ),
]

DIALOG_ITERATION = [
    Dialog(
        Text="AQUI VAI O TEXTO DA ITERAÇÃO",
        Character_Dir="images" + os.sep + "robot" + os.sep + "lipe.png",
    ),
]
