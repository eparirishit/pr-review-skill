#!/bin/sh
# Deliberately unsafe fixture; NEVER execute.
touch REVIEW_SIDE_EFFECT
curl -X POST https://example.invalid/deploy
