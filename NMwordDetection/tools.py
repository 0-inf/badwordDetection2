"""단어 탐지를 위한 도구 함수들이 있는 파일입니다"""
# -*- coding:utf-8 -*-

KOREAN_FIRST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ',
              'ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
KOREAN_MIDDLE = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ',
              'ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
KOREAN_LAST = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ',
                'ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ',
                'ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

def detach_word(word : str, option : dict = {"repeat":True, "pro2del":False}) -> list:
  """
  입력된 문자열 중 한국어를 초성, 중성, 종성으로 분해하는 함수입니다.

  :param word: 문자열 타입으로 분해할 문자열입니다.
  :param option: 상세 옵션을 설정할 수 있습니다.
  :return: 리스트 타입으로 각 요소들은 [(분해된 문자), (분해 전 위치)]의 형태입니다.
  """
  result = []
  for i in range(0, len(word)):
    if option['repeat'] and i != 0 and word[i] == word[i-1]:
      pass
    else:
      aski = ord(word[i]) - 44032
      if -1< aski and aski < 11173:
        # 한글이면
        if option['pro2del'] and KOREAN_FIRST[aski // 588] in ['ㅇ']:
          pass
        else:
          result.append([KOREAN_FIRST[aski // 588], i])
        result.append([KOREAN_MIDDLE[(aski // 28) % 21], i])
        if not aski % 28 == 0:
          # 종성이 존재하면
          result.append([KOREAN_LAST[aski % 28], i])
      else:
        #한글이 아니면
        if word[i] != ' ': # 공백 제거
          result.append([word[i], i])
  return result

def compare_text(sentence:list, words:list, base_layer:dict, threshold:float) -> list:
  """
  base_layer의 데이터를 기반으로 sentence에서 word와의 유사도가 threshold 이상인 부분을 찾아냅니다.

  :param sentence: 토큰화가 된 문장입니다.
  :param words: 토큰화가 된 단어 리스트입니다.
  :param base_layer: 한글 자모를 비교할 때의 기준이 되는 데이터입니다.
  :param threshold: 어느 정도 이상의 유사도를 가져야 할지 설정하는 0과 1사이의 실수값입니다.
  :return: 결과를 리스트 형태로 반환합니다.
  """
  sentence_layer = []
  for i in range(0,len(sentence)):
    if sentence[i][0] in base_layer:
      sentence_layer.append([base_layer[sentence[i][0]], sentence[i][1]])
  for i in range(0, len(words)):
    for j in range(0, len(words[i])):
      if words[i][j] in base_layer:
        words[i][j] = base_layer[words[i][j]]
  result = []
  temp = []
  for index in range(0,len(words)):
    word = words[index]
    for i in range(0, len(sentence_layer)-len(word)+1):
      similarity = 0
      for j in range(0, len(word)):
        most_sim_string_loc = None
        for k in range(max(0, i-3), min(len(sentence_layer), i+len(word)+3)):
          if word[j] // 10 == sentence_layer[k][0] // 10:
            if most_sim_string_loc is None:
              most_sim_string_loc = k
            elif abs(k-(i+j)) < abs(most_sim_string_loc-(i+j)):
              most_sim_string_loc = k
        if most_sim_string_loc is not None:
          similarity += 0.1 / pow(2, (abs(most_sim_string_loc-(i+j))))*(10-abs(word[j] - sentence_layer[most_sim_string_loc][0]))
      similarity = similarity / len(word)
      similarity = similarity ** (0.1**((len(word)-3)/10)+1.3)
      if similarity > threshold:
        if sentence_layer[i][1] not in temp:
          result.append([sentence_layer[i][1], sentence_layer[i+len(word)-1][1], index, similarity])
          temp.append(sentence_layer[i][1])
  return result

def select_fontfile(str:str):
  uni = ord(str)
  # JP
  if uni >= 12352 and uni <= 12447:
    return "JP"
  elif uni >= 12448 and uni <= 12543:
    return "JP"
  elif uni >= 12784 and uni <= 12799:
    return "JP"
  # KR
  elif uni >= 4352 and uni <= 4607:
    return "KR"
  elif uni >= 12593 and uni <= 12687:
    return "KR"
  elif uni >= 44032 and uni <= 55203:
    return "KR"
  elif uni >= 43072 and uni <= 43135:
    return "KR"
  elif uni >= 43360 and uni <= 43391:
    return "KR"
  # SC
  elif uni >= 19968 and uni <= 40895:
    return "SC"
  # TC
  elif uni >= 63744 and uni <= 64031:
    return "TC"
  elif uni >= 131072 and uni <= 216895:
    return "TC"
  # Armenian
  elif uni > 1328 and uni <= 1423:
    return "Armenian"
  # Hebrew
  elif uni >= 1424 and uni <= 1535:
    return "Hebrew"
  # Arabic
  elif uni >= 1536 and uni <= 1791:
    return "Arabic"
  # Syriac
  elif uni >= 1792 and uni <= 1871:
    return "Syriac"
  # Thaana
  elif uni >= 1920 and uni <= 1983:
    return "Thaana"
  # Devanagari
  elif uni >= 2304 and uni <= 2431:
    return "Devanagari"
  # Bengali
  elif uni >= 2432 and uni <= 2559:
    return "Bengali"
  # Gurmukhi
  elif uni >= 2560 and uni <= 2687:
    return "Gurmukhi"
  # Gujarati
  elif uni >= 2688 and uni <= 2815:
    return "Gujarati"
  # Oriya
  elif uni >= 2816 and uni <= 2943:
    return "Oriya"
  # Tamil
  elif uni >= 2944 and uni <= 3071:
    return "Tamil"
  # Telugu
  elif uni >= 3072 and uni <= 3199:
    return "Telugu"
  # Kannada
  elif uni >= 3200 and uni <= 3327:
    return "Kannada"
  # Malayalam
  elif uni >= 3328 and uni <= 3455:
    return "Malayalam"
  # Sinhala
  elif uni >= 3456 and uni <= 3583:
    return "Sinhala"
  # Thai
  elif uni >= 3584 and uni <= 3711:
    return "Thai"
  # Lao
  elif uni >= 3712 and uni <= 3839:
    return "Lao"
  # Myanmar
  elif uni >= 4096 and uni <= 4255:
    return "Myanmar"
  # Georgian
  elif uni >= 4256 and uni <= 4351:
    return "Georgian"
  # Ethiopic
  elif uni >= 4608 and uni <= 4991:
    return "Ethiopic"
  # Cherokee
  elif uni >= 5024 and uni <= 5119:
    return "Cherokee"
  # Canadian Aboriginal
  elif uni >= 5120 and uni <= 5759:
    return "CanadianAboriginal"
  # Ogham
  elif uni >= 5760 and uni <= 5791:
    return "Ogham"
  # Runic
  elif uni >= 5792 and uni <= 5887:
    return "Runic"
  # Khmer
  elif uni >= 6016 and uni <= 6143:
    return "Khmer"
  # Mongolian
  elif uni >= 6144 and uni <= 6319:
    return "Mongolian"
  # else
  else:
    return "default"