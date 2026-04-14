files := errors.py file.py helper.py imports.py main.py 
PWD := {{$PWD}}


all: files
	python3 $@

clean:
	rm -rf build/*

run: 
	python3 $@


.PHONY: all clean install uninstall