from django.shortcuts import render, redirect
import pymysql
import math, random
import pytz
import smtplib
import datetime
import requests
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import HttpResponseRedirect
from django import template
from yahoo_fin import stock_info as si
register = template.Library()
emailid = ""
himailsent = 0
timailsent = 0
fimailsent = 0
cimailsent = 0
wimailsent = 0
Hoimailsent = 0
emailreq = 1
emailpressed = 0

otpiscorrect = 'no'
bothcorrect = 'yes'
OTP = ""
emailotpnsend = ""
emailandpass = 'yes'
emptyfield = 'no'
signupall = 'no'
userexist ='no'
insuranceType = ""
insuranceType1 = ""
insuranceType2 = ""
insuranceType3 = ""
insuranceType4 = ""
insuranceType5 = ""
date1 = ""
date2 = ""
date3 = ""
date4 = ""
date5 = ""
date6 = ""
succespro = ""
succespass = ""
notfill = 'no'
filled = 'yes'
suggest = 'yes'
pwdruls = 'yes'
accsucc = 'no'
fpwdruls = 'yes'
cspwdruls = 'yes'
ssuccespro = ""
def Home(response):
    return render(response, "main/index.html", {})

def sign_up_in(response):
    global emailid
    global pwdruls
    global accsucc
    specsymb = ['@','#','$','%','&']
    if response.method == 'POST':
        if response.POST.get('sign_up'):
            name = response.POST.get('uname')
            email = response.POST.get('email')
            password = response.POST.get('password')
            if name == "" or email == "" or password == "":
                globals().update({'userexist': 'no'})
                globals().update({'signupall':'yes'})
            else:
                globals().update({'signupall': 'no'})
                try:
                    con = pymysql.connect(host="localhost", user="Kshitij", password="abcd@1234", database="sign_up")
                    cur = con.cursor()
                    cur.execute("select * from signup where email=%s", email)
                    row = cur.fetchone()
                    if row is not None:
                        globals().update({'signupall': 'no'})
                        globals().update({'userexist':'yes'})
                    else:
                        if len(password) >= 8:
                            if any(char.isdigit() for char in password):
                                if any(char.isupper() for char in password):
                                    if any(char in specsymb for char in password):
                                        globals().update({'userexist': 'no'})
                                        cur.execute("insert into signup(name,email,password)values(%s,%s,%s)", (name, email, password))
                                        con.commit()
                                        con.close()
                                        globals().update({'pwdruls': 'yes'})
                                        globals().update({'accsucc': 'yes'})
                                        print("Account created")
                                    else:
                                        globals().update({'accsucc': 'no'})
                                        globals().update({'pwdruls':'no'})
                                else:
                                    globals().update({'accsucc': 'no'})
                                    globals().update({'pwdruls':'no'})
                            else:
                                globals().update({'accsucc': 'no'})
                                globals().update({'pwdruls': 'no'})
                        else:
                            globals().update({'accsucc': 'no'})
                            globals().update({'pwdruls': 'no'})
                except Exception as es:
                    print("Some Exception Occurred")
                    print(str(es))

        if response.POST.get('sign_in'):
            email = response.POST.get('SEmail')
            emailid = str(email)
            password = response.POST.get('SPassword')
            if email == "" or password == "":
                globals().update({'emailandpass': 'yes'})
                globals().update({'emptyfield':'yes'})
            else:
                globals().update({'emptyfield':'no'})
                try:
                    con = pymysql.connect(host="localhost", user="Kshitij", password="abcd@1234", database="sign_up")
                    cur = con.cursor()
                    cur.execute("select * from signup where email=%s and password=%s", (email, password))
                    row = cur.fetchone()
                    if row is None:
                        globals().update({'emptyfield': 'no'})
                        globals().update({'emailandpass':'no'})
                    else:
                        globals().update({'emailandpass':'yes'})
                        globals().update({'accsucc': 'no'})
                        return redirect('/port')

                except Exception as es:
                    print("Exception occured !")
                    print(str(es))

    return render(response, "main/sign_up_in.html", {'emptyfield':emptyfield,'emailandpass':emailandpass,'signupall':signupall,
                                                     'userexist':userexist,'pwdruls':pwdruls,'accsucc':accsucc})
def forgetpass(response):
    digits = "0123456789"
    specsymb = ['@','#','$','%','&']
    global OTP
    if response.method == 'POST':
        if 'emailsend'in response.POST:
            globals().update({'emailotpnsend': response.POST.get('email')})
            for i in range(4):
                OTP += digits[math.floor(random.random() * 10)]
            to = emailotpnsend
            mailfrom = 'financiiofinanceassistant@gmail.com'
            your_pass = "10131517"
            body = " Your 4 digit OTP for Financiio to reset the password is :\n {} ".format(OTP)
            subject = 'OTP For Password Reset'
            message = MIMEMultipart()
            message['From'] = mailfrom
            message['To'] = to
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            text = message.as_string()

            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login(mailfrom, your_pass)
            mail.sendmail(mailfrom, to, text)
            mail.close()
            print('Mail had been sent succesfully')
            globals().update({'emailreq': 0})
            globals().update({'emailpressed': 1})
    if 'otpsubmit'in response.POST:
        if 'otpinp' in response.POST:
            enteredotp = response.POST.get('otpinp')
            print(enteredotp)
            enteredotp = str(enteredotp)
            OTP = str(OTP)
            print(OTP)
            if enteredotp == OTP:
                globals().update({'emailpressed': 0})
                globals().update({'otpiscorrect': 'yes'})
            else:
                globals().update({'emailpressed': 1})
                globals().update({'otpiscorrect':'No'})

    if 'updatepass' in response.POST:
        newpass = response.POST.get('newpassword')
        confpass = response.POST.get('confirmpassword')
        print(newpass)
        print(confpass)
        if newpass == confpass:
            if len(newpass) >= 8:
                if any(char.isdigit() for char in newpass):
                    if any(char.isupper() for char in newpass):
                        if any(char in specsymb for char in newpass):
                             con = pymysql.connect(host="localhost", user="Kshitij", password="abcd@1234", database="sign_up")
                             cur = con.cursor()
                             cur.execute("update signup set password=%s where email=%s", (newpass, emailotpnsend))
                             con.commit()
                             con.close()
                             globals().update({'otpiscorrect':'no'})
                             globals().update({'bothcorrect':'yes'})
                             globals().update({'emailreq':1})
                             globals().update({'OTP':''})
                             globals().update({'bothcorrect': 'yes'})
                             globals().update({'fpwdruls': 'yes'})
                             return redirect("/sign")
                        else:
                           globals().update({'fpwdruls':'no'})
                    else:
                        globals().update({'fpwdruls':'no'})
                else:
                    globals().update({'fpwdruls': 'no'})
            else:
                globals().update({'fpwdruls': 'no'})
        else:
            globals().update({'bothcorrect': 'no'})


    return render(response, "main/forgotPassword.html", {"emailreq":emailreq,"emailpressed":emailpressed,"otpiscorrect":otpiscorrect,
                                                         "bothcorrect":bothcorrect,'fpwdruls':fpwdruls})

