import facebook
import requests

access_token = 'EAAILMksB9q8BO7UznhTYByouO4tM1j2h43jSYDA9gN901ZCAHxzp950BrEMOZCN2UZBwlH4t0X10zEsZAxiZAZAviJvrmZCtcIVxNNG558hf92idDdmh5NOZBcyiHuOychbZAKRQZCrTqlxZBvNM67Hi4tSQ2PXeTzMYUA0EkpTEO9s6pzUxZBO1V0c2rrhJe3XcYxVX2xZAAUZAMYL9GLQ5tZCGONCNh1AF9uJtR6D78kiJgQZD'
graph = facebook.GraphAPI(access_token)

def get_data_facebook():
    #data = graph.get_object('116784698104891?fields=published_posts{likes},posts{likes{id,name},comments{message}}')
    data = graph.get_object('116784698104891?fields=published_posts{comments{id,message}}')
    return data

def publish_image_facebook(image_url, message):
    url = f"https://graph.facebook.com/me/photos?access_token={access_token}"
    payload = {
        'url': image_url,
        'caption': message
    }
    try:
        response = requests.post(url, data=payload)
        response_data = response.json()

        if response_data.get('id'):
            print("Imagen publicada en Facebook con éxito. ")
            return response_data
        else:
            print("Error al publicar la imagen en Facebook.")
            print(response_data)
            return response_data

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        raise f"Error de conexión {e}"