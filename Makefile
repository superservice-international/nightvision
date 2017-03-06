PYTHON := env/bin/python
PIP := env/bin/pip

.PHONY: build watch

all: install

$(PYTHON):
	virtualenv env

$(PIP): $(PYTHON)

install: $(PIP)
	$(PIP) install -r requirements.txt

post:
	env/bin/python take_picture.py
