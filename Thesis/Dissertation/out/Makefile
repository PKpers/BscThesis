all:
	pdflatex --shell-escape main.tex
	biber main
	pdflatex --shell-escape main.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out 
