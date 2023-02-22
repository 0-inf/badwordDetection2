from PIL import Image, ImageDraw, ImageFont
from os import getcwd
from numpy import all, array, zeros, linspace, where, ones
import cv2
from NMwordDetection.tools import select_fontfile

font_list_raw = {
  # 이름 변경 금지!!
  "default":"NotoSans.ttf",
  "JP":"NotoSansJP.otf",
  "KR":"NotoSansKR.otf",
  "SC":"NotoSansSC.otf",
  "TC":"NotoSansTC.otf",
  "Bamun":"NotoSansBamum.ttf",
  "Khmer":"NotoSansKhmer.ttf",
  "Mongolian":"NotoSansMongolian.ttf",
  "Tagbanwa":"NotoSansTagbanwa.ttf",
}
font_list = {}
for key, value in font_list_raw.items():
  font_list[key]=ImageFont.truetype(f"{getcwd()}\\NMwordDetection\\font\\{value}", 45)

def text_to_image(name:str, text:str) -> list:
  lines = text.split("\n")
  data = [] # data of location of each char in text [x1, y1, x2, y2], if char is \n, [-100,-100,-100,-100]
  image_width = 0 # width of image
  image_height = 0 # height of image
  line_height = [] # height of line(Most biggest height of char in line)
  draw_x = [] # x location of each line
  draw_y = [] # y location of each line
  for i in range(len(lines)):
    line = lines[i]
    line_width = 0 # width of line
    line_height.append(0) # height of line
    line_draw_x = [] # x location of each char in line
    line_draw_y = [] # y location of each char in line
    for j in range(len(line)):
      char = line[j]
      font = font_list[select_fontfile(char)]
      box = font.getbbox(char)
      line_height[i] = max(line_height[i], box[3]-box[1])
    for j in range(len(line)):
      char = line[j]
      font = font_list[select_fontfile(char)]
      box = font.getbbox(char)
      data.append((line_width, image_height, line_width+box[2]-box[0], image_height+line_height[i]))
      line_width += box[2]-box[0]
      if j == 0:
        line_draw_x.append(-box[0])
      line_draw_x.append(line_draw_x[-1]+box[2]-box[0])
      line_draw_y.append(image_height+line_height[i]-box[3])
    image_width = max(image_width, line_width)
    image_height += line_height[i]
    draw_x.append(line_draw_x)
    draw_y.append(line_draw_y)
    data.append((-100,-100,-100,-100))
  image = Image.new("RGB", (image_width, image_height), (255,255,255))
  draw = ImageDraw.Draw(image)
  for i in range(len(lines)):
    line = lines[i]
    for j in range(len(line)):
      char = line[j]
      font = font_list[select_fontfile(char)]
      draw.text((draw_x[i][j], draw_y[i][j]), char, font=font, fill=(0,0,0))
  image.save(f"{getcwd()}\\NMwordDetection\\temp\\{name}.png")
  return data

def image_modify(image:str, data:list = []) -> list:
  img = cv2.imread(f"{getcwd()}\\NMwordDetection\\temp\\{image}.png")
  thres_image = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
  if data == []:
    new_image_line = []
    for i in range(0,thres_image.shape[1]):
      check = True
      for j in range(0, thres_image.shape[0]):
        if not all(thres_image[j,i] == 255):
          check = False
          break
      if not check:
        new_image_line.append(i)
    new_image = zeros((thres_image.shape[0], len(new_image_line), 3), dtype="uint8")
    for i in range(0, len(new_image_line)):
      new_image[0:thres_image.shape[0],i] = thres_image[0:thres_image.shape[0],new_image_line[i]]
    cv2.imwrite(f"{getcwd()}\\NMwordDetection\\temp\\{image}.png", new_image)
    return [];
  else:
    new_data = []
    new_image_cut_y = [(-100,-100)]
    temp = []
    tmp_tmp = []
    for i in data:
      if (i[1], i[3]) not in new_image_cut_y:
        new_image_cut_y.append((i[1], i[3]))
      if i[1] != -100:
        tmp_tmp.append(i[2]-1)
      else:
        temp.append(tmp_tmp)
        tmp_tmp = []
    del new_image_cut_y[0]
    new_image_size = [0,thres_image.shape[0]]
    new_image_data = []
    for k in range(len(new_image_cut_y)):
      new_data.append((-100,-100,-100,-100))
      lines = new_image_cut_y[k]
      new_image_line = []
      tmp_tmp = [0]
      for i in range(0,thres_image.shape[1]):
        check = True
        for j in range(lines[0], lines[1]):
          if not all(thres_image[j,i] == 255):
            check = False
            break
        if not check:
          new_image_line.append(i)
        if i in temp[k]:
          new_data.append((tmp_tmp[-1], lines[0], len(new_image_line) if len(new_image_line) != tmp_tmp[-1] else len(new_image_line)+1, lines[1]))
          tmp_tmp.append(len(new_image_line))
      new_image_size[0] = max(new_image_size[0], len(new_image_line))
      new_image_data.append(new_image_line)
    new_image = ones((new_image_size[1], new_image_size[0], 3), dtype="uint8")*255
    for i in range(0, len(new_image_cut_y)):
      for j in range(0, len(new_image_data[i])):
        new_image[new_image_cut_y[i][0]:new_image_cut_y[i][1],j] = thres_image[new_image_cut_y[i][0]:new_image_cut_y[i][1],new_image_data[i][j]]
    cv2.imwrite(f"{getcwd()}\\NMwordDetection\\temp\\{image}_mod.png", new_image)
    return new_data[1:]

