FLSKFLAGS = --app UpScore
SECRET = key.secret

all: genSecret

genSecret:
	python -c 'import secrets; print(secrets.token_hex())' > $(SECRET)

.PHONY: clean run

clean:
	rm -rf $(SECRET)

run:
	flask $(FLSKFLAGS) run
