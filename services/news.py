import requests
from datetime import datetime, timedelta
import os
from config import NEWS_API_KEY

def get_news_for_region(region, max_items=5):
    """
    Obtiene noticias relevantes para una región específica
    
    Args:
        region: Datos de la región
        max_items: Número máximo de noticias a devolver
        
    Returns:
        dict: Datos de noticias
    """
    try:
        # Palabras clave relacionadas con la región
        keywords = [region['name']]
        
        # Agregar el país si está disponible
        if 'country' in region:
            keywords.append(region['country'])
            
        # Agregar keywords específicos si están disponibles
        if 'keywords' in region:
            keywords.extend(region['keywords'])
            
        # Construir la consulta
        query = ' OR '.join(keywords)
        
        # Configurar parámetros para NewsAPI
        params = {
            'apiKey': NEWS_API_KEY,
            'q': query,
            'language': 'es',  # Ajustar según el idioma preferido
            'sortBy': 'relevancy',
            'pageSize': max_items
        }
        
        # Agregar filtro de fechas (últimos 30 días por defecto)
        from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        params['from'] = from_date
        
        response = requests.get('https://newsapi.org/v2/everything', params=params)
        data = response.json()
        
        # Procesar y filtrar los resultados
        processed_data = {
            'region': region['name'],
            'articles': []
        }
        
        if 'articles' in data and data['articles']:
            # Filtrar artículos relevantes y formatear datos
            for article in data['articles'][:max_items]:
                processed_article = {
                    'title': article.get('title', ''),
                    'source': article.get('source', {}).get('name', 'Desconocido'),
                    'published_at': article.get('publishedAt', ''),
                    'url': article.get('url', ''),
                    'description': article.get('description', '')[:150] + '...' if article.get('description') else ''
                }
                processed_data['articles'].append(processed_article)
                
        return processed_data
    except Exception as e:
        print(f"Error al obtener noticias: {e}")
        return {
            'region': region['name'],
            'error': 'Error al obtener noticias',
            'message': str(e),
            'articles': []
        }

def filter_relevant_news(articles, region):
    """
    Filtra noticias para mostrar solo las más relevantes para el viaje
    
    Args:
        articles: Lista de artículos
        region: Datos de la región
        
    Returns:
        list: Artículos filtrados
    """
    # Palabras clave de relevancia para viajes
    travel_keywords = [
        'turismo', 'viaje', 'alerta', 'seguridad', 'clima',
        'transporte', 'aeropuerto', 'vuelo', 'cancelación',
        'festival', 'evento', 'cierre', 'huelga', 'protesta',
        'restricción', 'covid', 'emergencia', 'sanitaria'
    ]
    
    # Filtrar artículos que contengan palabras clave relevantes
    relevant_articles = []
    
    for article in articles:
        content = (article.get('title', '') + ' ' + article.get('description', '')).lower()
        
        # Verificar si alguna palabra clave está en el contenido
        if any(keyword in content for keyword in travel_keywords):
            relevant_articles.append(article)
            
    # Si no hay artículos relevantes, devolver algunos de los originales
    if not relevant_articles and articles:
        return articles[:3]
        
    return relevant_articles