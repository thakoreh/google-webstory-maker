from wsgiref import headers
from transformers import pipeline
import creds
import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

def requestsToPexels(category):
    url = f'https://api.pexels.com/v1/search?query={category}&orientation=vertical'
    headers = {'Authorization': creds.API_KEY}
    responseImg = requests.get(url, headers=headers)
    import random
    photo  = responseImg.json()['photos'][random.randint(1, 15)]
    photo  = photo['src']['portrait']
    imagePath  = getImage(photo,category)
    return imagePath

def getImage(photo,category):
    img_data = requests.get(photo).content
    img_name = f'{category}.jpg'
    with open(img_name, 'wb') as handler:
        handler.write(img_data)
    return img_name

def processImage(selectedPicForThisTopic,line,count):
    img = Image.open(selectedPicForThisTopic)

    # Resize the image 
    width = 800
    img_w = img.size[0]
    img_h = img.size[1]
    wpercent = (width/float(img_w))
    hsize = int((float(img_h)*float(wpercent)))
    rmg = img.resize((width,hsize), Image.ANTIALIAS)

    # Set x boundry
    # Take 10% to the left for min and 50% to the left for max
    x_min = (rmg.size[0] * 8) // 100
    x_max = (rmg.size[0] * 50) // 100
    # Randomly select x-axis
    from random import randint
    ran_x = randint(x_min, x_max)
    font = ImageFont.truetype(r'Antonio-Bold.ttf', 26)
    lines = text_wrap(line, font, rmg.size[0]-ran_x)
    # to add the appropriate line spacing
    line_height = font.getsize('hg')[1]

    y_min = (rmg.size[1] * 4) // 100   # 4% from the top
    y_max = (rmg.size[1] * 80) //100   # 90% to the bottom
    y_max -= (len(lines)*line_height)  # Adjust
    ran_y = randint(y_min, y_max)      # Generate random point

    draw = ImageDraw.Draw(rmg)
    ran_y = y_max
    # font = ImageFont.truetype(r'Antonio-Bold.ttf', 72)
    # lines = text_wrap(line, font, rmg.size[0]-ran_x)
    position = (ran_x, ran_y)
    color = 'rgb(0,0,0)'
    x = ran_x
    y = ran_y

    for line in lines:
        # draw.text((x,y), line, fill=color, font=font)
        
        # y = y + line_height    # update y-axis for new line

        left, top, right, bottom = draw.textbbox((x,y), line, font=font)
        draw.rectangle((left-5, top-5, right+5, bottom+5), fill="yellow")
        draw.text(position, line, font=font, fill="black")
        y = y + line_height
    # Redefine x and y-axis to insert author's name
    # author = "- Hiren Thakore"
    # y += 5                       # Add some line space
    # x += 20                      # Indent it a bit to the right
    # draw.text((x,y), author, fill=color, font=font)
    rmg.show()
    # img.save(f'sample-out_{count}.jpg')

    # bbox = draw.textbbox(position,line,font=font) # this will draw text with Blackcolor and 16 size
    # left, top, right, bottom = draw.textbbox(position, line, font=font)
    # draw.rectangle((left-5, top-5, right+5, bottom+5), fill="yellow")
    # draw.text(position, line, font=font, fill="black")
    # draw.rectangle(bbox, fill="red")
    # draw.text(position, line, font=font, fill="black")
    # img.save(f'sample-out_{count}.jpg')
    pass

def processImages(selectedPicForThisTopic,line,count):
    img = Image.open(selectedPicForThisTopic)
    font = ImageFont.truetype(r'Antonio-Bold.ttf', 26)
    position = (20, 900)
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox(position,line,font=font) # this will draw text with Blackcolor and 16 size
    left, top, right, bottom = draw.textbbox(position, line, font=font)
    draw.rectangle((left-5, top-5, right+5, bottom+5), fill="yellow")
    draw.text(position, line, font=font, fill="black")
    img.show()
    img.save(f'sample-out_{count}.jpg')
    pass

def text_wrap(text, font, max_width):
        """Wrap text base on specified width. 
        This is to enable text of width more than the image width to be display
        nicely.
        @params:
            text: str
                text to wrap
            font: obj
                font of the text
            max_width: int
                width to split the text with
        @return
            lines: list[str]
                list of sub-strings
        """
        lines = []
        
        # If the text width is smaller than the image width, then no need to split
        # just add it to the line list and return
        if font.getsize(text)[0]  <= max_width:
            lines.append(text)
        else:
            #split the line by spaces to get words
            words = text.split(' ')
            i = 0
            # append every word to a line while its width is shorter than the image width
            while i < len(words):
                line = ''
                while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                    line = line + words[i]+ " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                lines.append(line)
        return lines

def parseText(filename):
    with open(filename) as f:
        lines = f.readlines()
        print(lines)
        index = 0
        for line in lines:
            index+=1
            print(line)
            #AI to determine category
            sequence_to_classify = line
            candidate_labels = ['finance', 'cryptocurrency', 'travel', 'cooking','health','education']
            result=classifier(sequence_to_classify, candidate_labels)['labels'][0]
            print(result)
            selectedPicForThisTopic=requestsToPexels(result)
            print(selectedPicForThisTopic)
            processImage(selectedPicForThisTopic,line,index)

if __name__ =='__main__':
    processImages("cryptocurrency.jpg","How to Avoid Crypto Scams",1)
