# -*- coding: utf-8 -*-
"""
.. module:: libs
   :platform: Unix, Windows
   :synopsis: Libraires de fonctions nécéssaire à l'application encodeur

.. moduleauthor:: Samuel Darko <samidarko@gmail.com>

"""
import datetime, feedparser, os
from django.core.mail import EmailMultiAlternatives
from semiocoder.settings import EMAIL_FILE_PATH, SERVER_EMAIL
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def getAARFeed():
    """Renvoi les 6 dernières nouvelles des AAR via leur flux RSS
    
    :returns: dict
    """
    rss_url = 'http://www.archivesaudiovisuelles.fr/fr/rss/aar_rss.xml'
    feed = feedparser.parse(rss_url)
    news = []
    
    for item in feed["items"][:7]: 
        news.append({ 'title' : item['title'], 'link' : item['link'], 'date' : datetime.datetime.strptime(item['date'][5:16], "%d %b %Y") })

    return news


styles=getSampleStyleSheet()


def makeTaskLogToPdf(th):
    reportname = EMAIL_FILE_PATH+'/'+th.joblist+".pdf"
    doc = SimpleDocTemplate(reportname,pagesize=A4, rightMargin=72,leftMargin=72, topMargin=72,bottomMargin=18)
    Story=[]
    Story.append(Paragraph('Log de la joblist '+th.joblist, styles["Title"]))
    Story.append(Spacer(1, 12))

    logtab = th.log.split('\n')

    for line in logtab:
        if line.startswith('====='):
            Story.append(Paragraph(line, styles["Heading3"]))
        else:
            Story.append(Paragraph(line, styles["Normal"]))

    doc.build(Story)
    
    report = open(reportname)
    content = report.read()
    report.close()
    os.remove(reportname)
    
    return content


def notify(t, th):
    """Fonction de notification de l'utilisateur (A revoir)
    
    :returns: None
    """

    subject = str('La tache '+ th.joblist + ' s est termine avec le statut ' +th.state)
    from_email, to = SERVER_EMAIL, (t.owner.email,)
    text_content = th.log
    html_content = th.log.replace("\n", "\n<br>")
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    content = makeTaskLogToPdf(th)
    msg.attach('report.pdf', content, 'application/pdf')
    msg.send()