def suggestions(response):
    ssincome = 0
    con = pymysql.connect(host="localhost", user="Kshitij", password="abcd@1234", database="sign_up")
    cur = con.cursor()
    cur.execute("select income from signup where email=%s", (emailid))
    sincome = cur.fetchone()
    cur.execute("select age from signup where email=%s", (emailid))
    sage = cur.fetchone()
    cur.execute("select states from signup where email=%s", (emailid))
    sstates = cur.fetchone()
    cur.execute("select kids from signup where email=%s", (emailid))
    skids = cur.fetchone()
    sincome = str(sincome[0])
    sage =  str(sage[0])
    sstates =  str(sstates[0])
    skids =  str(skids[0])
    print(len(sincome))
    if len(sincome) < 1 or len(sage) < 1 or len(sstates) < 3 or len(skids) < 2:
        globals().update({'suggest': 'no'})
        globals().update({'notfill': 'no'})
    else:
        globals().update({'notfill': 'yes'})
        globals().update({'filled': 'yes'})
        globals().update({'suggest': 'yes'})
    con.close()
    if response.POST.get('getsuggestform'):
        globals().update({'notfill': 'yes'})
        globals().update({'filled': 'no'})
    if response.method == 'POST':
        if response.POST.get('suggestionsubmit'):
            income = response.POST.get('suggestincome')
            age = response.POST.get('suggestage')
            states = response.POST.get('suggeststates')
            kids = response.POST.get('suggestkids')
            try:
                con = pymysql.connect(host="localhost", user="Kshitij", password="abcd@1234", database="sign_up")
                cur = con.cursor()
                cur.execute("select email from signup where email=%s",(emailid))
                row = cur.fetchone()

                if row != None:
                    row = list(row)
                    if row[0] != emailid:
                        print("User Not Found")
                    else:
                        print(emailid)
                        cur.execute("update signup set income=%s, age=%s,states=%s,kids=%s where email=%s",
                                    (income, age, states, kids, emailid))
                        con.commit()
                        con.close()
                        print("Data Added Successfully")
                        globals().update({'filled': 'yes'})
                        globals().update({'suggest': 'yes'})
                else:
                    print("User Not Found")
            except Exception as es:
                print("Exception occured!")
                print(str(es))
        if suggest == 'yes' :
            return redirect('/suggestions')
    con = pymysql.connect(host="localhost", user="Kshitij", password="abcd@1234", database="sign_up")
    cur = con.cursor()
    cur.execute("select age from signup where email=%s", (emailid))
    sage = cur.fetchone()
    cur.execute("select states from signup where email=%s", (emailid))
    sstates = cur.fetchone()
    cur.execute("select kids from signup where email=%s", (emailid))
    skids = cur.fetchone()
    sage = int(sage[0])
    sstates = str(sstates[0])
    skids = str(skids[0])
    con.close()
    print(skids)
    print(sstates)

    cryptoapiKey = '91bf6424-512e-47a7-83b6-e1435264dec7'
    headers = {
        'X-CMC_PRO_API_KEY': cryptoapiKey,
        'Accepts': 'application/json'
    }

    params = {
        'start':'1',
        'limit':'100',
        'convert':'INR'
    }

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    json = requests.get(url, params=params, headers=headers).json()

    coins = json['data']

    cryptoData = []
    cryptoPrice = []

    cryptoDict = {}

    for x in coins:
        cryptoData.append(x['symbol'])
        cryptoPrice.append(float("{:.2f}".format(x['quote']['INR']['price'])))

    for cd in cryptoData:
        for cp in cryptoPrice:
            cryptoDict[cd] = cp
            cryptoPrice.remove(cp)
            break
        
    btc = cryptoDict['BTC']
    eth = cryptoDict['ETH']
    zec = cryptoDict['ZEC']
    trx = cryptoDict['TRX']
    ltc = cryptoDict['LTC']
    dash = cryptoDict['DASH']
    ada = cryptoDict['ADA']
    doge = cryptoDict['DOGE']

    #stockList1 = ['HINDUNILVR.NS', 'ULTRACEMCO.NS', 'TATASTEEL.NS', 'ADANIPORTS.NS', 'BPCL.NS', 'SBI', 'HCLTECH.NS', 'IRCTC.NS']
    stockList1 = ['DABUR.NS', 'HINDALCO.NS', 'ICICIBANK.NS', 'TATASTEEL.NS', 'ADANIENT.NS', 'TVSMOTOR.NS', 'LT.NS', 'INFY.NS']
    stockList2 = ['DIVISLAB.NS', 'BAJAJ-AUTO.NS', 'LTI.NS', 'MINDTREE.NS', 'ULTRACEMCO.NS', 'KAJARIACER.NS', 'DMART.NS', 'TITAN.NS']
    stockList3 = ['MRF.NS', 'NESTLEIND.NS', 'PAGEIND.NS', 'SHREECEM.NS', '3MINDIA.NS', 'BOSCHLTD.NS', 'BAJAJFINSV.NS', 'ATUL.NS']

    stkList1 = []
    stkList2 = []
    stkList3 = []

    for i in stockList1:
        stkList1.append(float("{:.2f}".format(si.get_live_price(i))))

    for i in stockList2:
        stkList2.append(float("{:.2f}".format(si.get_live_price(i))))

    for i in stockList3:
        stkList3.append(float("{:.2f}".format(si.get_live_price(i))))

    try:
        con = pymysql.connect(host="localhost", user="Kshitij", password="abcd@1234", database="sign_up")
        cur = con.cursor()
        cur.execute("select income from signup where email=%s", emailid)
        con.commit()
        ssincome = cur.fetchone()
        ssincome = ssincome[0]
        ssincome = int(ssincome)
        print(ssincome)
        con.close()
        globals().update({'succespro': 'updated'})
    except Exception as es:
        print("Some Exception Occurred")
        print(str(es))

    return render(response, "main/suggestions.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5,
                                                    "date1": date1,"date2": date2,"date3": date3,"date4": date4,
                                                    "date5": date5,"date6": date6,"notfill":notfill,'filled':filled,'suggest':suggest,'states':sstates,'age':sage,
                                                    'kids':skids,'btc': btc, 'eth': eth, 'zec': zec, 'trx': trx, 'ltc': ltc, 'dash': dash, 'ada': ada, 'doge': doge,
                                                    'stkList1': stkList1, 'stkList2': stkList2, 'stkList3': stkList3,'ssincome': ssincome,})


