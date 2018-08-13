import os
import re
from subprocess import PIPE, Popen
from threading import Thread
from Queue import Queue, Empty


class TextPlayer:
    def __init__(self, game_path):
        self.libdir = os.path.dirname(os.path.realpath(__file__))
        self.dfrotz_exec_path = '{}/frotz/dfrotz'.format(self.libdir)
        self.game_path = game_path
        self.game_filename = os.path.basename(self.game_path)

        # signal(SIGPIPE, SIG_DFL)

        # Verify that specified game file exists, else limit functionality
        if self.game_path is None or not os.path.exists(self.game_path):
            raise ValueError("Unrecognized game file or bad path")

        self.game_log = self.game_filename + '_log.txt'
        self.debug = False
        self.game_process = None
        self.output_queue = None

    def run(self):
        self.game_process = Popen([self.dfrotz_exec_path, self.game_path],
                                  stdin=PIPE, stdout=PIPE, bufsize=1)
        # Create Queue object
        self.output_queue = Queue()
        t = Thread(target=self.enqueue_pipe_output,
                   args=(self.game_process.stdout, self.output_queue))

        # Thread dies with the program
        t.daemon = True
        t.start()

        # Grab start info from game.
        start_output = self.get_command_output()
        # if ('Press' in start_output or 'press' in start_output
        #         or 'Hit' in start_output or 'hit' in start_output):
        #     start_output += self.execute_command(' \n')
        # if 'introduction' in start_output:
        #     start_output += self.execute_command('no\n')  # Parc

        return start_output

    # async pipe for game output buffer
    @staticmethod
    def enqueue_pipe_output(output, queue):
        for line in iter(output.readline, b''):
            queue.put(line)
        output.close()

    def parse_and_execute_command_file(self, fname):
        with open(fname, 'r') as gf:
            commands = gf.readlines()
        for comm in commands:
            print(self.execute_command(comm))

    def execute_command(self, command):
        self.game_process.stdin.write(command + '\n')
        return self.clean_command_output(self.get_command_output())

    def get_score(self):
        self.game_process.stdin.write('score\n')
        command_output = self.get_command_output()
        score_pattern = ('[0-9]+ [\(total ]*[points ]*[out ]*of'
                         ' [a maximum of ]*[a possible ]*[0-9]+')
        matchObj = re.search(score_pattern, command_output, re.M|re.I)
        if matchObj != None:
            score_words = matchObj.group().split(' ')
            return int(score_words[0]), int(score_words[len(score_words)-1])
        return None

    def clean_command_output(self, text):
        regex_list = ['[0-9]+/[0-9+]', 'Score:[ ]*[-]*[0-9]+',
                      'Moves:[ ]*[0-9]+', 'Turns:[ ]*[0-9]+',
                      '[0-9]+:[0-9]+ [AaPp][Mm]', ' [0-9]+ \.']
        for regex in regex_list:
            matchObj = re.search(regex, text, re.M|re.I)
            if matchObj != None:
                text = text[matchObj.end() + 1:]
        return text

    def get_command_output(self):
        command_output = ''
        output_continues = True

        # While there is still output in the queue
        while output_continues:
            try:
                line = self.output_queue.get(timeout=0.01)
            except Empty:
                output_continues = False
            else:
                command_output += line

        # Clean up the output
        command_output = (command_output
                          .replace('\n', ' ')
                          .replace('>', ' ')
                          .replace('<', ' '))
        return command_output

    def quit(self):
        if self.game_process is not None:
            self.game_process.stdin.write('quit\n')
            self.game_process.stdin.write('y\n')
            self.game_process.terminate()
            print(self.get_command_output())
        else:
            print('game not start')
