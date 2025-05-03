import feedparser
import re
from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime
import time

# Palabras clave que indican noticias potencialmente relevantes
alert_keywords = [
    'alert', 'security', 'protest', 'emergency', 'evacuation', 'earthquake',
    'storm', 'rain', 'flood', 'travel warning', 'demonstration', 'danger',
    'violence', 'outbreak', 'covid', 'hurricane', 'tsunami', 'closure', 'strike'
]

# Zonas de interés
regions = ['Thailand', 'Bangkok', 'Phuket', 'Chiang Mai', 'Krabi', 'Koh Samui']

# Fuentes RSS de noticias tailandesas e internacionales
rss_feeds = [
    'https://www.bangkokpost.com/rss/data/topstories.xml',
    'https://thethaiger.com/feed',
    'https://news.google.com/rss/search?q=thailand&hl=en-US&gl=US&ceid=US:en',
    'https://www.channelnewsasia.com/api/v1/rss-outbound-feed/latest_news'
]

def fetch_rss(feed_url):
    """Obtener noticias de un feed RSS"""
    try:
        feed = feedparser.parse(feed_url)
        results = []
        
        for entry in feed.entries:
            title = entry.get('title', '')
            description = entry.get('description', '') or entry.get('summary', '')
            
            # Limpiar HTML de la descripción
            description = re.sub(r'<.*?>', '', description)
            
            # Verificar si la noticia menciona alguna de las regiones
            content = (title + " " + description).lower()
            region_mentioned = any(region.lower() in content for region in regions)
            
            if not region_mentioned:
                continue
                
            # Verificar si contiene palabras clave de alerta
            has_alert = any(keyword.lower() in content for keyword in alert_keywords)
            
            if has_alert:
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

def get_filtered_news():
    all_results = []
    
    # Usar ThreadPoolExecutor para hacer las peticiones en paralelo
    with ThreadPoolExecutor(max_workers=len(rss_feeds)) as executor:
        tasks = [executor.submit(fetch_rss, feed) for feed in rss_feeds]
        
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
    print(len(unique_results))
    return unique_results[:20]  # Devuelve las 5 noticias más relevantes

if __name__ == '__main__':
    # Obtener las noticias
    news = get_filtered_news()
    
    # Imprimir resultados
    print(json.dumps(news, indent=2, ensure_ascii=False))
