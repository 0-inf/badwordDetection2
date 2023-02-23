from NMwordDetection.word_detection import word_detection
import cv2

test_text = """
동해 물과 백두산이 마르고 닳도록
하느님이 보우하사 우리나라 만세.
무궁화 삼천리 화려 강산
대한 사람, 대한으로 길이 보전하세.
남산 위에 저 소나무, 철갑을 두른 듯
바람서리 불변함은 우리 기상일세.
무궁화 삼천리 화려 강산
대한 사람, 대한으로 길이 보전하세.
가을 하늘 공활한데 높고 구름 없이
밝은 달은 우리 가슴 일편단심일세.
무궁화 삼천리 화려 강산
대한 사람, 대한으로 길이 보전하세.
이 기상과 이 맘으로 충성을 다하여
괴로우나 즐거우나 나라 사랑하세.
무궁화 삼천리 화려 강산
대한 사람, 대한으로 길이 보전하세.
"""

test = word_detection()
test.load_word_list(".\\words.txt")
결과 = test.word_detect(test_text, 0.7)
#결과 가공해보자
data = []
for i in range(len(결과['input'])):
  data.append(list(0.0 for i in range(len(test.word_list))))
print(f'입력된 문장 :\n {결과["input"]}')
print(f'======<{결과["filter0"]["name"]}>=====')
for i in 결과['filter0']['result']:
  if round(i[3]*100, 4) > 60:
    print(f"[{결과['input'][i[0]:i[1]+1].strip()}]는 {test.word_list[i[2]]}와 {round(i[3]*100, 4)}% 유사함")
  for j in range(i[0], i[1]+1):
    data[j][i[2]] = max(data[j][i[2]],i[3])
print(f'======<{결과["filter1"]["name"]}>=====')
for i in 결과['filter1']['result']:
  if round(i[3]*100, 4) > 60:
    print(f"[{결과['input'][i[0]:i[1]+1].strip()}]는 {test.word_list[i[2]]}와 {round(i[3]*100, 4)}% 유사함")
  for j in range(i[0], i[1]+1):
    data[j][i[2]] = max(data[j][i[2]],i[3])
print(f'======<{결과["filter2"]["name"]}>=====')
for i in 결과['filter2']['result']:
  if round(i[3]*100, 4) > 60:
    print(f"[{결과['input'][i[0]:i[1]+1].strip()}]는 {test.word_list[i[2]]}와 {round(i[3]*100, 4)}% 유사함")
  for j in range(i[0], i[1]+1):
    data[j][i[2]] = max(data[j][i[2]],i[3])
print(f'=====================')

#시각화
COLOR = (255,0,0)
loc_data = test.filter_list[2].sentence_image_data
target = cv2.imread(".\\NMwordDetection\\temp\\sentence.png")
for i in range(len(data)):
  for j in range(len(data[i])):
    temp = target.copy()
    cv2.rectangle(temp, (loc_data[i][0],loc_data[i][1]), (loc_data[i][2],loc_data[i][3]), COLOR, cv2.FILLED)
    target = cv2.addWeighted(target, 1-(data[i][j]*0.9), temp, data[i][j]*0.9, 0)
cv2.imshow(f"result(times:{결과['run_time']})", target)
cv2.waitKey(0)
cv2.destroyAllWindows()