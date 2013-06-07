#coding=utf8
__author__ = 'song'
import Image, ImageFont, ImageDraw
import ocr_normalize
import ocr_segmentation
import ocr_feature_extraction
import ocr_binary_image

def get_words_from_file(file_name):
    fi = file(file_name, "r")
    word_dict = {}
    text = fi.read().decode("utf-8")
    fi.close()
    for word in text:
        word_dict[word] = 1

    return word_dict.keys()


def create_image_from_word(word, font):
    assert isinstance(word, unicode)
    im = Image.new("L", (48, 48), 0)
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), word, font=font, fill=255)
    return im


def create():
    res = []
    res_word = []
    words = get_words_from_file("words1")
    font = ImageFont.truetype("TW-Kai-98_1.ttf", 48)
    for word in words:
        #print word
        im = create_image_from_word(word, font)
        _x, _y, x_, y_ = ocr_normalize.GetWordSide(im)
        try:
            im = ocr_segmentation.GetWord(im, _x, _y, x_-_x, y_-_y)
            im = im.resize((48, 48), Image.ANTIALIAS)
            im = ocr_binary_image.BinaryImage(im)
            im.save("image1/"+word.encode("utf-8")+".png")
        except:
            continue


#create()