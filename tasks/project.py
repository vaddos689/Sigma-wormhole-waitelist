import aiohttp
from loguru import logger
from config import semaphore
from fake_useragent import UserAgent
import asyncio
from faker import Faker

fake = Faker()


class Project:
    def __init__(self, mail: str):
        self.first_name = fake.first_name()
        self.mail = mail
        self.user_agent = UserAgent().random
        self.headers = {
            'accept': '*/*',
            'accept-language': 'ru,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://sigma.wormhole.com',
            'referer': 'https://sigma.wormhole.com/',
            'User-agent': self.user_agent
        }

    async def request(self):
        url = 'https://sigma.wormhole.com/api/airtable'

        json = {
            'emailAddress': self.mail,
            'firstName': self.first_name,
            'keepInformed': True
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=json) as response:
                if response.status == 201:
                    result = await response.json()
                    if result['message'] == 'Record added successfully':
                        return 'success'
                    else:
                        return result


async def start_task(mail: str):
    async with semaphore:
        project = Project(mail)
        response = await project.request()
        if response == 'success':
            logger.success(f'Mail: {mail} | Success')
        else:
            logger.error(f'Mail: {mail} | Error with request: {response}')


async def start_tasks():
    with open('mails.txt', 'r') as file:
        mails = [row.strip() for row in file]

    tasks = []
    for mail in mails:
        tasks.append(asyncio.create_task(start_task(mail)))
    await asyncio.gather(*tasks)
