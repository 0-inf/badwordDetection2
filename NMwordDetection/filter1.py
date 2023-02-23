"""한/영 키보드를 바꾸어 치는 욕설을 잡기 위한 필터입니다"""
import NMwordDetection.tools as tools

class filter1():

  def __init__(self) -> None:
    """
    초기 세팅 함수입니다.
    """
    self.name = "KoEnKeyBoFilter"
    self.description = "한글 단어를 영어 키보드로 쓰는 경우를 잡아내기 위한 필터입니다."
    self.key_change_data = {'q': 'ㅂ', 'Q': 'ㅃ', 'w': 'ㅈ', 'W': 'ㅉ', 'e': 'ㄷ', 'E': 'ㄸ',
                            'r': 'ㄱ', 'R': 'ㄲ', 't': 'ㅅ', 'T': 'ㅆ', 'y': 'ㅛ', 'Y': 'ㅛ',
                            'u': 'ㅕ', 'U': 'ㅕ', 'i': 'ㅑ', 'I': 'ㅑ', 'o': 'ㅐ', 'O': 'ㅒ',
                            'p': 'ㅔ', 'P': 'ㅖ', 'a': 'ㅁ', 'A': 'ㅁ', 's': 'ㄴ', 'S': 'ㄴ',
                            'd': 'ㅇ', 'D': 'ㅇ', 'f': 'ㄹ', 'F': 'ㄹ', 'g': 'ㅎ', 'G': 'ㅎ',
                            'h': 'ㅗ', 'H': 'ㅗ', 'j': 'ㅓ', 'J': 'ㅓ', 'k': 'ㅏ', 'K': 'ㅏ',
                            'l': 'ㅣ', 'L': 'ㅣ', 'z': 'ㅋ', 'Z': 'ㅋ', 'x': 'ㅌ', 'X': 'ㅌ',
                            'c': 'ㅊ', 'C': 'ㅊ', 'v': 'ㅍ', 'V': 'ㅍ', 'b': 'ㅠ', 'B': 'ㅠ',
                            'n': 'ㅜ', 'N': 'ㅜ', 'm': 'ㅡ', 'M': 'ㅡ'}
    self.base_layer = {'ㄱ':100,'ㄲ':100.5,'ㅋ':101.5,'ㄴ':110,'ㄹ':120,'ㄷ':130,'ㄸ':130.5,'ㅌ':131.5,'ㅂ':140,'ㅃ':140.5,
                       'ㅍ':141.5,'ㅅ':150,'ㅆ':150.5,'ㅎ':160,'ㅈ':170,'ㅉ':170.5,'ㅊ':171.5,'ㅇ':180,'ㅁ':190,
                       'ㅣ':300,'ㅟ':301,'ㅔ':310,'ㅚ':311,'ㅐ':320,'ㅡ':301,'ㅜ':302,'ㅓ':311,'ㅗ':312,'ㅏ':321,
                       'ㅕ':311.5,'ㅑ':320.5,'ㅛ':312.5,'ㅠ':302.5,'ㅒ':320.5,'ㅖ':310.5,'ㅢ':300.5,'ㅘ':321.5,'ㅙ':320.5,'ㅝ':311.5,'ㅞ':310.5}
    return None

  def threshold_better(self, threshold:int) -> int:
    """
    threshold를 더 높이는 함수입니다.

    :param threshold: 현재 threshold입니다.
    :return: 더 높은 threshold를 반환합니다.
    """
    return threshold*(-1*threshold*threshold+threshold+1)

  def detection(self, sentence:str, words:list, threshold:int) -> list:
    """
    filter1을 이용하여 입력된 단어 리스트를 찾는 함수입니다.

    :param sentence: 문자열 타입으로 단어들을 찾을 문장입니다.
    :param words: 찾을 단어들의 리스트입니다.
    :param threshold: 어느정도 이상의 유사도를 가져야 해당 단어라고 판별할지 값입니다.
    :return: 결과를 잘 정리하여 리스트 형태로 반환합니다.
    """
    tokenized_sentence = tools.detach_word(sentence)
    tokenized_words_list = []
    for i in words:
      temp = tools.detach_word(i)
      for j in range(0, len(temp)):
        temp[j] = temp[j][0]
      tokenized_words_list.append(temp)
    for i in range(0,len(tokenized_sentence)):
      if tokenized_sentence[i][0] in self.key_change_data:
        tokenized_sentence[i][0] = self.key_change_data[tokenized_sentence[i][0]]
    return tools.compare_text(tokenized_sentence, tokenized_words_list, self.base_layer, self.threshold_better(threshold))