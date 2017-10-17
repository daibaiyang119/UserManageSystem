class PageHelper(object):
    def __init__(self, total_count, current_page, url, count=10):
        self.total_count = total_count
        self.current_page = current_page
        self.count = count
        self.url = url

    @property
    def page_start(self):
        return (self.current_page-1)*self.count

    @property
    def page_end(self):
        return self.current_page*self.count

    def pager_str(self):
        # 总页数
        num1, num2 = divmod(self.total_count, self.count)  # num1是商, num2是余
        # 如果有余数，则商加一
        if num2 != 0:
            num1 += 1

        # 生成页码HTML
        html_str = ""

        # 上一页
        if self.current_page != 1:
            html_str += "<a href='%s?page=%s'>上一页</a>" % (self.url, self.current_page - 1)

        # 页码规则
        if num1 <= 10:
            range_start = 1
            range_end = num1+1
        else:
            if self.current_page < 6:
                range_start = 1
                range_end = 11
            else:
                range_start = self.current_page - 5
                range_end = self.current_page + 5
                if range_end > num1:
                    range_start = num1 - 9
                    range_end = num1 + 1

        for i in range(range_start, range_end):
            html_str += "<a href='%s?page=%s'>%s</a>" % (self.url, i, i)

        # 下一页
        if self.current_page != num1:
            html_str += "<a href='%s?page=%s'>下一页</a>" % (self.url, self.current_page + 1)

        return html_str