def make_better(x : float) -> float:
  return (-2*x*x+3*x)*x

class filter3():

  def __init__(self) -> None:
    """
    초기 세팅 함수입니다.
    """
    self.name = "ImageFilter"
    self.description = "한글과 비슷한 모습을 가지게 쓰는 말들을 찾아내는 필터입니다."
    self.sentence_image_data = []
    self.sentence_image_mod_data = []
    return None

  def setup(self, sentence:str, words:list) -> None:
    """
    Image필터를 세팅합니다. sentence와 words의 이미지를 만들고 후처리를 한 후 데이터를 반환합니다.
    """
    self.sentence_image_data = text_to_image("sentence", sentence)
    self.sentence_image_mod_data = image_modify("sentence", self.sentence_image_data)
    for i in range(0,len(words)):
      text_to_image(i, words[i])
      image_modify(i)
    return None

  def detection(self, sentence:str, words:list, threshold:int) -> list:
    """
    filter3을 이용하여 입력된 단어 리스트를 찾는 함수입니다.

    :param sentence: 문자열 타입으로 단어들을 찾을 문장입니다.
    :param words: 찾을 단어들의 리스트입니다.
    :param threshold: 어느정도 이상의 유사도를 가져야 해당 단어라고 판별할지 값입니다.
    :return: 결과를 잘 정리하여 리스트 형태로 반환합니다.
    """
    result = []
    raw_image = cv2.imread(f"{getcwd()}\\NMwordDetection\\temp\\sentence_mod.png")
    image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
    for i in range(0,len(words)):
      template = cv2.imread(f"{getcwd()}\\NMwordDetection\\temp\\{i}.png")
      template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
      template = cv2.Canny(template, 50, 200)
      (tH, tW) = template.shape[:2]
      for scale in linspace(0.2,1.0,20)[::-1]:
      #for scale in range(1,2):
        resized = cv2.resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))
        if resized.shape[0] < tH or resized.shape[1] < tW:
          break
        edged = cv2.Canny(resized, 50, 200)
        res = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
        loc = where(make_better(res) >= threshold)
        k = 0
        for pt in zip(*loc[::-1]):
          a = 0
          start = 0
          end = 0
          while a < len(self.sentence_image_mod_data):
            if self.sentence_image_mod_data[a][0] <= (pt[0]/scale) and self.sentence_image_mod_data[a][1] -0.1 < (pt[1]/scale) and self.sentence_image_mod_data[a][2] > (pt[0]/scale) and self.sentence_image_mod_data[a][3] >= (pt[1]/scale):
              start = a
            elif self.sentence_image_mod_data[a][0] <= (pt[0]/scale) + tW and self.sentence_image_mod_data[a][1] < (pt[1]/scale) + tH and self.sentence_image_mod_data[a][2] >= (pt[0]/scale) + tW and self.sentence_image_mod_data[a][3] >= (pt[1]/scale) + tH:
              end = a
              break
            a+=1
          result.append((start, end,i,make_better(res[loc][k])))
          k+=1
    return result