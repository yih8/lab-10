import logging
from abc import abstractmethod

from eliza import Eliza


class ElizaState:
    def __init__(self, hysteric_eliza):
        self.hysteric_eliza = hysteric_eliza

    @abstractmethod
    def switch_state(self, output):
        """ Decide how to react next based on the current output """

    @abstractmethod
    def process_output(self, output):
        """ React on the current output by formatting it according to the state """


class Normal(ElizaState):
    """ Answer normally """
    pass


class Angry(ElizaState):
    """ ANSWER ONLY IN UPPERCASE (use String.upper() to do this) """
    pass


class Sad(ElizaState):
    """ answer only in lowercase (use String.lower() to do this) """
    pass


class HystericEliza:
    def __init__(self):
        self.eliza = Eliza()
        self.state = "Normal"

    def load(self, replies):
        self.eliza.load(replies)

    def process_output(self, output):
        if self.state == "Normal":
            if output.startswith("Please"):
                self.state = "Sad"
            elif "n't " in output:
                self.state = "Angry"
        elif self.state == "Angry":
            if output.startswith("Do you") or output.startswith("Please"):
                self.state = "Normal"
            elif output.startswith("Why"):
                self.state = "Sad"
        elif self.state == "Sad":
            if output.startswith("Do "):
                self.state = "Normal"
        if self.state == "Normal":
            return output
        elif self.state == "Angry":
            return output.upper()
        elif self.state == "Sad":
            return output.lower()

    def run(self):
        initial = self.process_output(self.eliza.initial())
        print(initial)

        while True:
            sent = input('> ')

            output = self.eliza.respond(sent)
            if output is None:
                break
            
            formatted = self.process_output(output)
            print(formatted)

        final = self.process_output(self.eliza.final())
        print(final)


def main():
    eliza = HystericEliza()
    eliza.load('doctor.txt')
    eliza.run()


if __name__ == '__main__':
    logging.basicConfig()
    main()
