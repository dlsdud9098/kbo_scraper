from selenium import webself.driver
from selenium.webself.driver.common.by import By
import time
import pandas as pd
from selenium.webself.driver.support.ui import Select
from selenium.webself.driver.support.ui import Webself.driverWait
from selenium.webself.driver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium import webself.driver
from selenium.webself.driver.chrome.service import Service
from bs4 import BeautifulSoup
import requests

class KBO_Hitter_2002_2024:
    def __init__(self):
        # 크롬드라이버 실행
        self.driver = webself.driver.Chrome()
        self.driver.implicitly_wait(10) # seconds

        # wait until someid is clickable
        self.wait = Webself.driverWait(self.driver, 10)
        
        self.urls = [
            'https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx',
            'https://www.koreabaseball.com/Record/Player/HitterBasic/Basic2.aspx',
            'https://www.koreabaseball.com/Record/Player/HitterBasic/Detail1.aspx'
            ]
        
    # 페이지에서 테이블 추출
    def create_table(self.driver):
        # 페이지 소스 가져오기
        kbo_page = self.driver.page_source
        # html로 파싱
        soup = BeautifulSoup(kbo_page, 'html.parser')
        # 테이블 추출
        table = soup.select_one('#cphContents_cphContents_cphContents_udpContent > div.record_result > table')
        # 데이터프레임으로 변환
        table = pd.read_html(str(table), flavor='html5lib')[0]
        return table

    def team_list(self.driver):
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
    
    def page_click(self.driver):
        # 페이지 개수 확인
        page_count = len(self.driver.find_elements(By.CSS_SELECTOR, '#cphContents_cphContents_cphContents_udpContent > div.record_result > div > a'))
        # 페이지 크롤링
        df = create_table(self.driver)

        if page_count > 1:
            time.sleep(.2)
            # 다음 페이지 넘어가기
            self.driver.find_element(By.CSS_SELECTOR, '#cphContents_cphContents_cphContents_ucPager_btnNo2').click()
            time.sleep(.2)
            # 페이지 크롤
            df2 = create_table(self.driver)
            # 1, 2페이지 데이터 합치기
            df = pd.concat([df, df2])
            time.sleep(.2)
            # 1 페이지로 돌아가기
            self.driver.find_element(By.CSS_SELECTOR, '#cphContents_cphContents_cphContents_ucPager_btnNo1').click()
            
        return df
    
    def scrap_data(self):
        record_dfs = []
        seasons = [str(i) for i in range(2002, 2025)]

        for url in self.urls:
            self.driver.get(url)
            dfs = []
            for season in seasons:    
                # 시즌 콤보 박스 선택
                season_combo = self.driver.find_element(By.CSS_SELECTOR, '#cphContents_cDwdphContents_cphContents_ddlSeason_ddlSeason')
                # 시즌 콤보 박스 선택
                season_combo = Select(season_combo)
                # 값 선택
                season_combo.select_by_value(season)
                teams = team_list(self.driver)
                for team in teams:
                    time.sleep(.5)
                    combobox = self.driver.find_element(By.CSS_SELECTOR, '#cphContents_cphContents_cphContents_ddlTeam_ddlTeam')
                    team_combo = Select(combobox)
                    team_combo.select_by_visible_text(team)
                    time.sleep(.5)
                    df = page_click(self.driver)
                    df['year'] = season 
                    dfs.append(df)
                time.sleep(10)
                print(season,'년 완료!')
            record_dfs.append(dfs)
            
        # 인덱스 안맞음 방지
        df1 = pd.concat(record_dfs[0]).reset_index()
        df2 = pd.concat(record_dfs[1]).reset_index()
        df3 = pd.concat(record_dfs[2]).reset_index()

        df = pd.concat([df1, df2, df3], axis=1)
        # 필요없는 데이터 제거
        df.drop(['BB/K볼넷/삼진', 'GO땅볼', 'ISOP순수장타율', 'GO/AO땅볼/뜬공', 'HR홈런', 'OBP출루율', 'BB볼넷'], axis=1, inplace=True)
        df.loc[:, ~df.columns.duplicated()].to_csv('2002_2024.csv', encoding='cp949')
        
        df1 = pd.concat(record_dfs[0]).reset_index()
        df2 = pd.concat(record_dfs[1]).reset_index()
        df3 = pd.concat(record_dfs[2]).reset_index()
        
        df = pd.concat([df1, df2, df3], axis=1)
        df.drop(['BB/K볼넷/삼진', 'GO땅볼', 'ISOP순수장타율', 'GO/AO땅볼/뜬공', 'HR홈런', 'OBP출루율', 'BB볼넷'], axis=1, inplace=True)
        df = df.loc[:, ~df.columns.duplicated()]
        return df
        
    def save_data(self, df):
        df.to_csv('./csv_files/hitter/2002_2024.csv', encoding='cp949')
        
    def close_self.driver(self):
        self.driver.quit()