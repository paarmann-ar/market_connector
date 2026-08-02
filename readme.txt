extentions.
	selenium IDE https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd?hl=en
	chrome driver https://googlechromelabs.github.io/chrome-for-testing/
	
Conventions.
    A. Indentation
	    # Aligned with opening delimiter.
	    foo = long_function_name(var_one, var_two,
	                             var_three, var_four)

	B. Imports
		from subprocess import Popen, PIPE

	C. Whitespace in Expressions and Statements
		spam(ham[1], {eggs: 2})
		foo = (0,)
		ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]
		spam(1)
		dct['key'] = lst[index]
		x = 1
		x = x*2 - 1
		def munge(sep: AnyStr = None) -> PosInt:
		def complex(real, imag=0.0):
		if foo == 'blah':
		    do_blah_thing()
		
	D. Naming Conventions
		* 	Non-public method begin with a single underscore
		** 	with words separated by underscores

		Packages
			lowercase

		Module
			lower case

		Class 
			UpperCaseCamelCase
		
		Functions 
			lowercase

		Variable
			lowercase

		Bool Variable
			is_ + lowercase

		Arguments
			lowercase

		Global
			should be all lowercase

		Constant
			fully capitalized

test_applications struckture
	1. unit_testcases
		a. his folder conatin all unit of testcases
		b. start position of test is there

	2. userstory_epics
		a. this folder contain all epics open browser, login, ....
		b. run testcases one after one

Class Structure
	a. standard Functions
		1. __new__
			deploy Singltone pattern
			add attributte of providers from base classes

		2. __init__
			add field to classes

		3. setup
			place of eager loading

		4. __call__
			call dev-methods and extra methods

		5. prepare
			prepare Attributes

		6. __teardown
			!!!shutdown test in class and create report!!!! I am not sure about it

		7. decorators
			waitfor
				waiting for element visibility in base class (element_for_waiting_until_visible, type_of_element)


Create venv
        python -m venv C:\Users\mpaarmann\MyProjects\rdc_automat\.venv
        Create pth file in C:\Users\mpaarmann\Projects\rdc_automat\.venv\Lib\site-packages\rdc_automat.pth contain(C:\Users\mpaarmann\MyProjects\rdc_automat)
        cd C:\Users\mpaarmann\projects\rdc_automat\.venv\Scripts

		run activate.bat
		pip3 install --upgrade pip


Usefull Commands
		pip3 freeze > requirements.txt
		pip3 uninstall -r requirements.txt

		pip install --force-reinstall  -r requirements.txt
		pip3 install -r requirements.txt

		pip list	
		if get error with no module then 
			1. ctrl+shift+p
			2. venv
			3. add venv


Execute file
		pyinstaller -d all --clean  C:\Users\mpaarmann\Projects\rdc_automat\test_applications\md_365\controler\userstory_pytest.py

Execute py with save prompt
		C:\Users\mpaarmann\Projects\rdc_automat\test_applications\d_365\controler\temp.py | Out-File -filepath C:\Users\mpaarmann\Projects\rdc_automat\test_applications\d_365\controler\cmd_prompt.txt
		arineo_asp_import_bank_statement.exe > c:\Users\mpaarmann\Projects\rdc_automat\test_applications\d_365\controler\cmd_prompt.txt
