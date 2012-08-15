import datetime, feedparser
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from semiocoder.encoder.models import TaskHistory

def getAARFeed():
    rss_url = 'http://www.archivesaudiovisuelles.fr/fr/rss/aar_rss.xml'
    feed = feedparser.parse(rss_url)
    news = []
    
    for item in feed["items"][:7]: 
        news.append({ 'title' : item['title'], 'link' : item['link'], 'date' : datetime.datetime.strptime(item['date'][5:16], "%d %b %Y") })

    return news


def notify(level, history):
    semiocoder = User.objects.get(pk=1).email
    th = TaskHistory.objects.get(pk=history)
    if level == 1:
        addressee = [ User.objects.get(username__exact=th.owner).email ]
    elif level == 2:
        addressee = []
        groups = User.objects.get(username__exact=th.owner).groups.select_related()
        for g in groups:
            for u in g.user_set.select_related():
                addressee.append(u.email)
        if not addressee: addressee = [ User.objects.get(username__exact=th.owner).email ]
    else:
        addressee = [ semiocoder ]

    subject = str('La tache '+ th.joblist + ' s est termine avec le statut ' +th.state)
    from_email, to = semiocoder, addressee
    text_content = th.log
    html_content = th.log.replace("\n", "\n<br>")
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    #msg.attach_file('report.pdf', 'application/pdf')
    msg.send()



