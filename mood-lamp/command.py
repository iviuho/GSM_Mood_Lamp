import json

class Command_Manager:
    def __init__(self, path: str):
        try:
            with open(path, "r", encoding = "UTF8") as f:
                self.command_dict = json.load(f)
        except FileNotFoundError:
            print(path, "파일이 없음")
        self.command_list = [self.command_dict[i] for i in self.command_dict.keys()] # word_list는 "틀어줘, 켜, 틀어주세요"라는 단어가 들어감

    def is_command(self, text: str) -> bool:
        """입력된 문장의 마지막 단어가 명령어 목록 안에 포함되는지 확인한다.

        매개 변수
        ----------
        text: str
            확인을 원하는 문장

        리턴
        -------
        bool
            포함된다면(명령어가 맞다면) True, 아니면 False
        """
        for i in self.command_list:
            if text.split()[-1] in i:
                return True
            elif " ".join(text.split()[-2:]) in i:
                return True
        else:
            return False

    def get_command(self, text: str) -> str:
        """입력된 문장에 해당하는 함수를 문자열로 반환함.

        매개 변수
        ----------
        text: str
            확인을 원하는 문장

        리턴
        -------
        str
            실행해야 할 함수의 이름
        """
        return "".join([i if text in self.command_dict[i] else str() for i in self.command_dict.keys()])

if __name__ == "__main__":
    manager = Command_Manager("command.json")
    while True:
        msg = input("입력 : ")
        if manager.is_command(msg):
            print(manager.get_command(msg))
