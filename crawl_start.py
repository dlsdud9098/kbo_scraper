import os
from 1982_2001_hitter_crawl import KBO_Hitter_1982_2001
# from 2022_2024_hitter_crawl import KBO_Hitter_2002_2024

if __name__ == '__main__':
    folder_list = [
        './csv_files/hitter/',
        './csv_files/pitcher/'
    ]
    
    for folder in folder_list:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    scraper = KBO_Hitter_1982_2001()
    player_data = scraper.scrap_data()
    scraper.save_data(player_data)
    scraper.close_self.driver()
    
    # scraper = KBO_Hitter_2002_2024()
    # player_data = scraper.scrap_data()
    # scraper.save_data(player_data)
    # scraper.close_self.driver()
    
    