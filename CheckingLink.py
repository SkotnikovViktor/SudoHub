from transformers import AutoTokenizer, AutoModelForCausalLM
import re
from pathlib import Path
import aiohttp
import asyncio
from typing import Optional
import GUI


class AsyncCheckingForOriginality:
    URL_PATTERN = re.compile(r'''(?xi)
        \b(?:https?://|www\.)
        [^\s<>"{}|\\^`\[\]]+
        (?<![.,;:!?])
    ''', flags=re.VERBOSE)


    
    def __init__(self, text: str, timeout: float = 5.0, concurrency: int = 50):
        self.text = text
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.concurrency = concurrency
        self.result: Optional[float] = None
    




    async def _ping_link(self, session: aiohttp.ClientSession, link: str) -> bool:
        try:
            async with session.head(link, allow_redirects=True) as response:
                return 200 <= response.status < 400
        except:
            return False
    



    async def _process(self):
        links = list(set(
            (l if l.startswith(('http://', 'https://')) else 'https://' + l).strip()
            for l in self.URL_PATTERN.findall(self.text)))
        if not links:
            return
        
        connector = aiohttp.TCPConnector(limit=self.concurrency)
        async with aiohttp.ClientSession(connector=connector, timeout=self.timeout) as session:
            semaphore = asyncio.Semaphore(self.concurrency)
            
            async def bounded_ping(link):
                async with semaphore:
                    return await self._ping_link(session, link)
            
            tasks = [bounded_ping(link) for link in links]
            results = await asyncio.gather(*tasks)
            
            valid = sum(results)
            self.result = (valid * 100) / len(links) if links else None
    



    @classmethod
    async def check(cls, text: str, **kwargs) -> Optional[float]:
        instance = cls(text, **kwargs)
        await instance._process()
        return instance.result
    



      
def result_return(): #Функция, которая возвращает результат работы класса в файл GUI


    with open("result.txt", encoding="UTF-8") as file:
        text = file.read()


    result_check_link = asyncio.run(AsyncCheckingForOriginality.check(text, timeout=5, concurrency=30))

    if result_check_link == None:
        dict_result_check_link = {"link": "В тексте ссылки отсутствуют"} # Словарь о том, что ссылок нет 

    else:
        dict_result_check_link = {"link": result_check_link} # Словарь результата проверки ссылок
    
    
    return dict_result_check_link