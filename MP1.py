import vsa
import wnn

class mp1:

    def __init__(self, config):
        self.s = wnn.stack(config)

        self.last_answer_bit = -1 
        self.last_encoded_question = None
        self.last_question_text = "panic! you shouldn't see this!"

    def __init(self, config, memory):
        self.s = wnn.stack(config)

        self.last_answer_bit = -1 
        self.last_encoded_question = None
        self.last_question_text = "panic! you shouldn't see this!"

        # and here's where we somehow load up the entire system from a file

        self.load_memory(memory) 

    def yes_or_no(self,bit):
        if bit == 0:
            return "NO"
        elif bit == 1:
            return "YES"
        else:
            print("THE BIT IS WRONG SOMEHOW")

    def get_answer(self,question):
        self.last_question_text = question 
        encoded_question = vsa.encode(question)
        self.last_encoded_question = encoded_question 
        answer = self.s.read(encoded_question)[0]
        self.last_answer_bit = answer 
        return self.yes_or_no(answer)

    def retrain(self):
        correct_answer = -1
        if self.last_answer_bit == 0:
            correct_answer = 1
        elif self.last_answer_bit == 1:
            correct_answer = 0
        self.s.write_without_prior_read(self.last_encoded_question, correct_answer)
        self.last_answer_bit = correct_answer

    def batch_train(self, answers): # answer[0] is the question, answer[1] is 1/0 for yes/no 
        for a in answers:
            encoded_question = vsa.encode(a[0])
            self.s.write_without_prior_read(a[0],a[1])

    def load_from_file(self, filename):
        answers = []
        linecount = 0
        with open(filename, 'r', encoding="utf8") as file:
            for line in file:
                linecount = linecount + 1 
                tmp = line.split(" -> ")
                try:
                    answer = []
                    answer.append(tmp[0])
                    answer.append(int(tmp[1]))
                    answers.append(answer)
                except ValueError:
                    pass 
        print(linecount, "total lines processed")
        print("Beginning training...")
        self.batch_train(answers)
        print("Training complete.")
        return answers 

    def shell(self):
        print("WELCOME TO MP1.\nYOU MAY ASK BINARY QUESTIONS.\nTYPE EXIT TO END SESSION.")
        console_input = ""
        while console_input != "EXIT":
            console_input = str(input("> "))
            console_input = console_input.upper()
            if '?' in console_input:
                print(self.get_answer(console_input))
            elif "INCORRECT" in console_input:
                self.retrain()
                print("RESTATING QUESTION:", self.last_question_text)
                print(self.get_answer(self.last_question_text)) 
            elif "EXIT" in console_input:
                print("GOODBYE FOR NOW.")
                return 
            else:
                print("THAT IS NOT A QUESTION.")
                
config = [[256,4],[64,4],[16,4], [4,4],[1,4]]
m = mp1(config)
m.shell()
