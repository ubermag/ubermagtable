@ECHO OFF

set PROJECT=ubermagtable
set IPYNBPATH=docs/ipynb/*.ipynb
set PYTHON=python

REM Command file for testing


%PYTHON% -c "import sys; import %PROJECT%; sys.exit(%PROJECT%.test())"

REM test-coverage:
%PYTHON% -m pytest -v --cov=%PROJECT% --cov-report=xml --cov-config .coveragerc

REM test-docs:
%PYTHON% -m pytest -v --doctest-modules --ignore=%PROJECT%/tests %PROJECT%

REM test-ipynb:
%PYTHON% -m pytest -v --nbval %IPYNBPATH%

%PYTHON% -m pycodestyle --filename=*.py .


