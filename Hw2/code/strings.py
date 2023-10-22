class String:
    def __init__(self, l, r, length, k):
        self.l = l
        self.r = r
        self.length = length
        self.k = k
    
    def force(self):
        # 负号表示对于弹簧右侧物体，当弹簧拉伸时，弹簧对物体施加的力是向左的
        return -self.k * (self.r - self.l - self.length)
    
    def update(self, l=None, r=None):
        if l:
            self.l = l
        if r:
            self.r = r
