import abc
import geocoder
import asyncio

from typing import Any, Dict, Optional
from countryinfo import CountryInfo
from analyze_user_query import config

logger = config.logger

class AbstractIpGeolocation(abc.ABC):

    @abc.abstractmethod
    async def get_info_by_ip(self, ip: str) -> Dict[str, Any]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_country(self, ip: str) -> Optional[str]:
        raise NotImplementedError

class IpInfoService(AbstractIpGeolocation):
    
    async def get_info_by_ip(self, ip: str) -> Dict[str, Any]:
        try:
            if ip in ["localhost", "127.0.0.1", "0.0.0.0"]: 
                logger.warning(f"Localost ip: {ip}")
                return {}
            info = await asyncio.to_thread(geocoder.ip, ip)
            if not info or not info.ok:
                logger.warning(f"No data found for IP: {ip}")
                return {}
            return info.geojson
        except Exception as e:
            logger.error(f"Failed to get info for IP {ip}: {e}")
            raise
        
    async def get_country(self, ip: str) -> Optional[str]:
        try:
            country_info = await self.get_info_by_ip(ip)
            
            if not country_info or not country_info.get("features"):
                logger.warning(f"No features found for IP: {ip}")
                return None
            
            features = country_info["features"]
            if not features:
                return None
                
            code_country = features[0]["properties"]["country"]
            
            country_data = CountryInfo(code_country)
            return country_data.name()
            
        except KeyError as e:
            logger.error(f"Missing key in response: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to get country for IP {ip}: {e}")
            raise