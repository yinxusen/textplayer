import os
from textPlayer import TextPlayer


'''
for game in os.listdir(os.getcwd() + '/games'):
	print game
	t = TextPlayer()
	t.assign_variables(game, True)
	t.run()
	t.parse_and_execute_command_file('commands.txt')
	t.quit()
'''


t = TextPlayer('zork1.z5', True)
start_info = t.run()
print start_info
#t.parse_and_execute_command_file('commands.txt')
command_output = t.execute_command('look')
print command_output
t.quit()

