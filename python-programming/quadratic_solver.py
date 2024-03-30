import math


def main():
	"""
	File: quadratic_solver.py
	This programs calculates the roots when user provides necessary values
	"""
	print('Quadratic Solver!')
	a = int(input('Enter a: '))
	b = int(input('Enter b: '))
	c = int(input('Enter c: '))
	discriminant = b**2 - 4*a*c
	if discriminant > 0:
		root1 = (-b + math.sqrt(discriminant)) / 2*a
		root2 = (-b - math.sqrt(discriminant)) / 2*a
		print(f'Two roots: {root1}, {root2}')
	elif discriminant == 0:
		root = (-b + math.sqrt(discriminant)) / 2*a
		print(f'One root: {root}')
	else:
		print('No real roots')


# DO NOT EDIT CODE BELOW THIS LINE #


if __name__ == "__main__":
	main()
