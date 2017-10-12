# -*- coding:utf8 -*-
from xml.dom.minidom import parseString
import re


class Parser:

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def show_data(self):
        pass

    def __parse__(self):
        pass

    def __find_target__(self, ids):
        pass


class ScoreParser(Parser):

    def __init__(self, source, target):
        Parser.__init__(self, source, target)

    def show_data(self):
        ids = self.__parse__()
        text = self.__find_target__(ids)

        if text is None:
            return u"<content><type>没有找到对应ID的比赛</type></content>"

        tags = re.findall(r'<(.*?)>', text)
        en_to_zh = {
            "ID": u"比赛ID",
            "color": u"颜色值",
            "leagueID": u"联赛ID",
            "kind": u"类型(1联赛,2杯赛)",
            "level": u"是否是重要比赛(1重要赛事,0一般赛事)",
            "league": u"赛事类型(简体名,繁体名,英文名)",
            "subLeague": u"子联赛名",
            "subLeagueID": u"子联赛ID",
            "time": u"比赛时间",
            "time2": u"开场时间",
            "home": u"主队(简体名,繁体名,英文名,主队ID)",
            "away": u"客队(简体名,繁体名,英文名,客队ID)",
            "state": u"比赛状态",
            "homeScore": u"主队比分",
            "awayScore": u"客队比分",
            "bc1": u"主队上半场比分",
            "bc2": u"客队上半场比分",
            "red1": u"主队红牌",
            "red2": u"客队红牌",
            "yellow1": u"主队黄牌",
            "yellow2": u"客队黄牌",
            "order1": u"主队排名",
            "order2": u"客队排名",
            "explain": u"比赛说明",
            "zl": u"是否中立场",
            "tv": u"电视直播",
            "lineup": u"是否有阵容(1为有)",
            "explain2": u"比赛说明2(加时,点球等)",
            "corner1": u"主队角球",
            "corner2": u"客队角球"
                    }

        num_to_state = {
            '0': u'未开',
            '1': u'上半场',
            '2': u'中场',
            '3': u'下半场',
            '4': u'加时',
            '-11': u'待定',
            '-12': u'腰斩',
            '-13': u'中断',
            '-14': u'推迟',
            '-1': u'完场',
            '-10': u'取消'
        }
        outpage = u"<content><type>足球比分信息</type>"
        for tag in tags[1:-1]:
            if tag[-1] == '/':
                outpage += u"<item><key>%s</key><value></value></item>" % en_to_zh[str(tag[:-1])]
            elif tag[0] != '/':
                try:
                    content = re.findall('<' + tag + '>(.*?)</' + tag + '>', text)
                    content = content[0] if len(content) > 0 else 'None'

                    if tag == 'state':
                        content = num_to_state[content]
                    outpage += u"<item><key>{0}</key><value>{1}</value></item>".format(en_to_zh[str(tag)], content)
                except KeyError:
                    pass
        return outpage + u"</content>"

    def __parse__(self):
        return parseString(self.source).getElementsByTagName('ID')

    def __find_target__(self, ids):
        for id in ids:
            if self.target == id.childNodes[0].nodeValue:
                return id.parentNode.toxml()


