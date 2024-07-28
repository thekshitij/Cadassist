# -*- coding: utf-8 -*-
"""Innovent project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hnN9e8xLSs0QhsrELDhhbn9K52noW6vP
"""

'''
Dependencies required:
1. Download and install ollama
2. pip install langchain
3. pip install ollama
'''
from langchain.chains import SimpleSequentialChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

class automation():

    def __init__(self,user_input: None|str):
        if user_input==None:
            return "Enter a valid input"
        self.user_input=user_input
        self.error=None
        self.counter=1
        self.curr_response=None
        self.model = OllamaLLM(model="codellama")
        self.exit=False


    def run(self):
        start=self.curr_response.find("<CODE_START")+12
        end=self.curr_response.find("<CODE_END")
        code=self.curr_response[start:end]
        try:
            exec(code)
        except Exception as error:
            print("Error detected: ",error)
            self.error=error #error attr updated !
        else:
            print("No errors")
            self.error=None
        finally:
            print(".run() method complete!")



    def execute(self):
        self.generate_code()
        self.run()

        while self.error != None:
            print("regenerating....")
            self.generate_code()
            if self.exit:
                return "Execution failed try again"
            self.run()
        print(".execute() method complete!")



    def generate_code(self):
        if self.counter>=4:
            self.exit=True
        elif self.counter==1:
            prompt_template=ChatPromptTemplate.from_messages([
              ('system',"""You are an assistant to a CAD Designer and your job is to write a python function to make real time changes to a CAD project adhering to the
                        the user's instructions and execute the function with appropriate arguments as required . Important:
                        1. Envolope the code in <CODE_START> generated code here <CODE_END>
                        2. pip install required depencies"""),
              ('user',"""write a function to perform the following operation in the currently open CAD model using the `win32com.client` library : {user_input}
                  additionally check if AutoCAD is running, and handle errors gracefully and return an error message """) ])

            initial_generate=prompt_template | self.model
            response=initial_generate.invoke({'user_input':self.user_input})
            self.counter+=1 #counter attr updated !
        else:
            prompt_template_name = PromptTemplate(
            input_variables =['old code','error','user input'],
            template = """This is the code you generated earlier: {old code}
                          And this is the error that code generated: {error} .
                          Please fix this error and regenerate the function and call the function with the user's original requirements given below in mind or use random arguments if not provided , which is {user input}"""
            )

            regen_code =LLMChain(llm=self.model, prompt=prompt_template_name)
            response = regen_code.invoke({'old code': self.curr_response, 'error': self.error, 'user input':self.user_input})
            self.counter+=1 #counter attr updated !

        print(".generate_code() method complete! , counter =",self.counter-1)
        self.curr_response=response #updated current response !

input_1=automation("Draw a line from the start point: (2607.2537,1866.4554,0) to end point: (4153.9985,1411.3205,0) in the Drawing1.dwg document in AutoCAD")

input_1.execute()

print(input_1.curr_response)

'''
For executing a user input say input from user => "Draw a line from the start point: (2607.2537,1866.4554,0) to end point: (4153.9985,1411.3205,0) in the Drawing1.dwg document in AutoCAD "

create an instance of the 'automate'
'''