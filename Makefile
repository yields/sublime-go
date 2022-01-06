
dst= "$(HOME)/Library/Application Support/Sublime Text/Installed Packages/Golang.sublime-package"

install: clean
	@sleep .1
	@scripts/package.sh 1> /dev/null
	@mv Golang.sublime-package ${dst}
	@printf "\033[1m==>\033[0m Installed\n"

watch:
	@echo
	@ls -1 scripts/dev.py go/*.py conf/* | entr -pcr make install
	@echo

test:
	@pytest ./tests

coverage:
	@coverage run --include="go/*" -m pytest ./tests
	@coverage html
	@open htmlcov/index.html

clean:
	@rm -f ${dst}
	@rm -f Golang.sublime-package
	@rm -rf .pytest_cache {go,tests}/__pycache__ go/*.pyc
	@rm -rf htmlcov .coverage

deps:
	@pip3 install pytest
