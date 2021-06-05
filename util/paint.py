from colr import color as paint

class Paint:

    def __init__(self):

        # self.colors = ["#E8D533","#E4E833","#F2EF35","#94DB3C","#75F235", "#48EB31", "#31EB59", "#38EB7B"]
        # self.colors = ["#33A8F2","#3382F2","#2956F2","#3822F2","#7523FC","#A42BE6","#EC23FC","#F222A8"]
        self.colors = ["#F6736C","#D45D86","#EB74DA","#BD5DD4","#B56CF6","#8B71F6","#7481F6","#74B1F6"]
        self.num_colors = len(self.colors)

        
    def set_color(self, string, index=1):
        
        color = self.colors[index%self.num_colors]

        return paint(string, color), color