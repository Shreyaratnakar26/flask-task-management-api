# Build-tool automation (rubric 1.3) - Python equivalent of `mvn clean package`
.PHONY: clean install test package
clean:
	rm -rf build dist *.egg-info
install:
	pip install -r requirements-dev.txt
test:
	python -m pytest -v
package: clean
	python -m build
	@echo "Artifact(s):" && ls dist