class EarlyOddsParser(Parser):

    def __init__(self, source, target, company):
        Parser.__init__(self, source, target)
        self.company = company

    def show_data(self):

        company_odds = self.__find_target__(self.__parse__())
        if company_odds == {}:
            return u"<content><type>没有找到对应ID的比赛</type></content>"
        
        outpage = u"<content><type>联赛资料</type>"
        league_info = company_odds['league'].split(',')
        outpage += u"<item><key>联赛ID</key><value>%s</value></item>" % league_info[0].strip()
        outpage += u"<item><key>类型(1联赛,2杯赛)</key><value>%s</value></item>" % league_info[1]
        outpage += u"<item><key>颜色值</key><value>%s</value></item>" % league_info[2]
        outpage += u"<item><key>国语名</key><value>%s</value></item>" % league_info[3]
        outpage += u"<item><key>繁体名</key><value>%s</value></item>" % league_info[4]
        outpage += u"<item><key>英文名</key><value>%s</value></item>" % league_info[5]
        outpage += u"<item><key>资料库路径</key><value>%s</value></item>" % league_info[6]
        outpage += u"<item><key>是否是重要赛事(0次要赛事,1重要赛事)</key><value>%s</value></item></content>" % league_info[7]
        # -------------------------------------------------------
        
        outpage += u"<content><type>赛程资料</type>"
        match_info = match_info = company_odds['match'].split(',')
        outpage += u"<item><key>比赛ID</key><value>%s</value></item>" % match_info[0].strip()
        outpage += u"<item><key>联赛ID</key><value>%s</value></item>" % match_info[1]
        outpage += u"<item><key>比赛时间</key><value>%s</value></item>" % match_info[2]
        outpage += u"<item><key>开场时间</key><value>%s</value></item>" % match_info[3]
        outpage += u"<item><key>主队ID</key><value>%s</value></item>" % match_info[4]
        outpage += u"<item><key>主队国语名</key><value>%s</value></item>" % match_info[5]
        outpage += u"<item><key>主队繁体名</key><value>%s</value></item>" % match_info[6]
        outpage += u"<item><key>主队英文名</key><value>%s</value></item>" % match_info[7]
        outpage += u"<item><key>主队排名</key><value>%s</value></item>" % match_info[8]
        outpage += u"<item><key>客队ID</key><value>%s</value></item>" % match_info[9]
        outpage += u"<item><key>客队国语名</key><value>%s</value></item>" % match_info[10]
        outpage += u"<item><key>客队繁体名</key><value>%s</value></item>" % match_info[11]
        outpage += u"<item><key>客队英文名</key><value>%s</value></item>" % match_info[12]
        outpage += u"<item><key>客队排名</key><value>%s</value></item>" % match_info[13]
        outpage += u"<item><key>比赛状态(0未开,1上半场,2中场,3下半场,-11待定,-12腰斩,-13中断,-14推迟,-1完场)</key><value>%s</value></item>" % match_info[14]
        outpage += u"<item><key>主队得分</key><value>%s</value></item>" % match_info[15]
        outpage += u"<item><key>客队得分</key><value>%s</value></item>" % match_info[16]
        outpage += u"<item><key>中立场</key><value>%s</value></item>" % match_info[17]
        outpage += u"<item><key>级别(0彩票赛事,1重要赛事,2次要赛事)</key><value>%s</value></item>" % match_info[18]
        outpage += u"<item><key>主队红牌</key><value>%s</value></item>" % match_info[19]
        outpage += u"<item><key>客队红牌</key><value>%s</value></item>" % match_info[20]
        outpage += u"<item><key>主队黄牌</key><value>%s</value></item>" % match_info[21]
        outpage += u"<item><key>客队黄牌</key><value>%s</value></item></content>" % match_info[22]
        # -------------------------------------------------------
        outpage += u"<content><type>亚赔(让球盘)</type>"
        if 'asia_handicap' not in company_odds.keys():
            outpage += u"<item><key>NotFound</key><value>没有相关数据</value></item></content>"
        else:
            asia_info = company_odds['asia_handicap'].split(',')
            outpage += u"<item><key>比赛ID</key><value>%s</value></item>" % asia_info[0].strip()
            outpage += u"<item><key>公司ID</key><value>%s</value></item>" % asia_info[1]
            outpage += u"<item><key>初盘盘口</key><value>%s</value></item>" % asia_info[2]
            outpage += u"<item><key>主队初盘赔率</key><value>%s</value></item>" % asia_info[3]
            outpage += u"<item><key>客队初盘赔率</key><value>%s</value></item>" % asia_info[4]
            outpage += u"<item><key>即时盘口</key><value>%s</value></item>" % asia_info[5]
            outpage += u"<item><key>主队即时赔率</key><value>%s</value></item>" % asia_info[6]
            outpage += u"<item><key>客队即时赔率</key><value>%s</value></item>" % asia_info[7]
            outpage += u"<item><key>是否封盘</key><value>%s</value></item>" % asia_info[8]
            outpage += u"<item><key>是否走地</key><value>%s</value></item></content>" % asia_info[9]
        # -------------------------------------------------------
        outpage += u"<content><type>欧赔(标准盘)</type>"
        if 'eu_handicap' not in company_odds.keys():
            outpage += u"<item><key>NotFound</key><value>没有相关数据</value></item></content>"
        else:
            eu_info = company_odds['eu_handicap'].split(',')
            outpage += u"<item><key>比赛ID</key><value>%s</value></item>" % eu_info[0].strip()
            outpage += u"<item><key>公司ID</key><value>%s</value></item>" % eu_info[1]
            outpage += u"<item><key>初盘主胜赔率</key><value>%s</value></item>" % eu_info[2]
            outpage += u"<item><key>初盘和局赔率</key><value>%s</value></item>" % eu_info[3]
            outpage += u"<item><key>初盘客胜赔率</key><value>%s</value></item>" % eu_info[4]
            outpage += u"<item><key>即时盘主胜赔率</key><value>%s</value></item>" % eu_info[5]
            outpage += u"<item><key>即时盘和局赔率</key><value>%s</value></item>" % eu_info[6]
            outpage += u"<item><key>即时盘客胜赔率</key><value>%s</value></item></content>" % eu_info[7]
        # -------------------------------------------------------
        outpage += u"<content><type>大小球</type>"
        if 'bigsmall' not in company_odds.keys():
            outpage += u"<item><key>NotFound</key><value>没有相关数据</value></item></content>"
        else:
            bigsmall_info = company_odds['bigsmall'].split(',')
            outpage += u"<item><key>比赛ID</key><value>%s</value></item>" % bigsmall_info[0].strip()
            outpage += u"<item><key>公司ID</key><value>%s</value></item>" % bigsmall_info[1]
            outpage += u"<item><key>初盘盘口</key><value>%s</value></item>" % bigsmall_info[2]
            outpage += u"<item><key>初盘大球赔率</key><value>%s</value></item>" % bigsmall_info[3]
            outpage += u"<item><key>初盘小球赔率</key><value>%s</value></item>" % bigsmall_info[4]
            outpage += u"<item><key>即时盘盘口</key><value>%s</value></item>" % bigsmall_info[5]
            outpage += u"<item><key>即时盘大球赔率</key><value>%s</value></item>" % bigsmall_info[6]
            outpage += u"<item><key>即时盘小球赔率</key><value>%s</value></item></content>" % bigsmall_info[7]
        # -------------------------------------------------------
        outpage += u"<content><type>半场让球</type>"
        if 'half' not in company_odds.keys():
            outpage += u"<item><key>NotFound</key><value>没有相关数据</value></item></content>"
        else:
            half_info = company_odds['half'].split(',')
            outpage += u"<item><key>比赛ID</key><value>%s</value></item>" % half_info[0].strip()
            outpage += u"<item><key>公司ID</key><value>%s</value></item>" % half_info[1]
            outpage += u"<item><key>初盘盘口</key><value>%s</value></item>" % half_info[2]
            outpage += u"<item><key>主队初盘赔率</key><value>%s</value></item>" % half_info[3]
            outpage += u"<item><key>客队初盘赔率</key><value>%s</value></item>" % half_info[4]
            outpage += u"<item><key>即时盘口</key><value>%s</value></item>" % half_info[5]
            outpage += u"<item><key>主队即时赔率</key><value>%s</value></item>" % half_info[6]
            outpage += u"<item><key>客队即时赔率</key><value>%s</value></item></content>" % half_info[7]
        # -------------------------------------------------------
        outpage += u"<content><type>半场大小球</type>"
        if 'hbigsmall' not in company_odds.keys():
            outpage += u"<item><key>NotFound</key><value>没有相关数据</value></item></content>"
        else:
            hbigsmall_info = company_odds['hbigsmall'].split(',')
            outpage += u"<item><key>比赛ID</key><value>%s</value></item>" % hbigsmall_info[0].strip()
            outpage += u"<item><key>公司ID</key><value>%s</value></item>" % hbigsmall_info[1]
            outpage += u"<item><key>初盘盘口</key><value>%s</value></item>" % hbigsmall_info[2]
            outpage += u"<item><key>初盘大球赔率</key><value>%s</value></item>" % hbigsmall_info[3]
            outpage += u"<item><key>初盘小球赔率</key><value>%s</value></item>" % hbigsmall_info[4]
            outpage += u"<item><key>即时盘盘口</key><value>%s</value></item>" % hbigsmall_info[5]
            outpage += u"<item><key>即时盘大球赔率</key><value>%s</value></item>" % hbigsmall_info[6]
            outpage += u"<item><key>即时盘小球赔率</key><value>%s</value></item></content>" % hbigsmall_info[7]
        # -------------------------------------------------------
        return outpage

    def __find_target__(self, ids):
        result = dict()

        leagues = ids[0]
        matches = ids[1]
        asia_handicaps = ids[2]
        eu_handicaps = ids[3]
        bigsmalls = ids[4]
        halfs = ids[6]
        hbigsmalls = ids[7]

        for match in matches:
            if self.target in match:
                result['match'] = match
                for league in leagues:
                    if match.split(',')[1] in league:
                        result['league'] = league

        def add_to_result(clauses, name):
            for clause in clauses:
                company = clause.split(',')[1]
                if self.target in clause and self.company in company:
                    result[name] = clause

        add_to_result(asia_handicaps, 'asia_handicap')
        add_to_result(eu_handicaps, 'eu_handicap')
        add_to_result(bigsmalls, 'bigsmall')
        add_to_result(halfs, 'half')
        add_to_result(hbigsmalls, 'hbigsmall')

        return result

    def __parse__(self):
        def split_clause(clauses):
            return clauses.split(';')

        parts = self.source.split('$')
        return map(split_clause, parts)