def portfolio(response):
    savingsblc=0
    cursv1per = 0
    cursv2per = 0
    Goal2,tgsv2,curval,Goal1,cursv1 = 0,0,0,0,0
    tgsv1,Goal2,cursv2,Healthdate,HealthExp,Termdate,TermExp,Familydate,FamilyExp=0,0,0,0,0,0,0,0,0
    Cardate,CarExp,Wheelerdate,WheelerExp,HomeDate,HomeExp=0,0,0,0,0,0
    global himailsent
    global timailsent
    global fimailsent
    global cimailsent
    global wimailsent
    global Hoimailsent
    global insuranceType, insuranceType1, insuranceType2, insuranceType3, insuranceType4, insuranceType5

    try:
        con = pymysql.connect(host="localhost", user="Kshitij", password="abcd@1234", database="sign_up")
        cur = con.cursor()
        cur.execute("select HId from signup where email=%s", emailid)
        row = cur.fetchone()
        Healthdate = list(row)
        Healthdate = Healthdate[0]

        cur.execute("select HIr from signup where email=%s", emailid)
        row = cur.fetchone()
        HealthExp = list(row)
        HealthExp = HealthExp[0]
        currentdate =pytz.timezone('Asia/Calcutta')
        currentdate = datetime.date.today().strftime("%d/%m/%Y")
        currentdate = str(currentdate)
        print(currentdate)
        if currentdate == HealthExp:
            if himailsent == 0:
                to = emailid
                mailfrom = 'financiiofinanceassistant@gmail.com'
                your_pass = "10131517"
                body = " Your Health Insurance is about to expire on {} to avoid heavy due please renew it as soon as possible \n after renewing update the date on Financiio \n\n Thanks & Regards \n Financiio".format(Healthdate)
                subject = 'Reminder For Health Insurance Renewal'
                message = MIMEMultipart()
                message['From'] = mailfrom
                message['To'] = to
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                text = message.as_string()

                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login(mailfrom , your_pass)
                mail.sendmail(mailfrom , to, text)
                mail.close()
                globals().update({"himailsent" : "1"})
                print('Mail had been sent succesfully')
                globals().update({"insuranceType" : "health"})
            else:
                globals().update({"insuranceType" : ""})

        cur.execute("select TId from signup where email=%s", emailid)
        row = cur.fetchone()
        Termdate = list(row)
        Termdate = Termdate[0]

        cur.execute("select TIr from signup where email=%s", emailid)
        row = cur.fetchone()
        TermExp = list(row)
        TermExp = TermExp[0]
        if currentdate == TermExp:
            if timailsent == 0:
                to = emailid
                mailfrom = 'financiiofinanceassistant@gmail.com'
                your_pass = "10131517"
                body = " Your Term Life Insurance is about to expire on {} to avoid heavy due please renew it as soon as possible \n after renewing update the date on Financiio \n\n Thanks & Regards \n Financiio".format(Termdate)
                subject = 'Reminder For Term Life Insurance Renewal'
                message = MIMEMultipart()
                message['From'] = mailfrom
                message['To'] = to
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                text = message.as_string()

                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login(mailfrom , your_pass)
                mail.sendmail(mailfrom , to, text)
                mail.close()
                globals().update({'timailsent' : '1'})
                print('Mail had been sent succesfully')
                globals().update({'insuranceType1' : "termlife"})
            else:
                globals().update({'insuranceType1' : ""})
        cur.execute("select FId from signup where email=%s", emailid)
        row = cur.fetchone()
        Familydate = list(row)
        Familydate = Familydate[0]

        cur.execute("select FIr from signup where email=%s", emailid)
        row = cur.fetchone()
        FamilyExp = list(row)
        FamilyExp = FamilyExp[0]

        if currentdate == FamilyExp:
            if fimailsent == 0:
                to = emailid
                mailfrom = 'financiiofinanceassistant@gmail.com'
                your_pass = "10131517"
                body = " Your Family Health Insurance is about to expire on {} to avoid heavy due please renew it as soon as possible \n after renewing update the date on Financiio \n\n Thanks & Regards \n Financiio".format(Familydate)
                subject = 'Reminder For Family Health Insurance Renewal'
                message = MIMEMultipart()
                message['From'] = mailfrom
                message['To'] = to
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                text = message.as_string()

                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login(mailfrom , your_pass)
                mail.sendmail(mailfrom , to, text)
                mail.close()
                globals().update({'fimailsent' : '1'})
                print('Mail had been sent succesfully')
                globals().update({'insuranceType2' :"familyhealth"})
            else:
                globals().update({'insuranceType2' :""})

        cur.execute("select CId from signup where email=%s", emailid)
        row = cur.fetchone()
        Cardate = list(row)
        Cardate = Cardate[0]

        cur.execute("select CIr from signup where email=%s", emailid)
        row = cur.fetchone()
        CarExp = list(row)
        CarExp = CarExp[0]
        if currentdate == CarExp:
            if cimailsent == 0:
                to = emailid
                mailfrom = 'financiiofinanceassistant@gmail.com'
                your_pass = "10131517"
                body = " Your Car Insurance is about to expire on {} to avoid heavy due please renew it as soon as possible \n after renewing update the date on Financiio \n\n Thanks & Regards \n Financiio".format(Cardate)
                subject = 'Reminder For Car Insurance Renewal'
                message = MIMEMultipart()
                message['From'] = mailfrom
                message['To'] = to
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                text = message.as_string()

                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login(mailfrom , your_pass)
                mail.sendmail(mailfrom , to, text)
                mail.close()
                globals().update({'cimailsent' : '1'})
                print('Mail had been sent succesfully')
                globals().update({'insuranceType3': "car"})
            else:
                globals().update({'insuranceType3': ""})
        cur.execute("select 2WId from signup where email=%s", emailid)
        row = cur.fetchone()
        Wheelerdate = list(row)
        Wheelerdate = Wheelerdate[0]

        cur.execute("select 2Wr from signup where email=%s", emailid)
        row = cur.fetchone()
        WheelerExp = list(row)
        WheelerExp = WheelerExp[0]

        if currentdate == WheelerExp:
            if wimailsent == 0:
                to = emailid
                mailfrom = 'financiiofinanceassistant@gmail.com'
                your_pass = "10131517"
                body = " Your 2 Wheeler Insurance is about to expire on {} to avoid heavy due please renew it as soon as possible \n after renewing update the date on Financiio \n\n Thanks & Regards \n Financiio".format(Wheelerdate)
                subject = 'Reminder For 2 Wheeler Insurance Renewal'
                message = MIMEMultipart()
                message['From'] = mailfrom
                message['To'] = to
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                text = message.as_string()

                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login(mailfrom , your_pass)
                mail.sendmail(mailfrom , to, text)
                mail.close()
                globals().update({'wimailsent' : '1'})
                print('Mail had been sent succesfully')
                globals().update({'insuranceType4' : "twowheeler"})
            else:
                globals().update({'insuranceType4': ""})

        cur.execute("select HOD from signup where email=%s", emailid)
        row = cur.fetchone()
        HomeDate = list(row)
        HomeDate = HomeDate[0]

        cur.execute("select HOR from signup where email=%s", emailid)
        row = cur.fetchone()
        HomeExp = list(row)
        HomeExp = HomeExp[0]
        if currentdate == HomeExp:
            if Hoimailsent == 0:
                to = emailid
                mailfrom = 'financiiofinanceassistant@gmail.com'
                your_pass = "10131517"
                body = " Your Home Insurance is about to expire on {} to avoid heavy due please renew it as soon as possible \n after renewing update the date on Financiio \n\n Thanks & Regards \n Financiio".format(HomeDate)
                subject = 'Reminder For Home Insurance Renewal'
                message = MIMEMultipart()
                message['From'] = mailfrom
                message['To'] = to
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                text = message.as_string()

                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login(mailfrom , your_pass)
                mail.sendmail(mailfrom , to, text)
                mail.close()
                globals().update({'Hoimailsent' : '1'})
                print('Mail had been sent succesfully')
                globals().update({'insuranceType5' : "home"})
            else:
                globals().update({'insuranceType5': ""})

        cur.execute("select svgAmt from signup where email=%s", emailid)
        row = cur.fetchone()
        curval = list(row)
        curval = curval[0]
        if response.method == 'POST':
            if 'savingsadd' in response.POST:
                svg = "0"
                svg = response.POST.get('savingsblc')
                curval += int(svg)
                print(curval)
                cur.execute("update signup set svgAmt=%s where email=%s", (curval, emailid))
                con.commit()
                return HttpResponseRedirect("/port")
            if 'savingssub' in response.POST:
                svg = response.POST.get('savingsblc')
                curval -= int(svg)
                if curval < 0:
                    curval = 0
                cur.execute("update signup set svgAmt=%s where email=%s", (curval, emailid))
                con.commit()
                return HttpResponseRedirect("/port")
        cur.execute("select Goal1 from signup where email=%s", emailid)
        row = cur.fetchone()
        Goal1 = list(row)
        Goal1 = Goal1[0]

        cur.execute("select tgsv1 from signup where email=%s", emailid)
        row = cur.fetchone()
        tgsv1 = list(row)
        tgsv1 = tgsv1[0]

        if response.POST.get('goal1bothdata'):
            goal = response.POST.get('goalname1')
            cur.execute("update signup set Goal1=%s where email=%s", (goal, emailid))
            con.commit()
            cur.execute("select Goal1 from signup where email=%s", emailid)
            row = cur.fetchone()
            Goal1 = list(row)
            Goal1 = Goal1[0]

            goaltgt = response.POST.get('goalamount1')
            cur.execute("update signup set tgsv1=%s where email=%s", (goaltgt, emailid))
            con.commit()
            cursv1 = 0
            cur.execute("select tgsv1 from signup where email=%s", emailid)
            row = cur.fetchone()
            tgsv1 = list(row)
            tgsv1 = tgsv1[0]
            cur.execute("update signup set cursv1=%s where email=%s", (cursv1, emailid))
            con.commit()
            cursv1per = 0
            cur.execute("select cursv1 from signup where email=%s", emailid)
            row = cur.fetchone()
            cursv1 = list(row)
            cursv1 = cursv1[0]
            return HttpResponseRedirect("/port")

        cur.execute("select cursv1 from signup where email=%s", emailid)
        row = cur.fetchone()
        cursv1 = list(row)
        cursv1 = list(row)
        cursv1 = cursv1[0]
        if cursv1 != 0:
            cursv1per = math.trunc(((cursv1/tgsv1)* 100))
        if response.POST.get("goalamtrmv"):
            curgoal = response.POST.get("goaladdorrmv")
            cursv1 += int(curgoal)
            if cursv1 > tgsv1:
                cursv1 = tgsv1
            cur.execute("update signup set cursv1=%s where email=%s", (cursv1, emailid))
            con.commit()
            cur.execute("select cursv1 from signup where email=%s", emailid)
            row = cur.fetchone()
            cursv1 = list(row)
            cursv1 = list(row)
            cursv1 = cursv1[0]
            cur.execute("select tgsv1 from signup where email=%s", emailid)
            row = cur.fetchone()
            tgsv1 = list(row)
            tgsv1 = tgsv1[0]
            if cursv1 != 0:
                cursv1per = math.trunc(((cursv1/tgsv1)* 100))
            return HttpResponseRedirect("/port")

        if response.POST.get("goalamtrm"):
            curgoal = response.POST.get("goaladdorrmv")
            cursv1 -= int(curgoal)
            if cursv1 < 0:
                cursv1 = 0
            cur.execute("update signup set cursv1=%s where email=%s", (cursv1, emailid))
            con.commit()
            cur.execute("select cursv1 from signup where email=%s", emailid)
            row = cur.fetchone()
            cursv1 = list(row)
            cursv1 = list(row)
            cursv1 = cursv1[0]
            cur.execute("select tgsv1 from signup where email=%s", emailid)
            row = cur.fetchone()
            tgsv1 = list(row)
            tgsv1 = tgsv1[0]
            if cursv1!= 0:
                cursv1per = math.trunc(((cursv1/tgsv1)* 100))
            return HttpResponseRedirect("/port")

        cur.execute("select Goal2 from signup where email=%s", emailid)
        row = cur.fetchone()
        Goal2 = list(row)
        Goal2 = Goal2[0]

        cur.execute("select cursv2 from signup where email=%s", emailid)
        row = cur.fetchone()
        cursv2 = list(row)
        cursv2 = cursv2[0]

        cur.execute("select tgsv2 from signup where email=%s", emailid)
        row = cur.fetchone()
        tgsv2 = list(row)
        tgsv2 = tgsv2[0]
        if cursv2 != 0:
            cursv2per = math.trunc(((cursv2 / tgsv2) * 100))
        if response.POST.get("goal2bothdata"):
            goal = response.POST.get('goalname2')
            cur.execute("update signup set Goal2=%s where email=%s", (goal, emailid))
            con.commit()
            cur.execute("select Goal2 from signup where email=%s", emailid)
            row = cur.fetchone()
            Goal2 = list(row)
            Goal2 = Goal2[0]

            goaltgt = response.POST.get('goalamount2')
            print(goaltgt)
            cursv2 = 0
            cur.execute("update signup set tgsv2=%s where email=%s", (goaltgt, emailid))
            con.commit()
            cur.execute("update signup set cursv2=%s where email=%s", (cursv2, emailid))
            con.commit()
            cur.execute("select cursv2 from signup where email=%s", emailid)
            row = cur.fetchone()
            cursv2 = list(row)
            cursv2 = cursv2[0]

            cur.execute("select tgsv2 from signup where email=%s", emailid)
            row = cur.fetchone()
            tgsv2 = list(row)
            tgsv2 = tgsv2[0]
            cursv2per = 0
            return HttpResponseRedirect("/port")

        cur.execute("select cursv2 from signup where email=%s", emailid)
        row = cur.fetchone()
        cursv2 = list(row)
        cursv2 = cursv2[0]
        if response.POST.get("goalamtrmv1"):
            curgoal = response.POST.get("goaladdorrmv1")
            cursv2 += int(curgoal)
            if cursv2 > tgsv2:
                cursv2 = tgsv2
            cur.execute("update signup set cursv2=%s where email=%s", (cursv2, emailid))
            con.commit()
            print(curgoal)
            cur.execute("select cursv2 from signup where email=%s", emailid)
            row = cur.fetchone()
            cursv2 = list(row)
            cursv2 = cursv2[0]
            if cursv2 != 0:
                cursv2per = math.trunc(((cursv2 / tgsv2) * 100))
            return HttpResponseRedirect("/port")

        if response.POST.get("submitgoal1"):
            curgoal = response.POST.get("goaladdorrmv1")
            cursv2 -= int(curgoal)
            if cursv2 < 0:
                cursv2 = 0
            cur.execute("update signup set cursv2=%s where email=%s", (cursv2, emailid))
            con.commit()
            print(curgoal)
            cur.execute("select cursv2 from signup where email=%s", emailid)
            row = cur.fetchone()
            cursv2 = list(row)
            cursv2 = cursv2[0]
            if cursv2 != 0:
                cursv2per = math.trunc(((cursv2 / tgsv2) * 100))
            return HttpResponseRedirect("/port")

        cur.execute("select HId from signup where email=%s", emailid)
        row = cur.fetchone()
        Healthdate = list(row)
        Healthdate = Healthdate[0]

        cur.execute("select HIr from signup where email=%s", emailid)
        row = cur.fetchone()
        HealthExp = list(row)
        HealthExp = HealthExp[0]
        if response.POST.get("healthinc"):
            Hd = response.POST.get("validdate1").replace("-","/")
            cur.execute("update signup set HId=%s where email=%s", (Hd, emailid))
            con.commit()
            Hr = response.POST.get("notificdate1").replace("-","/")
            cur.execute("update signup set HIr=%s where email=%s", (Hr, emailid))
            con.commit()
            cur.execute("select HId from signup where email=%s", emailid)
            row = cur.fetchone()
            Healthdate = list(row)
            Healthdate = Healthdate[0]

            cur.execute("select HIr from signup where email=%s", emailid)
            row = cur.fetchone()
            HealthExp = list(row)
            HealthExp = HealthExp[0]
            print(HealthExp)
            himailsent = 0
            timailsent = 0
            if currentdate == HealthExp:
                    to = emailid
                    mailfrom = 'financiiofinanceassistant@gmail.com'
                    your_pass = "10131517"
                    body = " Your Health Insurance is about to expire on {} to avoid heavy due please renew it as soon as possible \n after renewing update the date on Financiio \n\n Thanks & Regards \n Financiio".format(Healthdate)
                    subject = 'Reminder For Health Insurance Renewal'
                    message = MIMEMultipart()
                    message['From'] = mailfrom
                    message['To'] = to
                    message['Subject'] = subject
                    message.attach(MIMEText(body, 'plain'))
                    text = message.as_string()

                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login(mailfrom, your_pass)
                    mail.sendmail(mailfrom, to, text)
                    mail.close()
                    himailsent = 1
                    print('Mail had been sent succesfully')
                    insuranceType = "health"
            else:
                    insuranceType= ""
        cur.execute("select TId from signup where email=%s", emailid)
        row = cur.fetchone()
        Termdate = list(row)
        Termdate = Termdate[0]

        cur.execute("select TIr from signup where email=%s", emailid)
        row = cur.fetchone()
        TermExp = list(row)
        TermExp = TermExp[0]
        if response.POST.get("healthinc2"):
            Td = response.POST.get("validdate2").replace("-","/")
            cur.execute("update signup set TId=%s where email=%s", (Td, emailid))
            con.commit()
            Tr = response.POST.get("notificdate2").replace("-","/")
            cur.execute("update signup set TIr=%s where email=%s", (Tr, emailid))
            con.commit()
            cur.execute("select TId from signup where email=%s", emailid)
            row = cur.fetchone()
            Termdate = list(row)
            Termdate = Termdate[0]

            cur.execute("select TIr from signup where email=%s", emailid)
            row = cur.fetchone()
            TermExp = list(row)
            TermExp = TermExp[0]
            if currentdate == TermExp:
                    to = emailid
                    mailfrom = 'financiiofinanceassistant@gmail.com'
                    your_pass = "10131517"
                    body = " Your Term Life Insurance is about to expire on {} to avoid heavy due please renew it as soon as possible \n after renewing update the date on Financiio \n\n Thanks & Regards \n Financiio".format(
                        Termdate)
                    subject = 'Reminder For Term Life Insurance Renewal'
                    message = MIMEMultipart()
                    message['From'] = mailfrom
                    message['To'] = to
                    message['Subject'] = subject
                    message.attach(MIMEText(body, 'plain'))
                    text = message.as_string()

                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login(mailfrom, your_pass)
                    mail.sendmail(mailfrom, to, text)
                    mail.close()
                    timailsent = 1
                    print('Mail had been sent succesfully')
                    insuranceType1 = "termlife"
            else:
                    insuranceType1 = ""
        cur.execute("select FId from signup where email=%s", emailid)
        row = cur.fetchone()
        Familydate = list(row)
        Familydate = Familydate[0]

        cur.execute("select FIr from signup where email=%s", emailid)
        row = cur.fetchone()
        FamilyExp = list(row)
        FamilyExp = FamilyExp[0]
        if response.POST.get("healthinc3"):
            Fd = response.POST.get("validdate3").replace("-","/")
            cur.execute("update signup set FId=%s where email=%s", (Fd, emailid))
            con.commit()
            print(Fd)
            Fr = response.POST.get("notificdate3").replace("-","/")
            cur.execute("update signup set FIr=%s where email=%s", (Fr, emailid))
            con.commit()
            print(Fr)
            cur.execute("select FId from signup where email=%s", emailid)
            row = cur.fetchone()
            Familydate = list(row)
            Familydate = Familydate[0]
            fimailsent = 0
            if currentdate == FamilyExp:

                    to = emailid
                    mailfrom = 'financiiofinanceassistant@gmail.com'
                    your_pass = "10131517"
                    body = " Your Family Health Insurance is about to expire on {} to avoid heavy due please renew it as soon as possible \n after renewing update the date on Financiio \n\n Thanks & Regards \n Financiio".format(
                        Familydate)
                    subject = 'Reminder For Family Health Insurance Renewal'
                    message = MIMEMultipart()
                    message['From'] = mailfrom
                    message['To'] = to
                    message['Subject'] = subject
                    message.attach(MIMEText(body, 'plain'))
                    text = message.as_string()

                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login(mailfrom, your_pass)
                    mail.sendmail(mailfrom, to, text)
                    mail.close()
                    fimailsent = 1
                    print('Mail had been sent succesfully')
                    insuranceType2 = "familyhealth"
            else:
                    insuranceType2 = ""
            cur.execute("select FIr from signup where email=%s", emailid)
            row = cur.fetchone()
            FamilyExp = list(row)
            FamilyExp = FamilyExp[0]
        cur.execute("select CId from signup where email=%s", emailid)
        row = cur.fetchone()
        Cardate = list(row)
        Cardate = Cardate[0]

        cur.execute("select CIr from signup where email=%s", emailid)
        row = cur.fetchone()
        CarExp = list(row)
        CarExp = CarExp[0]
        if response.POST.get("healthinc4"):
            Cd = response.POST.get("validdate4").replace("-","/")
            cur.execute("update signup set CId=%s where email=%s", (Cd, emailid))
            con.commit()
            print(Cd)
            Cr = response.POST.get("notificdate4").replace("-","/")
            cur.execute("update signup set CIr=%s where email=%s", (Cr, emailid))
            con.commit()
            print(Cr)
            cimailsent = 0
            if currentdate == CarExp:

                    to = emailid
                    mailfrom = 'financiiofinanceassistant@gmail.com'
                    your_pass = "10131517"
                    body = " Your Car Insurance is about to expire on {} to avoid heavy due please renew it as soon as possible \n after renewing update the date on Financiio \n\n Thanks & Regards \n Financiio".format(
                        Cardate)
                    subject = 'Reminder For Car Insurance Renewal'
                    message = MIMEMultipart()
                    message['From'] = mailfrom
                    message['To'] = to
                    message['Subject'] = subject
                    message.attach(MIMEText(body, 'plain'))
                    text = message.as_string()

                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login(mailfrom, your_pass)
                    mail.sendmail(mailfrom, to, text)
                    mail.close()
                    cimailsent = 1
                    print('Mail had been sent succesfully')
                    insuranceType3 = "car"
            else:
                    insuranceType3 = ""
        cur.execute("select CId from signup where email=%s", emailid)
        row = cur.fetchone()
        Cardate = list(row)
        Cardate = Cardate[0]

        cur.execute("select CIr from signup where email=%s", emailid)
        row = cur.fetchone()
        CarExp = list(row)
        CarExp = CarExp[0]

        cur.execute("select 2WId from signup where email=%s", emailid)
        row = cur.fetchone()
        Wheelerdate = list(row)
        Wheelerdate = Wheelerdate[0]

        cur.execute("select 2Wr from signup where email=%s", emailid)
        row = cur.fetchone()
        WheelerExp = list(row)
        WheelerExp = WheelerExp[0]
        if response.POST.get("healthinc5"):
            Wd = response.POST.get("validdate5").replace("-","/")
            cur.execute("update signup set 2WId=%s where email=%s", (Wd, emailid))
            con.commit()
            print(Wd)
            Wr = response.POST.get("notificdate5").replace("-","/")
            cur.execute("update signup set 2Wr=%s where email=%s", (Wr, emailid))
            con.commit()
            print(Wr)
            wimailsent = 0

            cur.execute("select 2WId from signup where email=%s", emailid)
            row = cur.fetchone()
            Wheelerdate = list(row)
            Wheelerdate = Wheelerdate[0]

            cur.execute("select 2Wr from signup where email=%s", emailid)
            row = cur.fetchone()
            WheelerExp = list(row)
            WheelerExp = WheelerExp[0]
            if currentdate == WheelerExp:

                    to = emailid
                    mailfrom = 'financiiofinanceassistant@gmail.com'
                    your_pass = "10131517"
                    body = " Your 2 Wheeler Insurance is about to expire on {} to avoid heavy due please renew it as soon as possible \n after renewing update the date on Financiio \n\n Thanks & Regards \n Financiio".format(
                        Wheelerdate)
                    subject = 'Reminder For 2 Wheeler Insurance Renewal'
                    message = MIMEMultipart()
                    message['From'] = mailfrom
                    message['To'] = to
                    message['Subject'] = subject
                    message.attach(MIMEText(body, 'plain'))
                    text = message.as_string()

                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login(mailfrom, your_pass)
                    mail.sendmail(mailfrom, to, text)
                    mail.close()
                    wimailsent = 1
                    print('Mail had been sent succesfully')
                    insuranceType4 = "twowheeler"
            else:
                    insuranceType4 = ""

        cur.execute("select HOD from signup where email=%s", emailid)
        row = cur.fetchone()
        HomeDate = list(row)
        HomeDate = HomeDate[0]

        cur.execute("select HOR from signup where email=%s", emailid)
        row = cur.fetchone()
        HomeExp = list(row)
        HomeExp = HomeExp[0]
        if response.POST.get("healthinc6"):
            HOD = response.POST.get("validdate6").replace("-","/")
            cur.execute("update signup set HOD=%s where email=%s", (HOD, emailid))
            con.commit()
            print(HOD)
            HOR = response.POST.get("notificdate6").replace("-","/")
            cur.execute("update signup set HOR=%s where email=%s", (HOR, emailid))
            con.commit()
            print(HOR)
            hoimailsent = 0
            cur.execute("select HOD from signup where email=%s", emailid)
            row = cur.fetchone()
            HomeDate = list(row)
            HomeDate = HomeDate[0]

            cur.execute("select HOR from signup where email=%s", emailid)
            row = cur.fetchone()
            HomeExp = list(row)
            HomeExp = HomeExp[0]
            if currentdate == HomeExp:
                    to = emailid
                    mailfrom = 'financiiofinanceassistant@gmail.com'
                    your_pass = "10131517"
                    body = " Your Home Insurance is about to expire on {} to avoid heavy due please renew it as soon as possible \n after renewing update the date on Financiio \n\n Thanks & Regards \n Financiio".format(
                        HomeDate)
                    subject = 'Reminder For Home Insurance Renewal'
                    message = MIMEMultipart()
                    message['From'] = mailfrom
                    message['To'] = to
                    message['Subject'] = subject
                    message.attach(MIMEText(body, 'plain'))
                    text = message.as_string()

                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login(mailfrom, your_pass)
                    mail.sendmail(mailfrom, to, text)
                    mail.close()
                    Hoimailsent = 1
                    print('Mail had been sent succesfully')
                    insuranceType5 = "home"
            else:
                insuranceType5 = ""
        cur.execute("select HId from signup where email=%s", emailid)
        row = cur.fetchone()
        globals().update({'date1' : list(row)})
        globals().update({'date1': date1[0]})
        cur.execute("select TId from signup where email=%s", emailid)
        row = cur.fetchone()
        globals().update({'date2': list(row)})
        globals().update({'date2': date2[0]})
        cur.execute("select FId from signup where email=%s", emailid)
        row = cur.fetchone()
        globals().update({'date3' : list(row)})
        globals().update({'date3': date3[0]})
        cur.execute("select CId from signup where email=%s", emailid)
        row = cur.fetchone()
        globals().update({'date4': list(row)})
        globals().update({'date4': date4[0]})
        cur.execute("select 2WId from signup where email=%s", emailid)
        row = cur.fetchone()
        globals().update({'date5': list(row)})
        globals().update({'date5': date5[0]})
        cur.execute("select HOD from signup where email=%s", emailid)
        row = cur.fetchone()
        globals().update({'date6': list(row)})
        globals().update({'date6': date6[0]})
    except Exception as es:
        print("Exception occured !")
        print(str(es))
    return render(response, "main/Portfolio.html", {"curval":curval,"Goal1":Goal1,"cursv1":cursv1,
                                                    "tgsv1":tgsv1,"cursv1per":cursv1per,"Goal2":Goal2,
                                                    "tgsv2":tgsv2,"cursv2":cursv2,"cursv2per":cursv2per,
                                                    "Healthdate":Healthdate,"HealthExp":HealthExp,
                                                    "Termdate":Termdate,"TermExp":TermExp,"Familydate":Familydate,
                                                    "FamilyExp":FamilyExp,"Cardate":Cardate,"CarExp":CarExp,
                                                    "Wheelerdate": Wheelerdate, "WheelerExp": WheelerExp,
                                                    "HomeDate": HomeDate, "HomeExp": HomeExp,"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5,"date1": date1,"date2": date2,
                                                    "date3": date3,"date4": date4,"date5": date5,"date6": date6,
                                                    })
