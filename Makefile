
dst= "$(HOME)/Library/Application Support/Sublime Text 3/Installed Packages/go.sublime-package"

install: clean
	@sleep .1
	@scripts/package.sh 1> /dev/null
	@mv go.sublime-package ${dst}
	@printf "\033[1m==>\033[0m Installed\n"

watch:
	@echo
	@ls -1 src/go/*.py conf/* | entr -pcr make install
	@echo

test:
	@pytest ./tests

release:
	@scripts/release.sh

clean:
	@rm -f ${dst}
	@rm -f go.sublime-package
	@rm -rf .pytest_cache src/go/__pycache__ src/go/*.pyc
