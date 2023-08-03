import facebook
import requests

#from ventas.models import APIFaceModel
#api_facebook_model =APIFaceModel.objects.all()
#access_token = api_facebook_model[0].token
access_token = ""
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