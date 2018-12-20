def word_music(msg):
    f = open("언어.txt", "r")

    data = f.read()
    
    msg_word = msg.split() #msg를 split 으로 정리    
    word_list = data.split() #word_list는 "틀어줘, 켜, 틀어주세요"라는 단어가 들어감

    #set_word_list = set(word_list)

    for x in range(len(word_list)):
        if word_list[x] == msg_word[-1]:
            del msg_word[-1]
            music = " ".join(msg_word)
            return music 
    return "없음"

if __name__ == "__main__":
    msg = input("입력 : ")
    print(word_music(msg))
