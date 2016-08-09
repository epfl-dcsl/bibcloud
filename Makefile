

all:
	./makeabbrev.py
	./makeabbrev.py short
	echo "abbreviation files updated; do a git status to see impact"
