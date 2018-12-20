class Command_Manager:
    def __init__(self, path: str):
        try:
            with open(path, "r", encoding = "UTF8") as f:
                self.command_list = f.read().split() # word_list는 "틀어줘, 켜, 틀어주세요"라는 단어가 들어감
        except FileNotFoundError:
            print(path, "파일이 없음")

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
        return True if text.split()[-1] in self.command_list else False

if __name__ == "__main__":
    manager = Command_Manager("word.txt")
    while True:
        msg = input("입력 : ")
        print(manager.is_command(msg))