class InplayParser(Parser):

    def __init__(self, source, target, company):
        Parser.__init__(self, source, target)
        self.company = company
        self.odds_type = ('1', '2', '4')

    def show_data(self):
        all_odds = self.__find_target__(self.__parse__())
        # ----------------------------------------------
        # print "%5s" % u"记录ID", "%8s" % u"比赛ID", "%3s" % u"时间", "%5s" % u"主队得分",\
        #     "%5s" % u"客队得分", "%4s" % u"主队红牌", "%4s" % u"客队红牌", "%2s" % u"类型",\
        #     "%3s" % u"公司ID", "%6s" % u"Home", "%6s" % u"Line", "%6s" % u"Away", "%10s" % u"变盘时间"
        outpage = u"<content><type>Handicap</type>"
        for text1 in all_odds['1']:
            # print "%s" % text1[0][3:], "%8s" % text1[1], "%4s" % text1[2],\
            #     "%7s" % text1[3], "%8s" % text1[4], "%8s" % text1[5],\
            #     "%8s" % text1[6], "%6s" % text1[7], "%5s" % text1[8],\
            #     "%8s" % text1[9], "%7s" % text1[10], "%6s" % text1[11], "%7s" % text1[12][:-4]
            list_text = [text1[0][3:]]
            for i in range(1, 12):
                list_text.append(text1[i])
            list_text.append(text1[12][:-4])
            outpage += u"<item><recordId>{0[0]}</recordId>" \
                       u"<matchId>{0[1]}</matchId>" \
                       u"<time>{0[2]}</time>" \
                       u"<homeScore>{0[3]}</homeScore>" \
                       u"<awayScore>{0[4]}</awayScore>" \
                       u"<homeR>{0[5]}</homeR>" \
                       u"<awayR>{0[6]}</awayR>" \
                       u"<Type>{0[7]}</Type>" \
                       u"<companyId>{0[8]}</companyId>" \
                       u"<Home>{0[9]}</Home>" \
                       u"<Line>{0[10]}</Line>" \
                       u"<Away>{0[11]}</Away>" \
                       u"<changeTime>{0[12]}</changeTime></item>".format(list_text)
        outpage += u"</content>"
        # ----------------------------------------------
        outpage += u"<content><type>Hilo</type>"
        # print "%5s" % u"记录ID", "%8s" % u"比赛ID", "%3s" % u"时间", "%5s" % u"主队得分", \
        #     "%5s" % u"客队得分", "%4s" % u"主队红牌", "%4s" % u"客队红牌", "%2s" % u"类型", \
        #     "%3s" % u"公司ID", "%6s" % u"High", "%6s" % u"Line", "%6s" % u"Low", "%10s" % u"变盘时间"
        for text1 in all_odds['2']:
            # print "%s" % text1[0][3:], "%8s" % text1[1], "%4s" % text1[2], \
            #     "%7s" % text1[3], "%8s" % text1[4], "%8s" % text1[5], \
            #     "%8s" % text1[6], "%6s" % text1[7], "%5s" % text1[8], \
            #     "%8s" % text1[9], "%7s" % text1[10], "%6s" % text1[11], "%7s" % text1[12][:-4]
            list_text = [text1[0][3:]]
            for i in range(1, 12):
                list_text.append(text1[i])
            list_text.append(text1[12][:-4])
            outpage += u"<item><recordId>{0[0]}</recordId>" \
                       u"<matchId>{0[1]}</matchId>" \
                       u"<time>{0[2]}</time>" \
                       u"<homeScore>{0[3]}</homeScore>" \
                       u"<awayScore>{0[4]}</awayScore>" \
                       u"<homeR>{0[5]}</homeR>" \
                       u"<awayR>{0[6]}</awayR>" \
                       u"<type>{0[7]}</type>" \
                       u"<companyId>{0[8]}</companyId>" \
                       u"<High>{0[9]}</High>" \
                       u"<Line>{0[10]}</Line>" \
                       u"<Low>{0[11]}</Low>" \
                       u"<changeTime>{0[12]}</changeTime></item>".format(list_text)
        outpage += u"</content>"
        # ----------------------------------------------
        outpage += u"<content><type>Standard</type>"
        # print "%5s" % u"记录ID", "%8s" % u"比赛ID", "%3s" % u"时间", "%5s" % u"主队得分", \
        #     "%5s" % u"客队得分", "%4s" % u"主队红牌", "%4s" % u"客队红牌", "%2s" % u"类型", \
        #     "%3s" % u"公司ID", "%6s" % u"Home", "%6s" % u"Draw", "%6s" % u"Away", "%10s" % u"变盘时间"-
        for text1 in all_odds['4']:
            # print "%s" % text1[0][3:], "%8s" % text1[1], "%4s" % text1[2], \
            #     "%7s" % text1[3], "%8s" % text1[4], "%8s" % text1[5], \
            #     "%8s" % text1[6], "%6s" % text1[7], "%5s" % text1[8], \
            #     "%8s" % text1[9], "%7s" % text1[10], "%6s" % text1[11], "%7s" % text1[12][:-4]
            list_text = [text1[0][3:]]
            for i in range(1, 12):
                list_text.append(text1[i])
            list_text.append(text1[12][:-4])
            outpage += u"<item><recordId>{0[0]}</recordId>" \
                       u"<matchId>{0[1]}</matchId>" \
                       u"<time>{0[2]}</time>" \
                       u"<homeScore>{0[3]}</homeScore>" \
                       u"<awayScore>{0[4]}</awayScore>" \
                       u"<homeR>{0[5]}</homeR>" \
                       u"<awayR>{0[6]}</awayR>" \
                       u"<type>{0[7]}</type>" \
                       u"<companyId>{0[8]}</companyId>" \
                       u"<Home>{0[9]}</Home>" \
                       u"<Draw>{0[10]}</Draw>" \
                       u"<Away>{0[11]}</Away>" \
                       u"<changeTime>{0[12]}</changeTime></item>".format(list_text)
        outpage += u"</content>"
        # ----------------------------------------------
        return outpage

    def __parse__(self):
        return parseString(self.source).getElementsByTagName('h')

    def __find_target__(self, ids):
        standard = list()
        handicap = list()
        hilo = list()

        all_odds = {
            '1': handicap,
            '2': hilo,
            '4': standard
        }

        for id in ids:
            content = id.toxml().split(',')
            company = content[8]
            odds_type = content[7]
            if company in self.company and odds_type in self.odds_type and self.target in content[1]:
                all_odds[odds_type].append(content)
        return all_odds

    @staticmethod
    def __compare_time(first_time, second_time):
        pass


