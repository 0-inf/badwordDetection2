from NMwordDetection.word_detection import word_detection

test = word_detection()
test.load_word_list(".\\words.txt")
결과 = test.word_detect("Tlqkf tlqkf qudtls qbdtls Sibal SSibal C발", 0.6)
#결과 가공해보자
print(f'입력된 문자 : {결과["input"]}')
print(f'======<{결과["filter0"]["name"]}>=====')
for i in 결과['filter0']['result']:
  print(f"[{결과['input'][i[0]:i[1]+1]}]는 {test.word_list[i[2]]}와 {round(i[3]*100, 4)}% 유사함")
print(f'======<{결과["filter1"]["name"]}>=====')
for i in 결과['filter1']['result']:
  print(f"[{결과['input'][i[0]:i[1]+1]}]는 {test.word_list[i[2]]}와 {round(i[3]*100, 4)}% 유사함")
print(f'=====================')