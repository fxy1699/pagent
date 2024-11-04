from loadTTS import load_tts
import os
import erniebot


class Agent:
    def __init__(self, token: str, system: str=None):
        erniebot.api_type = "aistudio"
        erniebot.access_token = token
        print("载入token", token, "\n")
        if system is None:
            self.system = '你是一个智能助手，需要根据用户的需求回复相应的简单问题, 你有check_whether,check_time,beam,text四个元动作，可以检查天气，检查时间，发出声音与生成文本。当用户对你说话时，你需要生成一段文本[response]，并发出声音。'
        else:
            self.system = system

        self.functions = [
            self.check_whether_desc(),
            self.check_time_desc(),
            self.beam_desc(),
            self.text_desc()
        ]
        self.messages = []
    
    def get_action(self, message):
        if isinstance(message, str):
            message = {'role': 'user', 'content': message}
        self.messages.append(message)

        create_kwargs = {
            'model': 'ernie-3.5',
            'messages': self.messages,
            'system': self.system,
            'functions': self.functions,
            'top_p':0
        }

        response = erniebot.ChatCompletion.create(**create_kwargs)

        if response.is_function_response:
            function_call = response.get_result()
            self.messages.append(response.to_message())
            return True, function_call
        else:
            # 模型返回普通的文本消息
            result = response.get_result()
            self.messages.append(response.to_message())
            return False, result
    
    @staticmethod
    def check_whether_desc():
        desc = {
            'name': 'check_whether',
            'description': '获得指定城市天气',
            'parameters': {
                'type': 'object',
                'properties': {
                    'location': {
                        'type': 'string',
                        'description': '城市名称',
                    },
                    'unit': {
                        'type': 'string',
                        'enum': [
                            '摄氏度',
                            '华氏度',
                        ],
                    },
                },
                'required': [
                    'location',
                    'unit',
                ],
            },
            'response':{
                'type': 'object',
                'properties': {
                    'temperature':{
                        'type': 'integer',
                        'description': '城市气温',
                    },
                    'unit': {
                        'type': 'string',
                        'enum': [
                            '摄氏度',
                            '华氏度',
                        ],
                    },
                },
            },
        }
        return desc

    @staticmethod
    def check_time_desc():
        desc = {
            'name': 'check_time',
            'description': '根据时区获得当前的时间',
            'parameters': {
                'type': 'object',
                'properties': {
                    'timezone': {
                        'type': 'string',
                        'description': '时区',
                    },
                },
                'required': [
                    'timezone',
                ],
            },
            'response':{
                'type': 'object',
                'properties': {
                    'time':{
                        'type': 'string',
                        'description': '时间',
                    },
                },
            },
        }
        return desc
    @staticmethod
    def beam_desc():
        desc = {
            'name': 'beam',
            'description': '发光',
            'parameters': {
                'type': 'object',
                'properties': {
                    'intext': {
                        'type': 'string',
                        'description': '需要转为音频的文本',
                    },
                },
                'required': [
                    'intext',
                ],
            },
        }
        return desc

    @staticmethod
    def text_desc():
        desc = {
            'name': 'text',
            'description': '生成文本',
            'parameters': {
                'type': 'object',
                'properties': {
                },
            },
            'response':{
                'type': 'object',
                'properties': {
                    'outtext':{
                        'type': 'string',
                        'description': '生成的文本',
                    },
                },
            },
        }
        return desc

if __name__ == "__main__":
    token = '5058cea7fe88ff722ba56f8639010b5e88a0954f'
    agent = Agent(token)
    command = '当前天津津南区的天气是，你不需要调用函数'

    while True:
        ret, action = agent.get_action(command)
        if ret:
            print(" <<< 文心大模型：", action["thoughts"])
            print("   - 调用方法：", action["name"])
            print("   - 调用参数：", action["arguments"])
        else:
            print(" <<< 文心大模型：", action)
            break
        
        command = "已完成以上动作"
        print(" >>> 反馈：", command, "\n")