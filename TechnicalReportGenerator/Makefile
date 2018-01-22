ifeq ('$(SOURCE_EXT)', '')
SOURCE_EXT=rst md
endif
SOURCES:=$(foreach ext, $(SOURCE_EXT), $(wildcard *.$(ext)))
ifeq ('$(DEST_EXT)', '')
DEST_EXT=pdf
endif
DESTINATIONS:=$(foreach source, $(SOURCES), $(addsuffix .$(DEST_EXT),$(basename $(source))))
GENERATED_DIR=generated

# clean files
CLEAN_EXT=pdf aux fdb_latexmk fls out tex toc xdv
CLEAN_SOURCES:=$(foreach ext, $(CLEAN_EXT), $(wildcard *.$(ext)))

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

%.md: %.rst ## Converts from rst to md
	pandoc $< \
		--filter tools/rst_filter.py \
		--output $@

%.tex: %.rst tools/project_infos.yaml ## Converts from rst to tex
	pandoc $< \
		--filter tools/rst_filter.py \
		--lua-filter tools/getMetadata.lua \
		--standalone \
		--listings \
		--to latex \
		--template tools/template.tex \
		--top-level-division section \
		--output $@

%.tex: %.md tools/project_infos.yaml ## Converts from md to tex
	pandoc $< \
		--filter tools/md_filter.py \
		--lua-filter tools/getMetadata.lua \
		--standalone \
		--listings \
		--to latex \
		--template tools/template.tex \
		--top-level-division section \
		--output $@

%.pdf: %.tex ## Converts from tex to pdf
	latexmk -pdf -xelatex $<
	latexmk -c $<


%.json: %.md
	pandoc $< --to json --lua-filter=getMetadata.lua | python -m json.tool > ${<:.md=.json}


%.json: %.rst
	pandoc $< --to json --lua-filter=getMetadata.lua | python -m json.tool > ${<:.rst=.json}

clean:
	rm $(CLEAN_SOURCES)
