SRC = src

BUILD = build

all: scss optimize

source: scss-watch serve-source

scss-watch: Makefile
	sass --scss --watch $(SRC)/scss:$(SRC)/css &
	
scss: Makefile
	sass --scss --update $(SRC)/scss:$(SRC)/css	

serve-build: Makefile
	$(shell cd $(BUILD); python -m SimpleHTTPServer)

serve-source: Makefile
	$(shell cd $(SRC); python -m SimpleHTTPServer)

optimize: Makefile
	requirejs-0.2.1/build/build.sh $(SRC)/js/app.build.js
	requirejs-0.2.1/build/build.sh $(SRC)/js/app.build.js


clean:
	rm -rf $(BUILD) jsdoc
