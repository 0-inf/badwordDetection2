from NMwordDetection.word_detection import word_detection
import cv2
import numpy

test = word_detection()
test.load_word_list(".\\words.txt")
결과 = test.word_detect("이건 욕설탐지모듈의 결과를 시각화한 결과랍니다.\n=============<결과>=============\n이게 테스트 문장인데, 이 멍청이 컴퓨터는 욕설 못찾을 겁니다.\n아닌가? ㅆ1발. 암튼 컴퓨터는 보통 멍청하기 때문에 Tlqkf만 해도\n못찾을 겁니다. 아니면 ㅆ1발이나 ^^ㅣ발, ㅆ|발,sibal 정도만 해도\n아마 이 qudtls이 욕설을 잘 찾아냈다면\n씨발은 파란색, 병신은 초록색, 멍청이는 빨간색으로 색칠 될거랍니다.\n그리고 더 색이 진할수록 그 유사도가 더 높은 거랍니다. 아래의 예시로 비교해보세요\n씨발 <= 더 진함 ㅆ/발", 0.6)
#결과 가공해보자
data = []
for i in range(len(결과['input'])):
  data.append(list(0.0 for i in range(len(test.word_list))))
print(f'입력된 문장 :\n {결과["input"]}')
print(f'======<{결과["filter0"]["name"]}>=====')
for i in 결과['filter0']['result']:
  print(f"[{결과['input'][i[0]:i[1]+1].strip()}]는 {test.word_list[i[2]]}와 {round(i[3]*100, 4)}% 유사함")
  for j in range(i[0], i[1]+1):
    data[j][i[2]] = max(data[j][i[2]],i[3])
print(f'======<{결과["filter1"]["name"]}>=====')
for i in 결과['filter1']['result']:
  print(f"[{결과['input'][i[0]:i[1]+1].strip()}]는 {test.word_list[i[2]]}와 {round(i[3]*100, 4)}% 유사함")
  for j in range(i[0], i[1]+1):
    data[j][i[2]] = max(data[j][i[2]],i[3])
print(f'======<{결과["filter2"]["name"]}>=====')
for i in 결과['filter2']['result']:
  print(f"[{결과['input'][i[0]:i[1]+1].strip()}]는 {test.word_list[i[2]]}와 {round(i[3]*100, 4)}% 유사함")
  for j in range(i[0], i[1]+1):
    data[j][i[2]] = max(data[j][i[2]],i[3])
print(f'=====================')

# 시각화
COLORLIST = [(255,0,0),(0,255,0),(0,0,255)]
loc_data = test.filter_list[2].sentence_image_data
target = cv2.imread(".\\NMwordDetection\\temp\\sentence.png")
for i in range(len(data)):
  for j in range(len(data[i])):
    temp = target.copy()
    cv2.rectangle(temp, (loc_data[i][0],loc_data[i][1]), (loc_data[i][2],loc_data[i][3]), COLORLIST[j], cv2.FILLED)
    target = cv2.addWeighted(target, 1-(data[i][j]*0.6), temp, data[i][j]*0.6, 0)
cv2.imshow(f"result(times:{결과['run_time']})", target)
cv2.waitKey(0)
cv2.destroyAllWindows()