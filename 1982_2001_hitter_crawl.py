from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup

class KBO_Hitter_1982_2001:
    def __init__(self):
        # 크롬드라이버 실행
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10) # seconds

        # wait until someid is clickable
        self.wait = WebDriverWait(self.driver, 10)

    # 페이지에서 테이블 추출
    def create_table(self):
        # 페이지 소스 가져오기
        kbo_page = self.driver.page_source
        # html로 파싱
        soup = BeautifulSoup(kbo_page, 'html.parser')
        # 테이블 추출
        table = soup.select_one('#cphContents_cphContents_cphContents_udpContent > div.record_result > table')
        # 데이터프레임으로 변환
        table = pd.read_html(str(table), flavor='html5lib')[0]
        return table

    def team_list(self):
        time.sleep(.5)
        # 콥보 박스 선택
        # combobox = self.driver.find_element(By.XPATH, '//*[@id="cphContents_cphContents_cphContents_ddlTeam_ddlTeam"]')
        combobox = self.driver.find_element(By.CSS_SELECTOR, '#cphContents_cphContents_cphContents_ddlTeam_ddlTeam')
        time.sleep(1)
        # 콤보박스 안의 옵션들 선택
        options = combobox.find_elements(By.TAG_NAME, 'option')[1:]
        
        # 팀 이름 출력
        teams = [option.text for option in options]
        # print(teams)
        
        return teams

    def page_click(self):
        df1 = self.create_table(self.driver)
        # 페이지 개수 세기 2
        page_count = len(self.driver.find_elements(By.CSS_SELECTOR, '#cphContents_cphContents_cphContents_udpContent > div.record_result > div > a'))
        if page_count > 1:
            # 2 페이지 클릭
            self.driver.find_element(By.CSS_SELECTOR, '#cphContents_cphContents_cphContents_ucPager_btnNo2').click()
            df2 = self.create_table(self.driver)
            time.sleep(.2)
            # 1 페이지로 되돌아가기
            self.driver.find_element(By.CSS_SELECTOR, '#cphContents_cphContents_cphContents_ucPager_btnNo1').click()
            
            df = pd.concat([df1, df2])
        else:
            return df1
        return df
    
    def scrap_data(self):
        # self.driver.get('https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx?sort=HRA_RT')
        self.driver.get('https://www.koreabaseball.com/Record/Player/PitcherBasic/BasicOld.aspx')
        # 데이터프레임 리스트
        dfs = []
        # 시즌 리스트
        seasons = [str(i) for i in range(1982,2002)]
        for season in seasons:
            time.sleep(.5)
            # 시즌 콤보 박스 선택
            season_combo = self.driver.find_element(By.CSS_SELECTOR, '#cphContents_cphContents_cphContents_ddlSeason_ddlSeason')
            # 시즌 콤보 박스 선택
            season_combo = Select(season_combo)
            # 값 선택
            season_combo.select_by_value(season)
            # 팀 목록 불러오기
            teams = self.team_list(self.driver)
            
            for team in teams:
                time.sleep(.5)
                combobox = self.driver.find_element(By.CSS_SELECTOR, '#cphContents_cphContents_cphContents_ddlTeam_ddlTeam')
                team_combo = Select(combobox)
                team_combo.select_by_visible_text(team)
                time.sleep(.5)
                df = self.page_click(self.driver)
                df['year'] = season
                dfs.append(df)
                
        self.close_driver()
                
        player_data = pd.concat(dfs)
        return player_data
        
    def save_data(self, player_data):
        player_data.to_csv('./csv_files/pitcher/1982_2001.csv', encoding='cp949')
    
    def close_driver(self):
        self.driver.quit()
    
# if __name__ == '__main__':
#     scraper = KBO_Hitter_1982_2001()
#     player_data = scraper.scrap_data()
#     scraper.save_data(player_data)
#     scraper.close_driver()