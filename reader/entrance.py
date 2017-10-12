# -*- coding:utf8 -*-
import downloader
import myparser


def start(*args):
    europe_id = args[2]
    p = None
    check_type_ball = args[0]
    check_type = args[1]
    if check_type_ball == 'soccer':
        if check_type == 'score':
            d = downloader.ScoreDownloader()
            p = myparser.ScoreParser(d.download(), europe_id)
        elif check_type == 'inplay':
            d = downloader.InplayOddsDownloader()
            company_id = args[3]
            p = myparser.InplayParser(d.download(), europe_id, company_id)
        elif check_type == 'early':
            company_id = args[3]
            d = downloader.EarlyOddsDownloader()
            p = myparser.EarlyOddsParser(d.download(), europe_id, company_id)

    elif check_type_ball == 'basketball':
        if check_type == 'score':
            d = downloader.BasketballScoreDownloader()
            p = myparser.BasketballScoreParser(d.download(), europe_id)
        elif check_type == 'odds':
            company_id = args[3]
            d = downloader.BasketballEarlyOddsDownloader()
            p = myparser.BasketballEarlyOddsParser(d.download(), europe_id, company_id)
    return p.show_data()
