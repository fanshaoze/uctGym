# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class stateTest(object):
	def __init__(self, _a, _b):
		self.a = _a
		self.b = _b

def print_hi(name):
	# Use a breakpoint in the code line below to debug your script.
	print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
	t0 = stateTest(1,[1,2])
	t1 = stateTest(1,[1,3])
	print(t0.__dict__ == t1.__dict__)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
