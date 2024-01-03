
from flask import Flask, render_template, jsonify, request

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os


app = Flask(__name__)

api_key = os.environ.get('API_KEY') 

@app.route('/', methods=('GET', 'POST'))
def index():

    options1 = [('TW','Taiwan'), ('HK', 'Hong Kong'),('US', 'United States'),('IN', 'India'),
                ('SG', 'Singapore'),('MY', 'Malaysia'),('ID', 'Indonesia'),('JP', 'Japan'),('KR', 'South Korea'),
                    ('BR', 'Brazil'),('RU', 'Russia'),('MX', 'Mexico'),('DE', 'Germany'),
                    ('GB', 'United Kingdom'),('FR', 'France'),('TR', 'Turkey'),('PH', 'Philippines'),('CA', 'Canada'),
                    ('VN', 'Vietnam'),('TH', 'Thailand'),('IT', 'Italy'),('ES', 'Spain'),('AR', 'Argentina'),
                    ('EG', 'Egypt'),('SA', 'Saudi Arabia'),('AU', 'Australia'),('CO', 'Colombia'),('NL', 'Netherlands'),
                    ('SE', 'Sweden'),('PL', 'Poland'),('AE', 'United Arab Emirates'),('ZA', 'South Africa'),
                    ('BE', 'Belgium'),('RO', 'Romania'),('CH', 'Switzerland'),('PT', 'Portugal'),
                    ('GR', 'Greece'),('CL', 'Chile'),('IL', 'Israel'),('PE', 'Peru'),('CZ', 'Czech Republic'),
                    ('HU', 'Hungary'),('DK', 'Denmark'),('AT', 'Austria'),('NO', 'Norway'),('FI', 'Finland'),
                    ('IE', 'Ireland'),('NZ', 'New Zealand'),('DZ', 'Algeria'),('UA', 'Ukraine'),('KZ', 'Kazakhstan'),
                    ('MA', 'Morocco'),('BG', 'Bulgaria'),('TN', 'Tunisia'),('SK', 'Slovakia'),('HR', 'Croatia'),
                    ('RS', 'Serbia'),('LT', 'Lithuania'),('LV', 'Latvia'),('EE', 'Estonia'),('SI', 'Slovenia'),
                    ('DO', 'Dominican Republic'),('LU', 'Luxembourg'),('CR', 'Costa Rica'),('UY', 'Uruguay'),
                    ('PA', 'Panama'),('PY', 'Paraguay'),('BA', 'Bosnia and Herzegovina'),
                    ('GT', 'Guatemala'),('IS', 'Iceland'),('MT', 'Malta'),('SV', 'El Salvador'),
                    ('EC', 'Ecuador'),('CY', 'Cyprus'),('HN', 'Honduras'),('NP', 'Nepal'),('JM', 'Jamaica'),
                    ('TT', 'Trinidad and Tobago'),('ZW', 'Zimbabwe'),('MZ', 'Mozambique')]
    # ('value1', 'Option 1')
    options2 = [('All', 'All'),('1', 'Film & Animation'), ('2', 'Autos & Vehicles'), ('10', 'Music'), ('15', 'Pets & Animals'), 
                ('17', 'Sports'), ('18', 'Short Movies'), ('19', 'Travel & Events'), ('20', 'Gaming'), ('21', 'Videoblogging'),
                ('22', 'People & Blogs'), ('23', 'Comedy'), ('24', 'Entertainment'), ('25', 'News & Politics'), ('26', 'Howto & Style'),
                ('27', 'Education'), ('28', 'Science & Technology'), ('30', 'Movies'), ('31', 'Anime/Animation'), ('32', 'Action/Adventure'), 
                ('33', 'Classics'), ('34', 'Comedy'), ('35', 'Documentary'), ('36', 'Drama'), ('37', 'Family'), ('38', 'Foreign'), ('39', 'Horror'),
                ('40', 'Sci-Fi/Fantasy'), ('41', 'Thriller'), ('42', 'Shorts'), ('43', 'Shows'), ('44', 'Trailers')]
    
    
    
    region = 'TW'
    category = 'All'


    if request.method == 'POST':
        region = request.form.get('region','TW')
        category = request.form.get('category','All')
 
    print('button',region,category)
    if category:
        attribute_value = '/returnjson'+'?region='+region+'&category='+category
    else:
        attribute_value = '/returnjson'+'?region='+region+'&category=All'

    print('pamarm',attribute_value)
    return render_template('index.html', attribute_value=attribute_value, options1=options1, options2=options2, selected_option1=region, selected_option2=category)


@app.route('/returnjson', methods=['GET']) 
def ReturnJSON(): 
 
    region = request.args.get('region')
    category = request.args.get('category',"All")
    if category == "All":
        category = None

    print('api',region,category)

    try:
        dicted_api = api_response_to_dic(get_api_response(api_key=api_key,regionCode=region,videoCategoryId=category))
    except HttpError as e:
        dicted_api = {'API_Error': e.reason} 
        print(e)

    return jsonify(dicted_api) 
  
def get_api_response(api_key,maxResults = 50, regionCode="TW", videoCategoryId=None,):
    
    youtube = build('youtube', 'v3', developerKey=api_key)


    request = youtube.videos().list(
        part="snippet, statistics",
        chart="mostPopular",
        maxResults=maxResults,
        regionCode=regionCode,
        videoCategoryId=videoCategoryId
    )
    response = request.execute()

    return response


def api_response_to_dic(response):
    
    # print(response['items'])
    list_of_dic = []
    rank = 1
    for i in response['items']:
        dic = {}
        # print(i['snippet'])
        # print(i['statistics'])
        # print('======')    
        dic['rank'] = rank
        dic['title'] = i['snippet']['title']
        dic['link'] = 'https://www.youtube.com/watch?v='+i['id']
        dic['channel'] = i['snippet']['channelTitle']
        dic['channel_id'] = i['snippet']['channelId']
        dic['thumbnail'] = i['snippet']['thumbnails']['medium']['url']
        dic['thumb_html'] =  '<a href="'+  'https://www.youtube.com/watch?v='+i['id']  +'" target="_blank">  <img src="'+i['snippet']['thumbnails']['medium']['url']+'">  </a>'
        dic['view'] = int(i['statistics']['viewCount'])
        if i['statistics'].get('likeCount'):
            dic['like'] = int(i['statistics']['likeCount'])
        else:
            dic['like'] = 0
            
        if i['statistics'].get('commentCount'):
            dic['comment'] = int(i['statistics']['commentCount'])
        else:
            dic['comment'] = 0
        # dic['comment'] = int(i['statistics']['commentCount'])
        dic['tags'] = '' # !!!!!!
        dic['category_id'] = i['snippet']['channelId']
        list_of_dic.append(dic)
        rank += 1

    return list_of_dic





# if __name__ == '__main__':

#     app.run(host='0.0.0.0', port=5000)
    
