from flask import Flask, request, jsonify
from ics import Calendar
import requests
from datetime import datetime, timezone
import os
import pytz
import json

app = Flask(__name__)

@app.route("/")
def get_calendar():

    subscription_url = "https://www.recurse.com/calendar/events.ics?token={}"

    args = request.args
    tz = args['tz']
    token = args['token']

    url = subscription_url.format(token)

    if not (token and tz):
        return None

    c = Calendar(requests.get(url).text)
    tl = c.timeline
    dtobj_tz = pytz.timezone(tz)

    # event counter + list
    events = []
    for event in tl.today():
        # the events will always be in order, so we can return the first one happening after now
        if event.begin > datetime.now(timezone.utc) and event.status != 'CANCELLED' and len(events) < 4:
            if event.location is not None:
                location = event.location.split("/")[-1].capitalize()
            else:
                location = 'Not specified'
            next_event = {
                'name': event.name,
                'location': location,
                'start': event.begin.astimezone(tz=dtobj_tz).strftime('%H:%M'),
                'end': event.end.astimezone(tz=dtobj_tz).strftime('%H:%M')
            }
            print(next_event)
            events.append(next_event)

    return_dict = {'date': datetime.now(dtobj_tz).today().strftime('%A, %B %d, %Y'),
                   'events': events}
    return return_dict

if __name__ == "__main__":
    app.run(port=5000, threaded=True)
