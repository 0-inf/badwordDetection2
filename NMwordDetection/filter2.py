"""한/영 키보드를 바꾸어 치는 욕설을 잡기 위한 필터입니다"""
import NMwordDetection.tools as tools

class filter2():

  def __init__(self) -> None:
    """
    초기 세팅 함수입니다.
    """
    self.name = "EnProFilter"
    self.description = "한글 단어를 영어 발음으로 쓰는 경우를 잡아내기 위한 필터입니다."
    self.base_layer = {'ㄱ':100,'ㄲ':100.5,'ㅋ':101.5,'ㄴ':110,'ㄹ':120,'ㄷ':130,'ㄸ':130.5,'ㅌ':131.5,'ㅂ':140,'ㅃ':140.5,
                       'ㅍ':141.5,'ㅅ':150,'ㅆ':150.5,'ㅎ':160,'ㅈ':170,'ㅉ':170.5,'ㅊ':171.5,'ㅇ':180,'ㅁ':190,
                       'ㅣ':300,'ㅟ':301,'ㅔ':310,'ㅚ':311,'ㅐ':320,'ㅡ':301,'ㅜ':302,'ㅓ':311,'ㅗ':312,'ㅏ':321,
                       'ㅕ':311.5,'ㅑ':320.5,'ㅛ':312.5,'ㅠ':302.5,'ㅒ':320.5,'ㅖ':310.5,'ㅢ':300.5,'ㅘ':321.5,'ㅙ':320.5,'ㅝ':311.5,'ㅞ':310.5}
    return None

  def detection(self, sentence:str, words:list, threshold:int) -> dict:
    """
    filter1을 이용하여 입력된 단어 리스트를 찾는 함수입니다.

    :param sentence: 문자열 타입으로 단어들을 찾을 문장입니다.
    :param words: 찾을 단어들의 리스트입니다.
    :param threshold: 어느정도 이상의 유사도를 가져야 해당 단어라고 판별할지 값입니다.
    :return: 결과를 잘 정리하여 딕셔너리 형태로 반환합니다.
    """
    # 욕설 처리
    tokenized_words_list = []
    for i in words:
      temp = tools.detach_word(i)
      for j in range(0, len(temp)):
        temp[j] = temp[j][0]
      tokenized_words_list.append(temp)
    
    # sentence 전처리
    one = {'a':'ㅏ', 'o':'ㅗ', 'u':'ㅜ', 'i':'ㅣ', 'e':'ㅔ', 'g':'ㄱ', 'k':'ㅋ',
           'd':'ㄷ', 't':'ㅌ', 'b':'ㅂ', 'p':'ㅍ', 'j':'ㅈ', 's':'ㅅ', 'h':'ㅎ',
           'n': 'ㄴ', 'm': 'ㅁ', 'r': 'ㄹ', 'l': 'ㄹ', 'c':'씨'}
    two = {'ng':'ㅇㅇ', 'ch':'ㅊㅊ', 'kk':'ㄲㄲ', 'tt':'ㄸㄸ', 'pp':'ㅃㅃ', 'ss':'ㅆㅆ', 'jj':'ㅉㅉ',
           'eo':'ㅓㅓ', 'eu':'ㅡㅡ', 'ae':'ㅐㅐ', 'oe':'ㅚㅚ', 'wi':'ㅟㅟ', 'ui':'ㅢㅢ', 'ya':'ㅑㅑ',
           'yo':'ㅛㅛ', 'yu':'ㅠㅠ', 'wa':'ㅘㅘ', 'wo':'ㅟㅟ', 'ye':'ㅖㅖ', 'we':'ㅞㅞ'}
    three = {'yeo':'ㅕㅕㅕ', 'yae':'ㅐㅐㅐ', 'wae':'ㅙㅙㅙ'}
    sentence = sentence.lower()
    for i in range(0, len(sentence)):
      if i <= len(sentence)-3:
        if sentence[i:i+3] in three:
          sentence = sentence[:i]+three[sentence[i:i+3]]+sentence[i+3:]
      if i <= len(sentence)-2:
        if sentence[i:i+2] in two:
          sentence = sentence[:i]+two[sentence[i:i+2]]+sentence[i+2:]
      if sentence[i] in one:
        sentence = sentence[:i]+one[sentence[i]]+sentence[i+1:]
    tokenized_sentence = tools.detach_word(sentence)
    return tools.compare_text(tokenized_sentence, tokenized_words_list, self.base_layer, 0.6)