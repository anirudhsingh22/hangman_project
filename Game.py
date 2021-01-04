from os import system, name
from random import randint

class Hangman:
  def __init__(
    self,
    engine,
    interface,
    symbols = { 'exit': '2', 'hint': '?', 'restart': '#', 'see_answer': '!' }
  ):
    self.engine = engine
    self.interface = interface
    self.symbols = symbols

  def start(self):
    while True:
      self.interface.print_main_menu()
      choice = self.interface.get_user_input()
      if choice == self.symbols['exit']: self.quit()
      else: self.play_game()

  def play_game(self):
    while not self.engine.game_is_won() and not self.engine.all_attempts_exhausted():
      self.interface.render_game_menu(
        self.engine.attempts_made,
        self.engine.max_attempts,
        self.engine.guesses,
        self.engine.misses,
        self.engine.hints_left
      )
      choice = self.interface.get_user_input()

      if choice == self.symbols['hint']:
        self.engine.get_next_hint()
      elif choice == self.symbols['restart']:
        self.engine.reset()
      elif choice == self.symbols['see_answer']:
        self.interface.show_answer(self.engine.word)
        self.interface.wait()
        break
      else:
        self.engine.guess(choice)

    if self.engine.game_is_won():
      self.interface.print_winning_message()
      self.interface.wait()

  def quit(self):
    self.interface.print_exit_message()
    exit()

class Interface:
  def __init__(self):
    self.hangmans = [
      '''






          ________|_
      ''',

      '''

                  |
                  |
                  |
                  |
                  |
          ________|
      ''',

      '''
              _____
                  |
                  |
                  |
                  |
                  |
          ________|_
      ''',

      '''
              _____
              |   |
                  |
                  |
                  |
                  |
          ________|_
      ''',

      '''
              _____
              |   |
              O   |
                  |
                  |
                  |
          ________|_
      ''',

      '''
              _____
              |   |
              O   |
              |   |
                  |
                  |
          ________|_
      ''',
    '''
              _____
              |   |
              O   |
              /|   |
                  |
                  |
          ________|_
    ''',

    '''
              _____
              |   |
              O   |
              /|\  |
                  |
                  |
          ________|_
    ''',

    '''
              _____
              |   |
              O   |
              /|\  |
              /    |
                  |
          ________|_
    ''',

    '''
              _____
              |   |
              O   |
              /|\  |
              / \  |
                  |
          ________|_
    '''
    ]

  def clear_screen(self):
    _ = system('cls') if name == 'nt' else system('clear')

  def print_exit_message(self):
    self.clear_screen()
    print("Thank you for playing")

  def print_main_menu(self):
    self.clear_screen()
    print("1. Start Game")
    print("2. Exit")

  def get_user_input(self, prompt = 'Enter your choice: '):
    return input(prompt)

  def print_hangman(self, attempts):
    print(self.hangmans[attempts])

  def print_list_with_label(self, arr, label):
    print('{0}: '.format(label), end='')
    for _ in arr: print(_, end=' ')
    print('\n')

  def print_with_label(self, value, label):
    print('{0}: {1}'.format(label, value))

  def show_answer(self, answer):
    self.clear_screen()
    print("Correct Answer Was: ", answer)

  def wait(self):
    print("Press enter key to continue...")
    _ = input('')

  def print_legend(self, max_attempts):
    print('Max Attempts: = {}'.format(max_attempts))
    print('Enter ? to get hint, # to restart and ! to see answer')

  def print_winning_message(self):
    print('Congratulations You have won the game')

  def render_game_menu(self, attempts_made, max_attempts, guesses, misses, hints_left):
    self.clear_screen()
    self.print_hangman(attempts_made)
    self.print_list_with_label(guesses, 'Word')
    self.print_list_with_label(misses, 'Misses')
    self.print_with_label(attempts_made, 'Attempts Made')
    self.print_with_label(hints_left, 'Hints Left')
    self.print_legend(max_attempts)


class Engine:
    def __init__(self, max_attempts = 9, max_hints = 3):
      self.WORDS = ['PHONE','HAPPY','APPLE','EARTH','GONGYIWEI', 'PYTHON','PIONEER','SINGAPORE','FATHER','MOTHER','GONGYIWEI']
      self.word = self.WORDS[randint(0, len(self.WORDS) - 1)]
      self.attempts_made = 0
      self.max_attempts = max_attempts
      self.hints_left = self.max_hints = max_hints
      self.guesses = ['_'] * len(self.word)
      self.misses = []

    def get_next_hint(self):
      if self.hints_left == 0: return
      self.hints_left -= 1
      for i in range(0, len(self.guesses)):
        if self.guesses[i] == '_':
          self.guesses[i] = self.word[i]
          break

    def guess(self, choice):
      if self.validate_guess(choice): return
      self.misses.append(choice)
      self.attempts_made += 1

    def validate_guess(self, choice):
      for index in range(0, len(self.word)):
        if self.word[index].lower() == choice.lower() and self.guesses[index] == '_':
          self.guesses[index] = self.word[index]
          return True
      return False

    def reset(self):
      self.attempts_made = 0
      self.hints_left = self.max_hints
      self.word = self.WORDS[randint(0, len(self.WORDS) - 1)]
      self.guesses = ['_'] * len(self.word)

    def game_is_won(self):
      return self.guesses.count('_') == 0

    def all_attempts_exhausted(self):
      return self.attempts_made == self.max_attempts

def main():
  Hangman(Engine(), Interface()).start()

if __name__ == '__main__': main()