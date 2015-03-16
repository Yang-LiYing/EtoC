from distutils.core import setup
import py2exe
setup(windows=['EtoC.py',{"script":"EtoC.py","uac_info":"requireAdministrator","icon_resources":[(1,"images/icon.ico")]}],
      data_files=[("images",["images/translate_off.png","images/translate_on.png"])])
