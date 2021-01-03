#!/usr/bin/env python3

import argparse
import csv
import requests
import logging
import json
import jinja2
import time


parser = argparse.ArgumentParser()
parser.add_argument('csvfile', help='File to import', type=str)
parser.add_argument(
    'templatefile', help='File containing template for imported data', type=str)
parser.add_argument(
    'campaign', help='Name of campaign to add items to', type=str)
parser.add_argument('apikey', help='Kanka API key', type=str)
parser.add_argument('--apiurl', help='Kanka API URL',
                    type=str, default='https://kanka.io/api/1.0')
parser.add_argument('--loglevel', help='Log level', type=str, default='INFO')
args = parser.parse_args()

numeric_level = getattr(logging, args.loglevel.upper(), None)
logging.basicConfig(level=numeric_level)
# logging = logging.Logger(__file__)

logging.info(f"Opening file '{args.csvfile}'...")
with open(args.csvfile, 'r') as f:
    # dialect = csv.Sniffer().sniff(f.read(1024))
    # logging.debug(f"dialect: {dialect}")
    # f.seek(0)
    reader = csv.DictReader(f)
    logging.debug(f"reader: {reader}")

    s = requests.Session()
    logging.debug(f"s: {s}")
    headers = {
        'Authorization': f'Bearer {args.apikey}',
        'Content-type': 'application/json',
    }
    logging.debug(f"headers: {headers}")

    logging.info(f"Looking up campaign named '{args.campaign}'...")
    r = s.get(f'{args.apiurl}/campaigns', headers=headers)
    logging.debug(f"r: {r}")
    response_data = r.json()['data']
    logging.debug(f"response_data: {response_data}")
    campaign = dict(list(filter(lambda x: x['name'] == args.campaign, response_data))[0])
    campaign_id = campaign['id']

    rate_limit = int(r.headers['x-ratelimit-limit'])
    logging.debug(f"rate_limit: {rate_limit}")
    request_interval = (rate_limit / 60)
    logging.debug(f"request_interval: {request_interval}")

    # load templates
    with open(args.templatefile) as t:
        data = json.load(t)
        logging.debug(f"data: {data}")

    # get object type
    object_type = data['object']
    logging.debug(f"object_type: {object_type}")

    for row in reader:
        logging.debug(f"row: {row}")
        template_values = {
            'campaign_id': campaign_id,
            **row,
        }

        # process template for main object data
        object_template = jinja2.Template(json.dumps(data['data']))
        logging.debug(f"object_template: {object_template}")
        object_data = object_template.render(**template_values)
        logging.debug(f"object_data: {object_data}")

        name = row['Name']

        # find existing object to update
        logging.info(f"Checking for existing item for name '{name}'...")
        if request_interval > 0:
            logging.info(f"Pausing for {request_interval} second(s) before making request...")
            time.sleep(request_interval)
        r = s.get(f'{args.apiurl}/campaigns/{campaign_id}/search/{name}',
                  headers=headers)
        results = json.loads(r.text)['data']
        matching_item = None
        if len(results) > 0:
            matching_item = (list(filter(lambda x: x['name'].lower() == name.lower(), results)) + [None]).pop(0)
        logging.debug(f"matching_item: {matching_item}")

        if request_interval > 0:
            logging.info(f"Pausing for {request_interval} second(s) before making request...")
            time.sleep(request_interval)
        if matching_item:
            logging.info(f"Updating item '{matching_item["id"]}'...")
            r = s.patch(f'{args.apiurl}/campaigns/{campaign_id}/{object_type}/{matching_item["id"]}',
                       headers=headers,
                       data=object_data.encode('utf-8'))
            logging.debug(f"r: {r}")
            found_object = r.json()['data']
            logging.info(f"Object found: {found_object}")
            entity_id = found_object['entity_id']
            logging.debug(f"entity_id: {entity_id}")

            template_values['entity_id'] = entity_id
        else:
            logging.info(f"Adding item")
            r = s.post(f'{args.apiurl}/campaigns/{campaign_id}/{object_type}',
                       headers=headers,
                       data=object_data.encode('utf-8'))
            logging.debug(f"r: {r}")
            created_object = r.json()['data']
            logging.info(f"Object created: {created_object}")
            entity_id = created_object['entity_id']
            logging.debug(f"entity_id: {entity_id}")

            template_values['entity_id'] = entity_id

        # process template for attribute data
        attributes = data['attributes']
        logging.debug(f"attributes: {attributes}")
        for attribute in attributes.values():
            logging.debug(f"attribute: {attribute}")
            attribute_template = jinja2.Template(json.dumps(attribute))
            logging.debug(f"attribute_template: {attribute_template}")
            attribute_data = attribute_template.render(**template_values)
            logging.debug(f"attribute_data: {attribute_data}")

            # find existing attribute to update
            logging.info(f"Checking for existing attributes on entity '{entity_id}'...")
            if request_interval > 0:
                logging.info(f"Pausing for {request_interval} second(s) before making request...")
                time.sleep(request_interval)
            r = s.get(f'{args.apiurl}/campaigns/{campaign_id}/entities/{entity_id}/attributes',
                       headers=headers)
            logging.debug(f"r: {r}")
            results = json.loads(r.text)['data']
            matching_attr = None
            if len(results) > 0:
                matching_attr = (
                    list(filter(lambda x: x['name'].lower() == attribute['name'].lower(), results)) + [None]).pop(0)
            logging.debug(f"matching_attr: {matching_attr}")

            if request_interval > 0:
                logging.info(f"Pausing for {request_interval} second(s) before making request...")
                time.sleep(request_interval)
            if matching_attr:
                logging.info(f"Updating attribute '{matching_attr["id"]}'...")
                r = s.patch(f'{args.apiurl}/campaigns/{campaign_id}/entities/{entity_id}/attributes/{matching_attr["id"]}',
                           headers=headers,
                           data=attribute_data.encode('utf-8'))
                logging.debug(f"r: {r}")
            else:
                logging.info(f"Adding attribute to entity '{entity_id}'...")
                r = s.post(f'{args.apiurl}/campaigns/{campaign_id}/entities/{entity_id}/attributes',
                        headers=headers,
                        data=attribute_data.encode('utf-8'))
                logging.debug(f"r: {r}")
