
dst= "$(HOME)/Library/Application Support/Sublime Text 3/Installed Packages/go.sublime-package"

install: clean
	@sleep .1
	@zip -j ${dst} ./src/go/*.py 1> /dev/null
	@zip -j ${dst} ./conf/* 1> /dev/null
	@printf "\033[1m==>\033[0m Installed\n"

watch:
	@echo
	@ls -1 src/go/*.py conf/* | entr -pcr make install
	@echo

test:
	@pytest ./tests

clean:
	@rm -f ${dst}
	@rm -rf .pytest_cache src/go/__pycache__ src/go/*.pyc
