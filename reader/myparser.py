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
            return u"没有找到对应ID的比赛"

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
        outpage = u"足球比分信息"
        for tag in tags[1:-1]:
            if tag[-1] == '/':
                outpage += u"%s:" % en_to_zh[str(tag[:-1])] + '\n'
            elif tag[0] != '/':
                try:
                    content = re.findall('<' + tag + '>(.*?)</' + tag + '>', text)
                    content = content[0] if len(content) > 0 else 'None'

                    if tag == 'state':
                        content = num_to_state[content]
                    outpage += u"{0}:{1}".format(en_to_zh[str(tag)], content) + '\n'
                except KeyError:
                    pass
        return outpage

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
            return u"没有找到对应ID的比赛"
        league_info = company_odds['league'].split(',')
        outpage = "---------------------------------------------------" + '\n'
        outpage += u"1.联赛资料:"+'\n'
        outpage += u"联赛ID:"+league_info[0].strip() + '\n'
        outpage += u"类型（1联赛,2杯赛):" + league_info[1] + '\n'
        outpage += u"颜色值:" + league_info[2] + '\n'
        outpage += u"国语名:" + league_info[3] + '\n'
        outpage += u"繁体名:" + league_info[4] + '\n'
        outpage += u"英文名:" + league_info[5] + '\n'
        outpage += u"资料库路径:" + league_info[6] + '\n'
        outpage += u"是否是重要赛事(0次要赛事,1重要赛事):" + league_info[7] + '\n'
        outpage += "---------------------------------------------------" + '\n'

        match_info = company_odds['match'].split(',')
        outpage += u"2.赛程资料:" + '\n'
        outpage += u"比赛ID:" + match_info[0].strip() + '\n'
        outpage += u"联赛ID:" + match_info[1] + '\n'
        outpage += u"比赛时间:" + match_info[2] + '\n'
        outpage += u"开场时间:" + match_info[3] + '\n'
        outpage += u"主队ID:" + match_info[4] + '\n'
        outpage += u"主队国语名:" + match_info[5] + '\n'
        outpage += u"主队繁体名:" + match_info[6] + '\n'
        outpage += u"主队英文名:" + match_info[7] + '\n'
        outpage += u"主队排名:" + match_info[8] + '\n'
        outpage += u"客队ID:" + match_info[9] + '\n'
        outpage += u"客队国语名:" + match_info[10] + '\n'
        outpage += u"客队繁体名:" + match_info[11] + '\n'
        outpage += u"客队英文名:" + match_info[12] + '\n'
        outpage += u"客队排名:" + match_info[13] + '\n'
        outpage += u"比赛状态(0未开,1上半场,2中场,3下半场,-11待定,-12腰斩,-13中断,-14推迟,-1完场):" + match_info[14] + '\n'
        outpage += u"主队得分:" + match_info[15] + '\n'
        outpage += u"客队得分:" + match_info[16] + '\n'
        outpage += u"中立场:" + match_info[17] + '\n'
        outpage += u"级别(0彩票赛事,1重要赛事,2次要赛事):" + match_info[18] + '\n'
        outpage += u"主队红牌:" + match_info[19] + '\n'
        outpage += u"客队红牌:" + match_info[20] + '\n'
        outpage += u"主队黄牌:" + match_info[21] + '\n'
        outpage += u"客队黄牌:" + match_info[22] + '\n'
        outpage += "---------------------------------------------------" + '\n'
        outpage += u"3.亚赔(让球盘):" + '\n'
        if 'asia_handicap' not in company_odds.keys():
            outpage += u"没有相关数据"+ '\n'
        else:
            asia_info = company_odds['asia_handicap'].split(',')
            outpage += u"比赛ID:" + asia_info[0].strip() + '\n'
            outpage += u"公司ID:" + asia_info[1] + '\n'
            outpage += u"初盘盘口:" + asia_info[2] + '\n'
            outpage += u"主队初盘赔率:" + asia_info[3] + '\n'
            outpage += u"客队初盘赔率:" + asia_info[4] + '\n'
            outpage += u"即时盘口:" + asia_info[5] + '\n'
            outpage += u"主队即时赔率:" + asia_info[6] + '\n'
            outpage += u"客队即时赔率:" + asia_info[7] + '\n'
            outpage += u"是否封盘:" + asia_info[8] + '\n'
            outpage += u"是否走地:" + asia_info[9] + '\n'
        outpage += "---------------------------------------------------" + '\n'
        outpage += u"4.欧赔(标准盘):" + '\n'
        if 'eu_handicap' not in company_odds.keys():
            outpage += u"没有相关数据"+ '\n'
        else:
            eu_info = company_odds['eu_handicap'].split(',')
            outpage += u"比赛ID:" + eu_info[0].strip() + '\n'
            outpage += u"公司ID:" + eu_info[1] + '\n'
            outpage += u"初盘主胜赔率:" + eu_info[2] + '\n'
            outpage += u"初盘和局赔率:" + eu_info[3] + '\n'
            outpage += u"初盘客胜赔率:" + eu_info[4] + '\n'
            outpage += u"即时盘主胜赔率:" + eu_info[5] + '\n'
            outpage += u"即时盘和局赔率:" + eu_info[6] + '\n'
            outpage += u"即时盘客胜赔率:" + eu_info[7] + '\n'
        outpage += "---------------------------------------------------" + '\n'
        outpage += u"5.大小球:" + '\n'
        if 'bigsmall' not in company_odds.keys():
            outpage += u"没有相关数据"+ '\n'
        else:
            bigsmall_info = company_odds['bigsmall'].split(',')
            outpage += u"比赛ID:" + bigsmall_info[0].strip() + '\n'
            outpage += u"公司ID:" + bigsmall_info[1] + '\n'
            outpage += u"初盘盘口:" + bigsmall_info[2] + '\n'
            outpage += u"初盘大球赔率:" + bigsmall_info[3] + '\n'
            outpage += u"初盘小球赔率:" + bigsmall_info[4] + '\n'
            outpage += u"即时盘盘口:" + bigsmall_info[5] + '\n'
            outpage += u"即时盘大球赔率:" + bigsmall_info[6] + '\n'
            outpage += u"即时盘小球赔率:" + bigsmall_info[7] + '\n'
        outpage += "---------------------------------------------------" + '\n'
        outpage += u"6.半场让球:" + '\n'
        if 'half' not in company_odds.keys():
            outpage += u"没有相关数据"+ '\n'
        else:
            half_info = company_odds['half'].split(',')
            outpage += u"比赛ID:" + half_info[0].strip() + '\n'
            outpage += u"公司ID:" + half_info[1] + '\n'
            outpage += u"初盘盘口:" + half_info[2] + '\n'
            outpage += u"主队初盘赔率:" + half_info[3] + '\n'
            outpage += u"客队初盘赔率:" + half_info[4] + '\n'
            outpage += u"即时盘口:" + half_info[5] + '\n'
            outpage += u"主队即时赔率:" + half_info[6] + '\n'
            outpage += u"客队即时赔率:" + half_info[7] + '\n'
        outpage += "---------------------------------------------------" + '\n'
        outpage += u"7.半场大小球:" + '\n'
        if 'hbigsmall' not in company_odds.keys():
            outpage += u"没有相关数据"+ '\n'
        else:
            hbigsmall_info = company_odds['hbigsmall'].split(',')
            outpage += u"比赛ID:" + hbigsmall_info[0].strip() + '\n'
            outpage += u"公司ID:" + hbigsmall_info[1] + '\n'
            outpage += u"初盘盘口:" + hbigsmall_info[2] + '\n'
            outpage += u"初盘大球赔率:" + hbigsmall_info[3] + '\n'
            outpage += u"初盘小球赔率:" + hbigsmall_info[4] + '\n'
            outpage += u"即时盘盘口:" + hbigsmall_info[5] + '\n'
            outpage += u"即时盘大球赔率:" + hbigsmall_info[6] + '\n'
            outpage += u"即时盘小球赔率:" + hbigsmall_info[7] + '\n'
            outpage += "---------------------------------------------------" + '\n'
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

        outpage = '\n'+ u"                              **Handicap**" + '\n'+ '\n'
        outpage += "%5s" % u"记录ID"+"%8s" % u"比赛ID"+"%3s" % u"时间"+"%5s" % u"主队得分"+\
                   "%5s" % u"客队得分"+"%4s" % u"主队红牌"+"%4s" % u"客队红牌"+"%2s" % u"类型"+\
                   "%3s" % u"公司ID"+"%6s" % u"Home"+"%6s" % u"Line"+"%6s" % u"Away"+"%13s" % u"变盘时间" + '\n'
        for text1 in all_odds['1']:
            outpage += "%s" % text1[0][3:]+"%8s" % text1[1]+"%4s" % text1[2]+\
                       "%7s" % text1[3]+"%8s" % text1[4]+"%8s" % text1[5]+\
                       "%8s" % text1[6]+"%6s" % text1[7]+"%5s" % text1[8]+\
                       "%8s" % text1[9]+"%7s" % text1[10]+"%6s" % text1[11]+"%22s" % text1[12][:-4]
            outpage += '\n'
        outpage += "-------------------------------------------------------------------------------------------------"
        # ----------------------------------------------
        outpage += '\n' +'\n' + u"                              **Hilo**" + '\n'+ '\n'
        outpage += "%5s" % u"记录ID"+"%8s" % u"比赛ID"+"%3s" % u"时间"+"%5s" % u"主队得分"+\
            "%5s" % u"客队得分"+"%4s" % u"主队红牌"+"%4s" % u"客队红牌"+"%2s" % u"类型"+\
            "%3s" % u"公司ID"+"%6s" % u"High"+"%6s" % u"Line"+"%6s" % u"Low"+"%13s" % u"变盘时间" + '\n'
        for text1 in all_odds['2']:
            outpage += "%s" % text1[0][3:]+"%8s" % text1[1]+"%4s" % text1[2]+\
                "%7s" % text1[3]+"%8s" % text1[4]+"%8s" % text1[5]+\
                "%8s" % text1[6]+"%6s" % text1[7]+"%5s" % text1[8]+\
                "%8s" % text1[9]+"%7s" % text1[10]+"%6s" % text1[11]+"%22s" % text1[12][:-4]
            outpage += '\n'
        outpage += "-------------------------------------------------------------------------------------------------"
        # ----------------------------------------------
        outpage += '\n' +'\n' + u"                              **Standard**" + '\n' + '\n'
        outpage += "%5s" % u"记录ID"+"%8s" % u"比赛ID"+"%3s" % u"时间"+"%5s" % u"主队得分"+\
            "%5s" % u"客队得分"+"%4s" % u"主队红牌"+"%4s" % u"客队红牌"+"%2s" % u"类型"+\
            "%3s" % u"公司ID"+"%6s" % u"Home"+"%6s" % u"Draw"+"%6s" % u"Away"+"%13s" % u"变盘时间" + '\n'
        for text1 in all_odds['4']:
            outpage += "%s" % text1[0][3:]+"%8s" % text1[1]+"%4s" % text1[2]+\
                "%7s" % text1[3]+"%8s" % text1[4]+"%8s" % text1[5]+\
                "%8s" % text1[6]+"%6s" % text1[7]+"%5s" % text1[8]+\
                "%8s" % text1[9]+"%7s" % text1[10]+"%6s" % text1[11]+"%22s" % text1[12][:-4]
            outpage += '\n'

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
            return u"没有找到对应ID的比赛"
        info = text.split('^')
        info_list = [info[0][12:]]
        for i in range(1, 35):
            info_list.append(info[i])
        info_list.append(info[35][0])
        return u"篮球比分信息\n" \
               u"赛事ID:{0[0]}\n" \
               u"联赛/杯赛ID:{0[1]}\n" \
               u"类型(1联赛,2杯赛):{0[2]}\n" \
               u"联赛名:{0[3]}\n" \
               u"分几节进行(2半场,4小节):{0[4]}\n" \
               u"颜色值:{0[5]}\n" \
               u"开赛时间:{0[6]}\n" \
               u"比赛状态:{0[7]}\n" \
               u"小节剩余时间:{0[8]}\n" \
               u"主队ID:{0[9]}\n" \
               u"主队名:{0[10]}\n" \
               u"客队ID:{0[11]}\n" \
               u"客队名:{0[12]}\n" \
               u"主队排名:{0[13]}\n" \
               u"客队排名:{0[14]}\n" \
               u"主队得分:{0[15]}\n" \
               u"客队得分:{0[16]}\n" \
               u"主队一节得分(上半场):{0[17]}\n" \
               u"客队一节得分(上半场):{0[18]}\n" \
               u"主队二节得分:{0[19]}\n" \
               u"客队二节得分:{0[20]}\n" \
               u"主队三节得分(下半场):{0[21]}\n" \
               u"客队三节得分(下半场):{0[22]}\n" \
               u"主队四节得分:{0[23]}\n" \
               u"客队四节得分:{0[24]}\n" \
               u"加时数:{0[25]}\n" \
               u"主队1'ot得分:{0[26]}\n" \
               u"客队1'ot得分:{0[27]}\n" \
               u"主队2'ot得分:{0[28]}\n" \
               u"客队2'ot得分:{0[29]}\n" \
               u"主队3'ot得分:{0[30]}\n" \
               u"客队3'ot得分:{0[31]}\n" \
               u"是否有技术统计:{0[32]}\n" \
               u"电视直播:{0[33]}\n" \
               u"备注(直播内容):{0[34]}\n" \
               u"中立场(1中立场,0非中立):{0[35]}\n".format(info_list)

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
            return u"没有找到对应ID的比赛"

        outpage = u"1.联赛资料"+'\n'
        league_info = company_odds['league'].split(',')
        outpage += u"联赛ID:" + league_info[0].strip() + '\n'
        outpage += u"类型(1联赛,2杯赛):" + league_info[1] + '\n'
        outpage += u"颜色值:" + league_info[2] + '\n'
        outpage += u"联赛名:" + league_info[3] + '\n'
        outpage += u"比赛分几节(2半场,4小节):"+ league_info[5] + '\n'
        outpage += "-------------------------------------------------------" + '\n'
        outpage += u"2.赛程资料"+'\n'
        match_info = company_odds['match'].split(',')
        outpage += u"比赛ID:" + match_info[0].strip() + '\n'
        outpage += u"联赛ID:" + match_info[1] + '\n'
        outpage += u"比赛时间:" + match_info[2] + '\n'
        outpage += u"主队ID:" + match_info[3] + '\n'
        outpage += u"主队国语名:" + match_info[4] + '\n'
        outpage += u"主队繁体名:" + match_info[5] + '\n'
        outpage += u"主队英文名:" + match_info[6] + '\n'
        outpage += u"主队排名:" + match_info[7] + '\n'
        outpage += u"客队ID:" + match_info[8] + '\n'
        outpage += u"客队国语名:" + match_info[9] + '\n'
        outpage += u"客队繁体名:" + match_info[10] + '\n'
        outpage += u"客队英文名:" + match_info[11] + '\n'
        outpage += u"客队排名:" + match_info[12] + '\n'
        outpage += u"比赛状态(0未开,1上半场,2中场,3下半场,-11待定,-12腰斩,-13中断,-14推迟,-1完场):" + match_info[13] + '\n'
        outpage += u"主队得分:" + match_info[14] + '\n'
        outpage += u"客队得分:" + match_info[15] + '\n'
        outpage += u"电视直播:" + match_info[16] + '\n'
        outpage += u"中立场(1中立场,0非中立):" + match_info[17] + '\n'
        outpage += u"是否是竞彩赛事:" + match_info[18] + '\n'
        outpage += "-------------------------------------------------------"+'\n'
        outpage += u"3.亚赔(让球盘):" + '\n'
        if 'asia_handicap' not in company_odds.keys():
            outpage += u"没有相关数据" + '\n'
        else:
            asia_info = company_odds['asia_handicap'].split(',')
            outpage += u"比赛ID:" + asia_info[0].strip() + '\n'
            outpage += u"公司ID:" + asia_info[1] + '\n'
            outpage += u"初盘盘口:" + asia_info[2] + '\n'
            outpage += u"主队初盘赔率:" + asia_info[3] + '\n'
            outpage += u"客队初盘赔率:" + asia_info[4] + '\n'
            outpage += u"即时盘口:" + asia_info[5] + '\n'
            outpage += u"主队即时赔率:" + asia_info[6] + '\n'
            outpage += u"客队即时赔率:" + asia_info[7] + '\n'
        outpage += "-------------------------------------------------------" + '\n'
        outpage += u"4.欧赔(标准盘):" + '\n'
        if 'eu_handicap' not in company_odds.keys():
            outpage += u"没有相关数据" + '\n'
        else:
            eu_info = company_odds['eu_handicap'].split(',')
            outpage += u"比赛ID:" + eu_info[0].strip() + '\n'
            outpage += u"公司ID:" + eu_info[1] + '\n'
            outpage += u"初盘主胜赔率:" + eu_info[2] + '\n'
            outpage += u"初盘客胜赔率:" + eu_info[3] + '\n'
            outpage += u"即时盘主胜赔率:" + eu_info[4] + '\n'
            outpage += u"即时盘客胜赔率:" % eu_info[5] + '\n'
        outpage += "-------------------------------------------------------" + '\n'
        outpage += u"5.大小球:" + '\n'
        if 'bigsmall' not in company_odds.keys():
            outpage += u"没有相关数据" + '\n'
        else:
            bigsmall_info = company_odds['bigsmall'].split(',')
            outpage += u"比赛ID:" + bigsmall_info[0].strip() + '\n'
            outpage += u"公司ID:" + bigsmall_info[1] + '\n'
            outpage += u"初盘盘口:" + bigsmall_info[2] + '\n'
            outpage += u"初盘大分赔率:" + bigsmall_info[3] + '\n'
            outpage += u"初盘小分赔率:" + bigsmall_info[4] + '\n'
            outpage += u"即时盘盘口:" + bigsmall_info[5] + '\n'
            outpage += u"即时盘大分赔率:" + bigsmall_info[6] + '\n'
            outpage += u"即时盘小分赔率:" + bigsmall_info[7] + '\n'
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
