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
		
Install Package
		altgraph==0.17.4
		attrs==25.3.0
		certifi==2025.4.26
		cffi==1.17.1
		charset-normalizer==3.4.1
		colorama==0.4.6
		comtypes==1.4.10
		dict2xml==1.7.6
		ffmpeg==1.4
		ffmpeg-python==0.2.0
		future==1.0.0
		h11==0.16.0
		idna==3.10
		merge==1.0.0
		mergedeep==1.3.4
		MouseInfo==0.1.3
		numpy==2.2.0
		opencv-python==4.10.0.84
		outcome==1.3.0.post0
		packaging==24.2
		pefile==2023.2.7
		pillow==11.0.0
		PyAutoGUI==0.9.54
		pycparser==2.22
		PyGetWindow==0.0.9
		pyinstaller==6.11.1
		pyinstaller-hooks-contrib==2024.10
		PyMsgBox==1.0.9
		pyotp==2.9.0
		pyperclip==1.9.0
		PyRect==0.2.0
		PyScreeze==1.0.1
		PySocks==1.7.1
		pytweening==1.2.0
		pywin32==310
		pywin32-ctypes==0.2.3
		pywinauto==0.6.8
		requests==2.32.3
		selenium==4.27.1
		setuptools==80.0.0
		six==1.17.0
		sniffio==1.3.1
		sortedcontainers==2.4.0
		trio==0.30.0
		trio-websocket==0.12.2
		typing_extensions==4.13.2
		urllib3==2.2.3
		websocket-client==1.8.0
		wsproto==1.2.0
		XlsxWriter==3.2.0
		xlwings==0.33.4
		xmltodict==0.14.2
