# services/news_alternative.py
import feedparser
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time
import os
import yaml
from services.itinerary import load_itinerary

# Palabras clave que indican noticias potencialmente relevantes
alert_keywords = [
    'alert', 'security', 'protest', 'emergency', 'evacuation', 'earthquake',
    'storm', 'rain', 'flood', 'travel warning', 'demonstration', 'danger',
    'violence', 'outbreak', 'covid', 'hurricane', 'tsunami', 'closure', 'strike',
    'tourist', 'ladyboy', 'tourism', 'hospital', 'spanish group'
]

# Fuentes RSS de noticias tailandesas e internacionales
rss_feeds = [
    'https://www.bangkokpost.com/rss/data/topstories.xml',
    'https://thethaiger.com/feed',
    'https://news.google.com/rss/search?q=thailand&hl=en-US&gl=US&ceid=US:en',
    'https://www.channelnewsasia.com/api/v1/rss-outbound-feed/latest_news'
]

def get_itinerary_regions(itinerary_name='thailand_2025.yaml'):
    """
    Obtiene las regiones y palabras clave del itinerario
    
    Args:
        itinerary_name: Nombre del archivo YAML en la carpeta data/itineraries/
        
    Returns:
        list: Lista de regiones y palabras clave para buscar
    """
    try:
        itinerary = load_itinerary(itinerary_name)
        regions_keywords = []
        
        # Extraer país principal
        if 'regions' in itinerary and itinerary['regions']:
            country = itinerary['regions'][0].get('country', '')
            if country:
                regions_keywords.append(country.lower())
        
        # Extraer nombres de regiones y palabras clave
        for region in itinerary.get('regions', []):
            # Añadir nombre de región
            if 'name' in region:
                regions_keywords.append(region['name'].lower())
            
            # Añadir palabras clave específicas de la región
            if 'keywords' in region and region['keywords']:
                for keyword in region['keywords']:
                    regions_keywords.append(keyword.lower())
        
        return list(set(regions_keywords))  # Eliminar duplicados
    except Exception as e:
        print(f"Error al obtener regiones: {e}")
        # Si hay error, devolver un conjunto por defecto para Tailandia
        return ['thailand', 'bangkok', 'phuket', 'chiang mai']

def fetch_rss(feed_url, regions_keywords):
    """
    Obtener noticias de un feed RSS
    
    Args:
        feed_url: URL del feed RSS
        regions_keywords: Lista de palabras clave para filtrar noticias
        
    Returns:
        list: Lista de noticias relevantes
    """
    try:
        feed = feedparser.parse(feed_url)
        results = []
        
        for entry in feed.entries:
            title = entry.get('title', '')
            description = entry.get('description', '') or entry.get('summary', '')
            
            # Limpiar HTML de la descripción
            description = re.sub(r'<.*?>', '', description)
            
            # Verificar si la noticia menciona alguna de las regiones del itinerario
            content = (title + " " + description).lower()
            region_mentioned = any(region in content for region in regions_keywords)
            
            if not region_mentioned:
                continue
                
            # Verificar si contiene palabras clave de alerta
            has_alert = any(keyword.lower() in content for keyword in alert_keywords)
            
            # Priorizar noticias con alertas pero incluir algunas sin alertas
            if has_alert or len(results) < 10:
                # Obtener la fecha de publicación y convertirla a formato ISO
                pub_date = entry.get('published', entry.get('pubDate', ''))
                try:
                    # Intentar analizar la fecha (los formatos pueden variar)
                    if pub_date:
                        date_obj = datetime(*entry.published_parsed[:6])
                        formatted_date = date_obj.isoformat()
                    else:
                        formatted_date = ''
                except (AttributeError, TypeError):
                    formatted_date = pub_date
                
                results.append({
                    'title': title,
                    'description': description[:200] + '...' if len(description) > 200 else description,
                    'url': entry.get('link', ''),
                    'publishedAt': formatted_date,
                    'source': feed_url.split('/')[2]
                })
        
        return results
    except Exception as e:
        print(f"Error fetching RSS {feed_url}: {str(e)}")
        return []

def get_filtered_news(itinerary_name='thailand_2025.yaml', max_items=20):
    """
    Obtiene noticias filtradas de todas las fuentes RSS
    
    Args:
        itinerary_name: Nombre del archivo YAML del itinerario
        max_items: Número máximo de noticias a devolver
        
    Returns:
        list: Lista de noticias relevantes para el itinerario
    """
    # Obtener regiones y palabras clave del itinerario
    regions_keywords = get_itinerary_regions(itinerary_name)
    
    all_results = []
    
    # Usar ThreadPoolExecutor para hacer las peticiones en paralelo
    with ThreadPoolExecutor(max_workers=len(rss_feeds)) as executor:
        # Pasar regiones_keywords como argumento a fetch_rss
        tasks = [executor.submit(fetch_rss, feed, regions_keywords) for feed in rss_feeds]
        
        for task in tasks:
            try:
                results = task.result()
                all_results.extend(results)
            except Exception as e:
                print(f"Error en tarea: {str(e)}")
    
    # Ordenar por fecha (si está disponible)
    try:
        all_results.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)
    except:
        print("No se pudieron ordenar los resultados por fecha")
    
    # Eliminar duplicados basados en título similar
    unique_results = []
    seen_titles = set()
    for article in all_results:
        title_key = article['title'].lower()[:50]  # Usar los primeros 50 caracteres como clave
        if title_key not in seen_titles:
            unique_results.append(article)
            seen_titles.add(title_key)
    
    return unique_results[:max_items]  # Devuelve las noticias más relevantes limitadas por max_items