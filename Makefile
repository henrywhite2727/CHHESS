ifeq ($(OS), Windows_NT)
run:
	python CHHESS/main.py 

build: setup.py
	python setup.py build bdist_wheel

clean:
	if exist "./build" rd /s /q build
	if exist "./dist" rd /s /q dist
	if exist "./CHHESS.egg-info" rd /s /q CHHESS.egg-info
else
run:
	python3 CHHESS/main.py 

build: setup.py
	python3 setup.py build bdist_wheel

clean:
	rm -rf build
	rm -rf dist
	rm -rf CHHESS.egg-info
endif