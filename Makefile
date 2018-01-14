ifeq ('$(SOURCE_EXT)', '')
SOURCE_EXT=rst md
endif
SOURCES = $(wildcard *.${SOURCE_EXT})
ifeq ('$(DEST_EXT)', '')
DEST_EXT=pdf
endif
DESTINATIONS = $(addsuffix .$(DEST_EXT),$(basename ${SOURCES}))
GENERATED_DIR=generated

help: ## Show help
	@printf "Technical report Creator using pandoc\
	\n\n\
	Usage : make all \
	SOURCE_EXT=<SOURCE_EXT> \
	DEST_EXT=<DEST_EXT>\n\n\
	SOURCE_EXT: Source file(s) extension.\n\tCan either be rst, md or tex. If not supplied, rst and md files are searched by default.\n\n\
	DEST_EXT: Destination file(s) extension.\n\tCan either be md, tex or pdf. If not supplied, pdf is made by default.\n";

.PHONY: all

all: ${DESTINATIONS} ## Build all rst or md files to pdf
	make clean

%.md: %.rst ## Converts from rst to md
	pandoc $< \
		--output $@

%.tex: %.md ## Converts from md to tex
	cat templates/header.yaml $< > "${<:.md=.tmp}"
	mv "${<:.md=.tmp}" $<
	pandoc $< \
		--standalone \
		--listings \
		--to latex \
		--template templates/template.tex \
		--top-level-division section \
		--output $@

%.pdf: %.tex ## Converts from tex to pdf
	mkdir $(GENERATED_DIR)
	#Don't know why but have to run it twice to have it work
	xelatex $< \
		--quiet \
		--output-directory=$(GENERATED_DIR)
	xelatex $< \
		--quiet \
		--output-directory=$(GENERATED_DIR)
	mv $(GENERATED_DIR)/*.pdf .

clean: ## Clean temporary files generated during conversion
	rm -r generated