class BasketballScoreParser(Parser):

    def __init__(self, source, target):
        Parser.__init__(self, source, target)

    def show_data(self):
        text = self.__find_target__(self.__parse__())

        if text is None:
            return u"<content><type>没有找到对应ID的比赛</type></content>"
        info = text.split('^')
        info_list = [info[0][12:]]
        for i in range(1, 35):
            info_list.append(info[i])
        info_list.append(info[35][0])
        return u"<content><type>篮球比分信息</type><item><key>赛事ID</key><value>{0[0]}</value></item>" \
               u"<item><key>联赛/杯赛ID </key><value>{0[1]}</value></item>" \
               u"<item><key>类型(1联赛,2杯赛)</key><value>{0[2]}</value></item>" \
               u"<item><key>联赛名</key><value>{0[3]}</value></item>" \
               u"<item><key>分几节进行(2半场,4小节)</key><value>{0[4]}</value></item>" \
               u"<item><key>颜色值</key><value>{0[5]}</value></item>" \
               u"<item><key>开赛时间</key><value>{0[6]}</value></item>" \
               u"<item><key>比赛状态</key><value>{0[7]}</value></item>" \
               u"<item><key>小节剩余时间</key><value>{0[8]}</value></item>" \
               u"<item><key>主队ID</key><value>{0[9]}</value></item>" \
               u"<item><key>主队名</key><value>{0[10]}</value></item>" \
               u"<item><key>客队ID</key><value>{0[11]}</value></item>" \
               u"<item><key>客队名</key><value>{0[12]}</value></item>" \
               u"<item><key>主队排名</key><value>{0[13]}</value></item>" \
               u"<item><key>客队排名</key><value>{0[14]}</value></item>" \
               u"<item><key>主队得分</key><value>{0[15]}</value></item>" \
               u"<item><key>客队得分</key><value>{0[16]}</value></item>" \
               u"<item><key>主队一节得分(上半场)</key><value>{0[17]}</value></item>" \
               u"<item><key>客队一节得分(上半场)</key><value>{0[18]}</value></item>" \
               u"<item><key>主队二节得分</key><value>{0[19]}</value></item>" \
               u"<item><key>客队二节得分</key><value>{0[20]}</value></item>" \
               u"<item><key>主队三节得分(下半场)</key><value>{0[21]}</value></item>" \
               u"<item><key>客队三节得分(下半场)</key><value>{0[22]}</value></item>" \
               u"<item><key>主队四节得分</key><value>{0[23]}</value></item>" \
               u"<item><key>客队四节得分</key><value>{0[24]}</value></item>" \
               u"<item><key>加时数</key><value>{0[25]}</value></item>" \
               u"<item><key>主队1'ot得分</key><value>{0[26]}</value></item>" \
               u"<item><key>客队1'ot得分</key><value>{0[27]}</value></item>" \
               u"<item><key>主队2'ot得分</key><value>{0[28]}</value></item>" \
               u"<item><key>客队2'ot得分</key><value>{0[29]}</value></item>" \
               u"<item><key>主队3'ot得分</key><value>{0[30]}</value></item>" \
               u"<item><key>客队3'ot得分</key><value>{0[31]}</value></item>" \
               u"<item><key>是否有技术统计</key><value>{0[32]}</value></item>" \
               u"<item><key>电视直播</key><value>{0[33]}</value></item>" \
               u"<item><key>备注(直播内容)</key><value>{0[34]}</value></item>" \
               u"<item><key>中立场(1中立场,0非中立)</key><value>{0[35]}</value></item></content>".format(info_list)

    def __parse__(self):
        return parseString(self.source).getElementsByTagName('h')

    def __find_target__(self, ids):
        for id in ids:
            if self.target in id.toxml():
                return id.toxml()


