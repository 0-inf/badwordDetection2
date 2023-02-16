from PIL import Image, ImageDraw, ImageFont
from os import getcwd
from numpy import all, array, zeros, linspace, where
import cv2

font_file = ImageFont.truetype(f"{getcwd()}\\NMwordDetection\\font\\NotoSansCJK.otf", 45)

def text_to_image(name:str, text:str) -> list:
  lines = text.split("\n")
  data = []
  image_width = 0
  image_height = 0
  for line in lines:
    image_width = max(image_width, font_file.getlength(line))
    image_height += (font_file.getbbox(line)[3] - font_file.getbbox(line)[1])
  canvas = Image.new("RGB", (int(image_width), int(image_height)), "white")
  draw = ImageDraw.Draw(canvas)
  line_draw_y = -font_file.getbbox(lines[0])[1]
  data_y = 0
  for line in lines:
    line_draw_x = -font_file.getbbox(line)[0]
    for letter in line:
      draw.text((line_draw_x, line_draw_y), letter, "black",font=font_file)
      data.append((line_draw_x, data_y, line_draw_x + int(font_file.getlength(letter)), data_y + int(font_file.getbbox(letter)[3] - font_file.getbbox(letter)[1])))
      line_draw_x += int(font_file.getlength(letter))
    line_draw_y += (font_file.getbbox(line)[3] - font_file.getbbox(line)[1])
    data_y += (font_file.getbbox(line)[3] - font_file.getbbox(line)[1])
  canvas.save(f"{getcwd()}\\NMwordDetection\\temp\\{name}.png","PNG")
  return data

def image_modify(image:str, data:list) -> list:
  img = cv2.imread(f"{getcwd()}\\NMwordDetection\\temp\\{image}.png")
  new_image = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
  cv2.imwrite(f"{getcwd()}\\NMwordDetection\\temp\\{image}.png", new_image)
  return data

class filter3():

  def __init__(self) -> None:
    """
    초기 세팅 함수입니다.
    """
    self.name = "ImageFilter"
    self.description = "한글과 비슷한 모습을 가지게 쓰는 말들을 찾아내는 필터입니다."
    self.sentence_image_data = []
    return None

  def setup(self, sentence:str, words:list) -> None:
    """
    Image필터를 세팅합니다. sentence와 words의 이미지를 만들고 후처리를 한 후 데이터를 반환합니다.
    """
    self.words_image_data = text_to_image("sentence", sentence)
    for i in range(0,len(words)):
      self.words_image_data.append(text_to_image(i, words[i]))
    return None

  def detection(self, sentence:str, words:list, threshold:int) -> dict:
    """
    filter3을 이용하여 입력된 단어 리스트를 찾는 함수입니다.

    :param sentence: 문자열 타입으로 단어들을 찾을 문장입니다.
    :param words: 찾을 단어들의 리스트입니다.
    :param threshold: 어느정도 이상의 유사도를 가져야 해당 단어라고 판별할지 값입니다.
    :return: 결과를 잘 정리하여 딕셔너리 형태로 반환합니다.
    """
    raw_image = cv2.imread(f"{getcwd()}\\NMwordDetection\\temp\\sentence.png")
    image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
    for i in range(0,len(words)):
      template = cv2.imread(f"{getcwd()}\\NMwordDetection\\temp\\{i}.png")
      template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
      template = cv2.Canny(template, 50, 200)
      (tH, tW) = template.shape[:2]
      for scale in linspace(0.2,1.0,20)[::-1]:
        resized = cv2.resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))
        if resized.shape[0] < tH or resized.shape[1] < tW:
          break
        edged = cv2.Canny(resized, 50, 200)
        res = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
        loc = where(res >= threshold)

        for pt in zip(*loc[::-1]):
          cv2.rectangle(raw_image, (int(pt[0]/scale),int(pt[1]/scale)), (int(pt[0]/scale) + tW, int(pt[1]/scale) + tH), (0,0,255), 2)
    cv2.imshow("Image", raw_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return None