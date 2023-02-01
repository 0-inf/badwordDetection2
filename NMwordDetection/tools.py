"""단어 탐지를 위한 도구 함수들이 있는 파일입니다"""
# -*- coding:utf-8 -*-

KOREAN_FIRST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ',
              'ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
KOREAN_MIDDLE = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ',
              'ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
KOREAN_LAST = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ',
                'ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ',
                'ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

def detach_word(word : str) -> list:
  """
  입력된 문자열 중 한국어를 초성, 중성, 종성으로 분해하는 함수입니다.

  :param word: 문자열 타입으로 분해할 문자열입니다.
  :return: 리스트 타입으로 각 요소들은 [(분해된 문자), (분해 전 위치)]의 형태입니다.
  """
  result = []
  for i in range(0, len(word)):
    aski = ord(word[i]) - 44032
    if -1< aski and aski < 11173:
      # 한글이면
      result.append([KOREAN_FIRST[aski // 588], i])
      result.append([KOREAN_MIDDLE[(aski // 28) % 21], i])
      if not aski % 28 == 0:
        # 종성이 존재하면
        result.append([KOREAN_LAST[aski % 28], i])
    else:
      #한글이 아니면 그냥 추가
      result.append([word[i], i])
  return result