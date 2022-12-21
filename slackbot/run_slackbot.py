from sqlalchemy import create_engine
import pandas as pd
import requests

engine = create_engine('postgresql://postgres:1234@postgresdb:5432/twitter', echo=True)
result = engine.execute('SELECT * FROM tweets ORDER BY created_at DESC').fetchone()._mapping

webhook_url = "https://hooks.slack.com/services/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"
requests.post(url=webhook_url, json={
    'blocks': [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f":fire:*_INCOMING MACHINE LEARNING TWEET_*:fire: \n\n*Posted at*: {result.created_at}  \n*Sentiment*: {result.sentiment}  \n*Tweet*:  \n\n_{result.text}_"
			},
			"accessory": {
				"type": "image",
				"image_url": "https://i.dailymail.co.uk/1s/2018/11/15/10/6216094-6390319-Michael_Rapaport_posted_a_short_clip_of_the_Chinchilla_Persian_k-m-12_1542278756274.jpg",
				"alt_text": "alt text for image"
			}
		},
    ]
})

#Tear down
engine.execute('DROP TABLE IF EXISTS tweets')
