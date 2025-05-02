import curses
import time
import pygame
import random

pygame.mixer.init()

#---------sounds-----------
typing_sound = pygame.mixer.Sound("typing.wav")
typing_sound.set_volume(0.8)
mistake_sound = pygame.mixer.Sound("duck-sound.mp3")
mistake_sound.set_volume(0.5)

code_list = [
    """Rina found an old key in her garden. Curious, she searched
for its lock and discovered a hidden box under a tree. Inside were
letters from her grandfather, full of wisdom and love.""",

    """A boy rested under a large banyan tree every day.
One day, the tree whispered, "Thank you for sitting with me."
From then on, they shared stories daily.""",

    """Liam sent paper boats down the stream with wishes written on them.
Years later, he received a letter from someone who found one—and granted his wish.""",

    """A street violinist never spoke a word.
One day, he vanished, leaving behind a note: “Music was my voice;
thank you for listening.""",

    """Maya's imaginary friend, Tiko, always protected her.
When she grew up and forgot him, she found an old drawing of
Tiko labeled: \"Your first guardian angel.\"""",

    """At exactly 3:15 p.m., the town clock stopped.
That moment, everything paused—and a boy saved a
cat stuck in traffic. Then time resumed.""",

    """Emma broke her mirror during an argument. In the
reflection, she saw not her face—but her kinder self.
She smiled, and the mirror healed.""",

    """Tom believed he could collect stars. He kept jars full of lightbugs.
One day, he looked up and saw a new star twinkle back.""",

    """A robot in a lab wanted to feel love. One day, a child hugged
it, saying, “You’re my friend.” Its metal heart glowed warm red.""",

    """Nina talked to her small cactus daily. When she cried, it bloomed
for the first time. She knew it cared.""",

    """Ali could predict rain by listening to the wind. One dry summer, he danced—and
clouds gathered. The villagers never questioned his gift again.""",

    """There was a door on the mountain with no handle. A traveler sat
before it and sang. It slowly opened to a paradise within.""",

    """A stray cat visited an old man every night. When the man passed,
neighbors found the cat guarding a diary with untold stories.""",

    """A girl believed the clouds were her canvas. She waved her paintbrush at the
sky, and the clouds always changed shape, following her dreams.""",

    """A thief stole only from the rich but left letters with kind advice.
One day, a letter was found on a poor child’s pillow—along with food.""",

    """A bus only appeared at midnight. It picked up tired dreamers and dropped
them off inside their own dreams—for just one hour."""
]
 
class Content():
    def __init__(self, screen):
        self.stdscr = screen
        self.paragraph = random.choice(code_list)
        self.wpm = 0
        self.correct_char = 0
        self.time_taken = 0
        self.lines = self.paragraph.splitlines()
    
    def show_paragraph(self):
        self.stdscr.addstr(self.paragraph)
        self.stdscr.refresh()

    def over_write(self): 
        start_time = time.time()

        for idx,line in enumerate(self.lines, start=0):
            char_in_line = [char for char in line]
            for char in range(len(line)):
                self.stdscr.addstr(idx,char,char_in_line[char], curses.color_pair(3))
                self.stdscr.refresh()
                key = chr(self.stdscr.getch())

                if key == char_in_line[char]:
                    typing_sound.play()
                    time.sleep(0.1)
                    self.stdscr.addstr(idx,char,char_in_line[char], curses.color_pair(1))
                    self.stdscr.refresh()
                    self.correct_char += 1
                    typing_sound.stop()

                elif key == curses.KEY_ENTER:
                    if char == len(line)-1:
                        break

                else:
                    mistake_sound.play()
                    self.stdscr.addstr(idx,char,char_in_line[char], curses.color_pair(2))
                    self.stdscr.refresh()
                    
                end_time = time.time()
                self.time_taken = (end_time - start_time)

                self.wpm = int(self.correct_char/(5*((self.time_taken)/60)))
                self.stdscr.addstr((len(self.lines)+2),0, f"Speed = {self.wpm} wpm")
                self.stdscr.refresh()
                mistake_sound.stop()

    def result(self, text):
        self.stdscr.addstr((len(self.lines)+4),0, text)
        self.stdscr.refresh()

    def accuracy(self):
            accuracy = int((self.correct_char/len(self.paragraph))*100)
            self.stdscr.addstr((len(self.lines)+3),0, f"Accuracy = {accuracy}%")
            self.stdscr.refresh()

            if accuracy == 100 and self.wpm >= 50:
                self.result("Result: Best!")
            elif 95 < accuracy < 100 and 50 > self.wpm >= 40:
                self.result("Result: Better!")
            elif 95 < accuracy < 100 and 40 > self.wpm >= 35:
                self.result("Result: Good!")    
            else:
                self.result("Result: Have to improve")


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1,curses.COLOR_GREEN,-1)
    curses.init_pair(2,curses.COLOR_RED, -1)
    curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)

    content = Content(stdscr)
    curses.curs_set(0)
    content.show_paragraph()
    content.over_write()
    content.accuracy()
    stdscr.refresh()
    stdscr.getch()
    
if __name__ == "__main__":
    curses.wrapper(main) 
