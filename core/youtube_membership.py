import os
import re
import random
import pickle
import requests
import pandas as pd
from config import settings

def read_csv(file_path):
    members_df = pd.read_csv(file_path)
    return members_df

def rename_csv_columns(members_df):
    members_df = members_df.rename(columns={
        'Membros': 'name',
        'Link do perfil': 'profile_url',
        'Nível atual': 'membership_level',
        'Tempo total no nível (meses)': 'total_time_in_level',
        'Tempo total como assinante (meses)': 'total_time_as_member',
        'Última atualização': 'last_update',
        'Carimbo de data/hora da última atualização': 'last_update_timestamp'
    })
    return members_df

def get_members_from_csv(file_path):
    members_df = read_csv(file_path)
    members_df = rename_csv_columns(members_df)
    members = members_df.to_dict('records')
    return members

def filter_members_by_level(members, level):
    return [member for member in members if member['membership_level'] == level]

def list_membership_levels(members):
    levels = set(member['membership_level'] for member in members)
    return list(levels)

def pick_random_member(members):
    return random.choice(members)
  
def get_user_photo_url(youtube_channel_url):
    channel_id = extract_channel_id(youtube_channel_url)
    if not channel_id:
        return None

    photo_url = fetch_channel_photo_url(channel_id)
    return photo_url

def extract_channel_id(youtube_channel_url):
    # Extrai o ID do canal a partir da URL
    regex = r'(?:youtube\.com\/channel\/)([^\/]+)'
    match = re.search(regex, youtube_channel_url)
    return match.group(1) if match else None

def fetch_channel_photo_url(channel_id):
    # Usa a API do YouTube para obter a URL da foto do perfil
    base_url = 'https://www.googleapis.com/youtube/v3/channels'
    params = {
        'part': 'snippet',
        'id': channel_id,
        'key': settings.YOUTUBE_API_KEY,
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if 'items' in data and data['items']:
        return data['items'][0]['snippet']['thumbnails']['default']['url']
    else:
        return None
   
def get_membership_badge_image(months):
    badge_file_name = None
    if months < 1:
        badge_file_name = "new.png"
    elif months < 2:
        badge_file_name = "1_month.png"
    elif months < 6:
        badge_file_name = "2_months.png"
    elif months < 12:
        badge_file_name = "6_months.png"
    elif months < 24:
        badge_file_name = "12_months.png"
    elif months < 36:
        badge_file_name = "24_months.png"
    elif months < 48:
        badge_file_name = "36_months.png"
    else:
        badge_file_name = "48_months.png"

    badge_image_path = os.path.join('assets', 'badges', badge_file_name)
    return badge_image_path


def get_member(member):
    # Carrega dados extras do membro
    photo_url = get_user_photo_url(member['profile_url'])
    badge_image = get_membership_badge_image(member['total_time_as_member'])

    return {
        'name': member['name'],
        'profile_url': member['profile_url'],
        'photo_url': photo_url,
        'membership_level': member['membership_level'],
        'total_time_in_level': member['total_time_in_level'],
        'total_time_as_member': member['total_time_as_member'],
        'badge_image': badge_image
    }