def base(response):
    return render(response, "main/base.html",{"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                              "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5,
                                              "date1": date1,"date2": date2,"date3": date3,"date4": date4,
                                              "date5": date5,"date6": date6,
                                              })
def base2(response):
    return render(response, "main/base.html",{"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                              "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5,
                                              "date1": date1,"date2": date2,"date3": date3,"date4": date4,
                                              "date5": date5,"date6": date6,
                                              })
def news(response):
    con = pymysql.connect(host="localhost", user="Kshitij", password="abcd@1234", database="sign_up")
    cur = con.cursor()
    newstype = ''
    newstyperet = ''
    newsall = 'yes'
    if response.POST.get('dailynewssubmit'):
        newstype = response.POST.get('suggestkids')
        newstype = str(newstype)
        cur.execute("update signup set newstype=%s where email=%s",(newstype, emailid))
    api_key = 'f2f02a5247e04407a75493458dd1d429'
    url = "https://newsapi.org/v2/everything?q=bitcoin&from=2021-06-19&to=2021-06-19&sortBy=popularity&apiKey={}".format(api_key)
    crypto_headline = []
    crypto_discript = []
    crypto_url = []
    crypto_img = []
    responses = requests.get(url)
    crypto_news = json.loads(responses.text)
    for i in range(0,20):
        crypto_headline.append(crypto_news['articles'][i]['title'])
        crypto_discript.append(crypto_news['articles'][i]['description'][:80])
        crypto_url.append(crypto_news['articles'][i]['url'])
        crypto_img.append(crypto_news['articles'][i]['urlToImage'])

    url = "https://newsapi.org/v2/everything?q=stocks&from=2021-06-19&to=2021-06-19&sortBy=popularity&apiKey={}".format(
        api_key)
    stocks_headline = []
    stocks_discript = []
    stocks_url = []
    stocks_img = []
    responses = requests.get(url)
    stocks_news = json.loads(responses.text)
    for i in range(0, 20):
        stocks_headline.append(stocks_news['articles'][i]['title'])
        stocks_discript.append(stocks_news['articles'][i]['description'][:80])
        stocks_url.append(stocks_news['articles'][i]['url'])
        stocks_img.append(stocks_news['articles'][i]['urlToImage'])
    cur.execute("select newstype from signup where email=%s", (emailid))
    newstyperet = cur.fetchone()
    newstyperet = str(newstyperet[0])
    print(newstyperet)
    if len(newstyperet) < 4:
        newsall = 'yes'
    else:
        newsall = 'no'
    return render(response,"main/dailynews.html",{'cheadline':crypto_headline,'cdicrip':crypto_discript,'curl':crypto_url,
                                                  'cimage':crypto_img,'sheadline':stocks_headline,'sdicrip':stocks_discript,'surl':stocks_url,
                                                   'simage':stocks_img,"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                   "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5,
                                                   "date1": date1,"date2": date2,"date3": date3,"date4": date4,
                                                   "date5": date5,"date6": date6,'newstyperet':newstyperet,'newsall':newsall})

