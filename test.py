from NMwordDetection.word_detection import word_detection
import cv2

test = word_detection()
test.load_word_list(".\\words.txt")
결과 = test.word_detect("Project Noto: 한국어만 감지할 순 없으니깐요\n유니코드의 모든 문자를...\nÅ4ŕƵ", 0.1)
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
COLORLIST = [(255,0,0),(0,255,0),(0,0,255)]
loc_data = test.filter_list[2].sentence_image_data
target = cv2.imread(".\\NMwordDetection\\temp\\sentence.png")
for i in range(len(data)):
  for j in range(len(data[i])):
    temp = target.copy()
    cv2.rectangle(temp, (loc_data[i][0],loc_data[i][1]), (loc_data[i][2],loc_data[i][3]), COLORLIST[j], cv2.FILLED)
    target = cv2.addWeighted(target, 1-(data[i][j]*0.6), temp, data[i][j]*0.6, 0)
cv2.imwrite("C:\\Users\\seolc\\OneDrive\\ghg\\uni_text.png", target)
cv2.imshow(f"result(times:{결과['run_time']})", target)
cv2.waitKey(0)
cv2.destroyAllWindows()