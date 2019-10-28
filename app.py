#!/usr/bin/env python3

from aws_cdk import core

from whats_new_podcast.whats_new_podcast_stack import WhatsNewPodcastStack


app = core.App()
WhatsNewPodcastStack(app, "whats-new-podcast")

app.synth()
