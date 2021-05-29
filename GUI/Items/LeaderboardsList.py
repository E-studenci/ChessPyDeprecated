import pygame

from GUI import Shapes


class LeaderboardsList:
    """
    Draws a simple leaderboard from a file

    Attributes
        center: (x,y)
            the center of the leaderboard in pixels
        font: (font_name, font_size, bold, italic)
            the font to be used
        font_color: (r,g,b,a)
            the font color to be used
        background_color: (r,g,b,a)
            the color of the background
        max_amount_of_records
            the amount of records from the file to render
        source_file
            the path to the source file
        text_empty
            the message to display if there are no records

    Methods
        render(screen)
            renders the leaderboard on the screen
    """

    def __init__(self, center, font, font_color, background_color, max_amount_of_records, source_file,
                 text_empty="PLAY MORE GAMES"):
        self.center = center
        self.font = font
        self.font_color = font_color
        self.background_color = background_color
        self.max_amount_of_records = max_amount_of_records
        self.source_file = source_file
        self.rows = self.__read_file()
        self.single_row_size = self.__calculate_size(self.rows)
        self.size = (self.single_row_size[0] + 20, self.single_row_size[1] * len(self.rows) + 20)
        self.top_left = (self.center[0] - self.size[0] // 2, self.center[1] - self.size[1] // 2)
        self.text_empty = text_empty

    def __read_file(self):
        ret_list = []
        with open(self.source_file) as f:
            lines = f.read().splitlines()
        for line in lines:
            columns = line.split(" : ")
            ret_list.append(columns)
        return ret_list

    def __calculate_size(self, row_list):
        max_height = 0
        max_width = 0
        font = pygame.font.SysFont(*self.font)
        for i in range(min(len(row_list), self.max_amount_of_records)):
            text_rect = font.render(f"{row_list[i][0]} VS {row_list[i][1]}"
                                    f" WINS: {row_list[i][2]} LOSSES {row_list[i][3]}"
                                    f" DRAWS: {row_list[i][4]}", True, self.font_color)
            if text_rect.get_size()[0] > max_width:
                max_width, max_height = text_rect.get_size()[0], text_rect.get_size()[1]
        return max_width, max_height

    def __update_size(self, row_list):
        self.single_row_size = self.__calculate_size(row_list)
        self.size = (self.single_row_size[0] + 20,
                     self.single_row_size[1] * min(len(row_list), self.max_amount_of_records) + 20)
        self.top_left = (self.center[0] - self.size[0] // 2, self.center[1] - self.size[1] // 2)

    def render(self, screen, filter_by_):
        """
        Draws the leaderboard on the screen

        :param screen: the screen the leaderboard should be drawn on
        """
        filter_by = filter_by_.lower()
        if filter_by.count(" vs ") > 1:
            return

        filter_by = filter_by.split(" vs ")
        filtered_list = []
        if len(filter_by) == 1:
            filtered_list = filter(lambda row: filter_by[0] in row[0].lower() or filter_by[0] in row[1].lower(),
                                   self.rows)
        elif len(filter_by) == 2:
            filtered_list = filter(lambda row:
                                   (filter_by[0] in row[0].lower() and filter_by[1] in row[1].lower())
                                   or (filter_by[1] in row[0].lower() and filter_by[0] in row[1].lower()),
                                   self.rows)
        filtered_list = list(filtered_list)
        self.__update_size(filtered_list)
        if len(filtered_list) > 0:
            Shapes.draw_rect(screen, self.center, self.size, self.background_color)
            top_left = self.top_left
            for i in range(min(len(filtered_list), self.max_amount_of_records)):
                row_center = (self.center[0], top_left[1] + self.single_row_size[1] // 2)
                Shapes.draw_text(screen, row_center, f"{filtered_list[i][0]} VS {filtered_list[i][1]}"
                                                     f" WINS: {filtered_list[i][2]} LOSSES: {filtered_list[i][3]}"
                                                     f" DRAWS: {filtered_list[i][4]}", self.font, self.font_color)
                top_left = (top_left[0], top_left[1] + (self.single_row_size[1] + 4))
        else:
            font = pygame.font.SysFont(*self.font)
            text_rect = font.render(self.text_empty, True, self.font_color)
            Shapes.draw_rect(screen, self.center, text_rect.get_size(), self.background_color)
            Shapes.draw_text(screen, self.center, self.text_empty, self.font, self.font_color)
