from NMwordDetection.word_detection import word_detection

test = word_detection()
test.load_word_list(".\\words.txt")
test.word_detect("이 병신같은 욕설 탐지 모듈은 씨발도 못 잡아내죠? ㅋㅋ ㅆ1발 ㅆ|발 ㅆ!발 Tlqkf Sibal")