def learn(response):
    return render(response,"main/learningplatform.html",{"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                   "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5,
                                                   "date1": date1,"date2": date2,"date3": date3,"date4": date4,
                                                   "date5": date5,"date6": date6,})
def settings(response):
    specsymb = ['@','#','$','%','&']

    if response.method == 'POST':
        if response.POST.get('logout'):
            globals().update({'emailid': ""})
            return redirect("/home")
        if response.POST.get('updateprofile'):
            st_name = response.POST.get('name')
            st_income = response.POST.get('suggestincome')
            st_age = response.POST.get('suggestage')
            st_state = response.POST.get('suggeststates')
            st_kids = response.POST.get('suggestkids')

            print(st_name)
            print(st_income)
            print(st_age)
            print(st_state)
            print(st_kids)
            try:
                con = pymysql.connect(host="localhost", user="Kshitij", password="abcd@1234", database="sign_up")
                cur = con.cursor()
                cur.execute("update signup set name=%s,income=%s,age=%s,states=%s,kids=%s where email=%s",
                                    (st_name,st_income, st_age, st_state, st_kids, emailid))
                con.commit()
                con.close()
                globals().update({'ssuccespro': 'updated'})
            except Exception as es:
                print("Some Exception Occurred")
                print(str(es))
        if response.POST.get('changepassword'):
            password = response.POST.get('updatepassword')
            cnfpassword = response.POST.get('re-updatepassword')

            print(password)
            print(cnfpassword)

            if password == cnfpassword:
                try:
                        if len(password) >= 8:
                            if any(char.isdigit() for char in password):
                                if any(char.isupper() for char in password):
                                    if any(char in specsymb for char in password):
                                        con = pymysql.connect(host="localhost", user="Kshitij", password="abcd@1234", database="sign_up")
                                        cur = con.cursor()
                                        cur.execute("update signup set password=%s where email=%s",(cnfpassword, emailid))
                                        con.commit()
                                        con.close()
                                        globals().update({'succespass':'updated'})
                                        globals().update({'cspwdruls': 'yes'})
                                    else:
                                        globals().update({'cspwdruls': 'no'})
                                else:
                                    globals().update({'cspwdruls': 'no'})
                            else:
                                globals().update({'cspwdruls': 'no'})
                        else:
                            globals().update({'cspwdruls': 'no'})
                except Exception as es:
                    print("Some Exception Occurred")
                    print(str(es))

                print("Password Updated Successfully")
            else:
                print("Variation found between entered password")
    return render(response, "main/settings.html", {'ssuccespro':ssuccespro,'succespass':succespass,"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5,
                                                    "date1": date1,"date2": date2,"date3": date3,"date4": date4,
                                                    "date5": date5,"date6": date6,'cspwdruls':cspwdruls})

def blogStk1(response):
    return render(response, "main/blogStk1.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogStk2(response):
    return render(response, "main/blogStk2.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogStk3(response):
    return render(response, "main/blogStk3.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogStk4(response):
    return render(response, "main/blogStk4.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogStk5(response):
    return render(response, "main/blogStk5.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogStk6(response):
    return render(response, "main/blogStk6.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogStk7(response):
    return render(response, "main/blogStk7.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogCryp1(response):
    return render(response, "main/blogCryp1.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogCryp2(response):
    return render(response, "main/blogCryp2.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogCryp3(response):
    return render(response, "main/blogCryp3.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogCryp4(response):
    return render(response, "main/blogCryp4.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogCryp5(response):
    return render(response, "main/blogCryp5.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogCryp6(response):
    return render(response, "main/blogCryp6.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})

def blogCryp7(response):
    return render(response, "main/blogCryp7.html", {"insuranceType":insuranceType,"insuranceType1":insuranceType1,"insuranceType2":insuranceType2,
                                                    "insuranceType3":insuranceType3,"insuranceType4":insuranceType4,"insuranceType5":insuranceType5})                                                    