class BasketballEarlyOddsParser(Parser):

    def __init__(self, source, target, company):
        Parser.__init__(self, source, target)
        self.company = company

    def show_data(self):

        company_odds = self.__find_target__(self.__parse__())
        if company_odds == {}:
            return u"<content><type>没有找到对应ID的比赛</type></content>"

        outpage = u"<content><type>联赛资料</type>"
        league_info = company_odds['league'].split(',')
        outpage += u"<item><key>联赛ID</key><value>%s</value></item>" % league_info[0].strip()
        outpage += u"<item><key>类型(1联赛,2杯赛)</key><value>%s</value></item>" % league_info[1]
        outpage += u"<item><key>颜色值</key><value>%s</value></item>" % league_info[2]
        outpage += u"<item><key>联赛名</key><value>%s</value></item>" % league_info[3]
        outpage += u"<item><key>比赛分几节(2半场,4小节)</key><value>%s</value></item></content>" % league_info[5]
        # -------------------------------------------------------
        outpage += u"<content><type>赛程资料</type>"
        match_info = match_info = company_odds['match'].split(',')
        outpage += u"<item><key>比赛ID</key><value>%s</value></item>" % match_info[0].strip()
        outpage += u"<item><key>联赛ID</key><value>%s</value></item>" % match_info[1]
        outpage += u"<item><key>比赛时间</key><value>%s</value></item>" % match_info[2]
        outpage += u"<item><key>主队ID</key><value>%s</value></item>" % match_info[3]
        outpage += u"<item><key>主队国语名</key><value>%s</value></item>" % match_info[4]
        outpage += u"<item><key>主队繁体名</key><value>%s</value></item>" % match_info[5]
        outpage += u"<item><key>主队英文名</key><value>%s</value></item>" % match_info[6]
        outpage += u"<item><key>主队排名</key><value>%s</value></item>" % match_info[7]
        outpage += u"<item><key>客队ID</key><value>%s</value></item>" % match_info[8]
        outpage += u"<item><key>客队国语名</key><value>%s</value></item>" % match_info[9]
        outpage += u"<item><key>客队繁体名</key><value>%s</value></item>" % match_info[10]
        outpage += u"<item><key>客队英文名</key><value>%s</value></item>" % match_info[11]
        outpage += u"<item><key>客队排名</key><value>%s</value></item>" % match_info[12]
        outpage += u"<item><key>比赛状态(0未开,1上半场,2中场,3下半场,-11待定,-12腰斩,-13中断,-14推迟,-1完场)</key><value>%s</value></item>" % match_info[13]
        outpage += u"<item><key>主队得分</key><value>%s</value></item>" % match_info[14]
        outpage += u"<item><key>客队得分</key><value>%s</value></item>" % match_info[15]
        outpage += u"<item><key>电视直播</key><value>%s</value></item>" % match_info[16]
        outpage += u"<item><key>中立场(1中立场,0非中立)</key><value>%s</value></item>" % match_info[17]
        outpage += u"<item><key>是否是竞彩赛事</key><value>%s</value></item></content>" % match_info[18]
        # -------------------------------------------------------
        outpage += u"<content><type>亚赔(让球盘)</type>"
        if 'asia_handicap' not in company_odds.keys():
            outpage += u"<item><key>NotFound</key><value>没有相关数据</value></item></content>"
        else:
            asia_info = company_odds['asia_handicap'].split(',')
            outpage += u"<item><key>比赛ID</key><value>%s</value></item>" % asia_info[0].strip()
            outpage += u"<item><key>公司ID</key><value>%s</value></item>" % asia_info[1]
            outpage += u"<item><key>初盘盘口</key><value>%s</value></item>" % asia_info[2]
            outpage += u"<item><key>主队初盘赔率</key><value>%s</value></item>" % asia_info[3]
            outpage += u"<item><key>客队初盘赔率</key><value>%s</value></item>" % asia_info[4]
            outpage += u"<item><key>即时盘口</key><value>%s</value></item>" % asia_info[5]
            outpage += u"<item><key>主队即时赔率</key><value>%s</value></item>" % asia_info[6]
            outpage += u"<item><key>客队即时赔率</key><value>%s</value></item></content>" % asia_info[7]
        # -------------------------------------------------------
        outpage += u"<content><type>欧赔(标准盘)</type>"
        if 'eu_handicap' not in company_odds.keys():
            outpage += u"<item><key>NotFound</key><value>没有相关数据</value></item></content>"
        else:
            eu_info = company_odds['eu_handicap'].split(',')
            outpage += u"<item><key>比赛ID</key><value>%s</value></item>" % eu_info[0].strip()
            outpage += u"<item><key>公司ID</key><value>%s</value></item>" % eu_info[1]
            outpage += u"<item><key>初盘主胜赔率</key><value>%s</value></item>" % eu_info[2]
            outpage += u"<item><key>初盘客胜赔率</key><value>%s</value></item>" % eu_info[3]
            outpage += u"<item><key>即时盘主胜赔率</key><value>%s</value></item>" % eu_info[4]
            outpage += u"<item><key>即时盘客胜赔率</key><value>%s</value></item></content>" % eu_info[5]
        # -------------------------------------------------------
        outpage += u"<content><type>大小球</type>"
        if 'bigsmall' not in company_odds.keys():
            outpage += u"<item><key>NotFound</key><value>没有相关数据</value></item></content>"
        else:
            bigsmall_info = company_odds['bigsmall'].split(',')
            outpage += u"<item><key>比赛ID</key><value>%s</value></item>" % bigsmall_info[0].strip()
            outpage += u"<item><key>公司ID</key><value>%s</value></item>" % bigsmall_info[1]
            outpage += u"<item><key>初盘盘口</key><value>%s</value></item>" % bigsmall_info[2]
            outpage += u"<item><key>初盘大分赔率</key><value>%s</value></item>" % bigsmall_info[3]
            outpage += u"<item><key>初盘小分赔率</key><value>%s</value></item>" % bigsmall_info[4]
            outpage += u"<item><key>即时盘盘口</key><value>%s</value></item>" % bigsmall_info[5]
            outpage += u"<item><key>即时盘大分赔率</key><value>%s</value></item>" % bigsmall_info[6]
            outpage += u"<item><key>即时盘小分赔率</key><value>%s</value></item></content>" % bigsmall_info[7]
        return outpage

    def __find_target__(self, ids):
        result = dict()

        leagues = ids[0]
        matches = ids[1]
        asia_handicaps = ids[2]
        eu_handicaps = ids[3]
        bigsmalls = ids[4]
        for match in matches:
            if self.target in match:
                result['match'] = match
                for league in leagues:
                    if match.split(',')[1] in league:
                        result['league'] = league

        def add_to_result(clauses, name):
            if name is 'bigsmall':
                company_id_dict = {'1': '4', '2': '5', '3': '6', '8': '11', '9': '12', '31': '34'}
                self.company = company_id_dict[self.company]
            for clause in clauses:
                company = clause.split(',')[1]
                if self.target in clause and self.company in company:
                    result[name] = clause

        add_to_result(asia_handicaps, 'asia_handicap')
        add_to_result(eu_handicaps, 'eu_handicap')
        add_to_result(bigsmalls, 'bigsmall')
        return result

    def __parse__(self):
        def split_clause(clauses):
            return clauses.split(';')

        parts = self.source.split('$')
        return map(split_clause, parts)
