from NMwordDetection.word_detection import word_detection

test = word_detection()
test.load_word_list(".\\words.txt")
결과 = test.word_detect("이런 씨발 ㅆ1발 슈발 ㅆ|발\n이렇게 여러줄을 입력해도\n이미지 필터는 잘 작동해요 씨발", 0.6)
#결과 가공해보자
print(f'입력된 문장 :\n {결과["input"]}')
print(f'======<{결과["filter0"]["name"]}>=====')
for i in 결과['filter0']['result']:
  print(f"[{결과['input'][i[0]:i[1]+1].strip()}]는 {test.word_list[i[2]]}와 {round(i[3]*100, 4)}% 유사함")
print(f'======<{결과["filter1"]["name"]}>=====')
for i in 결과['filter1']['result']:
  print(f"[{결과['input'][i[0]:i[1]+1].strip()}]는 {test.word_list[i[2]]}와 {round(i[3]*100, 4)}% 유사함")
print(f'======<{결과["filter2"]["name"]}>=====')
for i in 결과['filter2']['result']:
  print(f"[{결과['input'][i[0]:i[1]+1].strip()}]는 {test.word_list[i[2]]}와 {round(i[3]*100, 4)}% 유사함")
print(f'=====================')