# -*- coding: utf-8 -*-
"""
.. module:: libs
   :platform: Unix, Windows
   :synopsis: Libraires de fonctions nécéssaire à l'application encodeur

.. moduleauthor:: Samuel Darko <samidarko@gmail.com>

"""
import datetime, feedparser
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from semiocoder.encoder.models import TaskHistory

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


def notify(history):
    """Fonction de notification de l'utilisateur (A revoir)
    
    :returns: None
    """
    semiocoder = User.objects.get(pk=1).email
    th = TaskHistory.objects.get(pk=history)
    addressee = [ User.objects.get(username__exact=th.owner).email ]

    subject = str('La tache '+ th.joblist + ' s est termine avec le statut ' +th.state)
    from_email, to = semiocoder, addressee
    text_content = th.log
    html_content = th.log.replace("\n", "\n<br>")
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    #msg.attach_file('report.pdf', 'application/pdf')
    msg.send()



