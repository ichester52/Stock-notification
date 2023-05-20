import requests
import vonage
import datetime
stock_dic = {
    "TSLA": "Tesla Inc",
    "MSFT": "Microsoft Corp",
    "GOOG": "Alphabet Inc",
}
for stock in stock_dic:
    STOCK = stock
    COMPANY_NAME = stock_dic[stock]
    get_info = False

    ## STEP 1: Use https://www.alphavantage.co
    # When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
    url = "https://www.alphavantage.co/query"
    my_key = "YT8O3NV35T96JZ9M"

    parameters = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": STOCK,
        "apikey": my_key
    }

    response = requests.get(url, params=parameters)
    response.raise_for_status()
    stock_data = response.json()["Time Series (Daily)"]


    def format_days():
        count = 0
        both_days = []
        for date in stock_data:
            if count >= 3:
                break
            else:
                both_days.append(date)
                count += 1

        return both_days

    three_days = format_days()

    today = three_days[0]
    yesterday = three_days[1]

    yesterday_close = float(stock_data[today]["4. close"])
    before_close = float(stock_data[yesterday]["4. close"])




    percent_change = ((yesterday_close/before_close) * 100) - 100
    percent_change = round(percent_change, 2)

    if percent_change >= 5.0 or percent_change < -5.0:
        print("Get News")
        get_info = True


    if percent_change > 0:
        arrow = "🔺"
    else:
        arrow = "🔻"


    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    if get_info == True:
        news_parameters = {
            "q": COMPANY_NAME,
            "apiKey": "ed14d47a4b814e07ba2286452eb4cd6b"

        }

        news_url = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
        news_url.raise_for_status()
        articles_list = news_url.json()["articles"]
        article_1 = articles_list[0]
        article_2 = articles_list[1]
        article_3 = articles_list[2]
        print("this is activated")
    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.
        client = vonage.Client(key="a153641e", secret="6VxcjHERwefwXyGo")
        sms = vonage.Sms(client)

        responseData = sms.send_message(
            {
                "from": "16292238282",
                "to": "18326519354",
                "text": f"{COMPANY_NAME} {percent_change}%\nHeadline: {article_1['title']}\nBrief: {article_1['description']}",
            }
        )

        responseData2 = sms.send_message(
            {
                "from": "16292238282",
                "to": "18326519354",
                "text": f"{COMPANY_NAME} {percent_change}%\nHeadline: {article_2['title']}\nBrief: {article_2['description']}",
            }
        )
        responseData3 = sms.send_message(
            {
                "from": "16292238282",
                "to": "18326519354",
                "text": f"{COMPANY_NAME} {percent_change}%\nHeadline: {article_3['title']}\nBrief: {article_3['description']}",
            }
        )

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

