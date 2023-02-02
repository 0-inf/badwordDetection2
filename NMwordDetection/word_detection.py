"""단어 필터링 모듈입니다."""
# -*- coding:utf-8 -*-
import time
import NMwordDetection.filter1 as filter1
import NMwordDetection.filter2 as filter2

class word_detection():
  """
  단어 필터링 클래스입니다.
  """

  def __init__(self) -> None:
    """
    초깃값을 설정합니다
    """

    self.word_list = [] # 찾을 단어 원본 리스트
    self.filter_list = [filter1.filter1(), filter2.filter2()] # 검사할 필터 리스트

    return None

  def load_word_list(self, file_loc : str) -> list:
    """
    찾을 단어 리스트를 불러와 self.word_list에 저장합니다.

    :param file_loc: 불러올 txt파일의 경로입니다.
    :return: 불러온 이후 단어 리스트를 리턴합니다.
    """
    result = []
    f=open(file_loc,'r',encoding="utf-8")
    while True:
      line = f.readline()
      if not line:
        break
      if line.startswith('#'):
        #로 시작되는 줄은 주석임
        pass
      elif not line in result:
        result.append(line.strip())
    self.word_list = result
    return result

  def word_detect(self,sentence:str, threshold:float) -> dict:
    """
    입력된 문장에서 설정된 단어를 찾고 그 결과를 반환합니다

    :param sentence: 검사할 문장입니다.
    :param threshold: 민감도를 설정합니다. 0부터 1 사이의 실수이며 1에 가까울수록 유사도가 더 큰 것들만 찾습니다.
    :return: 결과입니다. 딕셔너리 형태로 각 필터에서 감지된 부분과 그 유사도를 가지고 있습니다.
    """
    start_time = time.time()
    result = {'input':sentence}
    for i in range(len(self.filter_list)):
      filter = self.filter_list[i]
      filter_detection_result = filter.detection(sentence, self.word_list, threshold)
      result[f'filter{i}'] = {
                                'name':filter.name,
                                'description':filter.description,
                                'result': filter_detection_result
                              }
    result['run_time'] = time.time() - start_time
    return result