import sys
import urllib.request
import re
import time

class get_translate_text:
    def __init__(self,want_translate_text,translate_engine = "cdict"):
        self.__text = want_translate_text
        self.__engine = translate_engine
        self.__engine_url = self.get_engine_url()

    def get_engine_url(self):
        if self.__engine is "cdict":
            return "http://cdict.net/?q="+self.__text
        else:#defult
            return "http://cdict.net/?q="+self.__text

    def get_translate(self,methon="cdict"):
        #There can addition search engine
        #if methon is "cdict":
        return self.get_translate_from_cdict()
        #add elif to addition engine 
   
    def get_translate_from_cdict(self):
        context = urllib.request.urlopen(self.__engine_url).read()
        context_utf_8 = context.decode('utf-8',errors='ignore')
        translate_text = re.search('<meta name="description" content=".*">',context_utf_8)
        translate_text_format = re.compile('(<meta name="description" content="|">)')
        text = translate_text_format.sub("",str(translate_text.group()))
        return text

if __name__ == "__main__":
    ob = get_translate_text("clipboard")
    getobtime = time.time()
    print(ob.get_translate())
    gettranslatedatatime = time.time()
    print("Use "+str(gettranslatedatatime-getobtime)+" second to find data!!")
