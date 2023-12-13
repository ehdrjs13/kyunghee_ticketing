from processData import GetPersonalData
from makeQR import GetQR
from PIL import Image, ImageDraw, ImageFont
import pandas

#티켓 이미지를 제작.

class makeTicket():
    def __init__(self) -> None:
        self.personalData = GetPersonalData('visitorList.xlsx')
        self.data = self.personalData.GetCode()
        self.qr = GetQR()
        for i in range(self.qr.data.shape[1]):
            num_four = str(i+1).zfill(4)
            self.qr.makeQR(num_four)

        return
    def makeImage(self, num) -> None:
        self.bg = Image.open('comps/template.jpg')
        self.draw =  ImageDraw.Draw(self.bg)
        self.font = ImageFont.truetype('comps/AppleSDGothicNeoEB.ttf', size = 35)

        self.NamePos = (540,315)
        self.SchoolPos = (540,445)
        self.NumPos = (540,580)
        self.GatePos = (540,210)
        self.CodePos = (570,680)

        name = self.data[num][0]
        school = self.data[num][1]
        code = self.data[num][3]

        self.draw.text(self.NamePos, name, fill = (0,0,0), font = self.font)
        self.draw.text(self.SchoolPos, school, fill = (0,0,0), font = self.font)
        self.draw.text(self.GatePos, code[0], fill = (0,0,0), font = self.font)
        self.draw.text(self.NumPos, code[1:5], fill = (0,0,0), font = self.font)
        


        self.qr = Image.open(f'qrcodes/{code[1:5]}.jpg')
        self.qr = self.qr.resize((230, 230)) 
        
        self.bg.paste(self.qr, (450, 670), self.qr)

        self.draw.text(self.CodePos, code, fill = (0,0,0),font= ImageFont.truetype('comps/AppleSDGothicNeoB.ttf', size = 15))
        



        self.bg.save(f'savedImg/{num}.png')
        


