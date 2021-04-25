import pygame

from GUI import Shapes


class LeaderboardsList:
    def __init__(self, center, font, font_color, background_color, max_amount_of_records, source_file):
        self.center = center
        self.font = font
        self.font_color = font_color
        self.background_color = background_color
        self.max_amount_of_records = max_amount_of_records
        self.source_file = source_file
        self.rows = self.__read_file()
        self.single_row_size = self.__calculate_size()
        self.size = (self.single_row_size[0] + 20, self.single_row_size[1] * len(self.rows) + 20)
        self.top_left = (self.center[0] - self.size[0] // 2, self.center[1] - self.size[1] // 2)

    def __read_file(self):
        ret_list = []
        with open(self.source_file) as f:
            lines = f.read().splitlines()
        for i in range(min(self.max_amount_of_records, len(lines))):
            columns = lines[i].split(" : ")
            ret_list.append(f"{columns[0]} VS {columns[1]}"
                            f" WINS: {columns[2]} VS {columns[3]}"
                            f" DRAWS: {columns[4]}")
        return ret_list

    def __calculate_size(self):
        max_height = 0
        max_width = 0
        font = pygame.font.SysFont(*self.font)
        for row in self.rows:
            text_rect = font.render(row, True, self.font_color)
            if text_rect.get_size()[1] > max_width:
                max_width, max_height = text_rect.get_size()[0], text_rect.get_size()[1]
        return max_width, max_height

    def render(self, screen):
        Shapes.draw_rect(screen, self.center, self.size, self.background_color)
        top_left = self.top_left
        for i in range(len(self.rows)):
            row_center = (self.center[0], top_left[1] + self.single_row_size[1] // 2)
            Shapes.draw_text(screen, row_center, self.rows[i], self.font, self.font_color)
            top_left = (top_left[0], top_left[1] + (self.single_row_size[1] + 4))
