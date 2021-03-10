from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
my_bot=Chatbot(name="PyBot",read_only=True,logic_adapters=['chatterbot.logic.MathematicalEvaluation','chatterbot.logic.BestMatch'])
small_talk=['hi',
'how are you']

math_talk_1=['pythagorad theorem','a squared plus b squared c squared']

math_talk_2=['law of cosines','c**2=a**2+b**2']
print(my_bot.get_response("hi"))

list_trainer=ListTrainer(my_bot)
for item in (small_talk,math_talk_1,math_talk_2):
    list_trainer.train(item)