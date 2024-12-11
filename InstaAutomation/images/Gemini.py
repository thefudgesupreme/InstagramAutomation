import os, pickle
import google.generativeai as genai

class Gemini:
    __MODEL_PRO = 'gemini-1.5-pro'
    __MODEL_VISION = 'gemini-1.5-pro'
    __GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    model = None
    def __init__(self,api:str=None,  vision:bool=False, creative:bool=False):
        self.api = api if api else self.__GOOGLE_API_KEY
        if creative:
            self.config=genai.GenerationConfig(
                max_output_tokens=16384,
                temperature=1.0,
                top_k=36,
                top_p=0.9,
            )
        else:
            self.config=genai.GenerationConfig()


        if vision:
            self.model =  genai.GenerativeModel(self.__MODEL_VISION,generation_config=self.config)
        else:
            self.model =  genai.GenerativeModel(self.__MODEL_PRO,generation_config=self.config)


    def chat(self, prompts):
        responses = []
        
        for prompt in prompts:
            try:
                response = self.model.generate_content(prompt)
                response.resolve()
                responses.append(response)
                del response
            except Exception as e:
                print(e)
                responses.append("Error:429")
        # if savehistory:
        #     if self.__MODEL_PRO == self.model.model_name.split('/')[1]:
        #         with open(file, 'wb') as fp:
        #             pickle.dump(chat.history, fp)


        return responses