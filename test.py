from NMwordDetection.word_detection import word_detection
import cv2

test_text = """
양자역학(量子力學 / Quantum mechanics)은 원자와 이를 이루는 아원자 입자들 같은
미시 세계와 그러한 계에서 일어나는 현상에 대해 탐구하는 현대물리학 분야이다.
양자역학은 주로 미시 세계에 활용되고 있지만 거시 세계와도 매우 밀접한 관련을 갖고 있다.
현실 세계의 모든 거시적인 존재들도 결국은 원자의 결합으로 이루어져 있다는 측면에서
거시와 미시의 관련성을 이해해 볼 수 있다.
ᄴ၊발
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