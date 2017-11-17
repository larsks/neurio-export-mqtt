#!/usr/bin/env python

import argparse
import json
import logging
import neurio
import os
import time

import paho.mqtt.client as mqtt

LOG = logging.getLogger(__name__)


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('--client-id',
                   default=os.environ.get('NEURIO_CLIENT_ID'))
    p.add_argument('--client-secret',
                   default=os.environ.get('NEURIO_CLIENT_SECRET'))
    p.add_argument('--sensor-id',
                   default=os.environ.get('NEURIO_SENSOR_ID'))
    p.add_argument('--location',
                   default=os.environ.get('NEURIO_LOCATION'))
    p.add_argument('--interval', '-i',
                   default=os.environ.get('NEURIO_POLL_INTERVAL', 60),
                   type=int)
    p.add_argument('--topic',
                   default=os.environ.get('NEURIO_TOPIC_PREFIX', 'sensor'))
    p.add_argument('--mqtt-server', '-s',
                   default=os.environ.get('NEURIO_MQTT_SERVER'))

    return p.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level='INFO')

    LOG.info('authenticating to neurio api')
    tp = neurio.TokenProvider(key=args.client_id,
                              secret=args.client_secret)
    nc = neurio.Client(token_provider=tp)

    LOG.info('connecting to mqtt broker')
    mq = mqtt.Client()
    mq.loop_start()
    mq.connect(args.mqtt_server)

    while True:
        sample = nc.get_samples_live_last(args.sensor_id)
        del sample['timestamp']
        sample['sensor_id'] = args.sensor_id
        sample['sensor_type'] = 'neurio'
        LOG.info('sending sample %s', sample)
        topic = '{}/neurio/{}'.format(args.topic, args.sensor_id)
        msg = json.dumps(sample)
        mq.publish(topic, msg)

        time.sleep(args.interval)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
