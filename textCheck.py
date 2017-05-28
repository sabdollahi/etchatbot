import enchant,language_check
import enchant.checker
from enchant.checker.CmdLineChecker import CmdLineChecker
spell_check = enchant.checker.SpellChecker("en_US")
grammarC = language_check.LanguageTool('en_US')
userInput = ""
NofChoice = 3
while userInput != "exit":
	userInput = input("Input: ")
	spell_check.set_text(userInput)
	# For spell check
	for serror in spell_check:
		print("There is an spelling error in your input : "+serror.word)
		q = 0
		NofChoice = 3	#change to outside if class
		suggest = spell_check.suggest(serror.word)
		print(suggest)
		userCorrect = ""
		while userCorrect not in range(0,NofChoice) and q<len(suggest):
			print("Did you mean : ")
			for choose in range(0,NofChoice):
				if q+choose == len(suggest):
					NofChoice = choose
					break
				print(str(choose)+". "+suggest[q+choose])
			print("If none of these is correct, please input 'next'")
			try:
				userCorrect = input("Correct number: ")
				
				if userCorrect == "next":
					q +=NofChoice
					continue
				userCorrect = int(userCorrect)
			except :
				print("Please input option or 'next'!")
		if userCorrect not in range(0,NofChoice):
			print("Do you want us to remember this word?")
			remember = input("yes or no: ")
			if remember == "yes":
				spell_check.add()
			elif remember == "no":
				print("Please input the correct spell :")
				remember = input("input: ")
				serror.replace(remember)
		else:
			serror.replace(suggest[q+userCorrect])
	Grammartext = spell_check.get_text()
	# For grammar check
	matches = grammarC.check(Grammartext)
	for gerror in matches:
		print("There is an grammar error in your input : ")
		print(gerror.msg)
	print("Correct sentence : " + language_check.correct(Grammartext, matches))