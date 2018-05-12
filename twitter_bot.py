#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tweepy
from tweepy.error import TweepError
import json
import datetime
import urllib.request
import pprint
pp = pprint.PrettyPrinter(indent=4)

import classifier

LEARNED_MODEL_FILEPATH = "learned_model/nijinet_v1_1.0_224.graphdef.pb"

def get_tweet_url_from_status(status):
	return "https://twitter.com/{0}/status/{1}".format(status.user.screen_name, status.id)

def get_image_url_from_status(status):
	try:
		#pp.pprint(status.extended_entities)
		#pp.pprint(status.extended_entities["media"])
		#pp.pprint(status.extended_entities["media"][0])
		#pp.pprint(status.extended_entities["media"][0]["media_url"])
		url = status.extended_entities["media"][0]["media_url"]
	except AttributeError as err:
		return None

	return "{0}:{1}".format(url, "small")

def download_image_file(url):
	local_filename, headers = urllib.request.urlretrieve(url)
	return local_filename

def fleetclassify_status(status):
	#pp.pprint(status)
	image_url = get_image_url_from_status(status)
	print("image: " + str(image_url))
	if not image_url:
		return None

	image_filepath = download_image_file(image_url)
	print("image filepath: " + str(image_filepath))
	image_paths = [image_filepath]

	result_txt = ''

	classifier_ = classifier.Classifier(LEARNED_MODEL_FILEPATH)
	predictions = classifier_.classify(image_paths)
	for image_path, prediction in zip(image_paths, predictions):
		if prediction < 0.5:
			result_txt += "艦これ"
		else:
			result_txt += "アズールレーン"
		result_txt += ' (%.3f)' % (prediction)

	return result_txt


class Listener(tweepy.StreamListener):
	def on_status(self, status):
		status.created_at += datetime.timedelta(hours=9)

		# ** reply when mention ("@" tweet)
		for user_mention in status.entities['user_mentions']:
			#print("receive mention: {0} {1}".format(status.user.screen_name, str(datetime.datetime.today())))
			#pp.pprint(user_mention)

			if str(status.user.screen_name) == client_info["screen_name"]:
				# exclude self mention.
				pass
			else:
				#print("receive mention: " + str(datetime.datetime.today()))

				# exec classify
				result_txt = fleetclassify_status(status)
				#print("result text: `{0}`".format(result_txt))

				if not result_txt:
					result_txt = "Tweetを解析できませんでした。画像が1枚以上含まれるTweetを行ってください。({0})" \
							.format(str(datetime.datetime.today()))

				# ** reply
				#try:
				#	tweet = "@{0} {1}".format(
				#			status.user.screen_name, result_txt)
				#	api.update_status(status=tweet, in_reply_to_status_id=status.id)
				#except TweepError as err:
				#	pp.pprint(err)

				# ** quote tweet(ja:`引用ツイート`)
				try:
					tweet_url = get_tweet_url_from_status(status)
					tweet = "@{0} {1}\n{2}".format(
							status.user.screen_name, result_txt, tweet_url)
					api.update_status(status=tweet, in_reply_to_status_id=status.id)
				except TweepError as err:
					pp.pprint(err)

			return True

		# ** favo when reply
		if str(status.in_reply_to_screen_name) == client_info["screen_name"]:
			if str(status.user.screen_name) == client_info["screen_name"]:
				# exclude self reply.
				pass
			else:
				print("receive reply: " + str(datetime.datetime.today()))
				try:
					api.create_favorite(status.id)
				except TweepError as err:
					pp.pprint(err)
				return True

		# ** favo when retweet
		if hasattr(status, "retweeted_status"):
			print("receive retweet: " + str(datetime.datetime.today()))
			try:
				api.create_favorite(status.id)
			except TweepError as err:
				pp.pprint(err)
			return True

		return True

	def on_error(self, status_code):
		print('Error code:' + str(status_code))
		return True

	def on_timeout(self):
		print('Timeout error')
		return True


# screen_name and access keys
f = open('client.json', 'r')
client_info = json.load(f)
f.close()

# auth
auth = tweepy.OAuthHandler(client_info["consumer_key"], client_info["consumer_secret"])
auth.set_access_token(client_info["access_token"], client_info["access_secret"])
api = tweepy.API(auth)

# tweeet when bot startup
api.update_status("Hello. : " + str(datetime.datetime.today()))

# stream
listener = Listener()
stream = tweepy.Stream(auth, listener)
stream.userstream()

