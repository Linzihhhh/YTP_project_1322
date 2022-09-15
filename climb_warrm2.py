from requests_html import HTMLSession
from bs4 import BeautifulSoup
session = HTMLSession()

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding" : "gzip, deflate, br",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cookie": "p_ab_id=1; p_ab_id_2=5; p_ab_d_id=699468570; privacy_policy_notification=0; a_type=0; b_type=1; c_type=21; _fbp=fb.1.1640079459214.1009884820; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=45914720=1^9=p_ab_id=1=1^10=p_ab_id_2=5=1^11=lang=zh_tw=1; _gcl_au=1.1.1643778035.1658044493; __utmz=235335808.1658671479.24.21.utmcsr=l.facebook.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _fbc=fb.1.1658671479043.IwAR2wdshdraqgAMvO3G82eAoD4rqG8LBsN4u2yFf1mAonqXHN-E08gIEuAvw; __utma=235335808.1867309452.1623720025.1658671479.1663225639.25; __utmc=235335808; __cf_bm=OyXITbsNEmjWM8A5KGJViMMA5tcwyJH1FTJCVysj5z4-1663225638-0-AVrMbqtEbZ6VABtvNPfoptNd0cun7gDdbaWQEf+cS2gryQldjqHO2wY1++8QwxDw1TujzPcDgZta2Y1mdkku2/Lb/bcPnBsxF/kN64h1MB020TnA6rVtzfN87d9UpH6wzv2qrUjaLpq7NSOeQR4VRStFgG70sm0G1UAd/10vaymexK0TSz9z+vtoHkSgcOrd4A==; _gid=GA1.2.1910327627.1663225641; device_token=22645c5d6ed993261368c8ee40e6acd6; tag_view_ranking=RcahSSzeRf~KrMg4c4zFf~UnI8eZzpBM~MSNRmMUDgC~X_1kwTzaXt~Lt-oEicbBr~fIMPtFR8GH~pzzjRSV6ZO~tgP8r-gOe_~mzJgaDwBF5~Ui7_qOnwP5~KOnmT1ndWG~zdXpSlHEIZ~jH0uD88V6F~j1qQtl730f~azESOjmQSV~0xsDLqCEW6~b_G3UDfpN0~GX5cZxE2GY~BVxjcWpHyF~kGYw4gQ11Z~7FO0s9zK4r~gpglyfLkWs~qnGN-oHRQo~QaiOjmwQnI~JooW_Hne2Q~lH5YZxnbfC~faHcYIP1U0~Bcdk6oWmUE~Ie2c51_4Sp~yZf1XmIy-U~w8ffkPoJ_S~v08uexvQq2~y3NlVImyly~HY55MqmzzQ~1HSjrqSB3U~XtgzxkCgH-~yqJYvivdJc~0T_w4L0CHO~PzEXgc_S56~WVrsHleeCL~FPCeANM2Bm~30YRghWWsb~-mS39rlV30~SxmI-ep6z3~sU2V5AmUzK~pnCQRVigpy~Ngz9KxUrJt~KsJYQeAdFM~wX1vEmvkKu~HLWLeyYOUF~vqXfdUbtfS~CrFcrMFJzz~zyKU3Q5L4C~88R-whWgJ8~q6LwUKoJuB~RTJMXD26Ak~aKhT3n4RHZ~nriWjM9urd~dve3nXgd1M~jk9IzfjZ6n~ZTBAtZUDtQ~KvAGITxIxH~pYlUxeIoeg~FGFzwIh-Ko~RybylJRnhJ~OuA32je5y3~C1gSQiPu1R~Ti1gvrVQFO~5WlN6qpDZj~1HD6lhXO_A~9PI9msRK8Q~ETjPkL0e6r~ZKYx1SDf_f~_n9ogDO5lU~b19054K89t~Bd2L9ZBE8q~0oMmMHTqle~33kJYz6eWM~lQGtQGMEhM~yCFAxlOQOj~qXzcci65nj~JN2fNJ_Ue2~ea63_dbx7n~2QTW_H5tVX~-jHKDumw7E~XgZwHIIL4V~j3leh4reoN~NBK37t_oSE~9OgM5t9f0L~mir4aNx9oM~skx_-I2o4Y~r70NVOGJ5H~4Dp_oH0cTU~P5glpXg6VU~R-5T1rCK5Y~hekaYsYtCT~4h0o0dAXfL~kovglUgBN2~K8esoIs2eW; PHPSESSID=45914720_kgYIe0oNt3L97XC2i6whW9TZj24JYBnO; privacy_policy_agreement=0; _ga=GA1.1.1867309452.1623720025; cto_bundle=o3xlLl94VHd2VUtHVm1BalBJczZzZDJTeEpUb3hvSzRxJTJGWW1WMUVmYSUyQkFGWWhDYWQ4VjhrUXQ2cTZYM1ZCMHBhQTh5dzlKMjNpRU1ja284SnZiZjBmY2RRNDNBUlRQY0tjQ3drMmhPcmFrMk9Mc01BMFZkdmdNUThEdkxmOVFTQ04lMkZqMzZOd1pZaUsxVERydWFFNFlKeE94S3clM0QlM0Q; _ga_75BBYNYN9J=GS1.1.1663225638.7.1.1663226965.0.0.0; __utmt=1; __utmb=235335808.9.10.1663225639",
    "referer": "https://www.pixiv.net/",
    "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-site",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}
res = session.get('https://www.pixiv.net/',headers=headers)
soup = BeautifulSoup(res.text,"html.parser")

print(soup.prettify())